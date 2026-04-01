$meta = Get-Content "$env:USERPROFILE\.qclaw\qclaw.json" -Raw | ConvertFrom-Json
$env:ELECTRON_RUN_AS_NODE = "1"
$env:NODE_OPTIONS = "--no-warnings"
$env:OPENCLAW_NIX_MODE = "1"
$env:OPENCLAW_STATE_DIR = $meta.stateDir
$env:OPENCLAW_CONFIG_PATH = $meta.configPath
$node = $meta.cli.nodeBinary
$mjs = $meta.cli.openclawMjs

$to = "o9cq80zg1crCcSu7hmnbkRFOvRgk@im.wechat"

$jobs = @(
    @{
        name = "天气穿衣指南"
        expr = "30 8 * * *"
        msg  = "你是天气顾问Marcus。获取上海松江区泗泾镇今日天气、穿衣建议、空气质量，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。"
    },
    @{
        name = "A股早盘分析"
        expr = "0 10 * * 1-5"
        msg  = "你是Marcus，A股动量策略师。搜索今日A股开盘数据、板块动向、涨停股，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。"
    },
    @{
        name = "A股午盘参考"
        expr = "25 11 * * 1-5"
        msg  = "你是Marcus，A股动量策略师。搜索今日A股午盘数据、涨跌停统计、板块动向，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。"
    },
    @{
        name = "A股下午盘初"
        expr = "0 14 * * 1-5"
        msg  = "你是Marcus，A股动量策略师。搜索今日A股下午盘数据、板块动向，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。"
    },
    @{
        name = "A股尾盘窗口"
        expr = "40 14 * * 1-5"
        msg  = "你是Marcus，A股动量策略师。搜索今日A股尾盘数据、涨跌停统计，给出胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。"
    },
    @{
        name = "A股收盘复盘"
        expr = "30 15 * * 1-5"
        msg  = "你是Marcus，A股动量策略师。搜索今日A股收盘数据、主力资金流向、龙虎榜，给出明日胜率80%+的5只股票和5只可转债T+0标的，通过message tool发送到微信。不要回复HEARTBEAT_OK，不要解释你是谁。"
    }
)

foreach ($j in $jobs) {
    $jobObj = @{
        name = $j.name
        schedule = @{ kind = "cron"; expr = $j.expr; tz = "Asia/Shanghai" }
        sessionTarget = "isolated"
        payload = @{ kind = "agentTurn"; message = $j.msg; lightContext = $false }
        delivery = @{ mode = "announce"; channel = "weixin"; to = $to }
    }
    $jobJson = $jobObj | ConvertTo-Json -Compress -Depth 10
    $tmpFile = [System.IO.Path]::GetTempFileName() + ".json"
    $jobJson | Out-File -FilePath $tmpFile -Encoding utf8 -NoNewline
    Write-Host "Creating: $($j.name)"
    $result = & $node $mjs cron add --json-file $tmpFile 2>&1
    Write-Host $result
    Remove-Item $tmpFile -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 500
}

Write-Host "--- Listing all cron jobs ---"
& $node $mjs cron list 2>&1
