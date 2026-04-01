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

let count = 0;
const queries = [
  '军工板块 涨停 2026年3月24日 原因',
  '绿色电力 风电 涨停 2026年3月24日',
  'A股明日热点板块预测 2026年3月25日',
  '北证50 科创板 今日强势 2026年3月24日',
];

let results = [];
for (const q of queries) {
  search(q, (err, msg) => {
    count++;
    if (msg) results.push({ q, msg });
    if (count === queries.length) {
      for (const r of results) {
        console.log('=== ' + r.q + ' ===');
        console.log(r.msg.substring(0, 1000));
        console.log('');
      }
    }
  });
}
