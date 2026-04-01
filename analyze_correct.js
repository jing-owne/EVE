const https = require('https');

function fetchQuote(secid, name, cost) {
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
          if (!d || !d.f43) return resolve({name, error: 'no data'});
          const price = d.f43 / 100;
          const preClose = d.f60 / 100;
          const open = d.f46 / 100;
          const high = d.f44 / 100;
          const low = d.f45 / 100;
          const pct = d.f170 / 100;
          const amount = d.f48 / 1e8;
          const inflow = (d.f62 || 0) / 1e8;
          const profitPct = ((price - cost) / cost * 100);

          // 走势判断
          let trend = '';
          if (price > open) trend = '盘中上涨↑';
          else if (price < open) trend = '盘中下跌↓';
          else trend = '横盘';

          // 买入建议
          let advice = '', emoji = '';
          if (profitPct < -8) {
            advice = '建议补仓'; emoji = '🟢';
          } else if (profitPct < -3) {
            advice = '可考虑补仓'; emoji = '🟡';
          } else if (profitPct < 0) {
            advice = '持有观望'; emoji = '🟡';
          } else if (profitPct > 15) {
            advice = '注意止盈'; emoji = '🔴';
          } else {
            advice = '持有观望'; emoji = '🟡';
          }

          // 成交额加分
          if (amount > 5 && profitPct < 0) {
            advice = '建议补仓'; emoji = '🟢';
          }

          resolve({
            name, cost,
            stockName: d.f58,
            price, open, high, low, preClose,
            pct, amount, inflow,
            profitPct: profitPct.toFixed(2),
            trend, advice, emoji
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
    {secid: '1.600480', name: '凌云股份', cost: 9.70},
    {secid: '1.601138', name: '工业富联', cost: 52.60},
    {secid: '0.002123', name: '梦网科技', cost: 11.50},
  ];

  const now = new Date().toLocaleString('zh-CN', {timeZone: 'Asia/Shanghai'});
  console.log('='.repeat(60));
  console.log('持仓实时分析 - ' + now);
  console.log('='.repeat(60));

  const results = [];
  for (const s of stocks) {
    const r = await fetchQuote(s.secid, s.name, s.cost);
    if (r.error) {
      console.log(s.name + ': 获取失败 - ' + r.error);
    } else {
      results.push(r);
    }
  }

  // 输出详情
  results.forEach(r => {
    const ps = r.profitPct > 0 ? '+' : '';
    const ts = r.pct > 0 ? '+' : '';
    console.log('\n' + r.emoji + ' [' + r.name + '] ' + r.stockName);
    console.log('  现价: ' + r.price.toFixed(2) + '  涨跌: ' + ts + r.pct.toFixed(2) + '%  走势: ' + r.trend);
    console.log('  开盘: ' + r.open.toFixed(2) + '  最高: ' + r.high.toFixed(2) + '  最低: ' + r.low.toFixed(2) + '  昨收: ' + r.preClose.toFixed(2));
    console.log('  成交额: ' + r.amount.toFixed(2) + '亿  主力净流入: ' + (r.inflow > 0 ? '+' : '') + r.inflow.toFixed(2) + '亿');
    console.log('  成本: ' + r.cost.toFixed(2) + '  收益: ' + ps + r.profitPct + '%  建议: ' + r.advice);
  });

  // 买入排行
  console.log('\n' + '='.repeat(60));
  console.log('买入优先级排行');
  console.log('='.repeat(60));
  const sorted = [...results].sort((a, b) => parseFloat(a.profitPct) - parseFloat(b.profitPct));
  sorted.forEach((r, i) => {
    const ps = r.profitPct > 0 ? '+' : '';
    console.log((i+1) + '. ' + r.emoji + ' ' + r.name + '  现价:' + r.price.toFixed(2) + '  收益:' + ps + r.profitPct + '%  → ' + r.advice);
  });

  console.log('\n止损原则：股票-3%无条件出');
}

main();
