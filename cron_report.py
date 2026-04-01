#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务脚本：工作日 9:20, 11:00, 13:30, 15:00 推送五大策略报告
支持多收件人和抄送
"""
import subprocess
import sys
import os
from datetime import datetime

def run_report():
    """执行报告生成和发送"""
    script_path = r'C:\Users\admin\.qclaw\workspace\send_strategy_email_v3_6.py'
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True, 
                              timeout=60)
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if result.returncode == 0:
            print(f'[{timestamp}] ✓ 报告发送成功')
            print(result.stdout)
            return True
        else:
            print(f'[{timestamp}] ✗ 报告发送失败')
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ✗ 超时')
        return False
    except Exception as e:
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ✗ 错误: {e}')
        return False

if __name__ == '__main__':
    run_report()

