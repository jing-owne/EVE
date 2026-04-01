@echo off
curl.exe -s -X POST "http://localhost:19000/proxy/prosearch/search" -H "Content-Type: application/json" -d "{\"keyword\":\"今日A股大盘指数收盘 涨跌停数量 2026年3月24日\"}" -o "%USERPROFILE%\search_out.txt" 2>&1
