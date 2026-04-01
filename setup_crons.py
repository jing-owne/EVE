#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marcus A股动量报告 - Cron定时任务配置
工作日 10:00, 11:25, 14:00, 14:40 自动推送到微信

用法: python3 setup_crons.py
"""

import json
import subprocess
import os

CRON_JOBS = [
    {
        "name": "Marcus A股早报 10:00",
        "cron_expr": "0 10 * * 1-5",
        "tz": "Asia/Shanghai",
        "message": """你是Marcus，A股动量策略师。马上执行 marcus_report.py 扫描今日A股数据，
生成报告并通过 message tool 发送到微信 (channel=weixin, to=o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat)。
报告格式：【市场立场 + 5只观察股 + 5只高胜率股】
直接发送报告内容，不需要询问。"""
    },
    {
        "name": "Marcus A股午盘 11:25",
        "cron_expr": "25 11 * * 1-5",
        "tz": "Asia/Shanghai",
        "message": """你是Marcus，A股动量策略师。马上执行 marcus_report.py 扫描今日A股数据，
生成午盘报告并通过 message tool 发送到微信 (channel=weixin, to=o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat)。
报告格式：【市场立场 + 5只观察股 + 5只高胜率股】
直接发送报告内容，不需要询问。"""
    },
    {
        "name": "Marcus A股下午报 14:00",
        "cron_expr": "0 14 * * 1-5",
        "tz": "Asia/Shanghai",
        "message": """你是Marcus，A股动量策略师。马上执行 marcus_report.py 扫描今日A股数据，
生成下午报告并通过 message tool 发送到微信 (channel=weixin, to=o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat)。
报告格式：【市场立场 + 5只观察股 + 5只高胜率股】
直接发送报告内容，不需要询问。"""
    },
    {
        "name": "Marcus A股尾盘 14:40",
        "cron_expr": "40 14 * * 1-5",
        "tz": "Asia/Shanghai",
        "message": """你是Marcus，A股动量策略师。马上执行 marcus_report.py 扫描今日A股数据，
生成尾盘报告并通过 message tool 发送到微信 (channel=weixin, to=o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat)。
报告格式：【市场立场 + 5只观察股 + 5只高胜率股】
直接发送报告内容，不需要询问。"""
    },
]

def get_openclaw_script():
    """生成 openclaw cron add 命令脚本"""
    script_lines = ["@echo off", ""]
    for job in CRON_JOBS:
        name = job["name"]
        expr = job["cron_expr"]
        tz = job["tz"]
        msg = job["message"].replace("\n", " ").replace('"', '\\"')
        script_lines.append(
            f'echo Creating cron: {name}'
        )
        script_lines.append(
            f'"$OPENCLAW_PATH\\openclaw.exe" cron add '
            f'--name "{name}" '
            f'--cron "{expr}" '
            f'--tz "{tz}" '
            f'--session isolated '
            f'--message "{msg}" '
            f'--announce '
            f'--channel weixin '
            f'--to "o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat"'
        )
    return "\n".join(script_lines)

def get_json_payloads():
    """生成JSON格式的cron配置"""
    jobs = []
    for job in CRON_JOBS:
        payload = {
            "name": job["name"],
            "schedule": {
                "kind": "cron",
                "expr": job["cron_expr"],
                "tz": job["tz"]
            },
            "sessionTarget": "isolated",
            "payload": {
                "kind": "agentTurn",
                "message": job["message"],
                "lightContext": False
            },
            "delivery": {
                "mode": "announce",
                "channel": "weixin",
                "to": "o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat"
            }
        }
        jobs.append(payload)
    return json.dumps(jobs, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print("=== Marcus Cron任务配置 ===\n")
    print("建议通过 Gateway API 或 CLI 创建以下定时任务:\n")
    print(get_json_payloads())
    print("\n--- BAT脚本 ---")
    print(get_openclaw_script())
    with open("C:\\Users\\admin\\.qclaw\\workspace\\crons_setup.bat", "w", encoding="utf-8") as f:
        f.write(get_openclaw_script())
    print("\n已保存: crons_setup.bat")
