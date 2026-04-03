import json, urllib.request

# 招标股份 301136 - 正确解析
code = '301136'
secid = f'0.{code}'

# 获取完整数据
url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f59,f60,f170,f171,f103,f104,f105,f106,f108,f162,f167'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode('utf-8'))
    
    if data.get('data'):
        d = data['data']
        
        # 正确解析数据（除以100）
        result = {
            'code': code,
            'name': '招标股份',
            'price': float(d.get('f43', 0)) / 100,
            'high': float(d.get('f44', 0)) / 100,
            'low': float(d.get('f45', 0)) / 100,
            'open': float(d.get('f46', 0)) / 100,
            'prev_close': float(d.get('f60', 0)) / 100,
            'change_pct': float(d.get('f170', 0)) / 100,
            'change_amount': float(d.get('f171', 0)) / 100,
            'volume': float(d.get('f47', 0)),
            'amount': float(d.get('f48', 0)),
            'turnover': float(d.get('f59', 0)) / 100 if d.get('f59') else 0,
            'main_inflow': float(d.get('f103', 0)),
            'super_inflow': float(d.get('f104', 0)),
            'big_inflow': float(d.get('f105', 0)),
            'retail_count': float(d.get('f106', 0)),
            'main_control': float(d.get('f108', 0)),
            'pe': float(d.get('f162', 0)) / 100 if d.get('f162') else 0,
            'pb': float(d.get('f167', 0)) / 100 if d.get('f167') else 0,
        }
        
        print('=' * 60)
        print(f"招标股份 ({result['code']}) - 正确数据")
        print('=' * 60)
        print(f"当前价格: {result['price']:.2f} 元")
        print(f"昨收价格: {result['prev_close']:.2f} 元")
        print(f"今日涨跌: {result['change_pct']:+.2f}%")
        print(f"涨跌金额: {result['change_amount']:+.2f} 元")
        print(f"今日最高: {result['high']:.2f} 元")
        print(f"今日最低: {result['low']:.2f} 元")
        print(f"今日开盘: {result['open']:.2f} 元")
        print(f"换手率: {result['turnover']:.2f}%")
        print(f"成交量: {result['volume']/10000:.2f} 万手")
        print(f"成交额: {result['amount']/100000000:.2f} 亿元")
        print('=' * 60)
        print("资金流向:")
        print(f"  主力净流入: {result['main_inflow']/10000:+.0f} 万元")
        print(f"  超大单流入: {result['super_inflow']/10000:.0f} 万元")
        print(f"  大单净流入: {result['big_inflow']/10000:+.0f} 万元")
        print(f"  主力控盘度: {result['main_control']:.4f}")
        print('=' * 60)
        print("估值指标:")
        print(f"  PE: {result['pe']:.2f}")
        print(f"  PB: {result['pb']:.2f}")
        print('=' * 60)
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
