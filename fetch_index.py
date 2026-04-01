# -*- coding: utf-8 -*-
import urllib.request
import json

# 指数数据
urls = {
    '上证指数': 'https://push2.eastmoney.com/api/qt/stock/get?secid=1.000001&fields=f43,f170,f171,f169',
    '深证成指': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.399001&fields=f43,f170,f171,f169',
    '创业板': 'https://push2.eastmoney.com/api/qt/stock/get?secid=0.399006&fields=f43,f170,f171,f169',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.eastmoney.com/'
}

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'data' in data and data['data']:
                price = data['data'].get('f43', 0) / 100
                change = data['data'].get('f170', 0) / 100
                pct = data['data'].get('f171', 0) / 100
                print(f'{name}: {price:.2f} ({pct:+.2f}%)')
    except Exception as e:
        print(f'{name}: 获取失败 - {e}')
