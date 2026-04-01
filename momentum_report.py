#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股日内动量策略报告生成器
筛选条件：
- 前一天涨幅≤5%
- 20天内有涨停
- 总涨幅≤20%
- 胜率≥70%
- 连续3天净流入
- MACD与KDJ双金叉
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def generate_momentum_report():
    """生成每日动量报告"""
    
    # 获取当前时间
    now = datetime.now()
    report_time = now.strftime("%Y-%m-%d %H:%M")
    
    # 报告头
    report = {
        "timestamp": report_time,
        "date": now.strftime("%Y-%m-%d"),
        "day_of_week": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()],
        "market_session": "早盘" if now.hour < 12 else "午盘" if now.hour < 15 else "收盘",
        "status": "数据获取中...",
        "note": "需要接入实时行情数据源（如tushare、akshare等）"
    }
    
    # 筛选条件说明
    report["filters"] = {
        "prev_day_gain": "≤5%",
        "limit_up_in_20d": "有",
        "total_gain": "≤20%",
        "win_rate": "≥70%",
        "net_inflow_3d": "连续3天净流入",
        "macd_kdj": "双金叉"
    }
    
    # 候选标的（示例数据）
    report["candidates"] = []
    report["message"] = "⚠️ 需要配置行情数据源才能生成实时报告"
    
    return report

def save_report(report):
    """保存报告到内存文件"""
    workspace = Path("C:/Users/admin/.qclaw/workspace")
    memory_dir = workspace / "memory"
    memory_dir.mkdir(exist_ok=True)
    
    # 按日期保存
    date_str = report["date"]
    memory_file = memory_dir / f"{date_str}.md"
    
    # 生成markdown格式
    content = f"""# A股动量报告 - {report['date']} {report['day_of_week']}

**生成时间:** {report['timestamp']}  
**市场阶段:** {report['market_session']}

## 筛选条件
- 前一天涨幅: {report['filters']['prev_day_gain']}
- 20天内涨停: {report['filters']['limit_up_in_20d']}
- 总涨幅: {report['filters']['total_gain']}
- 胜率: {report['filters']['win_rate']}
- 净流入: {report['filters']['net_inflow_3d']}
- 技术面: {report['filters']['macd_kdj']}

## 候选标的
{report['message']}

---
*需要接入实时行情数据源（tushare/akshare）来生成完整报告*
"""
    
    with open(memory_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 报告已保存: {memory_file}")
    return memory_file

if __name__ == "__main__":
    report = generate_momentum_report()
    save_report(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
