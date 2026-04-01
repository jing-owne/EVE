const https = require('https');

function fetchQuote(secid, name) {
  return new Promise((resolve) => {
    const url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=' + secid + '&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f62,f169,f170&_=' + Date.now();
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://quote.eastmoney.com/'
      }
    };
    https.get(url, options, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        try {
          const d = JSON.parse(body).data;
          if (!d) return resolve({name, error: 'no data'});
          resolve({
            name,
            stockName: d.f58,
            price: d.f43 / 100,
            open: d.f46 / 100,
            high: d.f44 / 100,
            low: d.f45 / 100,
            preClose: d.f60 / 100,
            pct: d.f170 / 100,
            amount: d.f48 / 1e8,
            inflow: (d.f62 || 0) / 1e8,
            raw_f43: d.f43,
            raw_f60: d.f60,
          });
        } catch(e) {
          resolve({name, error: e.message});
        }
      });
    }).on('error', e => resolve({name, error: e.message}));
  });
}

async function main() {
  const stocks = [
    {secid: '0.300014', name: '亿纬锂能', cost: 69.00},
    {secid: '0.002859', name: '凌云股份', cost: 9.80},
    {secid: '0.123098', name: '甬夕转债', cost: 171.00},
    {secid: '0.123090', name: '天准转债', cost: 174.00},
  ];

  console.log('='.repeat(60));
  console.log('实时行情 - ' + new Date().toLocaleString('zh-CN'));
  console.log('='.repeat(60));

  for (const s of stocks) {
    const r = await fetchQuote(s.secid, s.name);
    if (r.error) {
      console.log(s.name + ': 错误 - ' + r.error);
    } else {
      const profitPct = ((r.price - s.cost) / s.cost * 100).toFixed(2);
      const profitSign = profitPct > 0 ? '+' : '';
      const pctSign = r.pct > 0 ? '+' : '';
      console.log('');
      console.log('[' + s.name + '] ' + r.stockName);
      console.log('  现价: ' + r.price.toFixed(2) + '  开盘: ' + r.open.toFixed(2) + '  最高: ' + r.high.toFixed(2) + '  最低: ' + r.low.toFixed(2));
      console.log('  昨收: ' + r.preClose.toFixed(2) + '  涨跌: ' + pctSign + r.pct.toFixed(2) + '%  成交额: ' + r.amount.toFixed(2) + '亿');
      console.log('  成本: ' + s.cost.toFixed(2) + '  收益: ' + profitSign + profitPct + '%');
      console.log('  raw_f43=' + r.raw_f43 + '  raw_f60=' + r.raw_f60);
    }
  }
}

main();
