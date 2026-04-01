import warnings, os, json, sys
warnings.filterwarnings('ignore')
os.environ['TMP'] = os.environ['TEMP'] = 'C:\\Users\\admin\\AppData\\Local\\Temp'

import requests
from datetime import datetime, timedelta

# 获取松江区泗泾镇天气（用上海作为代理）
url = 'https://wttr.in/Shanghai?format=j1'

try:
    r = requests.get(url, timeout=10)
    data = r.json()
    
    current = data['current_condition'][0]
    forecast = data['weather']
    
    # 构建报告
    report = []
    report.append('🌤️ **松江区泗泾镇 天气 + 穿衣指南**')
    report.append(f'更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    report.append('')
    
    # 当前天气
    report.append('**【今日天气】**')
    report.append(f'温度: {current["temp_C"]}°C（体感{current["FeelsLikeC"]}°C）')
    report.append(f'天气: {current["weatherDesc"][0]["value"]}')
    report.append(f'湿度: {current["humidity"]}%')
    report.append(f'风速: {current["windspeedKmph"]} km/h')
    report.append(f'降水: {current["precipMM"]} mm')
    report.append(f'能见度: {current["visibility"]} km')
    report.append(f'气压: {current["pressure"]} mb')
    report.append('')
    
    # 穿衣建议
    report.append('**【穿衣建议】**')
    temp = int(current['temp_C'])
    if temp < 5:
        report.append('🧥 厚羽绒服 + 保暖内衣 + 围巾 + 帽子 + 手套')
    elif temp < 10:
        report.append('🧥 羽绒服/厚夹克 + 长袖 + 围巾')
    elif temp < 15:
        report.append('🧥 夹克/毛衣 + 长袖 + 可选围巾')
    elif temp < 20:
        report.append('👕 长袖衬衫/薄毛衣 + 外套')
    else:
        report.append('👕 短袖 + 薄外套')
    
    humidity = int(current['humidity'])
    if humidity > 80:
        report.append('💧 湿度很高，建议防潮')
    
    report.append('')
    
    # 空气质量
    report.append('**【空气质量】**')
    report.append(f'能见度: {current["visibility"]} km（{("良好" if int(current["visibility"]) > 10 else "一般" if int(current["visibility"]) > 5 else "较差")}）')
    report.append(f'降水: {current["precipMM"]} mm（{"有雨" if float(current["precipMM"]) > 0 else "无雨"}）')
    report.append('')
    
    # 未来7天预报
    report.append('**【未来7天预报】**')
    for i, day in enumerate(forecast[:7]):
        date_str = day['date']
        max_temp = day['maxtempC']
        min_temp = day['mintempC']
        desc = day['hourly'][0]['weatherDesc'][0]['value'] if day['hourly'] else '未知'
        report.append(f'{i+1}. {date_str}: {min_temp}~{max_temp}°C, {desc}')
    
    report.append('')
    report.append('⚠️ 数据来自 wttr.in，仅供参考。')
    
    # 输出
    output = '\n'.join(report)
    print(output)
    
except Exception as e:
    print(f'ERROR: {e}')
