// setup_crons_v3.js - Create cron jobs via openclaw CLI
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
    expr: '0 10 * * 1-5',
    msg: 'A股早盘报告：搜索今日A股开盘数据、板块动向、涨停股，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
  {
    name: 'A股午盘参考',
    expr: '25 11 * * 1-5',
    msg: 'A股午盘报告：搜索今日A股午盘数据、涨跌停统计、板块动向，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
  {
    name: 'A股下午盘初',
    expr: '0 14 * * 1-5',
    msg: 'A股下午盘报告：搜索今日A股下午盘数据、板块动向，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
  {
    name: 'A股尾盘窗口',
    expr: '40 14 * * 1-5',
    msg: 'A股尾盘报告：搜索今日A股尾盘数据、涨跌停统计，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
  {
    name: 'A股收盘复盘',
    expr: '30 15 * * 1-5',
    msg: 'A股收盘复盘：搜索今日A股收盘数据、主力资金流向、龙虎榜，给出明日胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。',
  },
];

for (const j of jobs) {
  const jobObj = {
    name: j.name,
    schedule: { kind: 'cron', expr: j.expr, tz: 'Asia/Shanghai' },
    sessionTarget: 'isolated',
    payload: { kind: 'agentTurn', message: j.msg, lightContext: false },
    delivery: { mode: 'announce', channel: 'weixin', to },
  };
  const tmpFile = path.join(os.tmpdir(), `cron_${Date.now()}.json`);
  fs.writeFileSync(tmpFile, JSON.stringify(jobObj), 'utf8');
  console.log(`Creating: ${j.name}`);
  try {
    const result = execFileSync(node, [mjs, 'cron', 'add', '--json-file', tmpFile], { env, encoding: 'utf8', timeout: 10000 });
    console.log(result);
  } catch (e) {
    console.log('Error:', e.message.substring(0, 200));
    // try without --json-file
    try {
      const result2 = execFileSync(node, [mjs, 'cron', 'add', JSON.stringify(jobObj)], { env, encoding: 'utf8', timeout: 10000 });
      console.log(result2);
    } catch (e2) {
      console.log('Error2:', e2.message.substring(0, 200));
    }
  }
  fs.unlinkSync(tmpFile);
}

console.log('\n--- Listing cron jobs ---');
try {
  const list = execFileSync(node, [mjs, 'cron', 'list'], { env, encoding: 'utf8', timeout: 10000 });
  console.log(list);
} catch (e) {
  console.log('List error:', e.message.substring(0, 300));
}
