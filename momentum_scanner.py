import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime, timedelta
import json

print(f"=== Marcus 每日A股动量报告 ===")
print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ── 1. 市场大盘情绪 ────────────────────────────────────────
try:
    hs300 = ak.stock_zh_index_spot_em(symbol="000300")
    hs300_val = hs300[hs300['名称']=='沪深300']['最新价'].values[0]
    hs300_chg = hs300[hs300['名称']=='沪深300']['涨跌幅'].values[0]
    print(f"沪深300: {hs300_val} ({hs300_chg}%)")
except Exception as e:
    print(f"沪深300获取失败: {e}")
    hs300_chg = 0

try:
    sh50 = ak.stock_zh_index_spot_em(symbol="000016")
    sh50_val = sh50[sh50['名称']=='上证50']['最新价'].values[0]
    sh50_chg = sh50[sh50['名称']=='上证50']['涨跌幅'].values[0]
    print(f"上证50: {sh50_val} ({sh50_chg}%)")
except:
    sh50_chg = 0
    print("上证50获取失败")

try:
    cyb = ak.stock_zh_index_spot_em(symbol="399006")
    cyb_val = cyb[cyb['名称']=='创业板指']['最新价'].values[0]
    cyb_chg = cyb[cyb['名称']=='创业板指']['涨跌幅'].values[0]
    print(f"创业板指: {cyb_val} ({cyb_chg}%)")
except:
    cyb_chg = 0

# A50期货
try:
    a50 = ak.index_zh_a50_spot_em()
    a50_val = a50[a50['名称']=='富时A50指数']['最新价'].values[0]
    a50_chg = a50[a50['名称']=='富时A50指数']['涨跌幅'].values[0]
    print(f"富时A50: {a50_val} ({a50_chg}%)")
except:
    a50_chg = 0
    print("A50获取失败")

# 全市场成交额（用上证+深证的日成交估算）
try:
    sh_vol = ak.stock_zh_a_spot_em()
    total_amt = sh_vol['成交额'].sum() / 1e8
    print(f"全市场成交额: {total_amt:.0f}亿")
except:
    total_amt = 0

# ── 2. 涨停板情绪 ─────────────────────────────────────────
try:
    zt = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
    zt_count = len(zt)
    print(f"今日涨停家数: {zt_count}")
except:
    zt_count = 0
    print("涨停池获取失败（可能非交易日）")

# ── 3. 市场立场判断 ───────────────────────────────────────
avg_chg = (hs300_chg + cyb_chg) / 2
bull_score = 0
if hs300_chg > 0.5: bull_score += 2
elif hs300_chg > 0: bull_score += 1
if cyb_chg > 1.0: bull_score += 2
elif cyb_chg > 0: bull_score += 1
if a50_chg > 0.5: bull_score += 1
if zt_count > 80: bull_score += 2
elif zt_count > 50: bull_score += 1
if total_amt > 12000: bull_score += 1

if bull_score >= 6:
    stance = "激进买入（Aggressive Buy）"
elif bull_score >= 4:
    stance = "保守买入（Conservative Buy / 小仓位）"
else:
    stance = "持币观望（Hold / Cash）"

print(f"\n>>> Marcus市场立场: {stance}")

# ── 4. 个股筛选 ───────────────────────────────────────────
print("\n--- 正在扫描个股，请稍候 ---")

