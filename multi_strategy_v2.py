# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://finance.eastmoney.com/',
    'Accept': 'application/json',
}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read().decode('utf-8', errors='replace')
        raw = raw.strip()
        if raw.startswith('jQuery'):
            raw = raw[raw.index('(')+1:raw.rindex(')')]
        return json.loads(raw)

# === 1. myhhub/stock 策略: 放量上涨 + 均线多头 + 停机坪 + 突破平台 ===
# 筛选: 换手率>5% + 成交额>2亿 + 涨幅>3% + 排除688
print('\n=== 策略1: myhhub/stock (放量突破+换手率) ===')
url = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=100&po=1&np=1&fltt=2&invt=2&fid=f8&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f2,f3,f5,f6,f7,f8,f10,f12,f14,f62&_=1'
try:
    data = fetch(url)
    if data.get('data') and data['data'].get('diff'):
        print('\n换手率TOP30 (排除688):')
        for i, s in enumerate(data['data']['diff'][:30]):
            code = str(s.get('f12',''))
            if code.startswith('688'):
                continue
            name = s.get('f14','?')
            pct = s.get('f3', 0) / 10
            turnover = s.get('f8', 0) / 10
            amount = s.get('f6', 0) / 100000000
            if pct > 0:
                print(f'{code} {name}: 换手{turnover:.2f}% 涨幅{pct:.1f}% 成交{amount:.1f}亿')
except Exception as e:
    print('Err:', e)

# === 2. Rockyzsu/stock 策略: 换手率前50热门股 ===
print('\n=== 策略2: Rockyzsu/stock (换手率+成交量) ===')
url2 = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f8&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f2,f3,f5,f6,f7,f8,f10,f12,f14,f62&_=2'
try:
    data = fetch(url2)
    if data.get('data') and data['data'].get('diff'):
        print('\n高换手活跃股 (排除688):')
        for s in data['data']['diff'][:30]:
            code = str(s.get('f12',''))
            if code.startswith('688'):
                continue
            name = s.get('f14','?')
            pct = s.get('f3', 0) / 10
            turnover = s.get('f8', 0) / 10
            amount = s.get('f6', 0) / 100000000
            print(f'{code} {name}: 换手{turnover:.2f}% 涨幅{pct:.1f}% 成交{amount:.1f}亿')
except Exception as e:
    print('Err:', e)

# === 3. 主力资金净流入排行 ===
print('\n=== 策略3: 主力资金净流入排行 ===')
url3 = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f2,f3,f5,f6,f7,f8,f10,f12,f14,f62&_=3'
try:
    data = fetch(url3)
    if data.get('data') and data['data'].get('diff'):
        print('\n主力净流入TOP30 (排除688):')
        for s in data['data']['diff'][:30]:
            code = str(s.get('f12',''))
            if code.startswith('688'):
                continue
            name = s.get('f14','?')
            pct = s.get('f3', 0) / 10
            inflow = s.get('f62', 0) / 100000000  # 主力净流入(元)
            if inflow > 0:
                print(f'{code} {name}: 主力净流入{inflow:.2f}亿 涨幅{pct:.1f}%')
except Exception as e:
    print('Err:', e)

# === 4. 涨停板封单金额 ===
print('\n=== 策略4: 涨停强势股 ===')
url4 = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f2,f3,f5,f6,f7,f8,f10,f12,f14&_=4'
try:
    data = fetch(url4)
    if data.get('data') and data['data'].get('diff'):
        print('\n涨停/大涨股 (排除688):')
        count = 0
        for s in data['data']['diff']:
            code = str(s.get('f12',''))
            if code.startswith('688'):
                continue
            name = s.get('f14','?')
            pct = s.get('f3', 0) / 10
            amount = s.get('f6', 0) / 100000000
            if pct >= 950:  # 接近涨停
                print(f'{code} {name}: 涨停 成交{amount:.1f}亿')
                count += 1
                if count >= 20:
                    break
except Exception as e:
    print('Err:', e)

print('\n=== 综合汇总: 满足多策略共振的标的 ===')
print('(换手率>=5% + 涨幅>=3% + 成交额>=2亿 + 主力净流入)')

# 综合筛选
try:
    # Get combined data
    url_c = 'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=200&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f2,f3,f5,f6,f7,f8,f10,f12,f14,f62&_=5'
    data = fetch(url_c)
    if data.get('data') and data['data'].get('diff'):
        candidates = []
        for s in data['data']['diff']:
            code = str(s.get('f12',''))
            if code.startswith('688'):
                continue
            name = s.get('f14','?')
            pct = s.get('f3', 0) / 10
            turnover = s.get('f8', 0) / 10
            amount = s.get('f6', 0) / 100000000
            inflow = s.get('f62', 0) / 100000000
            score = 0
            if turnover >= 5: score += 1
            if pct >= 5: score += 1
            if amount >= 2: score += 1
            if inflow > 1: score += 1
            if score >= 3 and pct > 0:
                candidates.append({
                    'code': code,
                    'name': name,
                    'pct': pct,
                    'turnover': turnover,
                    'amount': amount,
                    'inflow': inflow,
                    'score': score
                })
        candidates.sort(key=lambda x: (x['score'], x['pct']), reverse=True)
        print('\n综合评分>=3的标的:')
        for c in candidates[:15]:
            print(f"{c['code']} {c['name']}: 评分{c['score']} 涨幅{c['pct']:.1f}% 换手{c['turnover']:.2f}% 成交{c['amount']:.1f}亿 净流入{c['inflow']:.2f}亿")
except Exception as e:
    print('Err:', e)
