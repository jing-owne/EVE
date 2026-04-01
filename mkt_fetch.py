import warnings, os, json, sys, requests
warnings.filterwarnings('ignore')
os.environ['TMP'] = os.environ['TEMP'] = 'C:\\Users\\admin\\AppData\\Local\\Temp'

port = os.environ.get('AUTH_GATEWAY_PORT', '19000')
base = f'http://localhost:{port}/proxy/prosearch/search'

queries = [
    'A股今日涨停跌停数量 2026年3月24日',
    '沪深300 上证指数 创业板 今日收盘 2026年3月24日',
]

all_msgs = []
for kw in queries:
    try:
        r = requests.post(base, json={'keyword': kw, 'from_time': 1742745600}, timeout=20)
        d = r.json()
        if d.get('success') and d.get('message'):
            all_msgs.append(d['message'])
    except Exception as e:
        all_msgs.append(f'error: {e}')

combined = '\n\n---\n\n'.join(all_msgs)
# write ascii-safe
with open('C:\\Users\\admin\\.qclaw\\workspace\\mkt_raw.txt', 'w', encoding='utf-8', errors='replace') as f:
    f.write(combined)
print('done len=' + str(len(combined)))
