# -*- coding: utf-8 -*-
"""五大仓库策略综合选股"""
import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.eastmoney.com/'
}

# 策略1: 放量突破平台（myhhub/stock）
# 策略2: 换手率排名（Rockyzsu/stock）
# 策略3: 均线多头排列（myhhub/stock）
# 策略4: 主力资金净流入（综合）
# 策略5: 涨停强势股（综合）

# 获取今日强势股：涨幅>=5%且成交额>3亿
url1 = 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery&pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1'
try:
    req = urllib.request.Request(url1, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read().decode('utf-8')
        # strip jQuery wrapper
        raw = raw.strip()
        if raw.startswith('jQuery'):
            raw = raw[raw.index('(')+1:raw.rindex(')')]
        data = json.loads(raw)
        if data.get('data') and data['data'].get('diff'):
            stocks = data['data']['diff'][:50]
            print('=== 涨幅>=5%强势股 ===')
            for s in stocks[:15]:
                code = s.get('f12','')
                name = s.get('f14','')
                pct = s.get('f3', 0)
                amount = s.get('f6', 0) / 100000000
                turnover = s.get('f8', 0)
                # skip 688
                if str(code).startswith('688'):
                    continue
                print(f'{code} {name}: {pct/10:.1f}% 成交:{amount:.1f}亿 换手:{turnover/10:.2f}%')
except Exception as e:
    print('Err1:', e)

# 获取换手率排名
url2 = 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery&pn=1&pz=30&po=1&np=1&fltt=2&invt=2&fid=f8&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18&_=2'
try:
    req = urllib.request.Request(url2, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read().decode('utf-8')
        raw = raw.strip()
        if raw.startswith('jQuery'):
            raw = raw[raw.index('(')+1:raw.rindex(')')]
        data = json.loads(raw)
        if data.get('data') and data['data'].get('diff'):
            stocks = data['data']['diff'][:20]
            print('\n=== 换手率排名TOP20 ===')
            for s in stocks:
                code = s.get('f12','')
                name = s.get('f14','')
                pct = s.get('f3', 0)
                turnover = s.get('f8', 0) / 10
                amount = s.get('f6', 0) / 100000000
                if str(code).startswith('688'):
                    continue
                print(f'{code} {name}: 换手{turnover:.2f}% 涨幅{pct/10:.1f}% 成交{amount:.1f}亿')
except Exception as e:
    print('Err2:', e)

# 获取今日涨停股（不含688）
url3 = 'https://push2.eastmoney.com/api/qt/clist/get?cb=jQuery&pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11&_=3'
try:
    req = urllib.request.Request(url3, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read().decode('utf-8')
        raw = raw.strip()
        if raw.startswith('jQuery'):
            raw = raw[raw.index('(')+1:raw.rindex(')')]
        data = json.loads(raw)
        if data.get('data') and data['data'].get('diff'):
            stocks = data['data']['diff']
            print('\n=== 涨停股TOP30（不含688）===')
            count = 0
            for s in stocks:
                code = s.get('f12','')
                name = s.get('f14','')
                pct = s.get('f3', 0)
                amount = s.get('f6', 0) / 100000000
                if str(code).startswith('688'):
                    continue
                if pct >= 990:  # 涨停
                    print(f'{code} {name}: 涨停 成交{amount:.1f}亿')
                    count += 1
                    if count >= 30:
                        break
except Exception as e:
    print('Err3:', e)
