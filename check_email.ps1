$ErrorActionPreference = "Stop"
$skillDir = "D:\QClaw\resources\openclaw\config\skills\email-skill\scripts\windows"
$env:PATH = "C:\Windows\system32;C:\Windows;C:\Windows\System32\WindowsPowerShell\v1.0;$env:PATH"

# Check if 139.com is bound
$result = & "$skillDir\email_gateway.cmd" bind-check --email "18339435211@139.com" 2>&1
Write-Host $result
