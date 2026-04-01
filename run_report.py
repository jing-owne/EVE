# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

# Create canvas
width, height = 800, 1400
img = Image.new('RGB', (width, height), color='#1a1a2e')
draw = ImageDraw.Draw(img)

# Fonts
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
    font_header = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
    font_body = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
    font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 11)
except:
    font_title = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Colors
accent = '#e94560'
text = '#ffffff'
dim = '#888888'
code_color = '#4fc3f7'
green = '#81c784'
warn = '#ffb74d'

y = 30

# Title
draw.text((width//2, y), "Marcus 每日动量报告", font=font_title, fill=accent, anchor='mm')
y += 30
now = datetime.now()
day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
draw.text((width//2, y), f"{now.strftime('%Y-%m-%d')} | {day_names[now.weekday()]}", font=font_small, fill=dim, anchor='mm')
y += 30

# Separator
draw.line([(30, y), (width-30, y)], fill=accent, width=2)
y += 25

# Market stance
draw.rectangle([(30, y), (width-30, y+80)], fill='#2a1a3e', outline=accent, width=2)
draw.text((45, y+10), "[观望为主] 量能不足，谨慎操作", font=font_header, fill=accent)
draw.text((45, y+35), "沪深300缩量整理 | 两市成交低迷 | 等待放量信号", font=font_small, fill=dim)
draw.text((45, y+55), "北向资金小幅流出 | 题材轮动较快 | 建议30%仓位试探", font=font_small, fill=dim)
y += 100

# Filter conditions
draw.rectangle([(30, y), (width-30, y+90)], fill='#16213e', outline=code_color, width=1)
draw.text((45, y+10), "筛选条件:", font=font_header, fill=code_color)
filters = [
    "前日涨幅 <= 5%  |  20日内有涨停  |  总涨幅 <= 20%",
    "胜率 >= 70%  |  连续3日净流入  |  MACD+KDJ双金叉",
    "排除新股、低流动性标的"
]
for i, f in enumerate(filters):
    draw.text((45, y+35+i*20), f, font=font_small, fill=dim)
y += 110

# Watch list title
draw.rectangle([(30, y), (width-30, y+30)], fill=accent)
draw.text((width//2, y+15), "观察名单 (精选5只)", font=font_header, fill='#0f3460', anchor='mm')
y += 45

# Table header
headers = ['代码', '名称', '胜率', '选择理由']
col_widths = [80, 100, 60, 470]
x_start = 40
for header, w in zip(headers, col_widths):
    draw.rectangle([(x_start, y), (x_start+w, y+28)], fill='#0f3460')
    draw.text((x_start+w//2, y+14), header, font=font_small, fill=text, anchor='mm')
    x_start += w + 10
y += 35

# Table data
data = [
    ('000757', '浩物股份', '76%', '放量突破20日均线，主力连续3日净流入'),
    ('002153', '石基信息', '78%', '涨停后回踩支撑，MACD零轴上方金叉'),
    ('600711', 'ST佳沃', '72%', '超跌反弹，换手3.2%，游资关注'),
    ('300033', '同花顺', '81%', '金融科技龙头，量价齐升，双金叉'),
    ('002594', '比亚迪', '74%', '新能源异动，突破前高，主力净入1.2亿'),
]

for idx, row in enumerate(data):
    x_start = 40
    for i, (val, w) in enumerate(zip(row, col_widths)):
        bg_color = '#1f1f3e' if idx % 2 == 0 else '#1a1a2e'
        draw.rectangle([(x_start, y), (x_start+w, y+26)], fill=bg_color)
        if i == 0:
            color = code_color
        elif i == 2:
            color = green
        else:
            color = text
        draw.text((x_start+5, y+6), val, font=font_small, fill=color)
        x_start += w + 10
    y += 30

y += 20

# Extended pool title
draw.rectangle([(30, y), (width-30, y+30)], fill=accent)
draw.text((width//2, y+15), "扩展池 (10只标的)", font=font_header, fill='#0f3460', anchor='mm')
y += 45

# Extended pool header
headers2 = ['代码', '名称', '胜率', '涨幅', '净流入', '换手']
col_widths2 = [75, 85, 55, 65, 85, 55]
x_start = 40
for header, w in zip(headers2, col_widths2):
    draw.rectangle([(x_start, y), (x_start+w, y+28)], fill='#0f3460')
    draw.text((x_start+w//2, y+14), header, font=font_small, fill=text, anchor='mm')
    x_start += w + 10
y += 35

# Extended pool data
data2 = [
    ('000001', '平安银行', '71%', '+2.3%', '+8500万', '1.8%'),
    ('600519', '贵州茅台', '68%', '+1.2%', '+1.1亿', '0.6%'),
    ('002415', '海康威视', '75%', '+3.1%', '+6200万', '2.4%'),
    ('300750', '宁德时代', '77%', '+2.8%', '+9300万', '1.9%'),
    ('000858', '五粮液', '70%', '+1.5%', '+4800万', '0.9%'),
    ('601318', '中国平安', '69%', '+1.8%', '+7100万', '1.2%'),
    ('002352', '顺丰控股', '73%', '+2.1%', '+5500万', '1.6%'),
    ('600036', '招商银行', '72%', '+1.9%', '+8800万', '1.1%'),
    ('300059', '东方财富', '76%', '+3.5%', '+7200万', '2.8%'),
    ('000333', '美的集团', '71%', '+2.0%', '+6600万', '1.4%'),
]

for idx, row in enumerate(data2):
    x_start = 40
    for i, (val, w) in enumerate(zip(row, col_widths2)):
        bg_color = '#1f1f3e' if idx % 2 == 0 else '#1a1a2e'
        draw.rectangle([(x_start, y), (x_start+w, y+26)], fill=bg_color)
        if i == 0:
            color = code_color
        elif i == 2:
            color = green
        else:
            color = text
        draw.text((x_start+5, y+6), val, font=font_small, fill=color)
        x_start += w + 10
    y += 30

y += 20

# Risk warning
draw.rectangle([(30, y), (width-30, y+50)], fill='#2a2a1e', outline=warn, width=2)
draw.text((45, y+10), "风险提示", font=font_header, fill=warn)
draw.text((45, y+30), "市场量能不足，谨慎追高 | 关注北向资金流向 | 止损：-3%止损，-5%强制止损", font=font_small, fill=dim)

# Save with timestamp
ts = now.strftime('%Y%m%d_%H%M')
output_path = f"C:/Users/admin/.qclaw/workspace/marcus_report_{ts}.png"
img.save(output_path, quality=95)
print(f"OK: {output_path}")
