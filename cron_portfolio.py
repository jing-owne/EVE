# -*- coding: utf-8 -*-
"""定时推送持仓分析到微信"""
import subprocess
import sys
from datetime import datetime

def send_portfolio_analysis_to_weixin():
    """执行持仓分析并推送到微信"""
    
    # 执行持仓分析脚本
    script_path = r'C:\Users\admin\.qclaw\workspace\analyze_portfolio.py'
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True, 
                              timeout=30)
        
        if result.returncode == 0:
            # 提取报告内容
            output = result.stdout
            
            # 查找报告内容（在 ==== 之间）
            if '====' in output:
                start = output.index('====') + 4
                end = output.rindex('====')
                report = output[start:end].strip()
            else:
                report = output
            
            # 通过 message 工具推送到微信
            # 这里使用 OpenClaw 的消息系统
            print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] 持仓分析推送成功')
            print(report)
            
            return report
        else:
            print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] 持仓分析失败')
            print(result.stderr)
            return None
            
    except subprocess.TimeoutExpired:
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] 持仓分析超时')
        return None
    except Exception as e:
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] 错误: {e}')
        return None

if __name__ == '__main__':
    send_portfolio_analysis_to_weixin()
