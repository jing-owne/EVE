#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marcus 每日A股动量报告 - 定时推送脚本
工作日 10:00, 11:25, 14:00, 14:40 自动推送
"""

import json
import os
from datetime import datetime

def format_report():
    """从 report_data.json 读取并格式化报告"""
    try:
        with open('C:\\Users\\admin\\.qclaw\\workspace\\report_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return None

    msg = f"""📊 **Marcus · 每日A股动量报告**
{data['timestamp']}

━━━━━━━━━━━━━━━━━━━━
**【市场立场】**
{data['stance']}
- 沪深300: {data['hs300_val']}（{data['hs300_chg']}%）
- 创业板指: {data['cyb_val']}（{data['cyb_chg']}%）
- 上证指数: {data['sh_val']}（{data['sh000001_chg']}%）
- A50期指: {data['a50_chg']}%
- 全市场成交: {int(data['total_amt'])}亿
- 今日涨停: {data['zt_count']}家

━━━━━━━━━━━━━━━━━━━━
**【5% 观察名单】**
"""
    for i, stock in enumerate(data['top5'], 1):
        msg += f"""{i}. **{stock['code']} {stock['name']}** | 胜率: {stock['win_rate']}% | +{stock['chg']}% | 换手{stock['turnover']}% | 量比{stock['vol_ratio']}
"""

    msg += f"""
━━━━━━━━━━━━━━━━━━━━
**【高胜率观察（5只）】**
"""
    for i, stock in enumerate(data['top5_extra'], 1):
        msg += f"""{i}. {stock['code']} {stock['name']} | 胜率{stock['win_rate']}% | +{stock['chg']}% | 换手{stock['turnover']}%
"""

    msg += "\n⚠️ 仅为数据扫描，不构成投资建议。"
    return msg

if __name__ == '__main__':
    report = format_report()
    if report:
        print(report)
        # 这里可以集成 WeChat/Telegram 推送
    else:
        print("报告生成失败")
