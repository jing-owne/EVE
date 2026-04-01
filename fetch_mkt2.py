import warnings; warnings.filterwarnings('ignore')
import os, json
os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import requests

port = os.environ.get('AUTH_GATEWAY_PORT', '19000')
url = f'http://localhost:{port}/proxy/prosearch/search'

# 搜索1: 涨跌停数量
payload1 = {'keyword': 'A股 涨跌停 数量 2026年3月24日', 'from_time': 1784054400}

# 搜索2: 大盘指数
payload2 = {'keyword': '沪深300 上证指数 创业板 收盘 2026年3月24日', 'from_time': 1784054400}

all_data = {}

for name, payload in [('zt', payload1), ('idx', payload2)]:
    try:
        r = requests.post(url, json=payload, timeout=20)
        d = r.json()
        if d.get('success') and d.get('message'):
            all_data[name] = d['message']
    except Exception as e:
        all_data[name] = f'error: {e}'

# write to file
with open('C:\\Users\\admin\\.qclaw\\workspace\\mkt_search.txt', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)
print('saved')
