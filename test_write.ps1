foreach($dir in @("$env:USERPROFILE\Desktop","$env:USERPROFILE\Documents","D:\QClaw","C:\Users\admin\.qclaw")) {
    $f = Join-Path $dir "tw.txt"
    try {
        Set-Content -Path $f -Value "ok" -ErrorAction Stop
        Write-Host "OK: $dir"
        Remove-Item $f -Force -EA SilentlyContinue
    } catch {
        Write-Host "FAIL: $dir -- $($_.Exception.Message.Substring(0,50))"
    }
}
