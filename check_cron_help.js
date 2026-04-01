// setup_crons_v4.js - Create cron jobs via openclaw CLI with correct args
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const metaPath = path.join(os.homedir(), '.qclaw', 'qclaw.json');
const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));

const node = meta.cli.nodeBinary;
const mjs = meta.cli.openclawMjs;
const to = 'o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat';

const env = {
  ...process.env,
  ELECTRON_RUN_AS_NODE: '1',
  NODE_OPTIONS: '--no-warnings',
  OPENCLAW_NIX_MODE: '1',
  OPENCLAW_STATE_DIR: meta.stateDir,
  OPENCLAW_CONFIG_PATH: meta.configPath,
};

// First check help to understand the CLI args
try {
  const help = execFileSync(node, [mjs, 'cron', 'add', '--help'], { env, encoding: 'utf8', timeout: 10000 });
  console.log('HELP:', help);
} catch (e) {
  console.log('HELP output:', e.stdout || e.message.substring(0, 500));
}
