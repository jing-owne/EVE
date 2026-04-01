const https = require('https');

// 搜索股票代码
function searchStock(keyword) {
  return new Promise((resolve) => {
    const url = 'https://searchapi.eastmoney.com/api/suggest/get?input=' + encodeURIComponent(keyword) + '&type=14&token=D43BF722C8E33BDC906FB84D85E326E8&count=5';
    const options = {
      headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.eastmoney.com/' }
    };
    https.get(url, options, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        try {
          const data = JSON.parse(body);
          const items = (data.QuotationCodeTable && data.QuotationCodeTable.Data) || [];
          resolve(items.slice(0, 3).map(i => ({
            code: i.Code,
            name: i.Name,
            market: i.MktNum,
            type: i.SecurityType,
          })));
        } catch(e) {
          resolve([]);
        }
      });
    }).on('error', () => resolve([]));
  });
}

async function main() {
  const keywords = ['凌云股份', '甬夕转债', '天准转债'];
  
  for (const kw of keywords) {
    console.log('\n搜索: ' + kw);
    const results = await searchStock(kw);
    if (results.length === 0) {
      console.log('  未找到');
    } else {
      results.forEach(r => {
        console.log('  代码: ' + r.code + '  名称: ' + r.name + '  市场: ' + r.market + '  类型: ' + r.type);
      });
    }
  }
}

main();
