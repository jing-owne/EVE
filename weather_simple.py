import warnings, os, json, sys
warnings.filterwarnings('ignore')
os.environ['TMP'] = os.environ['TEMP'] = 'C:\\Users\\admin\\AppData\\Local\\Temp'

import requests
from datetime import datetime

url = 'https://wttr.in/Shanghai?format=j1'

try:
    r = requests.get(url, timeout=10)
    data = r.json()
    
    current = data['current_condition'][0]
    forecast = data['weather']
    
    # 构建报告
    report = []
    report.append('=== SHANGHAI WEATHER REPORT ===')
    report.append(f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    report.append('')
    
    # 当前天气
    report.append('[TODAY WEATHER]')
    report.append(f'Temp: {current["temp_C"]}C (feels {current["FeelsLikeC"]}C)')
    report.append(f'Condition: {current["weatherDesc"][0]["value"]}')
    report.append(f'Humidity: {current["humidity"]}%')
    report.append(f'Wind: {current["windspeedKmph"]} km/h')
    report.append(f'Precipitation: {current["precipMM"]} mm')
    report.append(f'Visibility: {current["visibility"]} km')
    report.append('')
    
    # 穿衣建议
    report.append('[OUTFIT SUGGESTION]')
    temp = int(current['temp_C'])
    if temp < 5:
        report.append('Heavy down jacket + warm underwear + scarf + hat + gloves')
    elif temp < 10:
        report.append('Down jacket/thick jacket + long sleeves + scarf')
    elif temp < 15:
        report.append('Jacket/sweater + long sleeves + optional scarf')
    elif temp < 20:
        report.append('Long sleeve shirt/thin sweater + jacket')
    else:
        report.append('Short sleeves + thin jacket')
    
    humidity = int(current['humidity'])
    if humidity > 80:
        report.append('High humidity - bring umbrella')
    
    report.append('')
    
    # 空气质量
    report.append('[AIR QUALITY]')
    report.append(f'Visibility: {current["visibility"]} km')
    report.append(f'Precipitation: {current["precipMM"]} mm')
    report.append('')
    
    # 未来7天
    report.append('[7-DAY FORECAST]')
    for i, day in enumerate(forecast[:7]):
        date_str = day['date']
        max_temp = day['maxtempC']
        min_temp = day['mintempC']
        desc = day['hourly'][0]['weatherDesc'][0]['value'] if day['hourly'] else 'Unknown'
        report.append(f'{i+1}. {date_str}: {min_temp}-{max_temp}C, {desc}')
    
    output = '\n'.join(report)
    print(output)
    
except Exception as e:
    print(f'ERROR: {e}')
