@echo off
set TEMP=C:\Users\admin\.qclaw\workspace\temp
set TMP=C:\Users\admin\.qclaw\workspace\temp
mkdir "%TEMP%" 2>nul
mkdir "%TEMP%\pkgs" 2>nul
pip install akshare pandas numpy pillow requests --target "C:\Users\admin\.qclaw\workspace\lib" --no-build-isolation
echo DONE
