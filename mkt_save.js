const fs = require('fs');
const https = require('http');

const port = process.env.AUTH_GATEWAY_PORT || '19000';
const data = JSON.stringify({
  keyword: 'A股今日涨跌停数量 沪深300 上证指数 创业板 收盘 2026年3月24日',
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
      const msg = d.message || JSON.stringify(d);
      // Write to user's home dir
      fs.writeFileSync('C:\\Users\\admin\\mkt_raw.txt', msg, 'utf8');
      console.log('SAVED:' + msg.length);
    } catch(e) {
      console.log('ERROR:' + e.message);
    }
  });
});

req.on('error', (e) => { console.log('REQERR:' + e.message); });
req.write(data);
req.end();
