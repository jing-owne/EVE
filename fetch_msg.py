import warnings; warnings.filterwarnings('ignore')
import os, json, sys
os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import requests

port = os.environ.get('AUTH_GATEWAY_PORT', '19000')
url = f'http://localhost:{port}/proxy/prosearch/search'

# 搜索
payload = {'keyword': 'A股 涨跌停 数量 沪深300 上证指数 收盘 2026年3月24日', 'from_time': 1784054400}

r = requests.post(url, json=payload, timeout=20)
d = r.json()
if d.get('success') and d.get('message'):
    msg = d['message']
    # 截取前800字符
    print(msg[:800])
