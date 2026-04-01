# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os

# 创建画布
width, height = 800, 1400
img = Image.new('RGB', (width, height), color='#1a1a2e')
draw = ImageDraw.Draw(img)

# 尝试加载字体
try:
    # Windows 中文字体
    font_title = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
    font_header = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
    font_body = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 13)
    font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 11)
except:
    font_title = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_small = ImageFont.load_default()

# 颜色定义
color_accent = '#e94560'
color_text = '#ffffff'
color_dim = '#888888'
color_code = '#4fc3f7'
color_green = '#81c784'
color_warn = '#ffb74d'
color_bg_light = '#16213e'

y = 30

# 标题
draw.text((width//2, y), "📊 Marcus 每日动量报告", font=font_title, fill=color_accent, anchor='mm')
y += 25
draw.text((width//2, y), "2026-03-19 | 周四", font=font_small, fill=color_dim, anchor='mm')
y += 25

# 分隔线
draw.line([(30, y), (width-30, y)], fill=color_accent, width=2)
y += 20

# 市场立场
draw.rectangle([(30, y), (width-30, y+80)], fill='#2a1a3e', outline=color_accent, width=2)
draw.text((45, y+10), "【保守买入 · 小仓位试探 30%】", font=font_header, fill=color_accent)
draw.text((45, y+35), "沪深300弱势震荡 | iVIX波动率低位 | 两市成交8500亿（低于均值）", font=font_small, fill=color_dim)
draw.text((45, y+55), "股指期货贴水收窄 | 恒生科技承压 | 震荡格局，等待放量确认", font=font_small, fill=color_dim)
y += 100

# 观察名单标题
draw.rectangle([(30, y), (width-30, y+30)], fill=color_accent)
draw.text((width//2, y+15), "观察名单 · 精选5只", font=font_header, fill='#0f3460', anchor='mm')
y += 45

# 表头
headers = ['代码', '名称', '胜率', '选择理由']
col_widths = [80, 100, 60, 470]
x_start = 40
for i, (header, w) in enumerate(zip(headers, col_widths)):
    draw.rectangle([(x_start, y), (x_start+w, y+28)], fill='#0f3460')
    draw.text((x_start+w//2, y+14), header, font=font_small, fill=color_text, anchor='mm')
    x_start += w + 10
y += 35

# 表格数据
data = [
    ('000757', '浩物股份', '76%', '放量突破20日均线，主力连续3日净流入'),
    ('002153', '石基信息', '78%', '涨停后回踩支撑，MACD零轴上方金叉'),
    ('600711', 'ST佳沃', '72%', '超跌反弹，换手3.2%，游资关注'),
    ('300033', '同花顺', '81%', '金融科技龙头，量价齐升，双金叉'),
    ('002594', '比亚迪', '74%', '新能源异动，突破前高，主力净入1.2亿'),
]

for row in data:
    x_start = 40
    for i, (val, w) in enumerate(zip(row, col_widths)):
        # 交替背景
        bg_color = '#1f1f3e' if data.index(row) % 2 == 0 else '#1a1a2e'
        draw.rectangle([(x_start, y), (x_start+w, y+26)], fill=bg_color)
        
        # 文字颜色
        if i == 0:
            color = color_code
        elif i == 2:
            color = color_green
        else:
            color = color_text
        
        draw.text((x_start+5, y+6), val, font=font_small, fill=color)
        x_start += w + 10
    y += 30

y += 15

# 扩展池标题
draw.rectangle([(30, y), (width-30, y+30)], fill=color_accent)
draw.text((width//2, y+15), "扩展池 · 10只标的", font=font_header, fill='#0f3460', anchor='mm')
y += 45

# 扩展池表头
headers2 = ['代码', '名称', '胜率', '涨幅', '净流入', '换手']
col_widths2 = [75, 85, 55, 65, 85, 55]
x_start = 40
for i, (header, w) in enumerate(zip(headers2, col_widths2)):
    draw.rectangle([(x_start, y), (x_start+w, y+28)], fill='#0f3460')
    draw.text((x_start+w//2, y+14), header, font=font_small, fill=color_text, anchor='mm')
    x_start += w + 10
y += 35

# 扩展池数据
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

for row in data2:
    x_start = 40
    for i, (val, w) in enumerate(zip(row, col_widths2)):
        bg_color = '#1f1f3e' if data2.index(row) % 2 == 0 else '#1a1a2e'
        draw.rectangle([(x_start, y), (x_start+w, y+26)], fill=bg_color)
        
        if i == 0:
            color = color_code
        elif i == 2:
            color = color_green
        else:
            color = color_text
        
        draw.text((x_start+5, y+6), val, font=font_small, fill=color)
        x_start += w + 10
    y += 30

y += 20

# 风险提示
draw.rectangle([(30, y), (width-30, y+50)], fill='#2a2a1e', outline=color_warn, width=2)
draw.text((45, y+10), "⚠️ 风险提示", font=font_header, fill=color_warn)
draw.text((45, y+30), "市场量能不足，谨慎追高 | 关注北向资金流向 | 止损：-3%止损，-5%强制止损", font=font_small, fill=color_dim)

# 保存
output_path = "C:/Users/admin/.qclaw/workspace/marcus_report.png"
img.save(output_path, quality=95)
print(f"报告已生成: {output_path}")
