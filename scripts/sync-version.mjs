#!/usr/bin/env node
// Writes one version into every manifest that carries one.
//
//   node scripts/sync-version.mjs 0.1.0
//
// Hosts read versions from different files (Claude Code and Cursor from their
// plugin.json, Gemini CLI from gemini-extension.json, npm and PyPI from their
// own metadata), so a release bumps all of them together.

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const version = process.argv[2];

if (!/^\d+\.\d+\.\d+$/.test(version ?? '')) {
  console.error('usage: node scripts/sync-version.mjs MAJOR.MINOR.PATCH');
  process.exit(1);
}

const jsonFiles = [
  'package.json',
  'plugin.json',
  '.claude-plugin/plugin.json',
  '.cursor-plugin/plugin.json',
  '.codex-plugin/plugin.json',
  'gemini-extension.json',
];

for (const file of jsonFiles) {
  const full = join(ROOT, file);
  const data = JSON.parse(readFileSync(full, 'utf8'));
  data.version = version;
  writeFileSync(full, `${JSON.stringify(data, null, 2)}\n`);
  console.log(`${file} -> ${version}`);
}

function replaceOnce(file, pattern, replacement) {
  const full = join(ROOT, file);
  const before = readFileSync(full, 'utf8');
  if (!pattern.test(before)) {
    console.error(`${file}: version line not found`);
    process.exit(1);
  }
  writeFileSync(full, before.replace(pattern, replacement));
  console.log(`${file} -> ${version}`);
}

replaceOnce('pyproject.toml', /^version\s*=\s*"[^"]+"/m, `version = "${version}"`);
replaceOnce('src/erdostack/__init__.py', /^__version__\s*=\s*"[^"]+"/m, `__version__ = "${version}"`);

console.log(`\nNext: update CHANGELOG.md, commit, then tag v${version}.`);
