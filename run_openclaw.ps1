$meta = Get-Content "$env:USERPROFILE\.qclaw\qclaw.json" -Raw | ConvertFrom-Json
$env:ELECTRON_RUN_AS_NODE = "1"
$env:NODE_OPTIONS = "--no-warnings"
$env:OPENCLAW_NIX_MODE = "1"
$env:OPENCLAW_STATE_DIR = $meta.stateDir
$env:OPENCLAW_CONFIG_PATH = $meta.configPath
$node = $meta.cli.nodeBinary
$mjs = $meta.cli.openclawMjs
& $node $mjs cron list
