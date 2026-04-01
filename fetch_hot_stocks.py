# -*- coding: utf-8 -*-
import urllib.request
import json

stocks = {
    '神剑股份': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.002361&fields=f43,f44,f45,f46,f47,f48,f170,f171,f57,f58',
    '新能泰山': 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.600720&fields=f43,f44,f45,f46,f47,f48,f170,f171,f57,f58',
    '闽发铝业': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.002578&fields=f43,f44,f45,f46,f47,f48,f170,f171,f57,f58',
    '万邦德': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.002550&fields=f43,f44,f45,f46,f47,f48,f170,f171,f57,f58',
    '宇通客车': 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.600066&fields=f43,f44,f45,f46,f47,f48,f170,f171,f57,f58',
    '舒华体育': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.001322&fields=f43,f44,f45,f46,f47,f48,f170,f171,f57,f58',
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
                d = data['data']
                price = d.get('f43', 0) / 100
                pct = d.get('f170', 0) / 100
                name_out = d.get('f58', name)
                print(f'{name_out}: {price:.2f} ({pct:+.2f}%)')
    except Exception as e:
        print(f'{name}: error')