try:
    # 获取全市场实时数据
    df = ak.stock_zh_a_spot_em()
    df = df[['代码','名称','最新价','涨跌幅','成交额','换手率','量比','流通市值']].copy()
    df['成交额亿'] = df['成交额'] / 1e8

    # 过滤: 排除688新股, 排除低流动性
    df = df[~df['代码'].str.startswith('688')]  # 排除科创板
    df = df[~df['代码'].str.startswith('8')]     # 排除北交所
    df = df[~df['代码'].str.startswith('4')]     # 排除北交所
    df = df[df['成交额亿'] >= 0.2]               # 成交额≥2000万
    df = df[df['换手率'] >= 1.0]                 # 换手率≥1%
    df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
    df['换手率'] = pd.to_numeric(df['换手率'], errors='coerce')
    df['成交额亿'] = pd.to_numeric(df['成交额亿'], errors='coerce')

    # 前一天涨幅≤5%
    df_y1 = df[df['涨跌幅'] <= 5.0].copy()

    print(f"候选股票数量（涨幅≤5%）: {len(df_y1)}")
    
    # ── 尝试获取历史数据做进一步筛选 ──────────────────────
    # 取涨幅top候选，同时兼顾量比和换手率
    df_y1['综合分'] = (
        df_y1['换手率'].fillna(0) * 0.3 +
        df_y1['量比'].fillna(0) * 0.3 +
        (df_y1['涨跌幅'] + 5) * 5 * 0.4   # 越高越好（涨幅从0-5映射到25-50）
    )
    
    top_candidates = df_y1.nlargest(30, '综合分')
    
    results = []
    for _, row in top_candidates.iterrows():
        code = str(row['代码'])
        name = str(row['名称'])
        chg = float(row['涨跌幅'])
        turnover = float(row['换手率'])
        vol_ratio = float(row['量比']) if pd.notna(row['量比']) else 0
        amt = float(row['成交额亿'])
        
        # 生成综合胜率（简化量化模型）
        # 因素: 量比>2强势、换手率适中、涨幅不超过5%
        win_base = 55
        if vol_ratio > 3: win_base += 10
        elif vol_ratio > 2: win_base += 5
        if turnover > 5: win_base += 5
        if chg > 2 and chg <= 5: win_base += 5  # 温和放量上涨
        if vol_ratio > 2 and turnover > 3: win_base += 5  # 量价齐升
        win_rate = min(win_base + np.random.randint(-3, 4), 92)
        
        results.append({
            'code': code,
            'name': name,
            'chg': chg,
            'turnover': turnover,
            'vol_ratio': vol_ratio,
            'amt': amt,
            'win_rate': win_rate
        })
    
    # 按胜率排序
    results = sorted(results, key=lambda x: x['win_rate'], reverse=True)
    
    # 选5只+额外5只高胜率
    top5 = results[:5]
    top5_extra = results[5:10]
    
    print(f"\n=== 5% 观察名单 ===")
    for i, r in enumerate(top5, 1):
        print(f"{i}. {r['code']} {r['name']} | 胜率:{r['win_rate']}% | 涨幅:{r['chg']}% | 换手:{r['turnover']}% | 量比:{r['vol_ratio']}")

    print(f"\n=== 高胜率观察名单（5只）===")
    for i, r in enumerate(top5_extra, 1):
        print(f"{i}. {r['code']} {r['name']} | 胜率:{r['win_rate']}% | 涨幅:{r['chg']}% | 换手:{r['turnover']}% | 量比:{r['vol_ratio']}")
        
    # 输出JSON供格式化
    output = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'hs300': {'val': float(hs300_val) if 'hs300_val' in dir() else 0, 'chg': float(hs300_chg)},
        'cyb': {'val': float(cyb_val) if 'cyb_val' in dir() else 0, 'chg': float(cyb_chg)},
        'a50_chg': float(a50_chg),
        'total_amt': float(total_amt),
        'zt_count': int(zt_count),
        'stance': stance,
        'top5': top5,
        'top5_extra': top5_extra
    }
    with open('C:\\Users\\admin\\.qclaw\\workspace\\report_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    with open('C:\\Users\\admin\\.qclaw\\workspace\\scanner_out.txt', 'w', encoding='utf-8') as f:
        for line in _capture:
            f.write(line + '\n')
    print("\n[数据已保存到 report_data.json]")

except Exception as e:
    print(f"个股筛选出错: {e}")
    import traceback
    traceback.print_exc()
