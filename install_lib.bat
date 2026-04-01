@echo off
set TEMP=C:\Users\admin\.qclaw\workspace\temp
set TMP=C:\Users\admin\.qclaw\workspace\temp
mkdir "%TEMP%" 2>nul
mkdir "C:\Users\admin\.qclaw\workspace\lib" 2>nul
pip install requests pandas numpy pillow --target "C:\Users\admin\.qclaw\workspace\lib" --quiet --no-build-isolation 2>&1
echo INSTALL_DONE
