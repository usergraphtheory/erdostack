#!/usr/bin/env node
// erdostack installer: copies the bundled skills into an agent's skills directory.
// It reads and writes local files only. No network access, no telemetry, no install scripts.
// Keep the AGENTS table in sync with src/erdostack/cli.py.

import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const VERSION = JSON.parse(readFileSync(join(ROOT, 'package.json'), 'utf8')).version;
const REPO = 'https://github.com/usergraphtheory/erdostack';

// Skills directory per agent, relative to the project root (project) or the home directory (global).
const AGENTS = {
  universal: { project: '.agents/skills', global: '.agents/skills' },
  'claude-code': { project: '.claude/skills', global: '.claude/skills' },
  cursor: { project: '.cursor/skills', global: '.cursor/skills' },
  'gemini-cli': { project: '.gemini/skills', global: '.gemini/skills' },
  opencode: { project: '.opencode/skills', global: '.config/opencode/skills' },
  copilot: { project: '.github/skills', global: null },
};

const HELP = `erdostack ${VERSION}
Graph skills for coding agents.

Usage:
  erdostack list                    List the bundled skills
  erdostack install [skill ...]     Copy skills into an agent's skills directory (default: all)
  erdostack path                    Print the directory that holds the bundled skills

Install options:
  -a, --agent <name>   ${Object.keys(AGENTS).join(', ')}
                       (default: universal, which writes to .agents/skills)
  -g, --global         Install for the current user instead of the current project
  -d, --dest <dir>     Write to this directory instead (overrides --agent and --global)
  -f, --force          Replace skills that are already installed
      --dry-run        Show what would be copied without writing anything

Other:
  -v, --version        Print the version
  -h, --help           Print this help

This tool only copies files. It makes no network requests and collects nothing.
${REPO}`;

function fail(message) {
  console.error(`erdostack: ${message}`);
  process.exit(1);
}

function sourceDir() {
  return resolve(process.env.ERDOSTACK_SKILLS_DIR || join(ROOT, 'skills'));
}

function bundledSkills() {
  const dir = sourceDir();
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((name) => {
      const full = join(dir, name);
      return statSync(full).isDirectory() && existsSync(join(full, 'SKILL.md'));
    })
    .sort();
}

function describe(skill) {
  const text = readFileSync(join(sourceDir(), skill, 'SKILL.md'), 'utf8');
  const match = text.match(/^description:\s*(.+)$/m);
  if (!match) return '';
  return match[1].trim().replace(/^["']|["']$/g, '');
}

function parseInstallArgs(args) {
  const options = { skills: [], agent: 'universal', global: false, dest: null, force: false, dryRun: false };
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '-a' || arg === '--agent') options.agent = args[++i];
    else if (arg === '-d' || arg === '--dest') options.dest = args[++i];
    else if (arg === '-g' || arg === '--global') options.global = true;
    else if (arg === '-f' || arg === '--force') options.force = true;
    else if (arg === '--dry-run') options.dryRun = true;
    else if (arg.startsWith('-')) fail(`unknown option ${arg}. Run "erdostack --help".`);
    else options.skills.push(arg);
  }
  return options;
}

function targetDir(options) {
  if (options.dest) return resolve(options.dest);
  const agent = AGENTS[options.agent];
  if (!agent) fail(`unknown agent "${options.agent}". Choose one of: ${Object.keys(AGENTS).join(', ')}, or pass --dest <dir>.`);
  if (options.global) {
    if (!agent.global) fail(`no known global skills directory for "${options.agent}". Pass --dest <dir> instead.`);
    return join(homedir(), agent.global);
  }
  return resolve(agent.project);
}

function list() {
  const skills = bundledSkills();
  if (skills.length === 0) {
    console.log(`erdostack ${VERSION} bundles no skills yet. Roadmap: ${REPO}/blob/main/ROADMAP.md`);
    return;
  }
  for (const skill of skills) {
    const description = describe(skill);
    console.log(description ? `${skill}  ${description}` : skill);
  }
}

function install(args) {
  const options = parseInstallArgs(args);
  const available = bundledSkills();
  if (available.length === 0) {
    console.log(`erdostack ${VERSION} bundles no skills yet, so there is nothing to install.`);
    console.log(`Roadmap: ${REPO}/blob/main/ROADMAP.md`);
    return;
  }
  const wanted = options.skills.length > 0 ? options.skills : available;
  const unknown = wanted.filter((skill) => !available.includes(skill));
  if (unknown.length > 0) fail(`unknown skill(s): ${unknown.join(', ')}. Run "erdostack list".`);

  const target = targetDir(options);
  let copied = 0;
  for (const skill of wanted) {
    const destination = join(target, skill);
    if (existsSync(destination) && !options.force) {
      console.log(`skip  ${skill} (already in ${target}; use --force to replace)`);
      continue;
    }
    if (options.dryRun) {
      console.log(`would copy  ${skill} -> ${destination}`);
      continue;
    }
    mkdirSync(target, { recursive: true });
    cpSync(join(sourceDir(), skill), destination, { recursive: true, force: true });
    console.log(`copied  ${skill} -> ${destination}`);
    copied += 1;
  }
  if (!options.dryRun) console.log(`${copied} skill(s) installed from erdostack ${VERSION}.`);
}

const [command, ...rest] = process.argv.slice(2);
switch (command) {
  case undefined:
  case '-h':
  case '--help':
  case 'help':
    console.log(HELP);
    break;
  case '-v':
  case '--version':
    console.log(VERSION);
    break;
  case 'list':
    list();
    break;
  case 'path':
    console.log(sourceDir());
    break;
  case 'install':
  case 'add':
    install(rest);
    break;
  default:
    fail(`unknown command "${command}". Run "erdostack --help".`);
}
