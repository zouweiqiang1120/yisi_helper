#!/usr/bin/env python3
# 招标股份分析

data = {
    'code': '301136',
    'name': '招标股份',
    'price': 16.29,
    'change_pct': 12.0,
    'main_inflow': 83618210.35,
    'super_inflow': 587769915.95,
    'big_inflow': 7182703.45,
    'retail_count': 100.0,
    'main_control': 0.0108,
    'pe': 468.11,
    'pb': 3.07
}

print('=' * 60)
print('招标股份 (301136) 分析')
print('=' * 60)
print(f"当前价格: {data['price']} 元")
print(f"今日涨跌: +{data['change_pct']}%")
print(f"主力净流入: +{data['main_inflow']/10000:.0f} 万元")
print(f"超大单流入: {data['super_inflow']/10000:.0f} 万元")
print(f"大单净流入: +{data['big_inflow']/10000:.0f} 万元")
print(f"主力控盘度: {data['main_control']:.4f}")
print(f"PE: {data['pe']:.1f}")
print(f"PB: {data['pb']:.2f}")
print('=' * 60)
print('分析:')
print('  - 今日大涨 12%，非常强势')
print('  - 主力资金净流入 8361 万，主力在买入')
print('  - 超大单流入 5.88 亿，有机构进场')
print('  - 但控盘度仅 0.01，筹码非常分散')
print('  - PE 468倍，估值极高，纯概念炒作')
print('=' * 60)
print('对比佳缘科技:')
print('  招标股份: 涨+12%，主力流入+8361万')
print('  佳缘科技: 跌-9%，主力流出-7883万')
print('  -> 资金从佳缘流向招标')
print('=' * 60)
