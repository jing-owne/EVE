import warnings; warnings.filterwarnings('ignore')
import os, json
os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['PYTHONIOENCODING']='utf-8'

import requests

port = os.environ.get('AUTH_GATEWAY_PORT', '19000')
url = f'http://localhost:{port}/proxy/prosearch/search'
payload = {
    'keyword': '今日A股大盘指数收盘 涨跌停数量 2026年3月24日',
    'from_time': 1784054400
}
try:
    resp = requests.post(url, json=payload, timeout=15)
    d = resp.json()
    out = json.dumps(d, ensure_ascii=False, indent=2)
    with open('C:\\Users\\admin\\AppData\\Local\\Temp\\search_result.json', 'w', encoding='utf-8') as f:
        f.write(out)
    print('saved, keys:', list(d.keys()))
    print('success:', d.get('success'))
except Exception as e:
    import traceback; traceback.print_exc()
