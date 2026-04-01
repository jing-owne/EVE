@echo off
copy /Y "C:\Users\admin\.qclaw\workspace\marcus_report.png" "C:\Users\admin\.qclaw\workspace\test_copy.png"
if errorlevel 1 (
    echo COPY_FAILED
) else (
    echo COPY_OK
)
