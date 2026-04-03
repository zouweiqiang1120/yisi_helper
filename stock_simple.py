#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票筛选分析工具 - 简化版
使用标准库实现，无需第三方依赖
"""

import json
import urllib.request
import urllib.parse
import ssl
from datetime import datetime

# 禁用SSL验证
ssl._create_default_https_context = ssl._create_unverified_context


def fetch_stock_data():
    """从东方财富获取股票数据"""
    url = "http://81.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1,
        "pz": 200,
        "po": 1,
        "np": 1,
        "fltt": 2,
        "invt": 2,
        "fid": "f20",
        "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23",
        "fields": "f2,f3,f9,f12,f14,f20,f23"
    }
    
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(
            full_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        stocks = []
        if data.get('data') and data['data'].get('diff'):
            for item in data['data']['diff']:
                code = item.get('f12', '')
                name = item.get('f14', '')
                price = float(item.get('f2', 0)) / 100 if item.get('f2') else 0
                change = float(item.get('f3', 0)) / 100 if item.get('f3') else 0
                pe = float(item.get('f9', 0)) / 100 if item.get('f9') else 0
                pb = float(item.get('f23', 0)) / 100 if item.get('f23') else 0
                cap = float(item.get('f20', 0)) / 100000000 if item.get('f20') else 0
                
                if code and name and price > 0:
                    stocks.append({
                        'code': code,
                        'name': name,
                        'price': price,
                        'change': change,
                        'pe': pe,
                        'pb': pb,
                        'cap': cap
                    })
        
        return stocks
    except Exception as e:
        print(f"Error: {e}")
        return []


def screen_stocks(stocks):
    """筛选股票"""
    results = []
    
    for s in stocks:
        score = 0
        reasons = []
        risks = []
        
        # 涨幅强势 (今日涨幅 > 3%)
        if s['change'] > 3:
            score += 30
            reasons.append(f"强势上涨 {s['change']:.1f}%")
        
        # 估值合理 (PE 5-50)
        if 5 < s['pe'] < 50:
            score += 25
            reasons.append(f"估值合理 PE{s['pe']:.1f}")
        elif s['pe'] <= 0:
            risks.append("亏损股")
        elif s['pe'] > 100:
            risks.append("估值偏高")
        
        # 市值适中 (50亿-1000亿)
        if 50 < s['cap'] < 1000:
            score += 20
            reasons.append("市值适中")
        elif s['cap'] < 50:
            risks.append("小市值")
        
        # 价格适中 (10-200元)
        if 10 < s['price'] < 200:
            score += 15
        
        # 排除ST股
        if 'ST' in s['name']:
            score -= 50
            risks.append("ST股")
        
        if score >= 30:
            results.append({
                'stock': s,
                'score': score,
                'reasons': reasons,
                'risks': risks
            })
    
    # 按评分排序
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def main():
    print("=" * 70)
    print("Stock Screener - 2026-03-16")
    print("=" * 70)
    
    print("\n[Step 1] Fetching stock data...")
    stocks = fetch_stock_data()
    print(f"Got {len(stocks)} stocks")
    
    print("\n[Step 2] Screening...")
    results = screen_stocks(stocks)
    print(f"Found {len(results)} candidates")
    
    print("\n" + "=" * 70)
    print("TOP 10 RESULTS")
    print("=" * 70)
    print(f"{'Rank':<5} {'Code':<8} {'Name':<12} {'Price':<8} {'Change':<8} {'PE':<8} {'Score':<6}")
    print("-" * 70)
    
    for i, r in enumerate(results[:10], 1):
        s = r['stock']
        print(f"{i:<5} {s['code']:<8} {s['name']:<12} {s['price']:<8.2f} {s['change']:<+8.1f}% {s['pe']:<8.1f} {r['score']:<6}")
    
    print("\n" + "=" * 70)
    print("TOP 3 RECOMMENDATIONS:")
    print("=" * 70)
    
    for i, r in enumerate(results[:3], 1):
        s = r['stock']
        print(f"\n{i}. {s['code']} {s['name']}")
        print(f"   Price: {s['price']:.2f}  Change: {s['change']:+.2f}%")
        print(f"   PE: {s['pe']:.1f}  Market Cap: {s['cap']:.1f}亿")
        print(f"   Score: {r['score']} points")
        print(f"   Reasons: {', '.join(r['reasons'])}")
        if r['risks']:
            print(f"   Risks: {', '.join(r['risks'])}")
    
    # Save to file
    filename = f"stock_report_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Stock Screening Report - 2026-03-16\n")
        f.write("=" * 70 + "\n\n")
        for i, r in enumerate(results[:10], 1):
            s = r['stock']
            f.write(f"{i}. {s['code']} {s['name']} - {s['change']:+.2f}% - Score: {r['score']}\n")
    
    print(f"\nReport saved to: {filename}")


if __name__ == "__main__":
    main()
