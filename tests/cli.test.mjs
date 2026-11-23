// Smoke tests for the repository validator and both installers.
// Run with: node --test tests/cli.test.mjs

import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const VERSION = JSON.parse(readFileSync(join(ROOT, 'package.json'), 'utf8')).version;

// A throwaway skill source, so the installers can be exercised before any real skill exists.
function fixture() {
  const source = mkdtempSync(join(tmpdir(), 'erdostack-src-'));
  mkdirSync(join(source, 'demo-skill', 'references'), { recursive: true });
  writeFileSync(
    join(source, 'demo-skill', 'SKILL.md'),
    '---\nname: demo-skill\ndescription: Fixture skill used by the installer tests.\n---\n\n# Demo\n',
  );
  writeFileSync(join(source, 'demo-skill', 'references', 'note.md'), 'note\n');
  mkdirSync(join(source, 'not-a-skill'));
  return source;
}

function run(command, args, env = {}) {
  const result = spawnSync(command, args, { cwd: ROOT, encoding: 'utf8', env: { ...process.env, ...env } });
  return { status: result.status, out: `${result.stdout ?? ''}${result.stderr ?? ''}`, error: result.error };
}

function findPython() {
  for (const candidate of ['python3', 'python']) {
    const probe = spawnSync(candidate, ['-c', 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)']);
    if (probe.status === 0) return candidate;
  }
  return null;
}

const installers = [{ label: 'node', command: process.execPath, prefix: [join(ROOT, 'bin', 'erdostack.mjs')], env: {} }];
const python = findPython();
if (python) {
  installers.push({ label: 'python', command: python, prefix: ['-m', 'erdostack'], env: { PYTHONPATH: join(ROOT, 'src') } });
}

test('repository validates', () => {
  const result = run(process.execPath, [join(ROOT, 'scripts', 'validate.mjs')]);
  assert.equal(result.status, 0, result.out);
});

test('validator rejects a mismatched tag', () => {
  const result = run(process.execPath, [join(ROOT, 'scripts', 'validate.mjs'), '--tag', 'v999.0.0']);
  assert.notEqual(result.status, 0);
  assert.match(result.out, /does not match version/);
});

for (const installer of installers) {
  test(`${installer.label}: reports its version`, () => {
    const result = run(installer.command, [...installer.prefix, '--version'], installer.env);
    assert.equal(result.status, 0, result.out);
    assert.equal(result.out.trim(), VERSION);
  });

  test(`${installer.label}: lists only folders that contain SKILL.md`, () => {
    const env = { ...installer.env, ERDOSTACK_SKILLS_DIR: fixture() };
    const result = run(installer.command, [...installer.prefix, 'list'], env);
    assert.equal(result.status, 0, result.out);
    assert.match(result.out, /demo-skill\s+Fixture skill/);
    assert.doesNotMatch(result.out, /not-a-skill/);
  });

  test(`${installer.label}: installs, skips existing, and replaces with --force`, () => {
    const env = { ...installer.env, ERDOSTACK_SKILLS_DIR: fixture() };
    const dest = mkdtempSync(join(tmpdir(), 'erdostack-dest-'));

    const dry = run(installer.command, [...installer.prefix, 'install', '--dest', dest, '--dry-run'], env);
    assert.equal(dry.status, 0, dry.out);
    assert.equal(existsSync(join(dest, 'demo-skill')), false);

    const first = run(installer.command, [...installer.prefix, 'install', '--dest', dest], env);
    assert.equal(first.status, 0, first.out);
    assert.equal(existsSync(join(dest, 'demo-skill', 'SKILL.md')), true);
    assert.equal(existsSync(join(dest, 'demo-skill', 'references', 'note.md')), true);

    const second = run(installer.command, [...installer.prefix, 'install', '--dest', dest], env);
    assert.match(second.out, /skip\s+demo-skill/);

    const forced = run(installer.command, [...installer.prefix, 'install', 'demo-skill', '--dest', dest, '--force'], env);
    assert.match(forced.out, /copied\s+demo-skill/);
  });

  test(`${installer.label}: rejects unknown skills`, () => {
    const env = { ...installer.env, ERDOSTACK_SKILLS_DIR: fixture() };
    const result = run(installer.command, [...installer.prefix, 'install', 'no-such-skill'], env);
    assert.notEqual(result.status, 0);
    assert.match(result.out, /unknown skill/);
  });
}
