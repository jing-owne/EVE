import warnings; warnings.filterwarnings('ignore')
import os, json
os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'

try:
    import requests
    port = os.environ.get('AUTH_GATEWAY_PORT', '19000')
    url = f'http://localhost:{port}/proxy/prosearch/search'
    payload = {
        'keyword': '今日A股大盘指数收盘 涨跌停数量 2026年3月24日',
        'from_time': 1784054400
    }
    resp = requests.post(url, json=payload, timeout=15)
    print('status:', resp.status_code)
    data = resp.json()
    print(data.get('message', data))
except Exception as e:
    import traceback; traceback.print_exc()
