const fs = require('fs');
const path = require('path');
const os = require('os');
const f = path.join(os.homedir(), '.qclaw', 'workspace', 'memory', '2026-03-30.md');
let content = fs.readFileSync(f, 'utf8');
const entry = '\n\n---\n\n## 亿纬锂能（300014）持仓追踪\n- **持仓成本**：用户自有（未告知）\n- **2026-03-31 13:07**：当前价63.25元，今日跌幅-8.45%，成交量5.7亿（放量下跌）\n- **关键支撑**：63.00元 / 62.50止损 / 60.00深度支撑\n- **补仓建议**：仓位≤20%可补1成；仓位≥30%不补\n- **下次关注**：尾盘（14:40）是否守住63支撑';
fs.appendFileSync(f, entry, 'utf8');
console.log('Tracking entry added to memory');
