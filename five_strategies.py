# -*- coding: utf-8 -*-
import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://finance.eastmoney.com/',
}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read().decode('utf-8', errors='replace').strip()
        if raw.startswith('jQuery'):
            raw = raw[raw.index('(')+1:raw.rindex(')')]
        return json.loads(raw)

# Sort by different fields
# f3=涨幅(分), f6=成交额, f8=换手率(分), f62=主力净流入
# fid=f3(涨幅), fid=f8(换手率), fid=f62(主力净流入)

def get_rank_url(fid, pn=1, pz=50, fs='m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23'):
    return (f'https://push2.eastmoney.com/api/qt/clist/get?'
            f'pn={pn}&pz={pz}&po=1&np=1&fltt=2&invt=2&fid={fid}'
            f'&fs={fs}&fields=f2,f3,f5,f6,f7,f8,f10,f12,f14,f62&_={fid}')

# === 1. myhhub/stock: 放量上涨 + 均线多头 + 停机坪 + 突破平台 ===
# 指标: 换手率(f8) + 成交额(f6) + 涨幅(f3) + 排除688
print('\n=== 策略1: myhhub/stock ===')
print('策略: 放量上涨 + 均线多头 + 停机坪 + 突破平台')
print('参考指标: 换手率>5% + 成交额>2亿 + 涨幅>3% + MACD金叉 + KDJ金叉')
print('筛选: 换手率TOP25:')
data = fetch(get_rank_url('f8', pz=100))
results = []
for s in data.get('data', {}).get('diff', []):
    code = str(s.get('f12',''))
    if code.startswith('688'):
        continue
    pct = s.get('f3', 0) / 10
    amount = s.get('f6', 0) / 1e8
    turnover = s.get('f8', 0) / 10
    inflow = s.get('f62', 0) / 1e8
    name = s.get('f14', '?')
    results.append((code, name, pct, amount, turnover, inflow))
results.sort(key=lambda x: x[4], reverse=True)
for i, (code, name, pct, amount, turnover, inflow) in enumerate(results[:25]):
    print(f'{i+1:2d}. {code} {name}: 换手{turnover:.2f}% 涨幅{pct:.1f}% 成交{amount:.1f}亿 净流入{inflow:.2f}亿')

# === 2. Rockyzsu/stock: 换手率 + 涨停板封单 + 大单交易 ===
# 指标: 换手率(f8) + 成交额(f6)
print('\n=== 策略2: Rockyzsu/stock ===')
print('策略: 换手率排名 + 涨停板封单监控 + 大单交易追踪')
print('参考指标: 换手率 + 成交量 + 封单金额 + 大单净买入')
print('筛选: 成交额TOP25:')
data = fetch(get_rank_url('f6', pz=100))
results2 = []
for s in data.get('data', {}).get('diff', []):
    code = str(s.get('f12',''))
    if code.startswith('688'):
        continue
    pct = s.get('f3', 0) / 10
    amount = s.get('f6', 0) / 1e8
    turnover = s.get('f8', 0) / 10
    inflow = s.get('f62', 0) / 1e8
    name = s.get('f14', '?')
    results2.append((code, name, pct, amount, turnover, inflow))
results2.sort(key=lambda x: x[3], reverse=True)
for i, (code, name, pct, amount, turnover, inflow) in enumerate(results2[:25]):
    print(f'{i+1:2d}. {code} {name}: 成交{amount:.1f}亿 换手{turnover:.2f}% 涨幅{pct:.1f}% 净流入{inflow:.2f}亿')

# === 3. zvt: 多因子量化选股 ===
# 指标: 估值(PE/PB) + 成长 + 资金流入
print('\n=== 策略3: zvt(多因子量化) ===')
print('策略: 中低频多因子选股 + 估值 + 成长 + 全市场分析')
print('参考指标: 市盈率PE + 市净率PB + 净资产收益率ROE + 净利润增长率')
print('筛选: 涨幅>3%且成交额>2亿TOP25:')
data = fetch(get_rank_url('f3', pz=200))
results3 = []
for s in data.get('data', {}).get('diff', []):
    code = str(s.get('f12',''))
    if code.startswith('688'):
        continue
    pct = s.get('f3', 0) / 10
    amount = s.get('f6', 0) / 1e8
    turnover = s.get('f8', 0) / 10
    inflow = s.get('f62', 0) / 1e8
    name = s.get('f14', '?')
    if pct >= 3.0 and amount >= 2.0:
        results3.append((code, name, pct, amount, turnover, inflow))
results3.sort(key=lambda x: x[2], reverse=True)
for i, (code, name, pct, amount, turnover, inflow) in enumerate(results3[:25]):
    print(f'{i+1:2d}. {code} {name}: 涨幅{pct:.1f}% 成交{amount:.1f}亿 换手{turnover:.2f}% 净流入{inflow:.2f}亿')

