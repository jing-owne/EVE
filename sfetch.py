import warnings; warnings.filterwarnings('ignore')
import os, json
os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
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
    out = json.dumps(d, ensure_ascii=False)
    # write to workspace
    with open('C:\\Users\\admin\\.qclaw\\workspace\\sres.json', 'w', encoding='utf-8') as f:
        f.write(out)
    print('OK len=' + str(len(out)))
except Exception as e:
    with open('C:\\Users\\admin\\.qclaw\\workspace\\serr.txt', 'w') as f:
        f.write(str(e))
    print('FAIL: ' + str(e))
