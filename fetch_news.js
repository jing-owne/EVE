const http = require('http');
const PORT = process.env.AUTH_GATEWAY_PORT || 19000;

function search(keyword) {
  return new Promise((resolve) => {
    const fromTime = Math.floor(Date.now() / 1000) - 86400; // 最近24小时
    const data = JSON.stringify({ keyword, from_time: fromTime });
    
    const options = {
      hostname: 'localhost',
      port: PORT,
      path: '/proxy/prosearch/search',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    };
    
    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          resolve({ keyword, success: result.success, message: result.message || '' });
        } catch (e) {
          resolve({ keyword, success: false, message: 'Parse error' });
        }
      });
    });
    
    req.on('error', (e) => {
      resolve({ keyword, success: false, message: e.message });
    });
    
    req.write(data);
    req.end();
  });
}

async function main() {
  const keywords = [
    'A股涨停板 2026年3月31日',
    '央行货币政策 2026年3月',
    '商业航天 高铁 摩托车',
  ];
  
  console.log('[QClaw] 开始搜索财经新闻...\n');
  
  for (const kw of keywords) {
    const result = await search(kw);
    console.log(`【${kw}】`);
    if (result.success) {
      console.log(result.message.substring(0, 800));
    } else {
      console.log(`搜索失败: ${result.message}`);
    }
    console.log('\n' + '='.repeat(60) + '\n');
  }
}

main();
