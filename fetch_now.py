import warnings; warnings.filterwarnings('ignore')
import os, json, sys
os.environ['TMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP']='C:\\Users\\admin\\AppData\\Local\\Temp'
import requests

port = os.environ.get('AUTH_GATEWAY_PORT', '19000')
url = f'http://localhost:{port}/proxy/prosearch/search'
payload = {'keyword': '今日A股涨跌停数量 2026年3月24日', 'from_time': 1784054400}
try:
    r = requests.post(url, json=payload, timeout=20)
    d = r.json()
    sys.stdout.write('SUCCESS' if d.get('success') else 'FAIL')
    sys.stdout.write('|HASMSG' if d.get('message') else '|NOMSG')
except Exception as e:
    sys.stdout.write('ERROR:' + str(e))
