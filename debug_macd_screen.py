# -*- coding: utf-8 -*-
"""技术面筛选脚本 v2 - 放宽条件：MACD多周期向上（不必金叉）+ 7日连续上涨"""
import json
import urllib.request
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ========== 获取股票数据 ==========

def get_kline_data(code, period='101'):
    """获取K线数据"""
    if code.startswith('300') or code.startswith('000'):
        secid = f'0.{code}'
    elif code.startswith('600') or code.startswith('601') or code.startswith('603'):
        secid = f'1.{code}'
    else:
        secid = f'0.{code}'
    
    url = f'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57&klt={period}&fqt=1&end=20500101&lmt=100'
    
    try:
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
            
            if data.get('data') and data['data'].get('klines'):
                return data['data']['klines']
        return None
    except:
        return None

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    if len(prices) < slow + signal:
        return None, None, None
    
    def ema(data, period):
        multiplier = 2 / (period + 1)
        ema_values = [sum(data[:period]) / period]
        for price in data[period:]:
            ema_values.append((price - ema_values[-1]) * multiplier + ema_values[-1])
        return ema_values
    
    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)
    
    if len(ema_fast) < len(ema_slow):
        ema_fast = ema_fast[-len(ema_slow):]
    elif len(ema_slow) < len(ema_fast):
        ema_slow = ema_slow[-len(ema_fast):]
    
    dif = [f - s for f, s in zip(ema_fast, ema_slow)]
    dea = ema(dif, signal)
    
    if len(dif) < len(dea):
        dif = dif[-len(dea):]
    elif len(dea) < len(dif):
        dea = dea[-len(dif):]
    
    macd = [2 * (d - de) for d, de in zip(dif, dea)]
    
    return dif, dea, macd

def check_macd_status(dif, dea, macd):
    """检查MACD状态"""
    if not dif or not dea or len(dif) < 3 or len(dea) < 3:
        return {'golden_cross': False, 'upward': False, 'red_bar': False}
    
    # 当天金叉：DIF上穿DEA
    golden_cross = dif[-1] > dea[-1] and dif[-2] <= dea[-2]
    
    # 向上趋势：DIF和DEA最近3天都在上升
    upward = (dif[-1] > dif[-2] > dif[-3]) and (dea[-1] > dea[-2] > dea[-3])
    
    # 红柱：MACD柱为正
    red_bar = macd[-1] > 0
    
    return {'golden_cross': golden_cross, 'upward': upward, 'red_bar': red_bar}

def check_7day_upward(prices):
    """检查是否连续7天上涨"""
    if len(prices) < 7:
        return False, 0
    
    count = 0
    for i in range(-7, 0):
        if prices[i] > prices[i-1]:
            count += 1
    
    return count >= 5, count  # 放宽：5天以上上涨即可

def analyze_stock(code, name):
    """分析股票"""
    results = {
        'code': code,
        'name': name,
        'daily': {},
        'weekly': {},
        'monthly': {},
        'seven_day_up': False,
        'seven_day_count': 0,
        'score': 0
    }
    
    # 日线
    daily_klines = get_kline_data(code, '101')
    if daily_klines:
        prices = [float(k.split(',')[2]) for k in daily_klines]
        dif, dea, macd = calculate_macd(prices)
        
        if dif and dea and macd:
            results['daily'] = check_macd_status(dif, dea, macd)
            
            up, count = check_7day_upward(prices)
            results['seven_day_up'] = up
            results['seven_day_count'] = count
    
    # 周线
    weekly_klines = get_kline_data(code, '102')
    if weekly_klines:
        prices = [float(k.split(',')[2]) for k in weekly_klines]
        dif, dea, macd = calculate_macd(prices)
        
        if dif and dea and macd:
            results['weekly'] = check_macd_status(dif, dea, macd)
    
    # 月线
    monthly_klines = get_kline_data(code, '103')
    if monthly_klines:
        prices = [float(k.split(',')[2]) for k in monthly_klines]
        dif, dea, macd = calculate_macd(prices)
        
        if dif and dea and macd:
            results['monthly'] = check_macd_status(dif, dea, macd)
    
    # 计算得分
    score = 0
    if results.get('daily', {}).get('upward'):
        score += 25
    if results.get('daily', {}).get('golden_cross'):
        score += 10
    if results.get('daily', {}).get('red_bar'):
        score += 5
    
    if results.get('weekly', {}).get('upward'):
        score += 25
    if results.get('weekly', {}).get('golden_cross'):
        score += 10
    if results.get('weekly', {}).get('red_bar'):
        score += 5
    
    if results.get('monthly', {}).get('upward'):
        score += 25
    if results.get('monthly', {}).get('golden_cross'):
        score += 10
    if results.get('monthly', {}).get('red_bar'):
        score += 5
    
    if results['seven_day_up']:
        score += 30
    
    results['score'] = min(score, 100)
    
    return results

# ========== 主程序 ==========

if __name__ == '__main__':
    print('[DEBUG] MACD多周期共振筛选（放宽条件）\n')
    
    fs = 'm:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23'
    url = f'https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f3&fs={fs}&fields=f3,f12,f14'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://finance.eastmoney.com/',
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode('utf-8', errors='replace').strip()
            if raw.startswith('jQuery'):
                raw = raw[raw.index('(')+1:raw.rindex(')')]
            data = json.loads(raw)
            
            if data.get('data') and data['data'].get('diff'):
                stocks = data['data']['diff']
                
                results_list = []
                
                for i, stock in enumerate(stocks[:30]):
                    code = str(stock.get('f12', ''))
                    name = stock.get('f14', '')
                    
                    if code.startswith('688') or code.startswith('8'):
                        continue
                    
                    print(f'[{i+1}/30] {name} ({code})...', end=' ')
                    
                    result = analyze_stock(code, name)
                    results_list.append(result)
                    
                    if result['score'] >= 70:
                        print(f"✓ 得分={result['score']} (日:{result['daily'].get('upward', False)} 周:{result['weekly'].get('upward', False)} 月:{result['monthly'].get('upward', False)} 7日:{result['seven_day_count']})")
                    else:
                        print(f"得分={result['score']}")
                
                # 排序
                results_list.sort(key=lambda x: x['score'], reverse=True)
                
                print(f'\n{"="*60}')
                print(f'TOP10 多周期共振得分')
                print(f'{"="*60}\n')
                
                for i, r in enumerate(results_list[:10]):
                    d = r['daily']
                    w = r['weekly']
                    m = r['monthly']
                    
                    print(f"{i+1}. {r['name']} ({r['code']}) - 得分: {r['score']}")
                    print(f"   日线: 向上={d.get('upward', False)} 金叉={d.get('golden_cross', False)} 红柱={d.get('red_bar', False)}")
                    print(f"   周线: 向上={w.get('upward', False)} 金叉={w.get('golden_cross', False)} 红柱={w.get('red_bar', False)}")
                    print(f"   月线: 向上={m.get('upward', False)} 金叉={m.get('golden_cross', False)} 红柱={m.get('red_bar', False)}")
                    print(f"   7日上涨: {r['seven_day_count']}/7天")
                    print()
            
    except Exception as e:
        print(f'错误: {e}')
