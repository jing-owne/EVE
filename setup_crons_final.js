// setup_crons_final.js - Create cron jobs with correct CLI args
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

const jobs = [
  {
    name: 'A股早盘分析',
    cron: '0 10 * * 1-5',
    msg: 'A股早盘报告：搜索今日A股开盘数据、板块动向、涨停股，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
  {
    name: 'A股午盘参考',
    cron: '25 11 * * 1-5',
    msg: 'A股午盘报告：搜索今日A股午盘数据、涨跌停统计、板块动向，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
  {
    name: 'A股下午盘初',
    cron: '0 14 * * 1-5',
    msg: 'A股下午盘报告：搜索今日A股下午盘数据、板块动向，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
  {
    name: 'A股尾盘窗口',
    cron: '40 14 * * 1-5',
    msg: 'A股尾盘报告：搜索今日A股尾盘数据、涨跌停统计，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
  {
    name: 'A股收盘复盘',
    cron: '30 15 * * 1-5',
    msg: 'A股收盘复盘：搜索今日A股收盘数据、主力资金流向、龙虎榜，给出明日胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
];

for (const j of jobs) {
  console.log(`\nCreating: ${j.name}`);
  try {
    const args = [
      mjs, 'cron', 'add',
      '--name', j.name,
      '--cron', j.cron,
      '--tz', 'Asia/Shanghai',
      '--session', 'isolated',
      '--message', j.msg,
      '--announce',
      '--channel', 'weixin',
      '--to', to,
    ];
    const result = execFileSync(node, args, { env, encoding: 'utf8', timeout: 15000 });
    console.log('OK:', result.trim().substring(0, 200));
  } catch (e) {
    const out = (e.stdout || '') + (e.stderr || '') + e.message;
    console.log('Result:', out.substring(0, 300));
  }
}

// List all jobs
console.log('\n--- All cron jobs ---');
try {
  const list = execFileSync(node, [mjs, 'cron', 'list'], { env, encoding: 'utf8', timeout: 15000 });
  console.log(list);
} catch (e) {
  console.log('List:', (e.stdout || e.message).substring(0, 500));
}
