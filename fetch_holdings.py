# -*- coding: utf-8 -*-
import urllib.request
import json

stocks = {
    '凌云股份': 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.600480&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f60,f170,f171,f169',
    '亿纬锂能': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.300014&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f60,f170,f171,f169',
    '巨轮智能': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.002031&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f60,f170,f171,f169',
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
                high = d.get('f44', 0) / 100
                low = d.get('f45', 0) / 100
                open_p = d.get('f46', 0) / 100
                vol = d.get('f47', 0)
                amount = d.get('f48', 0)
                pct = d.get('f170', 0) / 100
                chg = d.get('f171', 0) / 100
                turnover = d.get('f168', 0) / 100 if d.get('f168') else 0
                pe = d.get('f162', 0) / 100 if d.get('f162') else 0
                pb = d.get('f167', 0) / 100 if d.get('f167') else 0
                print(f'{name}: {price:.2f} ({pct:+.2f}%) H:{high:.2f} L:{low:.2f} O:{open_p:.2f} Vol:{vol} Amt:{amount}')
    except Exception as e:
        print(f'{name}: error')

# 甬矽转债
print('---')
try:
    url = 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.118036&fields=f43,f44,f45,f46,f47,f48,f170,f171,f57,f58,f60'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode('utf-8'))
        if 'data' in data and data['data']:
            d = data['data']
            price = d.get('f43', 0) / 100
            high = d.get('f44', 0) / 100
            low = d.get('f45', 0) / 100
            pct = d.get('f170', 0) / 100
            print(f'Yongxi Bond: {price:.2f} ({pct:+.2f}%) H:{high:.2f} L:{low:.2f}')
except Exception as e:
    print('Yongxi Bond: error')
