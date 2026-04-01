$PORT = if ($env:AUTH_GATEWAY_PORT) { $env:AUTH_GATEWAY_PORT } else { "19000" }
Write-Host "[QClaw] AUTH_GATEWAY_PORT: $PORT"

$FROM_TIME = python -c "import time; print(int(time.time()) - 86400)"
Write-Host "[QClaw] FROM_TIME: $FROM_TIME"

$body = @{
    keyword = "A股午盘 涨停板 板块涨幅 2026年4月1日"
    from_time = [int]$FROM_TIME
} | ConvertTo-Json -Compress

Write-Host "[QClaw] Body: $body"

$response = Invoke-RestMethod -Uri "http://localhost:$PORT/proxy/prosearch/search" -Method POST -ContentType "application/json" -Body $body
$response | ConvertTo-Json -Depth 10
