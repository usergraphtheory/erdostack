#!/usr/bin/env node
// Repository validator. Zero dependencies, so it runs anywhere Node 20+ does.
//
//   node scripts/validate.mjs                   check manifests, versions and skills
//   node scripts/validate.mjs --require-skills  also fail when skills/ holds no skill (release gate)
//   node scripts/validate.mjs --tag v1.2.3      also fail when the tag does not match the version
//
// What it checks:
//   1. Every host manifest parses, carries the plugin name, and agrees on the version.
//   2. Every skills/<name>/SKILL.md follows the Agent Skills spec (https://agentskills.io/specification).
//   3. Every engine pack in references/engines/ states when it was last verified.

import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const NAME = 'erdostack';
const args = process.argv.slice(2);
const requireSkills = args.includes('--require-skills');
const tagIndex = args.indexOf('--tag');
const tag = tagIndex >= 0 ? args[tagIndex + 1] : null;

const errors = [];
const warnings = [];
const error = (message) => errors.push(message);
const warn = (message) => warnings.push(message);

function readJson(relativePath) {
  const full = join(ROOT, relativePath);
  if (!existsSync(full)) {
    error(`${relativePath}: missing`);
    return null;
  }
  try {
    return JSON.parse(readFileSync(full, 'utf8'));
  } catch (cause) {
    error(`${relativePath}: invalid JSON (${cause.message})`);
    return null;
  }
}

function readText(relativePath) {
  const full = join(ROOT, relativePath);
  if (!existsSync(full)) {
    error(`${relativePath}: missing`);
    return '';
  }
  return readFileSync(full, 'utf8');
}

// --- 1. Manifests and versions ---------------------------------------------

const pkg = readJson('package.json');
const version = pkg?.version;
if (!/^\d+\.\d+\.\d+$/.test(version ?? '')) error(`package.json: version "${version}" is not MAJOR.MINOR.PATCH`);

const versioned = {
  'plugin.json': readJson('plugin.json'),
  '.claude-plugin/plugin.json': readJson('.claude-plugin/plugin.json'),
  '.cursor-plugin/plugin.json': readJson('.cursor-plugin/plugin.json'),
  '.codex-plugin/plugin.json': readJson('.codex-plugin/plugin.json'),
  'gemini-extension.json': readJson('gemini-extension.json'),
};
for (const [file, manifest] of Object.entries(versioned)) {
  if (!manifest) continue;
  if (manifest.name !== NAME) error(`${file}: name is "${manifest.name}", expected "${NAME}"`);
  if (manifest.version !== version) error(`${file}: version ${manifest.version} does not match package.json ${version}`);
  if (!manifest.description) error(`${file}: description is missing`);
}
if (pkg && pkg.name !== NAME) error(`package.json: name is "${pkg.name}", expected "${NAME}"`);

const agentPlugin = versioned['plugin.json'];
if (agentPlugin) {
  const allowed = ['$schema', 'name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords', 'extensions'];
  for (const key of Object.keys(agentPlugin)) {
    if (!allowed.includes(key)) error(`plugin.json: "${key}" is not a permitted Agent Plugins field (the schema is closed)`);
  }
  if (!/^https:\/\/agent-plugins\.org\/schemas\/\d+\.\d+\.\d+\/plugin\.schema\.json$/.test(agentPlugin.$schema ?? '')) {
    error('plugin.json: $schema must be the canonical Agent Plugins schema URL');
  }
}

for (const file of ['.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json']) {
  const marketplace = readJson(file);
  if (!marketplace) continue;
  if (!marketplace.name) error(`${file}: name is missing`);
  const entries = Array.isArray(marketplace.plugins) ? marketplace.plugins : [];
  if (!entries.some((entry) => entry.name === NAME)) error(`${file}: no plugin entry named "${NAME}"`);
}

const pyproject = readText('pyproject.toml');
const pyVersion = pyproject.match(/^version\s*=\s*"([^"]+)"/m)?.[1];
if (pyVersion !== version) error(`pyproject.toml: version ${pyVersion} does not match package.json ${version}`);
const initVersion = readText('src/erdostack/__init__.py').match(/^__version__\s*=\s*"([^"]+)"/m)?.[1];
if (initVersion !== version) error(`src/erdostack/__init__.py: __version__ ${initVersion} does not match package.json ${version}`);

