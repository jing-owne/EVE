# -*- coding: utf-8 -*-
"""
每日A股动量报告生成器
日期：2026-03-23（周一）
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import datetime
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import akshare as ak
import json

print("=" * 60)
print("[REPORT] A股动量精选报告  2026-03-23（周一）")
print("=" * 60)

today = "20260323"
report_data = {}

# ─────────────────────────────────────────────
# 1. 获取今日涨停股（东方财富 强势池）
# ─────────────────────────────────────────────
try:
    zt_strong = ak.stock_zt_pool_strong_em(date=today)
    report_data["zt_strong_count"] = len(zt_strong)
    print(f"\n[OK] 今日涨停强势池: {len(zt_strong)} 只")

    if len(zt_strong) > 0:
        cols = [c for c in ["代码","名称","涨停统计","连板数","流通市值","换手率","涨停原因类别"] if c in zt_strong.columns]
        zt_show = zt_strong[cols].head(20)
        report_data["zt_strong_top"] = zt_show.to_dict(orient="records")
        print(zt_show.to_string())
except Exception as e:
    print(f"[WARN] 涨停强势池: {e}")
    report_data["zt_strong_count"] = 0
    report_data["zt_strong_top"] = []

# ─────────────────────────────────────────────
# 2. 获取今日弱势股（跌停池）
# ─────────────────────────────────────────────
try:
    zt_weak = ak.stock_zt_pool_weak_em(date=today)
    report_data["zt_weak_count"] = len(zt_weak)
    print(f"\n[OK] 今日跌停池: {len(zt_weak)} 只")
except Exception as e:
    print(f"[WARN] 跌停池: {e}")
    report_data["zt_weak_count"] = 0

# ─────────────────────────────────────────────
# 3. 获取今日行业板块涨跌
# ─────────────────────────────────────────────
try:
    sector_rank = ak.stock_board_industry_name_em()
    sector_rank_sorted = sector_rank.sort_values("涨跌幅", ascending=False)
    report_data["sector_top"] = sector_rank_sorted.head(10).to_dict(orient="records")
    print(f"\n[OK] 今日行业涨幅Top10:")
    print(sector_rank_sorted[["板块名称","涨跌幅","总市值","上涨家数","下跌家数"]].head(10).to_string())
    report_data["sector_bottom"] = sector_rank_sorted.tail(5)[["板块名称","涨跌幅"]].to_dict(orient="records")
except Exception as e:
    print(f"[WARN] 行业板块: {e}")
    report_data["sector_top"] = []

# ─────────────────────────────────────────────
# 4. 获取概念板块涨跌
# ─────────────────────────────────────────────
try:
    concept_rank = ak.stock_board_concept_name_em()
    concept_sorted = concept_rank.sort_values("涨跌幅", ascending=False)
    report_data["concept_top"] = concept_sorted.head(10).to_dict(orient="records")
    print(f"\n[OK] 今日概念涨幅Top10:")
    print(concept_sorted[["板块名称","涨跌幅","上涨家数","下跌家数"]].head(10).to_string())
except Exception as e:
    print(f"[WARN] 概念板块: {e}")
    report_data["concept_top"] = []

# ─────────────────────────────────────────────
# 5. 获取主要指数收盘数据
# ─────────────────────────────────────────────
try:
    indices_info = {}
    for name, code in [("上证指数","000001"),("深证成指","399001"),("创业板指","399006"),("科创50","000688")]:
        df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                 start_date="20260320", end_date=today)
        if len(df) >= 2:
            last = df.iloc[-1]
            prev = df.iloc[-2]
            chg = float(last["涨跌幅"])
            indices_info[name] = {
                "close": float(last["收盘"]),
                "prev_close": float(prev["收盘"]),
                "change_pct": chg,
                "volume": float(last["成交量"]),
                "amount": float(last["成交额"])
            }
            print(f"\n{name}: 收于 {last['收盘']:.2f}  涨跌 {chg:+.2f}%  成交额 {float(last['成交额'])/1e8:.1f}亿")
    report_data["indices"] = indices_info
except Exception as e:
    print(f"[WARN] 指数数据: {e}")
    report_data["indices"] = {}

# ─────────────────────────────────────────────
# 6. 市场宽度（上涨/下跌家数）
# ─────────────────────────────────────────────
try:
    market_em = ak.stock_spot_em()
    # 过滤沪深A股
    ashare = market_em[market_em["代码"].str.startswith(("0","3","6"))]
    rising  = int(ashare[ashare["涨跌幅"] > 0].shape[0])
    falling = int(ashare[ashare["涨跌幅"] < 0].shape[0])
    flat    = int(ashare[ashare["涨跌幅"] == 0].shape[0])
    report_data["market_breadth"] = {"rising": rising, "falling": falling, "flat": flat}
    print(f"\n[OK] 市场宽度 - 涨: {rising} | 跌: {falling} | 平: {flat}")
except Exception as e:
    print(f"[WARN] 市场宽度: {e}")

# ─────────────────────────────────────────────
# 7. 北向资金（沪深港通）
# ─────────────────────────────────────────────
try:
    north = ak.stock_hsgt_north_net_flow_in_em(symbol="北向资金")
    if north is not None and len(north) > 0:
        last_row = north.iloc[-1]
        report_data["north_capital"] = {
            "date": str(last_row.get("日期","")),
            "north_money": float(last_row.get("北向资金", 0)),
            "shanghai_money": float(last_row.get("沪股通", 0)),
            "shenzhen_money": float(last_row.get("深股通", 0))
        }
        print(f"\n[OK] 北向资金: {float(last_row.get('北向资金',0)):+.2f}亿")
        print(f"    沪股通: {float(last_row.get('沪股通',0)):+.2f}亿 | 深股通: {float(last_row.get('深股通',0)):+.2f}亿")
except Exception as e:
    print(f"[WARN] 北向资金: {e}")

print("\n" + "=" * 60)
print("[DONE] 数据抓取完毕 ✅")
print("=" * 60)

# 保存原始数据供分析用
with open("C:/Users/admin/.qclaw/workspace/report_raw_20260323.json", "w", encoding="utf-8") as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)
print("[FILE] 原始数据已保存至 report_raw_20260323.json")
