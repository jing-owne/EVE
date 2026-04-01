const https = require('https');
const http = require('http');

// 测试抓取金十数据
function fetchJin10() {
  return new Promise((resolve) => {
    // 金十快讯API
    const url = 'https://www.jin10.com/flash_newest.js?t=' + Date.now();
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.jin10.com/',
        'Accept': '*/*',
      }
    };
    https.get(url, options, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        console.log('状态码:', res.statusCode);
        console.log('原始数据前500字:');
        console.log(body.substring(0, 500));
        resolve(body);
      });
    }).on('error', e => {
      console.log('错误:', e.message);
      resolve(null);
    });
  });
}

// 也试试另一个接口
function fetchJin10Flash() {
  return new Promise((resolve) => {
    const url = 'https://flash-api.jin10.com/get_flash_list?channel=-8200&vip=1&since=0&max_time=' + Math.floor(Date.now()/1000) + '&flash_type=1';
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://www.jin10.com/',
        'x-app-id': 'rU6QIu7JHe2gOUeR',
        'x-version': '1.4.0.0',
      }
    };
    https.get(url, options, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        console.log('\n--- Flash API ---');
        console.log('状态码:', res.statusCode);
        console.log('数据前800字:');
        console.log(body.substring(0, 800));
        resolve(body);
      });
    }).on('error', e => {
      console.log('Flash API错误:', e.message);
      resolve(null);
    });
  });
}

async function main() {
  console.log('=== 测试金十数据抓取 ===\n');
  await fetchJin10();
  await fetchJin10Flash();
}

main();
