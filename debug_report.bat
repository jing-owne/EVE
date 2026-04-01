@echo off
REM 调试模式启动脚本 - 不发送任何邮件
REM 用于测试和调试

setlocal enabledelayedexpansion

echo [DEBUG] 五大策略报告 - 调试模式
echo ================================
echo.
echo 说明: 此模式下不会发送任何邮件，仅用于测试
echo.

set PYTHON=python
set SCRIPT=C:\Users\admin\.qclaw\workspace\send_strategy_email_v3_6.py

REM 启用调试模式
set DEBUG_MODE=true

echo [DEBUG] 启动报告生成...
echo.

%PYTHON% %SCRIPT%

echo.
echo [DEBUG] 调试完成！
pause