if (tag && tag !== `v${version}`) error(`tag ${tag} does not match version ${version} (expected v${version})`);

for (const logo of ['assets/logo.svg', 'assets/logo.png']) {
  if (!existsSync(join(ROOT, logo))) error(`${logo}: missing (referenced by plugin manifests)`);
}

// --- 2. Skills ---------------------------------------------------------------

// Reads the top-level scalar keys of YAML frontmatter. Skills in this repo keep
// frontmatter to plain `key: value` lines (quoted when the value contains a colon),
// which is also what the strictest host parsers accept.
function parseFrontmatter(text, where) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) {
    error(`${where}: missing YAML frontmatter (the file must start with ---)`);
    return null;
  }
  const fields = {};
  for (const line of match[1].split(/\r?\n/)) {
    if (!line.trim() || line.trim().startsWith('#') || /^\s/.test(line)) continue;
    const pair = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!pair) {
      error(`${where}: cannot parse frontmatter line "${line}"`);
      continue;
    }
    let value = pair[2].trim();
    const quoted = /^(".*"|'.*')$/.test(value);
    if (quoted) value = value.slice(1, -1);
    else if (/:\s/.test(value)) error(`${where}: "${pair[1]}" contains ": " and must be quoted, or some installers skip the skill`);
    if (/^[>|]/.test(value)) error(`${where}: "${pair[1]}" uses a block scalar; write it on one line`);
    fields[pair[1]] = value;
  }
  return { fields, body: text.slice(match[0].length) };
}

const skillsDir = join(ROOT, 'skills');
const skillNames = existsSync(skillsDir)
  ? readdirSync(skillsDir).filter((entry) => statSync(join(skillsDir, entry)).isDirectory())
  : [];
let validSkills = 0;

for (const dir of skillNames) {
  const where = `skills/${dir}/SKILL.md`;
  const file = join(skillsDir, dir, 'SKILL.md');
  if (!existsSync(file)) {
    error(`skills/${dir}: no SKILL.md`);
    continue;
  }
  const parsed = parseFrontmatter(readFileSync(file, 'utf8'), where);
  if (!parsed) continue;
  const { name, description } = parsed.fields;
  if (!name) error(`${where}: name is missing`);
  else {
    if (name !== dir) error(`${where}: name "${name}" must match the directory name "${dir}"`);
    if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(name)) error(`${where}: name must be lowercase letters, digits and single hyphens`);
    if (name.length > 64) error(`${where}: name is longer than 64 characters`);
  }
  if (!description) error(`${where}: description is missing`);
  else if (description.length > 1024) error(`${where}: description is longer than 1024 characters`);
  const lines = parsed.body.split(/\r?\n/).length;
  if (lines > 500) warn(`${where}: body is ${lines} lines; move detail into references/ (keep bodies short and procedural)`);
  if (!parsed.body.trim()) error(`${where}: body is empty`);
  validSkills += 1;
}

if (requireSkills && validSkills === 0) error('skills/: no skills found, and --require-skills was passed');

// --- 3. Engine packs ---------------------------------------------------------

const enginesDir = join(ROOT, 'references', 'engines');
const packs = existsSync(enginesDir)
  ? readdirSync(enginesDir).filter((entry) => entry.endsWith('.md') && entry !== 'README.md')
  : [];
for (const pack of packs) {
  const text = readFileSync(join(enginesDir, pack), 'utf8');
  if (!/^Last verified:\s*\d{4}-\d{2}-\d{2}/m.test(text)) {
    error(`references/engines/${pack}: add a "Last verified: YYYY-MM-DD" line (engine facts go stale)`);
  }
}

// --- Report --------------------------------------------------------------------

for (const message of warnings) console.warn(`warning: ${message}`);
if (errors.length > 0) {
  for (const message of errors) console.error(`error: ${message}`);
  console.error(`\n${errors.length} problem(s) found.`);
  process.exit(1);
}
console.log(`ok: ${NAME} ${version}, ${validSkills} skill(s), ${packs.length} engine pack(s), ${Object.keys(versioned).length + 2} versioned manifests in sync.`);
