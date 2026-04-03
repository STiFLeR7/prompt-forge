#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

// Colors
const cyan = '\x1b[36m';
const green = '\x1b[32m';
const yellow = '\x1b[33m';
const red = '\x1b[31m';
const bold = '\x1b[1m';
const dim = '\x1b[2m';
const reset = '\x1b[0m';

const pkg = require('../package.json');

// Parse args
const args = process.argv.slice(2);
const hasClaude = args.includes('--claude');
const hasGemini = args.includes('--gemini');
const hasAll = args.includes('--all');
const hasGlobal = args.includes('--global') || args.includes('-g');
const hasLocal = args.includes('--local') || args.includes('-l');
const hasUninstall = args.includes('--uninstall') || args.includes('-u');
const hasHelp = args.includes('--help') || args.includes('-h');

if (hasHelp) {
  console.log(`
${bold}Prompt Forge Installer v${pkg.version}${reset}

${bold}Usage:${reset}
  npx prompt-forge-cc@latest              ${dim}# Interactive install${reset}
  npx prompt-forge-cc --claude --global   ${dim}# Claude Code, all projects${reset}
  npx prompt-forge-cc --gemini --global   ${dim}# Gemini CLI, all projects${reset}
  npx prompt-forge-cc --all --global      ${dim}# All runtimes${reset}
  npx prompt-forge-cc --uninstall         ${dim}# Remove Prompt Forge${reset}

${bold}Options:${reset}
  --claude          Install for Claude Code
  --gemini          Install for Gemini CLI
  --all             Install for all runtimes
  --global, -g      Install globally (all projects)
  --local, -l       Install locally (current project only)
  --uninstall, -u   Remove Prompt Forge
  --help, -h        Show this help
`);
  process.exit(0);
}

// Skill files to copy (relative to package root)
const SKILL_FILES = [
  'SKILL.md',
  'src/core/intent_parser.md',
  'src/core/prompt_builder.md',
  'src/core/constraints.md',
  'src/core/modes.md',
  'src/adapters/claude.md',
  'src/adapters/gemini.md',
  'src/adapters/openai.md',
  'src/commands/prompt-forge.md',
  'src/utils/helpers.md',
  'prompts/templates/task-type-blueprints.md',
  'prompts/templates/gsd-output-format.md',
  'prompts/templates/superpowers-output-format.md',
  'prompts/templates/context-file-template.md',
  'prompts/templates/anthropic-prompting-guide.md',
  'prompts/examples/example-session.md',
  'evals/test_cases.md',
  'evals/adversarial_cases.md',
  'evals/benchmark.md',
  'evals/scoring.md',
  'docs/architecture.md',
  'docs/usage.md',
];

const packageRoot = path.resolve(__dirname, '..');

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function copyFileSync(src, dest) {
  const destDir = path.dirname(dest);
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }
  fs.copyFileSync(src, dest);
}

function removeDir(dir) {
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
    return true;
  }
  return false;
}

function getTargetDir(runtime, isGlobal) {
  const home = os.homedir();
  if (runtime === 'claude') {
    const base = isGlobal ? path.join(home, '.claude') : path.join(process.cwd(), '.claude');
    return path.join(base, 'skills', 'prompt-forge');
  }
  if (runtime === 'gemini') {
    const base = isGlobal ? path.join(home, '.gemini') : path.join(process.cwd(), '.gemini');
    return path.join(base, 'skills', 'prompt-forge');
  }
  return null;
}

function installRuntime(runtime, isGlobal) {
  const targetDir = getTargetDir(runtime, isGlobal);
  if (!targetDir) return false;

  const scope = isGlobal ? 'global' : 'local';
  console.log(`\n${cyan}Installing Prompt Forge for ${bold}${runtime}${reset}${cyan} (${scope})...${reset}`);
  console.log(`${dim}  Target: ${targetDir}${reset}`);

  let copied = 0;
  for (const file of SKILL_FILES) {
    const src = path.join(packageRoot, file);
    const dest = path.join(targetDir, file);
    if (fs.existsSync(src)) {
      copyFileSync(src, dest);
      copied++;
    }
  }

  console.log(`${green}  Copied ${copied} files.${reset}`);
  return true;
}

