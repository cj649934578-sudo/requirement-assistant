#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");

const PACKAGE_ROOT = path.resolve(__dirname, "..");
const SKILL_NAME = "requirement-assistant";
const INCLUDED_PATHS = [
  "agents",
  "evals",
  "examples",
  "references",
  "schemas",
  "scripts",
  "ra.ps1",
  "README.md",
  "SKILL.md",
];

function usage() {
  console.log(`
Requirement Assistant Skill Installer

Usage:
  npx @chaidd/requirement-assistant-skill@latest install [--target user|project] [--dir <path>]
  npx @chaidd/requirement-assistant-skill@latest help

Options:
  --target user     Install to %USERPROFILE%/.codex/skills/${SKILL_NAME} (default)
  --target project  Install to <current working dir>/.codex/skills/${SKILL_NAME}
  --dir <path>      Install to an explicit parent skills directory or exact target directory

Examples:
  npx @chaidd/requirement-assistant-skill@latest install
  npx @chaidd/requirement-assistant-skill@latest install --target project
  npx @chaidd/requirement-assistant-skill@latest install --dir C:\\Users\\you\\.codex\\skills
`);
}

function parseArgs(argv) {
  const args = [...argv];
  const command = args.shift() || "install";
  let target = "user";
  let dir = "";

  while (args.length > 0) {
    const token = args.shift();
    if (token === "--target") {
      target = args.shift() || "";
      continue;
    }
    if (token === "--dir") {
      dir = args.shift() || "";
      continue;
    }
    throw new Error(`Unknown argument: ${token}`);
  }

  return { command, target, dir };
}

function resolveInstallDir(target, dir) {
  if (dir) {
    const resolved = path.resolve(dir);
    return path.basename(resolved).toLowerCase() === SKILL_NAME ? resolved : path.join(resolved, SKILL_NAME);
  }
  if (target === "project") {
    return path.join(process.cwd(), ".codex", "skills", SKILL_NAME);
  }
  if (target === "user") {
    return path.join(os.homedir(), ".codex", "skills", SKILL_NAME);
  }
  throw new Error(`Unsupported target: ${target}`);
}

function ensureSafeTarget(targetDir) {
  const normalized = path.normalize(targetDir).toLowerCase();
  if (!normalized.includes(`${path.sep}.codex${path.sep}skills${path.sep}`)) {
    throw new Error(`Refusing to install outside a .codex/skills directory: ${targetDir}`);
  }
  if (path.basename(normalized) !== SKILL_NAME) {
    throw new Error(`Target must resolve to a ${SKILL_NAME} directory: ${targetDir}`);
  }
}

function copyEntry(name, targetDir) {
  const source = path.join(PACKAGE_ROOT, name);
  const destination = path.join(targetDir, name);
  const stat = fs.statSync(source);
  if (stat.isDirectory()) {
    fs.cpSync(source, destination, { recursive: true, force: true });
    return;
  }
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.copyFileSync(source, destination);
}

function install(targetDir) {
  ensureSafeTarget(targetDir);
  fs.rmSync(targetDir, { recursive: true, force: true });
  fs.mkdirSync(targetDir, { recursive: true });
  for (const name of INCLUDED_PATHS) {
    copyEntry(name, targetDir);
  }
}

function main() {
  let parsed;
  try {
    parsed = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    usage();
    process.exit(2);
  }

  if (parsed.command === "help" || parsed.command === "--help" || parsed.command === "-h") {
    usage();
    return;
  }

  if (parsed.command !== "install") {
    console.error(`ERROR: Unsupported command: ${parsed.command}`);
    usage();
    process.exit(2);
  }

  const targetDir = resolveInstallDir(parsed.target, parsed.dir);

  try {
    install(targetDir);
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }

  console.log(`Installed ${SKILL_NAME} to: ${targetDir}`);
  console.log("Next steps:");
  console.log("1. Restart Codex if it is already running");
  console.log("2. Run the local checks from the installed skill directory if desired:");
  console.log("   .\\ra.ps1 check-examples");
  console.log("   .\\ra.ps1 run-evals");
}

main();
