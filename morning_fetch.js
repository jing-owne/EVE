const https = require('http');

const port = process.env.AUTH_GATEWAY_PORT || '19000';

function search(keyword, callback) {
  const data = JSON.stringify({ keyword, from_time: 1742745600 });
  const options = {
    hostname: 'localhost', port, path: '/proxy/prosearch/search',
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
  };
  const req = https.request(options, (res) => {
    let body = '';
    res.on('data', c => body += c);
    res.on('end', () => {
      try {
        const d = JSON.parse(body);
        callback(null, d.success ? d.message : null);
      } catch(e) { callback(e); }
    });
  });
  req.on('error', e => callback(e));
  req.write(data);
  req.end();
}

search('A股今日开盘 沪深300 上证指数 创业板 涨跌停 2026年3月25日', (err, msg) => {
  if (msg) {
    console.log(msg.substring(0, 2000));
  } else {
    console.log('ERROR:', err);
  }
});
