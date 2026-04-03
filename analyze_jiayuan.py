#!/usr/bin/env python3
# 佳缘科技 301117 分析

data = {
    'price': 47.56,
    'high': 52.48,
    'low': 47.29,
    'open': 52.45,
    'volume': 70519.28,
    'amount': 347108959.91,
    'change_pct': -9.32,
    'pb': 4.71,
}

print('=' * 60)
print('佳缘科技 (301117) 分析')
print('=' * 60)
print(f'当前价格: {data["price"]} 元')
print(f'今日涨跌: {data["change_pct"]}%')
print(f'今日开盘: {data["open"]} 元')
print(f'今日最高: {data["high"]} 元')
print(f'今日最低: {data["low"]} 元')
print(f'市净率PB: {data["pb"]}')
print(f'成交量: {data["volume"]/10000:.2f} 万手')
print(f'成交额: {data["amount"]/100000000:.2f} 亿元')
print('=' * 60)
print('技术面分析:')
print(f'  - 今日大跌 {abs(data["change_pct"])}%，从开盘52.45跌至47.56')
print('  - 接近跌停，短期走势极弱')
print('  - 成交量放大，抛压沉重')
print('=' * 60)
print('基本面风险:')
print('  - 市盈率负值: 公司处于亏损状态')
print('  - PB 4.71: 估值偏高')
print('  - 小市值创业板，波动大')
print('=' * 60)
print('综合评估: HIGH RISK')
print('  ⚠️ 亏损股，今日大跌，不建议介入')
print('=' * 60)
