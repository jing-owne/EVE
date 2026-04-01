const https = require('https');

function tryUrl(url, referer) {
  return new Promise((resolve) => {
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': referer || 'https://yunshangtool.cn/',
      }
    };
    https.get(url, options, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => resolve({ url, status: res.statusCode, body: body.substring(0, 500) }));
    }).on('error', e => resolve({ url, error: e.message }));
  });
}

async function main() {
  // 尝试几个可能的API
  const urls = [
    'https://api.yunshangtool.cn/daily-quote/',
    'https://api.yunshangtool.cn/quote/today',
    'https://v1.yunshangtool.cn/api/daily-quote',
    'https://api.xyc.com.cn/daily-quote/',
    'https://v2.jinrishici.com/sentence',
    'https://www.tianapi.com/quote/',
    'https://www.mxnzp.com/api/daily_sentence/recommend',
  ];
  for (const u of urls) {
    const r = await tryUrl(u, 'https://yunshangtool.cn/daily-quote/');
    if (r.status === 200) {
      console.log('✅', u);
      console.log(r.body);
    } else {
      console.log('❌', u, r.status || r.error);
    }
  }
}

main();
