# -*- coding: utf-8 -*-
"""五大策略选股报告 v3.6 - 支持调试模式（不发送邮件）"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import json
import urllib.request
from datetime import datetime
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ========== 调试模式开关 ==========
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'

if DEBUG_MODE:
    print('[DEBUG] 调试模式已启用 - 不会发送任何邮件')

# ========== 获取每日一言 ==========

def fetch_daily_quote():
    """从 hitokoto 获取每日一言"""
    try:
        # c=d 诗词, c=h 影视, c=i 网络
        url = 'https://v1.hitokoto.cn/?c=d&c=h&c=i&encode=json'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8', errors='replace'))
            hitokoto = data.get('hitokoto', '')
            from_src = data.get('from', '')
            from_who = data.get('from_who', '')
            source = f'——{from_who}《{from_src}》' if from_who else f'——《{from_src}》' if from_src else ''
            return {'text': hitokoto, 'source': source}
    except Exception as e:
        print(f'每日一言获取失败: {e}')
        return {'text': '不积跬步，无以至千里；不积小流，无以成江海。', 'source': '——荀子《劝学》'}

# ========== 获取金十快讯 ==========

def fetch_jin10_news(limit=15):
    """抓取金十数据最新快讯"""
    try:
        url = f'https://www.jin10.com/flash_newest.js?t={int(__import__("time").time()*1000)}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://www.jin10.com/',
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode('utf-8', errors='replace').strip()
            # 格式: var newest = [...]
            if raw.startswith('var newest'):
                raw = raw[raw.index('['): raw.rindex(']')+1]
            items = json.loads(raw)
            news = []
            for item in items[:limit]:
                content = item.get('data', {}).get('content', '').strip()
                time_str = item.get('time', '')[:16]  # 只取到分钟
                important = item.get('important', 0)
                if content:
                    news.append({'time': time_str, 'content': content, 'important': important})
            return news
    except Exception as e:
        print(f'金十快讯获取失败: {e}')
        return []

def build_jin10_html(news_list):
    """生成金十快讯HTML - 只保留A股/财经相关内容"""
    if not news_list:
        return ''
    
    # A股/财经关键词过滤
    finance_keywords = [
        'A股', '股市', '沪指', '深成', '创业板', '涨停', '跌停', '板块', '主力',
        '央行', '货币', '利率', '降准', '降息', '财政', '政策', '经济', 'GDP', 'PMI',
        '人民币', '汇率', '外汇', '黄金', '原油', '大宗', '期货', '债券',
        '美联储', '美股', '纳斯达克', '道琼斯', '标普', '港股', '恒指',
        '上市', '融资', '并购', '重组', '分红', '回购', '增持', '减持',
        '科技', '芯片', '半导体', 'AI', '人工智能', '新能源', '锂电', '光伏',
        '贸易', '关税', '出口', '进口', '供应链', '制造业',
    ]
    
    filtered = []
    for item in news_list:
        content = item['content']
        if any(kw in content for kw in finance_keywords):
            filtered.append(item)
    
    # 如果过滤后太少，补充原始条目
    if len(filtered) < 3:
        filtered = news_list
    
    rows = ''
    for item in filtered:
        bg = '#fff8e1' if item['important'] else '#fff'
        star = '⭐ ' if item['important'] else ''
        rows += f'''<tr style="background:{bg}">
  <td style="color:#888;white-space:nowrap;padding:6px 10px;font-size:12px;">{item["time"]}</td>
  <td style="padding:6px 10px;font-size:13px;line-height:1.6;">{star}{item["content"]}</td>
</tr>'''
    return f'''
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  <thead><tr style="background:#f39c12;color:#fff;">
    <th style="padding:8px 10px;text-align:left;width:120px;">时间</th>
    <th style="padding:8px 10px;text-align:left;">快讯内容</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>'''

print('Fetching daily quote...')
daily_quote = fetch_daily_quote()
print(f'Quote: {daily_quote["text"][:30]}...')

print('Fetching Jin10 news...')
jin10_news = fetch_jin10_news(10)
print(f'Got {len(jin10_news)} jin10 items')

# ========== 获取实时新闻 ==========

def fetch_news_from_prosearch(keyword):
    """从 ProSearch 获取实时新闻"""
    try:
        PORT = 19000
        from_time = int(__import__('time').time()) - 86400
        
        cmd = [
            'curl', '-s', '-X', 'POST',
            f'http://localhost:{PORT}/proxy/prosearch/search',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({
                "keyword": keyword,
                "from_time": from_time
            })
        ]
        
        output = subprocess.check_output(cmd, timeout=10).decode('utf-8', errors='replace')
        data = json.loads(output)
        
        if data.get('success'):
            return data.get('message', '')
        return None
    except:
        return None

print('Fetching news from ProSearch...')
today_str_kw = datetime.now().strftime('%Y年%m月%d日')
news_results = {}
keywords = [
    f'A股涨停板 {today_str_kw}',
    f'A股热点板块 {today_str_kw}',
    '央行货币政策',
]
for kw in keywords:
    result = fetch_news_from_prosearch(kw)
    if result:
        news_results[kw] = result[:600]

# ========== 股票数据获取 ==========

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

print('Fetching stock data...')

data1 = fetch(get_url('f8', 100))
data2 = fetch(get_url('f6', 100))
data3 = fetch(get_url('f3', 200))
data4 = fetch(get_url('f3', 200))
data5 = fetch(get_url('f62', 100))

s1 = clean_stocks(data1)
s1.sort(key=lambda x: x['turnover'], reverse=True)

s2 = clean_stocks(data2)
s2.sort(key=lambda x: x['amount'], reverse=True)

s3 = clean_stocks(data3, min_pct=1.0)
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
    if not data_list:
        html += '''<tr><td colspan="7" style="text-align:center;color:#aaa;padding:16px;font-size:13px;">
        📭 当前筛选条件下暂无符合标的
        </td></tr>'''
    html += '</tbody></table>'
    return html

s1_html = section('策略① 放量上涨', '放量上涨 + 均线多头 + 停机坪 + 突破平台',
    '换手率 + 成交额 + 涨幅 + MACD金叉 + KDJ金叉',
    '按换手率排序，取TOP10（排除688）', s1, ['code','name','pct','amount','turnover','inflow'], 10)

s2_html = section('策略② 成交额排名', '换手率排名 + 涨停板封单监控 + 大单交易追踪',
    '换手率 + 成交量 + 封单金额 + 大单净买入',
    '按成交额排序，取TOP10（排除688）', s2, ['code','name','amount','turnover','pct','inflow'], 10)

s3_html = section('策略③ 多因子量化', '中低频多因子选股 + 估值 + 成长 + 全市场分析',
    '市盈率PE + 市净率PB + 净资产收益率ROE + 净利润增长率',
    '筛选: 涨幅≥1% 且 成交额≥2亿（排除688）', s3, ['code','name','pct','amount','turnover','inflow'], 10)

s4_html = section('策略④ AI技术面', 'AI大模型K线技术指标分析 + 市场情绪分析',
    'KDJ金叉 + MACD金叉 + RSI + CCI + 量价配合',
    '筛选: 涨幅>0% 且 换手率>1% 且 主力净流入>0（排除688）', s4, ['code','name','inflow','pct','amount','turnover'], 10)

s5_html = section('策略⑤ 目标价+机构', '目标价上涨空间 + 董监高交易追踪 + 机构持仓变动',
    '目标价偏离度 + 董监高净买入 + 机构持股比例 + 北向资金',
    '筛选: 主力净流入≥1亿（排除688）', s5, ['code','name','inflow','pct','amount','turnover'], 10)

# 五大策略标题包装
strategies_html = '''
<h1 style="color:#1a1a2e;margin:20px 0 10px 0;font-size:18px;font-weight:bold;border-left:5px solid #e94560;padding-left:12px;">
  📋 五大策略详细列表
</h1>
''' + s1_html + s2_html + s3_html + s4_html + s5_html

# 综合胜率 TOP15（汇总五大策略前10）
top15 = ranked[:15]
rank_html = f'''
<h1 style="color:#fff;background:linear-gradient(135deg,#e94560,#1a1a2e);margin:20px 0 10px 0;font-size:18px;font-weight:bold;padding:12px 18px;border-radius:8px;letter-spacing:1px;">
  🏆 综合胜率 TOP15
</h1>
<p style="color:#555;font-size:13px;margin:5px 0 8px 0;">
  <b style="color:#e94560">汇总来源:</b> 五大策略各取前10，去重后按综合评分排序 &nbsp;|&nbsp;
  <b style="color:#e94560">评分规则:</b> 命中策略数 × 20分 + 主力净流入 + 换手率 + 成交额加分
</p>
<table class="data-table rank-table">
  <thead><tr>
    <th>排名</th><th>代码</th><th>名称</th><th>综合胜率</th>
    <th>策略命中</th><th>涨跌幅</th><th>主力净流入</th><th>换手率</th>
  </tr></thead><tbody>
'''
medals = ['🥇','🥈','🥉']
for i, (code, v) in enumerate(top15):
    pct = v['pct']
    win_rate = min(50 + v['cnt'] * 10 + int(v['inflow'] * 2), 97)
    medal = medals[i] if i < 3 else f'{i+1}'
    row_bg = '#fff3cd' if i < 3 else ('#fafafa' if i % 2 == 0 else '#fff')
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

# 操作建议 | 风险提示（含每日一言）
advice_html = f'''
<h1 style="color:#1a1a2e;margin:20px 0 10px 0;font-size:18px;font-weight:bold;border-left:5px solid #27ae60;padding-left:12px;">
  💡 操作建议 | 风险提示
</h1>
<div style="background:linear-gradient(135deg,#f8f9ff,#f0f4ff);border-radius:8px;padding:14px 20px;margin-bottom:14px;border-left:3px solid #6366f1;">
  <p style="margin:0;font-size:15px;color:#374151;font-style:italic;line-height:1.8;text-align:center;">
    「{daily_quote["text"]}」
  </p>
  <p style="margin:6px 0 0 0;font-size:12px;color:#9ca3af;text-align:center;">{daily_quote["source"]}</p>
</div>
<div style="background:#f0f8f0;padding:14px 16px;border-radius:6px;font-size:13px;line-height:1.9;color:#333;">
  <p><b style="color:#27ae60">📈 买入信号:</b></p>
  <ul style="margin:5px 0;padding-left:20px;">
    <li>综合胜率≥70% 的标的，可在支撑位布局</li>
    <li>MACD + KDJ 双金叉，且成交额≥2亿</li>
    <li>连续3天净流入，换手率2-5%（温和放量）</li>
    <li>涨幅≤5%，20天内有涨停历史</li>
  </ul>
  <p style="margin-top:10px;"><b style="color:#e94560">📉 卖出信号:</b></p>
  <ul style="margin:5px 0;padding-left:20px;">
    <li><b style="color:#e94560">⚠️ 止损原则：股票-3% 无条件出场</b></li>
    <li>涨幅≥9.5% 且换手率≥5%，高位获利了结</li>
    <li>MACD死叉或KDJ高位钝化，减仓信号</li>
    <li>主力净流出转向，警惕出货</li>
  </ul>
  <p style="margin-top:10px;"><b style="color:#1a1a2e">🛡️ 风险管理:</b></p>
  <ul style="margin:5px 0;padding-left:20px;">
    <li>单笔仓位不超过总资金的5%</li>
    <li>排除新股、低流动性标的（日均成交&lt;1亿）</li>
    <li>避免追高，等待回调后布局</li>
    <li>关注政策风险、财报预期不确定性</li>
  </ul>
</div>
'''

# 金十快讯
jin10_html = f'''
<h1 style="color:#1a1a2e;margin:20px 0 10px 0;font-size:18px;font-weight:bold;border-left:5px solid #f39c12;padding-left:12px;">
  ⚡ 金十快讯
</h1>
''' + (build_jin10_html(jin10_news) if jin10_news else '<p style="color:#aaa;font-size:13px;">暂无快讯数据</p>')

# 今日市场总结（动态）
def build_summary_html(news_results, today_str):
    # 从 ProSearch 结果提取关键信息
    news_block = ''
    if news_results:
        for kw, content in news_results.items():
            if content:
                # 截取前200字
                snippet = content[:200].replace('<', '&lt;').replace('>', '&gt;')
                news_block += f'<p style="margin:6px 0;"><b style="color:#3498db">· </b>{snippet}…</p>\n'
    
    if not news_block:
        news_block = '<p style="color:#aaa;font-size:12px;">今日市场数据获取中，请以实盘为准</p>'
    
    return f'''
<h1 style="color:#1a1a2e;margin:20px 0 10px 0;font-size:18px;font-weight:bold;border-left:5px solid #3498db;padding-left:12px;">
  📈 今日市场总结
</h1>
<div style="background:#f0f4f8;padding:14px 16px;border-radius:6px;font-size:13px;line-height:1.9;color:#333;">
  <p><b style="color:#3498db">📅 {today_str} 盘中动态：</b></p>
  {news_block}
  <p style="margin-top:10px;font-size:12px;color:#e94560;">⚠️ 风险提示：市场波动较大，注意仓位控制，止损-3%无条件出</p>
</div>
'''

summary_html = build_summary_html(news_results, datetime.now().strftime('%Y-%m-%d'))

# Marcus签名
signature_html = f'''
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
    数据来源：东方财富、新浪财经、同花顺、财经网、第一财经 | 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
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
    <p>{datetime.now().strftime("%Y-%m-%d")}（{["周一","周二","周三","周四","周五","周六","周日"][datetime.now().weekday()]}）盘中 &nbsp;|&nbsp; 排除688 &nbsp;|&nbsp; 数据来源：东方财富、新浪财经、同花顺、财经网、第一财经</p>
  </div>
  <div style="padding:20px 25px">
    {advice_html}
    {jin10_html}
    {rank_html}
    {summary_html}
    {strategies_html}
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

def send(to_email, cc_emails, subject, html_body, cfg):
    if DEBUG_MODE:
        print('[DEBUG] 邮件发送已跳过（调试模式）')
        print(f'[DEBUG] 收件人: {to_email}')
        print(f'[DEBUG] 抄送: {cc_emails}')
        print(f'[DEBUG] 主题: {subject}')
        return
    
    host = cfg.get('SMTP_HOST', 'smtp.qq.com')
    port = int(cfg.get('SMTP_PORT', 465))
    user = cfg.get('SMTP_USER', '')
    password = cfg.get('SMTP_PASS', '')
    from_name = cfg.get('FROM_NAME', 'Marcus')

    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr([from_name, user])
    msg['To'] = to_email
    
    if cc_emails:
        cc_list = [e.strip() for e in cc_emails.split(',')]
        msg['Cc'] = ', '.join(cc_list)
    
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))

    all_recipients = [to_email]
    if cc_emails:
        all_recipients.extend([e.strip() for e in cc_emails.split(',')])

    with smtplib.SMTP_SSL(host, port) as server:
        server.login(user, password)
        server.sendmail(user, all_recipients, msg.as_string())
    
    print(f'发送成功: {to_email}')
    if cc_emails:
        print(f'抄送: {cc_emails}')

cfg = load_config()
to_email = cfg.get('TO_EMAIL', '18339435211@139.com')

# 调试邮件只发主收件人（无抄送）
# 定时任务通过环境变量 SCHEDULED_TASK=true 触发完整抄送
is_scheduled = os.environ.get('SCHEDULED_TASK', '').lower() == 'true'
cc_emails = cfg.get('CC_EMAILS', '') if is_scheduled else ''

today_str = datetime.now().strftime('%Y-%m-%d')
day_name = ['周一','周二','周三','周四','周五','周六','周日'][datetime.now().weekday()]
subject = f'📊 五大策略综合选股报告 | {today_str}（{day_name}）收盘'

send(to_email, cc_emails, subject, html, cfg)

if not DEBUG_MODE:
    print('Done!')
else:
    print('[DEBUG] 报告生成完成（未发送）')
