import json, urllib.request

# 招标股份 301136 - 重新获取完整数据
code = '301136'
secid = f'0.{code}'

url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f59,f60,f170,f171'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode('utf-8'))
    
    print('Raw data:')
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    if data.get('data'):
        d = data['data']
        print('\nParsed values:')
        print(f"f43 (current price raw): {d.get('f43')}")
        print(f"f44 (high raw): {d.get('f44')}")
        print(f"f45 (low raw): {d.get('f45')}")
        print(f"f46 (open raw): {d.get('f46')}")
        print(f"f60 (prev close raw): {d.get('f60')}")
        print(f"f170 (change pct raw): {d.get('f170')}")
        
        # 计算真实的涨跌幅
        price_raw = d.get('f43', 0)
        prev_close_raw = d.get('f60', 0)
        
        if price_raw and prev_close_raw:
            price = float(price_raw) / 100
            prev_close = float(prev_close_raw) / 100
            change_pct = (price - prev_close) / prev_close * 100
            
            print(f'\nCalculated:')
            print(f'Price: {price}')
            print(f'Prev Close: {prev_close}')
            print(f'Change %: {change_pct:.2f}%')
            
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
