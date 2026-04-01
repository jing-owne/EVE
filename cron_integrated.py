# -*- coding: utf-8 -*-
"""集成脚本：发送邮件报告 + 微信推送持仓分析"""
import subprocess
import sys
import os
from datetime import datetime

# 设置编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

def run_integrated_task():
    """执行集成任务"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f'[{timestamp}] 开始执行集成任务...\n')
    
    # 1. 发送邮件报告（定时任务模式，带抄送）
    print(f'[{timestamp}] 步骤1: 发送五大策略报告邮件...')
    email_script = r'C:\Users\admin\.qclaw\workspace\send_strategy_email_v3_6.py'
    
    env = os.environ.copy()
    env['SCHEDULED_TASK'] = 'true'  # 定时任务：触发完整抄送
    
    try:
        result = subprocess.run([sys.executable, email_script], 
                              capture_output=True, 
                              text=True, 
                              timeout=60,
                              encoding='utf-8',
                              errors='replace',
                              env=env)
        
        if result.returncode == 0:
            print(f'[{timestamp}] OK 邮件报告发送成功')
            if '发送成功' in result.stdout:
                print(result.stdout.split('\n')[-2])
        else:
            print(f'[{timestamp}] NG 邮件报告发送失败')
    except Exception as e:
        print(f'[{timestamp}] NG 邮件报告错误: {str(e)[:50]}')
    
    print()
    
    # 2. 推送持仓分析到微信
    print(f'[{timestamp}] 步骤2: 推送持仓分析到微信...')
    portfolio_script = r'C:\Users\admin\.qclaw\workspace\cron_portfolio.py'
    
    try:
        result = subprocess.run([sys.executable, portfolio_script], 
                              capture_output=True, 
                              text=True, 
                              timeout=30,
                              encoding='utf-8',
                              errors='replace')
        
        if result.returncode == 0:
            print(f'[{timestamp}] OK 持仓分析推送成功')
        else:
            print(f'[{timestamp}] NG 持仓分析推送失败')
    except Exception as e:
        print(f'[{timestamp}] NG 持仓分析错误: {str(e)[:50]}')
    
    print()
    print(f'[{timestamp}] 集成任务完成!')

if __name__ == '__main__':
    run_integrated_task()