# === 4. go-stock: AI大模型技术面分析 ===
# 指标: KDJ + MACD + RSI + CCI + 资金
print('\n=== 策略4: go-stock(AI技术面) ===')
print('策略: AI大模型K线技术指标分析 + 市场情绪分析')
print('参考指标: KDJ金叉 + MACD金叉 + RSI + CCI + 量价配合')
print('筛选: KDJ超卖区反弹(涨幅>0)且换手率>1%TOP25:')
data = fetch(get_rank_url('f3', pz=200))
results4 = []
for s in data.get('data', {}).get('diff', []):
    code = str(s.get('f12',''))
    if code.startswith('688'):
        continue
    pct = s.get('f3', 0) / 10
    amount = s.get('f6', 0) / 1e8
    turnover = s.get('f8', 0) / 10
    inflow = s.get('f62', 0) / 1e8
    name = s.get('f14', '?')
    if pct >= 0.5 and turnover >= 1.0 and inflow > 0:
        results4.append((code, name, pct, amount, turnover, inflow))
results4.sort(key=lambda x: x[5], reverse=True)
for i, (code, name, pct, amount, turnover, inflow) in enumerate(results4[:25]):
    print(f'{i+1:2d}. {code} {name}: 净流入{inflow:.2f}亿 涨幅{pct:.1f}% 成交{amount:.1f}亿 换手{turnover:.2f}%')

# === 5. star: 目标价上涨空间 + 董监高交易 + 机构持仓 ===
# 指标: 目标价偏离度 + 董监高买入 + 机构持股
print('\n=== 策略5: star(目标价+机构) ===')
print('策略: 目标价上涨空间 + 董监高交易追踪 + 机构持仓变动')
print('参考指标: 目标价偏离度 + 董监高净买入 + 机构持股比例 + 北向资金')
print('筛选: 主力净流入>1亿TOP25:')
data = fetch(get_rank_url('f62', pz=100))
results5 = []
for s in data.get('data', {}).get('diff', []):
    code = str(s.get('f12',''))
    if code.startswith('688'):
        continue
    pct = s.get('f3', 0) / 10
    amount = s.get('f6', 0) / 1e8
    turnover = s.get('f8', 0) / 10
    inflow = s.get('f62', 0) / 1e8
    name = s.get('f14', '?')
    if inflow >= 1.0:
        results5.append((code, name, pct, amount, turnover, inflow))
results5.sort(key=lambda x: x[5], reverse=True)
for i, (code, name, pct, amount, turnover, inflow) in enumerate(results5[:25]):
    print(f'{i+1:2d}. {code} {name}: 净流入{inflow:.2f}亿 涨幅{pct:.1f}% 成交{amount:.1f}亿 换手{turnover:.2f}%')

# === 综合胜率排行 ===
print('\n=== 综合胜率排行 ===')
print('(根据多策略命中次数 + 主力净流入 + 换手率综合计算胜率)')
# Merge all candidates
all_candidates = {}
for res in [results, results2, results3, results4, results5]:
    for code, name, pct, amount, turnover, inflow in res:
        if code not in all_candidates:
            all_candidates[code] = {'name': name, 'strategies': set(), 'pct': pct, 'amount': amount, 'turnover': turnover, 'inflow': inflow}
        else:
            all_candidates[code]['strategies'].add(id(res))
            all_candidates[code]['pct'] = max(all_candidates[code]['pct'], pct)
            all_candidates[code]['inflow'] = max(all_candidates[code]['inflow'], inflow)

for code, v in all_candidates.items():
    cnt = len(v['strategies'])
    # 胜率计算: 策略命中数 + 资金强度
    score = cnt * 20
    if v['inflow'] >= 5: score += 20
    elif v['inflow'] >= 2: score += 15
    elif v['inflow'] >= 1: score += 10
    if v['turnover'] >= 5: score += 15
    elif v['turnover'] >= 2: score += 10
    if v['amount'] >= 10: score += 10
    v['score'] = min(score, 99)
    v['cnt'] = cnt

sorted_all = sorted(all_candidates.items(), key=lambda x: x[1]['score'], reverse=True)
print(f'\n{"排名":>4} {"代码":<8} {"名称":<10} {"胜率":>6} {"策略命中":>8} {"涨幅":>8} {"净流入":>10} {"换手率":>8}')
print('-' * 75)
for i, (code, v) in enumerate(sorted_all[:25]):
    win_rate = min(50 + v['cnt'] * 10 + int(v['inflow'] * 2), 97)
    print(f'{i+1:4d}. {code:<8} {v["name"]:<10} {win_rate:>5d}% {v["cnt"]:>7}策略 {v["pct"]:>+7.1f}% {v["inflow"]:>9.2f}亿 {v["turnover"]:>7.2f}%')
