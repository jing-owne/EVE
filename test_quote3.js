const https = require('https');

// 测试一言接口
function testApi(url, name) {
  return new Promise((resolve) => {
    const options = { headers: { 'User-Agent': 'Mozilla/5.0' } };
    https.get(url, options, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        console.log(name + ' [' + res.statusCode + ']:');
        console.log(body.substring(0, 300));
        console.log('');
        resolve();
      });
    }).on('error', e => { console.log(name + ' 错误:', e.message); resolve(); });
  });
}

async function main() {
  await testApi('https://v1.hitokoto.cn/?c=d&c=h&c=i&encode=json', 'hitokoto');
  await testApi('https://api.quotable.io/random?lang=zh', 'quotable');
  await testApi('https://api.uomg.com/api/rand.qinghua?format=json', 'uomg情话');
  await testApi('https://api.vvhan.com/api/ian/rand?type=json', 'vvhan一言');
}
main();