function uninstallRuntime(runtime, isGlobal) {
  const targetDir = getTargetDir(runtime, isGlobal);
  if (!targetDir) return false;
  if (removeDir(targetDir)) {
    const scope = isGlobal ? 'global' : 'local';
    console.log(`${green}  Removed Prompt Forge from ${runtime} (${scope}).${reset}`);
    return true;
  }
  return false;
}

// ---------------------------------------------------------------------------
// Interactive prompts
// ---------------------------------------------------------------------------

function createRL() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
}

function ask(rl, question) {
  return new Promise((resolve) => rl.question(question, resolve));
}

async function promptRuntime(rl) {
  console.log(`\n${bold}Which runtime?${reset}`);
  console.log(`  ${cyan}1${reset} Claude Code`);
  console.log(`  ${cyan}2${reset} Gemini CLI`);
  console.log(`  ${cyan}3${reset} Both`);
  const answer = await ask(rl, `\n${bold}Choose (1-3):${reset} `);
  const choice = answer.trim();
  if (choice === '1') return ['claude'];
  if (choice === '2') return ['gemini'];
  if (choice === '3') return ['claude', 'gemini'];
  console.log(`${yellow}Invalid choice, defaulting to Claude Code.${reset}`);
  return ['claude'];
}

async function promptScope(rl) {
  console.log(`\n${bold}Install scope?${reset}`);
  console.log(`  ${cyan}1${reset} Global ${dim}(all projects — recommended)${reset}`);
  console.log(`  ${cyan}2${reset} Local  ${dim}(current project only)${reset}`);
  const answer = await ask(rl, `\n${bold}Choose (1-2):${reset} `);
  return answer.trim() === '2' ? false : true;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log(`\n${bold}${cyan}Prompt Forge${reset} ${dim}v${pkg.version}${reset}`);
  console.log(`${dim}A prompt compiler skill for coding agents${reset}`);

  // Resolve runtimes
  let runtimes = [];
  if (hasAll) {
    runtimes = ['claude', 'gemini'];
  } else {
    if (hasClaude) runtimes.push('claude');
    if (hasGemini) runtimes.push('gemini');
  }

  let isGlobal = hasGlobal ? true : hasLocal ? false : null;

  // Uninstall flow
  if (hasUninstall) {
    console.log(`\n${yellow}Uninstalling Prompt Forge...${reset}`);
    let removed = false;
    for (const runtime of ['claude', 'gemini']) {
      removed = uninstallRuntime(runtime, true) || removed;
      removed = uninstallRuntime(runtime, false) || removed;
    }
    if (!removed) {
      console.log(`${dim}  Nothing to remove.${reset}`);
    }
    console.log(`\n${green}Done.${reset}\n`);
    return;
  }

  // Interactive mode if no flags
  if (runtimes.length === 0 || isGlobal === null) {
    const rl = createRL();
    try {
      if (runtimes.length === 0) {
        runtimes = await promptRuntime(rl);
      }
      if (isGlobal === null) {
        isGlobal = await promptScope(rl);
      }
    } finally {
      rl.close();
    }
  }

  // Install
  for (const runtime of runtimes) {
    installRuntime(runtime, isGlobal);
  }

  // Done
  console.log(`\n${green}${bold}Prompt Forge installed.${reset}`);
  console.log(`\n${dim}Invoke with:${reset}`);
  if (runtimes.includes('claude')) {
    console.log(`  ${cyan}Claude Code:${reset}  /prompt-forge [your intent]`);
  }
  if (runtimes.includes('gemini')) {
    console.log(`  ${cyan}Gemini CLI:${reset}   /prompt-forge [your intent]`);
  }
  console.log('');
}

main().catch((err) => {
  console.error(`${red}Error: ${err.message}${reset}`);
  process.exit(1);
});
