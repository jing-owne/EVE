# -*- coding: utf-8 -*-
import urllib.request
import json

# 重点股票
stocks = {
    '华电辽能': 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.600396&fields=f43,f170,f171',
    '融捷股份': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.002192&fields=f43,f170,f171',
    '湖南发展': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.000722&fields=f43,f170,f171',
    '华电能源': 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.600726&fields=f43,f170,f171',
    '中超控股': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.002471&fields=f43,f170,f171',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.eastmoney.com/'
}

for name, url in stocks.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'data' in data and data['data']:
                price = data['data'].get('f43', 0) / 100
                pct = data['data'].get('f171', 0) / 100
                print(f'{name}: {price:.2f} ({pct:+.2f}%)')
    except Exception as e:
        print(f'{name}: error')
