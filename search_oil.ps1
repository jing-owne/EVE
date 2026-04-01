$PORT = if ($env:AUTH_GATEWAY_PORT) { $env:AUTH_GATEWAY_PORT } else { "19000" }
$FROM_TIME = [int](Get-Date -UFormat %s) - 2592000
$keyword = "2026" + [char]0x5E74 + "3" + [char]0x6708 + [char]0x4E2D + [char]0x56FD + [char]0x6C7D + [char]0x6CB9 + [char]0x4EF7 + [char]0x683C + [char]0x8C03 + [char]0x6574 + " 92" + [char]0x53F7 + "95" + [char]0x53F7 + "98" + [char]0x53F7
$bodyObj = [ordered]@{ keyword = $keyword; from_time = $FROM_TIME }
$bodyJson = $bodyObj | ConvertTo-Json -Compress
$bytes = [System.Text.Encoding]::UTF8.GetBytes($bodyJson)
$response = Invoke-WebRequest -Method Post -Uri ("http://localhost:" + $PORT + "/proxy/prosearch/search") -ContentType "application/json" -Body $bytes
[System.Text.Encoding]::UTF8.GetString($response.Content)
