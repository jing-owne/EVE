@echo off
REM 快速启动定时任务脚本（Windows）
REM 以管理员身份运行此脚本

setlocal enabledelayedexpansion

echo [QClaw] 五大策略报告 + 持仓分析 - 定时任务设置
echo ================================================
echo.

set SCRIPT_PATH=C:\Users\admin\.qclaw\workspace\cron_integrated.py
set PYTHON=python

REM 检查 Python 是否可用
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未找到，请先安装 Python
    pause
    exit /b 1
)

echo [OK] Python 已安装
echo.

REM 创建定时任务
echo [创建] 工作日 9:20 推送报告...
schtasks /create /tn "Stock Report 9:20" /tr "%PYTHON% %SCRIPT_PATH%" /sc daily /st 09:20 /d MON,TUE,WED,THU,FRI /f >nul 2>&1
if errorlevel 0 echo [OK] 任务已创建

echo [创建] 工作日 11:00 推送报告...
schtasks /create /tn "Stock Report 11:00" /tr "%PYTHON% %SCRIPT_PATH%" /sc daily /st 11:00 /d MON,TUE,WED,THU,FRI /f >nul 2>&1
if errorlevel 0 echo [OK] 任务已创建

echo [创建] 工作日 13:30 推送报告...
schtasks /create /tn "Stock Report 13:30" /tr "%PYTHON% %SCRIPT_PATH%" /sc daily /st 13:30 /d MON,TUE,WED,THU,FRI /f >nul 2>&1
if errorlevel 0 echo [OK] 任务已创建

echo [创建] 工作日 15:00 推送报告...
schtasks /create /tn "Stock Report 15:00" /tr "%PYTHON% %SCRIPT_PATH%" /sc daily /st 15:00 /d MON,TUE,WED,THU,FRI /f >nul 2>&1
if errorlevel 0 echo [OK] 任务已创建

echo.
echo [OK] 所有定时任务已设置完成！
echo.
echo 功能说明:
echo   - 邮件报告: 发送到 18339435211@139.com (抄送3人)
echo   - 持仓分析: 微信推送持仓分析
echo   - 推送时间: 工作日 9:20, 11:00, 13:30, 15:00
echo.
echo 收件人配置:
echo   主收件人: 18339435211@139.com
echo   抄送: 732016354@qq.com, 850229452@qq.com, 2625260548@qq.com
echo.
echo 持仓配置:
echo   文件: portfolio_config.txt
echo   格式: 代码,名称,成本价,持仓数量
echo   例如: 300014,亿纬锂能,25.50,100
echo.
echo 查看任务列表:
schtasks /query /tn "Stock Report*"
echo.
pause
