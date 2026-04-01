const https = require('http');

const port = process.env.AUTH_GATEWAY_PORT || '19000';
const data = JSON.stringify({
  keyword: 'A股今日涨跌停数量 沪深300 上证指数 收盘 2026年3月24日',
  from_time: 1742745600
});

const options = {
  hostname: 'localhost',
  port: port,
  path: '/proxy/prosearch/search',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(data)
  }
};

const req = https.request(options, (res) => {
  let body = '';
  res.on('data', (chunk) => { body += chunk; });
  res.on('end', () => {
    try {
      const d = JSON.parse(body);
      if (d.success && d.message) {
        // extract key numbers
        const lines = d.message.split('\n');
        for (const line of lines) {
          if (line.includes('涨停') || line.includes('跌停') || 
              line.includes('沪深300') || line.includes('上证指数') ||
              line.includes('创业板') || line.includes('收盘') ||
              line.includes('%')) {
            console.log(line);
          }
        }
      } else {
        console.log('SEARCH_FAILED');
      }
    } catch(e) {
      console.log('PARSE_ERROR: ' + body.substring(0, 300));
    }
  });
});

req.on('error', (e) => { console.log('ERROR: ' + e.message); });
req.write(data);
req.end();
