@echo off
mkdir C:\temp 2>nul
set TEMP=C:\temp
set TMP=C:\temp
pip install akshare pandas numpy pillow requests --quiet
echo DONE
