# -*- coding: utf-8 -*-
"""持仓分析 + 买入建议"""
import json
import urllib.request
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 持仓配置
portfolio = [
    {'code': '300014', 'name': '亿纬锂能', 'cost': 69.00},
    {'code': '002859', 'name': '凌云股份', 'cost': 9.80},
    {'code': '123098', 'name': '甬夕转债', 'cost': 171.00},
    {'code': '123090', 'name': '天准转债', 'cost': 174.00},
]

# 获取实时行情
def get_realtime_quote(code):
    try:
        if code.startswith('300') or code.startswith('000'):
            secid = f'0.{code}'
        elif code.startswith('123'):  # 转债
            secid = f'0.{code}'
        else:
            secid = f'0.{code}'
        
        # 获取实时数据
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f169,f170'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://quote.eastmoney.com/',
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode('utf-8', errors='replace').strip()
            if raw.startswith('jQuery'):
                raw = raw[raw.index('(')+1:raw.rindex(')')]
            data = json.loads(raw)
            
            if data.get('data'):
                d = data['data']
                return {
                    'code': code,
                    'price': d.get('f43', 0) / 100,  # 当前价
                    'open': d.get('f46', 0) / 100,  # 开盘价
                    'high': d.get('f44', 0) / 100,  # 最高价
                    'low': d.get('f45', 0) / 100,   # 最低价
                    'pre_close': d.get('f60', 0) / 100,  # 昨收
                    'volume': d.get('f47', 0),  # 成交量
                    'amount': d.get('f48', 0) / 1e8,  # 成交额（亿）
                    'pct': d.get('f170', 0) / 100,  # 涨跌幅
                    'inflow': d.get('f62', 0) / 1e8,  # 主力净流入
                }
        return None
    except Exception as e:
        print(f'获取 {code} 数据失败: {e}')
        return None

# 分析走势
def analyze_trend(data, cost):
    if not data:
        return None
    
    result = {
        'code': data['code'],
        'price': data['price'],
        'cost': cost,
        'pct': data['pct'],
        'open': data['open'],
        'high': data['high'],
        'low': data['low'],
        'pre_close': data['pre_close'],
        'amount': data['amount'],
    }
    
    # 计算收益
    if cost > 0:
        profit_pct = (data['price'] - cost) / cost * 100
        result['profit_pct'] = profit_pct
    else:
        result['profit_pct'] = 0
    
    # 判断走势
    # 开盘价 vs 当前价
    if data['price'] > data['open']:
        trend = '盘中上涨'
        trend_score = 1
    elif data['price'] < data['open']:
        trend = '盘中下跌'
        trend_score = -1
    else:
        trend = '横盘'
        trend_score = 0
    
    # 当前价 vs 昨收
    if data['price'] > data['pre_close']:
        daily_trend = '今日上涨'
        daily_score = 1
    elif data['price'] < data['pre_close']:
        daily_trend = '今日下跌'
        daily_score = -1
    else:
        daily_trend = '今日持平'
        daily_score = 0
    
    result['trend'] = trend
    result['trend_score'] = trend_score
    result['daily_trend'] = daily_trend
    result['daily_score'] = daily_score
    
    # 综合评分
    score = 50  # 基础分
    
    # 走势评分
    score += trend_score * 10
    score += daily_score * 10
    
    # 成交额评分
    if data['amount'] >= 5:
        score += 10
    elif data['amount'] >= 2:
        score += 5
    
    # 主力净流入评分
    if data.get('inflow', 0) > 0:
        score += 10
    elif data.get('inflow', 0) < -1:
        score -= 10
    
    # 距离成本价的位置
    if cost > 0:
        if data['price'] < cost * 0.95:  # 低于成本5%
            score += 15  # 买入机会
        elif data['price'] < cost:  # 低于成本
            score += 10
        elif data['price'] > cost * 1.05:  # 高于成本5%
            score -= 5  # 不建议追高
    
    result['score'] = min(max(score, 0), 100)
    
    # 买入建议
    if score >= 70:
        result['action'] = '建议买入'
        result['action_reason'] = '走势良好，成交活跃'
    elif score >= 60:
        result['action'] = '可以考虑'
        result['action_reason'] = '走势平稳，关注成交量'
    elif score >= 50:
        result['action'] = '观望'
        result['action_reason'] = '等待更好时机'
    else:
        result['action'] = '不建议买入'
        result['action_reason'] = '走势偏弱，风险较大'
    
    return result

# 主程序
print('='*60)
print('📊 持仓分析 + 买入建议')
print(f'更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print('='*60)
print()

results = []

for stock in portfolio:
    code = stock['code']
    name = stock['name']
    cost = stock['cost']
    
    print(f'分析 {name} ({code})...', end=' ')
    
    data = get_realtime_quote(code)
    if data:
        result = analyze_trend(data, cost)
        if result:
            results.append(result)
            print(f'当前价: {result["price"]:.2f}, 涨跌: {result["pct"]:+.2f}%')
        else:
            print('分析失败')
    else:
        print('数据获取失败')

print()
print('='*60)
print('📈 持仓收益分析')
print('='*60)
print()

for r in results:
    print(f"**{r['code']}**")
    print(f"  当前价: ¥{r['price']:.2f} | 涨跌: {r['pct']:+.2f}%")
    print(f"  开盘: ¥{r['open']:.2f} | 最高: ¥{r['high']:.2f} | 最低: ¥{r['low']:.2f}")
    print(f"  成交额: {r['amount']:.2f}亿")
    if r['cost'] > 0:
        print(f"  成本价: ¥{r['cost']:.2f} | 收益: {r['profit_pct']:+.2f}%")
    print(f"  走势: {r['trend']} ({r['daily_trend']})")
    print()

print('='*60)
print('💡 买入建议')
print('='*60)
print()

# 按评分排序
results.sort(key=lambda x: x['score'], reverse=True)

for i, r in enumerate(results):
    action_emoji = '🟢' if r['action'] == '建议买入' else '🟡' if r['action'] == '可以考虑' else '🔴'
    print(f"{i+1}. {action_emoji} **{r['code']}** - 评分: {r['score']}")
    print(f"   当前价: ¥{r['price']:.2f} | 涨跌: {r['pct']:+.2f}%")
    if r['cost'] > 0:
        print(f"   距成本: {r['profit_pct']:+.2f}% (成本¥{r['cost']:.2f})")
    print(f"   建议: {r['action']}")
    print(f"   理由: {r['action_reason']}")
    print()

print('='*60)
print('⚠️ 免责声明：以上仅为技术分析，不构成投资建议')
print('止损原则：股票-3%无条件出')
print('='*60)
