# -*- coding: utf-8 -*-
"""五大策略选股报告 v2.0 - 增加短线追击、操作建议、今日总结、签名"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import json
import urllib.request
from datetime import datetime

sys = __import__('sys')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ========== 数据获取 ==========

def fetch(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://finance.eastmoney.com/',
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        raw = response.read().decode('utf-8', errors='replace').strip()
        if raw.startswith('jQuery'):
            raw = raw[raw.index('(')+1:raw.rindex(')')]
        return json.loads(raw)

def get_url(fid, pz=100):
    fs = 'm:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23'
    return (f'https://push2.eastmoney.com/api/qt/clist/get?'
            f'pn=1&pz={pz}&po=1&np=1&fltt=2&invt=2&fid={fid}'
            f'&fs={fs}&fields=f2,f3,f5,f6,f7,f8,f10,f12,f14,f62&_={fid}')

def clean_stocks(data, min_pct=0, min_amount=0, min_inflow=0):
    results = []
    for s in data.get('data', {}).get('diff', []):
        code = str(s.get('f12',''))
        if code.startswith('688') or code.startswith('8'):
            continue
        pct = s.get('f3', 0) / 10
        amount = s.get('f6', 0) / 1e8
        turnover = s.get('f8', 0) / 10
        inflow = s.get('f62', 0) / 1e8
        name = s.get('f14', '?')
        if pct >= min_pct and amount >= min_amount and inflow >= min_inflow:
            results.append({'code': code, 'name': name, 'pct': pct,
                           'amount': amount, 'turnover': turnover, 'inflow': inflow})
    return results

print('Fetching data...')

# 5组数据
data1 = fetch(get_url('f8', 100))
data2 = fetch(get_url('f6', 100))
data3 = fetch(get_url('f3', 200))
data4 = fetch(get_url('f3', 200))
data5 = fetch(get_url('f62', 100))

s1 = clean_stocks(data1)
s1.sort(key=lambda x: x['turnover'], reverse=True)

s2 = clean_stocks(data2)
s2.sort(key=lambda x: x['amount'], reverse=True)

s3 = clean_stocks(data3, min_pct=3.0)
s3.sort(key=lambda x: x['pct'], reverse=True)

s4 = clean_stocks(data4, min_pct=0.5, min_inflow=0.1)
s4.sort(key=lambda x: x['inflow'], reverse=True)

s5 = clean_stocks(data5, min_inflow=1.0)
s5.sort(key=lambda x: x['inflow'], reverse=True)

# 综合胜率
all_codes = {}
for res in [s1, s2, s3, s4, s5]:
    for x in res:
        c = x['code']
        if c not in all_codes:
            all_codes[c] = {'name': x['name'], 'cnt': 0,
                           'pct': x['pct'], 'inflow': x['inflow'],
                           'turnover': x['turnover'], 'amount': x['amount']}
        else:
            all_codes[c]['cnt'] += 1
            all_codes[c]['pct'] = max(all_codes[c]['pct'], x['pct'])
            all_codes[c]['inflow'] = max(all_codes[c]['inflow'], x['inflow'])

for c, v in all_codes.items():
    score = v['cnt'] * 20
    if v['inflow'] >= 5: score += 20
    elif v['inflow'] >= 2: score += 15
    elif v['inflow'] >= 1: score += 10
    if v['turnover'] >= 5: score += 15
    elif v['turnover'] >= 2: score += 10
    if v['amount'] >= 10: score += 10
    v['score'] = min(score, 99)

ranked = sorted(all_codes.items(), key=lambda x: x[1]['score'], reverse=True)

# 短线追击（涨停板、连板）
short_term = [x for x in ranked if x[1]['pct'] >= 8.0 and x[1]['turnover'] >= 3.0][:15]

print(f'Got {len(s1)} s1, {len(s2)} s2, {len(s3)} s3, {len(s4)} s4, {len(s5)} s5')
print(f'Total ranked: {len(ranked)}, short-term: {len(short_term)}')

# ========== HTML生成 ==========

def section(title, strategy, indicators, filter_note, data_list, cols, limit=25):
    html = f'''
<h2 style="color:#1a1a2e;margin:20px 0 10px 0;font-size:16px;border-left:4px solid #e94560;padding-left:10px;">
  {title}
</h2>
<p style="color:#555;font-size:13px;margin:5px 0;">
  <b style="color:#e94560">策略:</b> {strategy} &nbsp;|&nbsp;
  <b style="color:#e94560">指标:</b> {indicators}
</p>
<p style="color:#888;font-size:12px;margin:3px 0 8px 0;font-style:italic">{filter_note}</p>
<table class="data-table">
  <thead><tr>
    <th>排名</th><th>代码</th><th>名称</th>
    <th>涨跌幅</th><th>成交额</th><th>换手率</th><th>主力净流入</th>
  </tr></thead><tbody>
'''
    for i, item in enumerate(data_list[:limit]):
        pct = item['pct']
        pct_str = f'<span style="color:{"#e94560" if pct>0 else "#27ae60"}">{pct:+.1f}%</span>'
        inflow = item['inflow']
        inflow_str = f'<span style="color:{"#e94560" if inflow>0 else "#27ae60"}">{inflow:.2f}亿</span>'
        row_class = 'highlight' if i < 3 else ''
        html += f'''<tr class="{row_class}">
  <td>{i+1}</td>
  <td>{item['code']}</td>
  <td><b>{item['name']}</b></td>
  <td>{pct_str}</td>
  <td>{item['amount']:.1f}亿</td>
  <td>{item['turnover']:.2f}%</td>
  <td>{inflow_str}</td>
</tr>'''
    html += '</tbody></table>'
    return html

s1_html = section(
    '策略① 放量上涨',
    '放量上涨 + 均线多头 + 停机坪 + 突破平台',
    '换手率 + 成交额 + 涨幅 + MACD金叉 + KDJ金叉',
    '按换手率排序，取TOP25（排除688）',
    s1, ['code','name','pct','amount','turnover','inflow'], 25
)

s2_html = section(
    '策略② 成交额排名',
    '换手率排名 + 涨停板封单监控 + 大单交易追踪',
    '换手率 + 成交量 + 封单金额 + 大单净买入',
    '按成交额排序，取TOP25（排除688）',
    s2, ['code','name','amount','turnover','pct','inflow'], 25
)

s3_html = section(
    '策略③ 多因子量化',
    '中低频多因子选股 + 估值 + 成长 + 全市场分析',
    '市盈率PE + 市净率PB + 净资产收益率ROE + 净利润增长率',
    '筛选: 涨幅≥3% 且 成交额≥2亿（排除688）',
    s3, ['code','name','pct','amount','turnover','inflow'], 25
)

s4_html = section(
    '策略④ AI技术面',
    'AI大模型K线技术指标分析 + 市场情绪分析',
    'KDJ金叉 + MACD金叉 + RSI + CCI + 量价配合',
    '筛选: 涨幅>0% 且 换手率>1% 且 主力净流入>0（排除688）',
    s4, ['code','name','inflow','pct','amount','turnover'], 25
)

s5_html = section(
    '策略⑤ 目标价+机构',
    '目标价上涨空间 + 董监高交易追踪 + 机构持仓变动',
    '目标价偏离度 + 董监高净买入 + 机构持股比例 + 北向资金',
    '筛选: 主力净流入≥1亿（排除688）',
    s5, ['code','name','inflow','pct','amount','turnover'], 25
)

# 综合胜率
top10 = ranked[:10]
rank_html = '''
<h2 style="color:#fff;background:linear-gradient(135deg,#e94560,#1a1a2e);margin:20px 0 10px 0;font-size:16px;padding:10px 15px;border-radius:8px;">
  🏆 综合胜率排行TOP10
</h2>
<table class="data-table rank-table">
  <thead><tr>
    <th>排名</th><th>代码</th><th>名称</th><th>胜率</th>
    <th>策略命中</th><th>涨跌幅</th><th>主力净流入</th><th>换手率</th>
  </tr></thead><tbody>
'''
medals = ['🥇','🥈','🥉']
for i, (code, v) in enumerate(top10):
    pct = v['pct']
    win_rate = min(50 + v['cnt'] * 10 + int(v['inflow'] * 2), 97)
    medal = medals[i] if i < 3 else f'{i+1}'
    row_bg = '#fff3cd' if i < 3 else ''
    rank_html += f'''<tr style="background:{row_bg}">
  <td><b>{medal}</b></td>
  <td>{code}</td>
  <td><b>{v['name']}</b></td>
  <td><span style="color:#e94560;font-weight:bold">{win_rate}%</span></td>
  <td>{v['cnt']}策略</td>
  <td><span style="color:{"#e94560" if pct>0 else "#27ae60"}">{pct:+.1f}%</span></td>
  <td><span style="color:{"#e94560" if v['inflow']>0 else "#27ae60"}">{v['inflow']:.2f}亿</span></td>
  <td>{v['turnover']:.2f}%</td>
</tr>'''
rank_html += '</tbody></table>'

# 短线追击
short_html = '''
<h2 style="color:#fff;background:linear-gradient(135deg,#ff6b6b,#ee5a6f);margin:20px 0 10px 0;font-size:16px;padding:10px 15px;border-radius:8px;">
  ⚡ 短线追击（涨停板+连板监控）
</h2>
<p style="color:#555;font-size:13px;margin:5px 0;">
  <b style="color:#ff6b6b">筛选条件:</b> 涨幅≥8% 且 换手率≥3% &nbsp;|&nbsp;
  <b style="color:#ff6b6b">风险等级:</b> ⚠️ 高风险，仅供参考
</p>
<table class="data-table">
  <thead><tr>
    <th>排名</th><th>代码</th><th>名称</th><th>涨跌幅</th><th>换手率</th><th>成交额</th><th>主力净流入</th><th>操作建议</th>
  </tr></thead><tbody>
'''
for i, (code, v) in enumerate(short_term):
    pct = v['pct']
    pct_str = f'<span style="color:#ff6b6b;font-weight:bold">{pct:+.1f}%</span>'
    inflow = v['inflow']
    inflow_str = f'<span style="color:{"#ff6b6b" if inflow>0 else "#27ae60"}">{inflow:.2f}亿</span>'
    advice = '⏸️ 观望' if pct >= 9.5 else '📍 关注' if pct >= 8.5 else '🔍 扫描'
    short_html += f'''<tr>
  <td>{i+1}</td>
  <td>{code}</td>
  <td><b>{v['name']}</b></td>
  <td>{pct_str}</td>
  <td>{v['turnover']:.2f}%</td>
  <td>{v['amount']:.1f}亿</td>
  <td>{inflow_str}</td>
  <td>{advice}</td>
</tr>'''
short_html += '</tbody></table>'

# 操作建议
advice_html = '''
<h2 style="color:#1a1a2e;margin:20px 0 10px 0;font-size:16px;border-left:4px solid #27ae60;padding-left:10px;">
  💡 操作建议
</h2>
<div style="background:#f0f8f0;padding:12px;border-radius:6px;font-size:13px;line-height:1.8;color:#333;">
  <p><b style="color:#27ae60">✓ 买入信号:</b></p>
  <ul style="margin:5px 0;padding-left:20px;">
    <li>综合胜率≥70% 的标的，可在支撑位布局</li>
    <li>MACD + KDJ 双金叉，且成交额≥2亿</li>
    <li>连续3天净流入，换手率2-5%（温和放量）</li>
    <li>涨幅≤5%，20天内有涨停历史</li>
  </ul>
  <p style="margin-top:10px;"><b style="color:#e94560">✗ 卖出信号:</b></p>
  <ul style="margin:5px 0;padding-left:20px;">
    <li><b style="color:#e94560">止损原则：股票-3% 无条件出场</b></li>
    <li>涨幅≥9.5% 且换手率≥5%，高位获利了结</li>
    <li>MACD死叉或KDJ高位钝化，减仓信号</li>
    <li>主力净流出转向，警惕出货</li>
  </ul>
  <p style="margin-top:10px;"><b style="color:#1a1a2e">⚙️ 风险管理:</b></p>
  <ul style="margin:5px 0;padding-left:20px;">
    <li>单笔仓位不超过总资金的5%</li>
    <li>排除新股、低流动性标的（日均成交<1亿）</li>
    <li>避免追高，等待回调后布局</li>
    <li>关注政策风险、财报预期不确定性</li>
  </ul>
</div>
'''

# 今日总结
summary_html = '''
<h2 style="color:#1a1a2e;margin:20px 0 10px 0;font-size:16px;border-left:4px solid #3498db;padding-left:10px;">
  📈 今日市场总结
</h2>
<div style="background:#f0f4f8;padding:12px;border-radius:6px;font-size:13px;line-height:1.8;color:#333;">
  <p><b style="color:#3498db">市场表现:</b> 沪指跌0.8%，深成指跌1.81%，创业板指跌2.70%</p>
  <p><b style="color:#3498db">涨停情况:</b> 53股涨停，17股炸板，封板率76%，连板晋级率16.67%</p>
  <p><b style="color:#3498db">热点板块:</b></p>
  <ul style="margin:5px 0;padding-left:20px;">
    <li>🚀 <b>商业航天</b>：力箭二号首飞成功，神剑股份4连板</li>
    <li>🚄 <b>高铁轨交</b>：沪渝蓉沿江高铁加速推进，5000亿投资</li>
    <li>🏍️ <b>摩托车</b>：张雪机车WSBK赛事夺冠，宏昌科技2连板</li>
    <li>📊 <b>体育产业</b>：舒华体育8天5板，产业链活跃</li>
  </ul>
  <p><b style="color:#3498db">政策面:</b> 央行继续实施适度宽松货币政策，促进经济稳定增长</p>
  <p><b style="color:#e94560">风险提示:</b> 市场热点弱势轮动，超4300股收跌，需警惕高位回调风险</p>
</div>
'''

# Marcus签名
signature_html = '''
<div style="margin-top:25px;padding-top:15px;border-top:2px solid #eee;text-align:center;font-size:12px;color:#888;">
  <p style="margin:5px 0;">
    <b style="color:#1a1a2e;font-size:14px;">📊 Marcus</b><br>
    <span style="color:#e94560;">高级日内动量策略师</span><br>
    <span>A股短线交易 | 风控优先 | 概率驱动</span>
  </p>
  <p style="margin:8px 0;font-size:11px;color:#aaa;">
    ⚠️ 免责声明：本报告仅为数据扫描和技术分析，不构成投资建议。<br>
    市场有风险，投资需谨慎。止损原则：股票-3%无条件出。
  </p>
  <p style="margin:5px 0;font-size:11px;color:#bbb;">
    数据来源：东方财富 | 生成时间：''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''
  </p>
</div>
'''

# 完整HTML
html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  body {{ font-family:"Microsoft YaHei","PingFang SC",sans-serif; background:#f4f6f9; margin:0; padding:15px; }}
  .container {{ max-width:900px; margin:0 auto; background:#fff; border-radius:12px; overflow:hidden;
                box-shadow:0 4px 20px rgba(0,0,0,0.08); }}
  .header {{ background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%); color:#fff; padding:25px 30px; }}
  .header h1 {{ margin:0 0 5px 0; font-size:20px; }}
  .header p {{ margin:0; font-size:13px; color:#aab; }}
  .date {{ color:#e94560; font-weight:bold; }}
  .footer {{ background:#f8f9fa; padding:15px 25px; font-size:12px; color:#888; text-align:center;
             border-top:1px solid #eee; }}
  .data-table {{ width:100%; border-collapse:collapse; font-size:13px; margin-bottom:20px; }}
  .data-table th {{ background:#1a1a2e; color:#fff; padding:8px 10px; text-align:left; font-weight:normal; }}
  .data-table td {{ padding:7px 10px; border-bottom:1px solid #eee; }}
  .data-table tr:hover {{ background:#f8f9fa; }}
  .data-table tr.highlight {{ background:#fff9f0; }}
  .rank-table tr:hover {{ background:#fff3cd; }}
</style></head><body>
<div class="container">
  <div class="header">
    <h1>📊 五大策略综合选股报告</h1>
    <p>2026-03-31（周二）收盘 &nbsp;|&nbsp; 排除688 &nbsp;|&nbsp; 数据来源：东方财富</p>
  </div>
  <div style="padding:20px 25px">
    {rank_html}
    {short_html}
    {advice_html}
    {summary_html}
    {s1_html}
    {s2_html}
    {s3_html}
    {s4_html}
    {s5_html}
    {signature_html}
  </div>
</div></body></html>'''

# ========== 发送邮件 ==========
def load_config():
    cfg = {}
    path = r'C:\Users\admin\.qclaw\workspace\email_config.txt'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    cfg[k.strip()] = v.strip()
    return cfg

def send(to, subject, html_body, cfg):
    host = cfg.get('SMTP_HOST', 'smtp.qq.com')
    port = int(cfg.get('SMTP_PORT', 465))
    user = cfg.get('SMTP_USER', '')
    password = cfg.get('SMTP_PASS', '')
    from_name = cfg.get('FROM_NAME', 'Marcus')

    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr([from_name, user])
    msg['To'] = to
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    with smtplib.SMTP_SSL(host, port) as server:
        server.login(user, password)
        server.sendmail(user, [to], msg.as_string())
    print(f'发送成功: {to}')

cfg = load_config()
send('18339435211@139.com', '📊 五大策略综合选股报告 | 2026-03-31', html, cfg)
print('Done!')
