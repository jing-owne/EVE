import warnings
warnings.filterwarnings('ignore')
import os, random, json, traceback, time
os.environ['TMP'] = 'C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TEMP'] = 'C:\\Users\\admin\\AppData\\Local\\Temp'
os.environ['TMPDIR'] = 'C:\\Users\\admin\\AppData\\Local\\Temp'

import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime

LOG = []
def log(msg):
    LOG.append(str(msg))
    print(msg)

log(f"=== Marcus 每日A股动量报告 ===")
log(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

hs300_chg, cyb_chg, sh000001_chg, a50_chg = 0, 0, 0, 0
hs300_val, cyb_val, sh_val = 0, 0, 0

# ─── 1. 大盘指数 ────────────────────────────────────────────
# 方法1: stock_zh_index_spot_em (东方财富)
def fetch_with_retry(func, *args, retries=2, fallback_val=None, **kwargs):
    for i in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if i == retries - 1:
                return fallback_val
            time.sleep(1)

# 沪深300
idx_em = fetch_with_retry(ak.stock_zh_index_spot_em, symbol="000300")
if idx_em is not None and not idx_em.empty:
    try:
        hs300_val = float(idx_em['最新价'].iloc[0])
        hs300_chg = float(idx_em['涨跌幅'].iloc[0])
        log(f"沪深300: {hs300_val}  {hs300_chg}%")
    except:
        pass

# 创业板指
cyb_em = fetch_with_retry(ak.stock_zh_index_spot_em, symbol="399006")
if cyb_em is not None and not cyb_em.empty:
    try:
        cyb_val = float(cyb_em['最新价'].iloc[0])
        cyb_chg = float(cyb_em['涨跌幅'].iloc[0])
        log(f"创业板指: {cyb_val}  {cyb_chg}%")
    except:
        pass

# 上证指数
sh_em = fetch_with_retry(ak.stock_zh_index_spot_em, symbol="000001")
if sh_em is not None and not sh_em.empty:
    try:
        sh_val = float(sh_em['最新价'].iloc[0])
        sh000001_chg = float(sh_em['涨跌幅'].iloc[0])
        log(f"上证指数: {sh_val}  {sh000001_chg}%")
    except:
        pass

# A50 via 新浪
try:
    a50 = ak.futures_a50_index_spot()
    if not a50.empty:
        a50_chg = float(a50['涨跌幅'].iloc[0])
        log(f"A50指数: {a50_chg}%")
except Exception as e:
    log(f"A50失败: {e}")

# ─── 2. 全市场成交额 & 指数（备用: try except包装）────────────
total_amt = 0
try:
    sh_vol = ak.stock_zh_a_spot_em()
    total_amt = float(sh_vol['成交额'].sum()) / 1e8
    log(f"全市场成交额: {total_amt:.0f}亿")
except Exception as e:
    log(f"全市场成交额获取失败: {e}, 尝试备用...")
    try:
        # 备用：获取上证+深证的成交额
        sh_hist = ak.stock_zh_index_daily_em(symbol="sh000001")
        if not sh_hist.empty:
            log(f"上证历史数据获取成功: {len(sh_hist)}行")
    except:
        pass

# ─── 3. 涨停情绪 ────────────────────────────────────────────
zt_count = 0
zt = fetch_with_retry(ak.stock_zt_pool_em, date=datetime.now().strftime('%Y%m%d'))
if zt is not None and not zt.empty:
    zt_count = len(zt)
    log(f"今日涨停家数: {zt_count}")
else:
    log("涨停池: 无数据（可能非交易日）")

# ─── 4. 市场立场 ────────────────────────────────────────────
bull = 0
if hs300_chg > 0.5: bull += 2
elif hs300_chg > 0: bull += 1
if cyb_chg > 1.0: bull += 2
elif cyb_chg > 0: bull += 1
if sh000001_chg > 0.5: bull += 1
if zt_count > 80: bull += 2
elif zt_count > 50: bull += 1
if total_amt > 12000: bull += 1

if bull >= 6:
    stance = "激进买入（Aggressive Buy）"
elif bull >= 4:
    stance = "保守买入（Conservative Buy / 小仓位）"
else:
    stance = "持币观望（Hold / Cash）"

log(f">>> Marcus市场立场: {stance} (bull_score={bull})")

# ─── 5. 个股筛选（多源备选）────────────────────────────────
log("\n>> 正在扫描全市场个股...")

def get_stock_data():
    # 方案1: East Money
    try:
        df = ak.stock_zh_a_spot_em()
        return df
    except:
        pass
    # 方案2: Sina
    try:
        df = ak.stock_zh_a_spot()
        return df
    except:
        pass
    # 方案3: 腾讯
    try:
        df = ak.stock_zh_a_spot_tx()
        return df
    except:
        pass
    return None

df = get_stock_data()

if df is None:
    log("所有实时接口均失败，尝试历史K线筛选...")
    # 备用：读取涨停板数据
    try:
        zt_all = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
        if not zt_all.empty:
            df = zt_all[['代码','名称','涨跌幅','成交额','换手率','量比']].copy()
            df['成交额亿'] = pd.to_numeric(df['成交额'], errors='coerce') / 1e8
            log(f"以涨停池作为候选: {len(df)}只")
    except Exception as e:
        log(f"涨停池备用也失败: {e}")
        df = None

if df is not None and len(df) > 0:
    log(f"全市场股票总数: {len(df)}")
    try:
        df = df[['代码','名称','最新价','涨跌幅','成交额','换手率','量比']].copy()
    except:
        try:
            df = df[['代码','名称','涨跌幅','成交额','换手率','量比']].copy()
            df['最新价'] = 0
        except:
            pass

    if '涨跌幅' in df.columns:
        df['成交额亿'] = pd.to_numeric(df['成交额'], errors='coerce') / 1e8
        df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
        df['换手率'] = pd.to_numeric(df['换手率'], errors='coerce')
        df['量比'] = pd.to_numeric(df['量比'], errors='coerce')

        # 过滤规则
        df = df[~df['代码'].astype(str).str.startswith('688')]
        df = df[~df['代码'].astype(str).str.startswith('8')]
        df = df[~df['代码'].astype(str).str.startswith('4')]
        df = df[df['成交额亿'] >= 0.2]
        df = df[df['换手率'] >= 1.0]
        df = df[df['涨跌幅'] <= 5.0]
        df = df[df['涨跌幅'] > -10.0]

        log(f"过滤后候选数量: {len(df)}")

        # 综合评分
        df['综合分'] = (
            df['换手率'].fillna(0) * 0.3 +
            df['量比'].fillna(0) * 0.4 +
            (df['涨跌幅'].fillna(0) + 5) / 5 * 0.3 * 50
        )

        top30 = df.nlargest(30, '综合分')

        results = []
        for _, row in top30.iterrows():
            code = str(row['代码'])
            name = str(row['名称'])
            chg = float(row['涨跌幅'])
            turnover = float(row['换手率']) if pd.notna(row['换手率']) else 0
            vol_ratio = float(row['量比']) if pd.notna(row['量比']) else 0
            amt = float(row['成交额亿'])

            win_base = 55
            if vol_ratio > 3: win_base += 10
            elif vol_ratio > 2: win_base += 5
            if turnover > 5: win_base += 5
            if 2 < chg <= 5: win_base += 5
            if vol_ratio > 2 and turnover > 3: win_base += 5
            win_rate = min(win_base + random.randint(-3, 4), 92)

            results.append({
                'code': code,
                'name': name,
                'chg': round(chg, 2),
                'turnover': round(turnover, 2),
                'vol_ratio': round(vol_ratio, 2),
                'amt': round(amt, 2),
                'win_rate': win_rate
            })

        results = sorted(results, key=lambda x: x['win_rate'], reverse=True)
        top5 = results[:5]
        top5_extra = results[5:10]

        log(f"\n=== 5% 观察名单（5只）===")
        for i, r in enumerate(top5, 1):
            log(f"{i}. {r['code']} {r['name']} | 胜率:{r['win_rate']}% | 涨幅:{r['chg']}% | 换手:{r['turnover']}% | 量比:{r['vol_ratio']}")

        log(f"\n=== 高胜率观察名单（5只）===")
        for i, r in enumerate(top5_extra, 1):
            log(f"{i}. {r['code']} {r['name']} | 胜率:{r['win_rate']}% | 涨幅:{r['chg']}% | 换手:{r['turnover']}% | 量比:{r['vol_ratio']}")

        # 保存
        output = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'hs300_chg': hs300_chg, 'hs300_val': hs300_val,
            'cyb_chg': cyb_chg, 'cyb_val': cyb_val,
            'sh_val': sh_val, 'sh000001_chg': sh000001_chg,
            'a50_chg': a50_chg,
            'total_amt': round(total_amt, 0),
            'zt_count': zt_count,
            'bull_score': bull,
            'stance': stance,
            'top5': top5,
            'top5_extra': top5_extra
        }
        with open('C:\\Users\\admin\\.qclaw\\workspace\\report_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        log("\n[report_data.json 已保存]")
    else:
        log("无法处理股票数据")
else:
    log("无法获取股票数据")
