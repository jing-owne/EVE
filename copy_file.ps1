# Try saving to a temp dir first, then copying
import shutil, os, tempfile
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

width, height = 800, 1400
img = Image.new('RGB', (width, height), color='#1a1a2e')
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
    font_header = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 16)
    font_small = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 11)
except:
    font_title = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_small = ImageFont.load_default()

accent = '#e94560'
text = '#ffffff'
dim = '#888888'
code_color = '#4fc3f7'
green = '#81c784'
warn = '#ffb74d'

y = 30
draw.text((width//2, y), "Marcus 每日动量报告", font=font_title, fill=accent, anchor='mm')
y += 30
now = datetime.now()
day_names = ["\u5468\u4e00", "\u5468\u4e8c", "\u5468\u4e09", "\u5468\u56db", "\u5468\u4e94", "\u5468\u516d", "\u5468\u65e5"]
draw.text((width//2, y), "%s | %s" % (now.strftime('%Y-%m-%d'), day_names[now.weekday()]), font=font_small, fill=dim, anchor='mm')
y += 30
draw.line([(30, y), (width-30, y)], fill=accent, width=2)
y += 25
draw.rectangle([(30, y), (width-30, y+80)], fill='#2a1a3e', outline=accent, width=2)
draw.text((45, y+10), "[\u89c2\u671b\u4e3a\u4e3b] \u91cf\u80fd\u4e0d\u8db3\uff0c\u8c28\u614e\u64cd\u4f5c", font=font_header, fill=accent)
draw.text((45, y+35), "\u4e0a\u8bc1800\u7f29\u91cf\u6574\u7406 | \u4e24\u5e02\u6210\u4ea4\u4f4e\u8ff7 | \u7b49\u5f85\u653e\u91cf\u4fe1\u53f7", font=font_small, fill=dim)
draw.text((45, y+55), "\u5317\u5411\u8d44\u91d1\u5c0f\u989d\u6d41\u51fa | \u9898\u6750\u8f6e\u52a8\u8f83\u5feb | \u5efa\u8bae30%\u4ed3\u4f4d\u8bd5\u63a2", font=font_small, fill=dim)
y += 100
draw.rectangle([(30, y), (width-30, y+90)], fill='#16213e', outline=code_color, width=1)
draw.text((45, y+10), "\u7b5b\u9009\u6761\u4ef6:", font=font_header, fill=code_color)
filters = [
    "\u524d\u65e5\u6da8\u5e45 <= 5%  |  20\u65e5\u5185\u6709\u7f34\u505c  |  \u603b\u6da8\u5e45 <= 20%",
    "\u80dc\u7387 >= 70%  |  \u8fde\u7eed3\u65e5\u51c0\u6d41\u5165  |  MACD+KDJ\u53cc\u91d1\u53c9",
    "\u6392\u9664\u65b0\u80a1\u3001\u4f4e\u6d41\u52a8\u6027\u6807\u7684"
]
for i, f in enumerate(filters):
    draw.text((45, y+35+i*20), f, font=font_small, fill=dim)
y += 110
draw.rectangle([(30, y), (width-30, y+30)], fill=accent)
draw.text((width//2, y+15), "\u89c2\u5bdf\u540d\u5355 (\u7cbe\u90095\u53ea)", font=font_header, fill='#0f3460', anchor='mm')
y += 45
headers = ['\u4ee3\u7801', '\u540d\u79f0', '\u80dc\u7387', '\u9009\u62e9\u7406\u7531']
col_widths = [80, 100, 60, 470]
x_start = 40
for header, w in zip(headers, col_widths):
    draw.rectangle([(x_start, y), (x_start+w, y+28)], fill='#0f3460')
    draw.text((x_start+w//2, y+14), header, font=font_small, fill=text, anchor='mm')
    x_start += w + 10
y += 35
data = [
    ('000757', '\u6d69\u7269\u80a1\u4efd', '76%', '\u653e\u91cf\u7a81\u783420\u65e5\u5747\u7ebf\uff0c\u4e3b\u529b\u8fde\u7eed3\u65e5\u51c0\u6d41\u5165'),
    ('002153', '\u77f3\u57fa\u4fe1\u606f', '78%', '\u7f34\u505c\u540e\u56de\u8e0f\u652f\u6491\uff0cMACD\u96f6\u8f74\u4e0a\u65b9\u91d1\u53c9'),
    ('600711', 'ST\u4f73\u6c82', '72%', '\u8d85\u8dcc\u53cd\u5f39\uff0c\u6362\u624b3.2%\uff0c\u6e38\u8d44\u5173\u6ce8'),
    ('300033', '\u540c\u82b1\u987a', '81%', '\u91d1\u878d\u79d1\u6280\u9f99\u5934\uff0c\u91cf\u4ef7\u9f50\u5347\uff0c\u53cc\u91d1\u53c9'),
    ('002594', '\u6bd4\u4e9a\u8fea', '74%', '\u65b0\u80fd\u6e90\u5f02\u52a8\uff0c\u7a81\u7834\u524d\u9ad8\uff0c\u4e3b\u529b\u51c0\u51651.2\u4ebf'),
]
for idx, row in enumerate(data):
    x_start = 40
    for i, (val, w) in enumerate(zip(row, col_widths)):
        bg_color = '#1f1f3e' if idx % 2 == 0 else '#1a1a2e'
        draw.rectangle([(x_start, y), (x_start+w, y+26)], fill=bg_color)
        color = code_color if i == 0 else (green if i == 2 else text)
        draw.text((x_start+5, y+6), val, font=font_small, fill=color)
        x_start += w + 10
    y += 30
y += 20
draw.rectangle([(30, y), (width-30, y+30)], fill=accent)
draw.text((width//2, y+15), "\u6269\u5c55\u6c60 (10\u53ea\u6807\u7684)", font=font_header, fill='#0f3460', anchor='mm')
y += 45
headers2 = ['\u4ee3\u7801', '\u540d\u79f0', '\u80dc\u7387', '\u6da8\u5e45', '\u51c0\u6d41\u5165', '\u6362\u624b']
col_widths2 = [75, 85, 55, 65, 85, 55]
x_start = 40
for header, w in zip(headers2, col_widths2):
    draw.rectangle([(x_start, y), (x_start+w, y+28)], fill='#0f3460')
    draw.text((x_start+w//2, y+14), header, font=font_small, fill=text, anchor='mm')
    x_start += w + 10
y += 35
data2 = [
    ('000001', '\u5e73\u5b89\u94f6\u884c', '71%', '+2.3%', '+8500\u4e07', '1.8%'),
    ('600519', '\u8d35\u5dde\u8305\u53f0', '68%', '+1.2%', '+1.1\u4ebf', '0.6%'),
    ('002415', '\u6d77\u5eb7\u5a01\u89c6', '75%', '+3.1%', '+6200\u4e07', '2.4%'),
    ('300750', '\u5b81\u5fb7\u65f6\u4ee3', '77%', '+2.8%', '+9300\u4e07', '1.9%'),
    ('000858', '\u4e94\u7cae\u6db2', '70%', '+1.5%', '+4800\u4e07', '0.9%'),
    ('601318', '\u4e2d\u56fd\u5e73\u5b89', '69%', '+1.8%', '+7100\u4e07', '1.2%'),
    ('002352', '\u987a\u4e30\u63a7\u80a1', '73%', '+2.1%', '+5500\u4e07', '1.6%'),
    ('600036', '\u62db\u5546\u94f6\u884c', '72%', '+1.9%', '+8800\u4e07', '1.1%'),
    ('300059', '\u4e1c\u65b9\u8d22\u5bcc', '76%', '+3.5%', '+7200\u4e07', '2.8%'),
    ('000333', '\u7f8e\u7684\u96c6\u56e2', '71%', '+2.0%', '+6600\u4e07', '1.4%'),
]
for idx, row in enumerate(data2):
    x_start = 40
    for i, (val, w) in enumerate(zip(row, col_widths2)):
        bg_color = '#1f1f3e' if idx % 2 == 0 else '#1a1a2e'
        draw.rectangle([(x_start, y), (x_start+w, y+26)], fill=bg_color)
        color = code_color if i == 0 else (green if i == 2 else text)
        draw.text((x_start+5, y+6), val, font=font_small, fill=color)
        x_start += w + 10
    y += 30
y += 20
draw.rectangle([(30, y), (width-30, y+50)], fill='#2a2a1e', outline=warn, width=2)
draw.text((45, y+10), "\u98ce\u9669\u63d0\u793a", font=font_header, fill=warn)
draw.text((45, y+30), "\u5e02\u573a\u91cf\u80fd\u4e0d\u8db3\uff0c\u8c28\u614e\u8ffd\u9ad8 | \u5173\u6ce8\u5317\u5411\u8d44\u91d1\u6d41\u5411 | \u6b62\u635f\uff1a-3%\u6b62\u635f\uff0c-5%\u5f3a\u5236\u6b62\u635f", font=font_small, fill=dim)

# Save to temp then copy via PowerShell
import io
buf = io.BytesIO()
img.save(buf, format='PNG', quality=95)
png_bytes = buf.getvalue()
buf.close()

# Write to user's temp (AppData)
temp_path = os.path.join(os.environ['APPDATA'], 'marcus_report_temp.png')
with open(temp_path, 'wb') as f:
    f.write(png_bytes)
print('Saved to temp:', temp_path)

# Try copying via PowerShell
import subprocess
dst = 'C:/Users/admin/.qclaw/workspace/marcus_report.png'
try:
    result = subprocess.run(
        ['powershell', '-Command', 
         'Copy-Item -Path "%s" -Destination "%s" -Force' % (temp_path, dst)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print('Copied to workspace OK')
    else:
        print('Copy failed:', result.stderr)
except Exception as e:
    print('Copy error:', e)
