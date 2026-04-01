// add_crons.js - Directly write cron jobs to jobs.json
const fs = require('fs');
const path = require('path');
const os = require('os');
const { v4: uuidv4 } = require('crypto');

// Simple UUID v4 without external deps
function uuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

const jobsFile = path.join(os.homedir(), '.qclaw', 'cron', 'jobs.json');
const bakFile = jobsFile + '.bak2';

// Read existing
const data = JSON.parse(fs.readFileSync(jobsFile, 'utf8'));
console.log('Existing jobs:', data.jobs.length);

// Backup
fs.writeFileSync(bakFile, JSON.stringify(data, null, 2), 'utf8');
console.log('Backup saved to:', bakFile);

const to = 'o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat';
const now = Date.now();

const newJobs = [
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

// Remove existing Marcus jobs if any
data.jobs = data.jobs.filter(j => !newJobs.some(nj => nj.name === j.name));

// Add new jobs
for (const j of newJobs) {
  const job = {
    id: uuid(),
    agentId: 'main',
    sessionKey: 'agent:main:main',
    name: j.name,
    enabled: true,
    createdAtMs: now,
    updatedAtMs: now,
    schedule: { expr: j.expr, kind: 'cron', tz: 'Asia/Shanghai' },
    sessionTarget: 'isolated',
    wakeMode: 'now',
    payload: { kind: 'agentTurn', message: j.msg, lightContext: false },
    delivery: { mode: 'announce', channel: 'weixin', to },
    state: { consecutiveErrors: 0 },
  };
  data.jobs.push(job);
  console.log(`Added: ${j.name} (${j.expr})`);
}

// Write back
fs.writeFileSync(jobsFile, JSON.stringify(data, null, 2), 'utf8');
console.log('\nTotal jobs now:', data.jobs.length);
console.log('Jobs saved to:', jobsFile);
