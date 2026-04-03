import urllib.request
import json

# 盘锦市经纬度: 41.1244, 122.0703
url = 'https://api.open-meteo.com/v1/forecast?latitude=41.1244&longitude=122.0703&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=Asia/Shanghai'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        data = json.loads(response.read().decode('utf-8'))
    
    current = data['current']
    
    # 天气代码转描述
    weather_codes = {
        0: '晴朗', 1: ' mainly clear', 2: '多云', 3: '阴天',
        45: '雾', 48: '雾凇',
        51: '毛毛雨', 53: '中雨', 55: '大雨',
        61: '小雨', 63: '中雨', 65: '大雨',
        71: '小雪', 73: '中雪', 75: '大雪',
        95: '雷雨'
    }
    
    weather = weather_codes.get(current['weather_code'], '未知')
    
    print('盘锦市今日天气')
    print('=' * 40)
    print(f"温度: {current['temperature_2m']}°C")
    print(f"体感: {current['apparent_temperature']}°C")
    print(f"天气: {weather}")
    print(f"湿度: {current['relative_humidity_2m']}%")
    print(f"风速: {current['wind_speed_10m']} km/h")
    print('=' * 40)
    
except Exception as e:
    print(f'获取天气失败: {e}')
