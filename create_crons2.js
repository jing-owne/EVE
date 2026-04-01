const https = require('http');

const port = process.env.AUTH_GATEWAY_PORT || '19000';

// 创建定时任务的函数
function createCron(name, cronExpr, message, channel, to) {
  const data = JSON.stringify({
    name: name,
    schedule: {
      kind: 'cron',
      expr: cronExpr,
      tz: 'Asia/Shanghai'
    },
    sessionTarget: 'isolated',
    payload: {
      kind: 'agentTurn',
      message: message,
      lightContext: true
    },
    delivery: {
      mode: 'announce',
      channel: channel || 'weixin',
      to: to || 'o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat'
    }
  });

  const options = {
    hostname: 'localhost',
    port: port,
    path: '/cron/add',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(data)
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        console.log(`${name}: ${res.statusCode}`);
        try {
          const json = JSON.parse(body);
          if (json.jobId) {
            console.log(`  jobId: ${json.jobId}`);
          }
          if (json.error) {
            console.log(`  error: ${json.error.message || JSON.stringify(json.error)}`);
          }
        } catch(e) {}
        resolve({ name, status: res.statusCode, body });
      });
    });
    req.on('error', e => {
      console.log(`${name}: ERROR ${e.message}`);
      reject(e);
    });
    req.write(data);
    req.end();
  });
}

// 定时任务配置
const crons = [
  {
    name: '天气穿衣指南',
    expr: '30 8 * * *',  // 每天 08:30
    message: '你是天气顾问。执行天气报告脚本，获取松江区泗泾镇的天气、穿衣建议、空气质量和7天预报，通过 message tool 发送到微信。'
  },
  {
    name: 'A股早盘分析',
    expr: '0 10 * * 1-5',  // 工作日 10:00
    message: '你是Marcus，A股动量策略师。执行A股报告脚本，获取今日开盘数据、板块动向、重点观察股，通过 message tool 发送到微信。格式：【市场立场 + 板块动向 + 重点观察股】'
  },
  {
    name: 'A股午盘参考',
    expr: '25 11 * * 1-5',  // 工作日 11:25
    message: '你是Marcus，A股动量策略师。执行A股报告脚本，获取午盘数据、涨跌停统计、板块动向，通过 message tool 发送到微信。'
  },
  {
    name: 'A股下午盘初',
    expr: '0 14 * * 1-5',  // 工作日 14:00
    message: '你是Marcus，A股动量策略师。执行A股报告脚本，获取下午盘初数据、板块动向，通过 message tool 发送到微信。'
  },
  {
    name: 'A股尾盘窗口',
    expr: '40 14 * * 1-5',  // 工作日 14:40
    message: '你是Marcus，A股动量策略师。执行A股报告脚本，获取尾盘数据、涨跌停统计，通过 message tool 发送到微信。'
  },
  {
    name: 'A股收盘复盘',
    expr: '30 15 * * 1-5',  // 工作日 15:30
    message: '你是Marcus，A股动量策略师。执行收盘复盘脚本，分析今日收盘数据、明日机会、重点股票（含代码和选择理由），通过 message tool 发送到微信。'
  }
];

// 创建所有定时任务
async function main() {
  console.log('开始创建定时任务...\n');
  for (const cron of crons) {
    try {
      await createCron(cron.name, cron.expr, cron.message);
      await new Promise(r => setTimeout(r, 500)); // 间隔500ms
    } catch (e) {
      console.log(`${cron.name} 创建失败`);
    }
  }
  console.log('\n定时任务创建完成');
}

main();
