import warnings; warnings.filterwarnings('ignore')
import os, json, sys
os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import requests

port = os.environ.get('AUTH_GATEWAY_PORT', '19000')

# 搜索1: 涨跌停数量
url1 = f'http://localhost:{port}/proxy/prosearch/search'
payload1 = {'keyword': 'A股 涨跌停 数量 2026年3月24日', 'from_time': 1784054400}

# 搜索2: 大盘指数
payload2 = {'keyword': '沪深300 上证指数 创业板 收盘 2026年3月24日', 'from_time': 1784054400}

results = []

for i, payload in enumerate([payload1, payload2], 1):
    try:
        r = requests.post(url1, json=payload, timeout=20)
        d = r.json()
        if d.get('success') and d.get('message'):
            results.append(f'=== Search {i} ===')
            results.append(d['message'][:2000])
    except Exception as e:
        results.append(f'Search {i} error: {e}')

sys.stdout.write('\n'.join(results))
