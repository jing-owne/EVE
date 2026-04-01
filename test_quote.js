const https = require('https');

const url = 'https://yunshangtool.cn/daily-quote/';
const options = {
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'text/html',
  }
};

https.get(url, options, (res) => {
  let body = '';
  res.on('data', c => body += c);
  res.on('end', () => {
    // 输出全部内容看结构
    console.log(body.substring(0, 3000));
  });
}).on('error', e => console.log('错误:', e.message));
