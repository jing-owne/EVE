# -*- coding: utf-8 -*-
"""
Marcus 定时任务启动器
用于 Windows 任务计划程序调用
"""

import sys
import os

# 设置编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 添加路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from scanner import scan_market, generate_report, OUTPUT_FILE
from datetime import datetime
import json

def run_task():
    """执行定时任务"""
    now = datetime.now()
    
    # 检查是否工作日
    if now.weekday() >= 5:  # 周六周日
        print("⏭️ 非工作日，跳过")
        return
    
    print(f"{'='*50}")
    print(f"📊 Marcus 定时任务")
    print(f"📅 {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")
    
    # 扫描市场
    stocks, status = scan_market()
    report = generate_report(stocks)
    
    print(report)
    
    # 保存结果
    output = {
        'timestamp': now.isoformat(),
        'status': status,
        'count': len(stocks),
        'stocks': stocks
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 已保存: {OUTPUT_FILE}")
    
    return report

if __name__ == "__main__":
    run_task()
