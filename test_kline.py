# -*- coding: utf-8 -*-
"""测试K线数据获取"""
import json
import urllib.request

code = '300014'  # 亿纬锂能
secid = f'0.{code}'

url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=1&end=20500101&lmt=10'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://quote.eastmoney.com/',
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=10) as response:
    raw = response.read().decode('utf-8', errors='replace').strip()
    
    print('原始数据前500字:')
    print(raw[:500])
    print('\n')
    
    if raw.startswith('jQuery'):
        raw = raw[raw.index('(')+1:raw.rindex(')')]
    
    data = json.loads(raw)
    
    if data.get('data'):
        print('数据结构:')
        print(json.dumps(data['data'], indent=2, ensure_ascii=False)[:1000])
        
        if data['data'].get('klines'):
            print('\nK线数据（最近10天）:')
            for k in data['data']['klines']:
                parts = k.split(',')
                print(f"日期: {parts[0]}, 开盘: {parts[1]}, 收盘: {parts[2]}, 最高: {parts[3]}, 最低: {parts[4]}, 成交量: {parts[5]}, 成交额: {parts[6]}")
