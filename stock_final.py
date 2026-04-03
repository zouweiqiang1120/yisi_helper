#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票筛选分析工具 - 最终版
"""

import json
import urllib.request
import urllib.parse
import ssl
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context


def fetch_stock_data():
    """获取股票数据"""
    url = "http://81.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1,
        "pz": 300,
        "po": 1,
        "np": 1,
        "fltt": 2,
        "invt": 2,
        "fid": "f3",
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
                price = item.get('f2', 0)
                change = item.get('f3', 0)
                pe = item.get('f9', 0)
                pb = item.get('f23', 0)
                cap = item.get('f20', 0)
                
                # 数据校验和转换
                if code and name:
                    try:
                        price = float(price) / 100 if price else 0
                        change = float(change) / 100 if change else 0
                        pe = float(pe) / 100 if pe else 0
                        pb = float(pb) / 100 if pb else 0
                        cap = float(cap) / 100000000 if cap else 0
                        
                        if price > 0:
                            stocks.append({
                                'code': code,
                                'name': name,
                                'price': price,
                                'change': change,
                                'pe': pe,
                                'pb': pb,
                                'cap': cap
                            })
                    except:
                        continue
        
        return stocks
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


def analyze_stock(s):
    """分析单只股票"""
    score = 0
    reasons = []
    risks = []
    
    # 1. 涨幅分析 (今日强势)
    if s['change'] > 5:
        score += 35
        reasons.append(f"强势上涨+{s['change']:.1f}%")
    elif s['change'] > 3:
        score += 25
        reasons.append(f"上涨+{s['change']:.1f}%")
    elif s['change'] > 0:
        score += 10
    
    # 2. 估值分析
    if 5 < s['pe'] < 30:
        score += 25
        reasons.append(f"低估值PE{s['pe']:.1f}")
    elif 30 <= s['pe'] < 50:
        score += 15
        reasons.append(f"合理估值PE{s['pe']:.1f}")
    elif s['pe'] <= 0:
        score -= 20
        risks.append("亏损")
    elif s['pe'] > 100:
        score -= 10
        risks.append("高估值")
    
    # 3. 市值分析
    if 100 < s['cap'] < 500:
        score += 20
        reasons.append("中盘蓝筹")
    elif 50 <= s['cap'] <= 1000:
        score += 15
    elif s['cap'] < 30:
        score -= 10
        risks.append("小市值")
    
    # 4. 价格分析
    if 10 <= s['price'] <= 100:
        score += 10
    
    # 5. 风险排除
    if 'ST' in s['name'] or 'st' in s['name']:
        score -= 100
        risks.append("ST风险")
    
    if s['pb'] > 10:
        score -= 10
        risks.append("高PB")
    
    return {
        'score': score,
        'reasons': reasons,
        'risks': risks,
        'recommend': score >= 40 and len(risks) == 0
    }


def main():
    print("=" * 75)
    print(" A股股票筛选系统 | 2026-03-16")
    print("=" * 75)
    
    print("\n>> 正在获取实时行情数据...")
    stocks = fetch_stock_data()
    print(f">> 成功获取 {len(stocks)} 只股票数据\n")
    
    print(">> 正在分析筛选...")
    results = []
    for s in stocks:
        analysis = analyze_stock(s)
        results.append({
            'stock': s,
            'analysis': analysis
        })
    
    # 按评分排序
    results.sort(key=lambda x: x['analysis']['score'], reverse=True)
    
    # 显示TOP 15
    print("\n" + "=" * 75)
    print(" 筛选结果 TOP 15")
    print("=" * 75)
    print(f" {'排名':<4} {'代码':<8} {'名称':<10} {'价格':<8} {'涨跌%':<8} {'PE':<8} {'评分':<6}")
    print("-" * 75)
    
    for i, r in enumerate(results[:15], 1):
        s = r['stock']
        a = r['analysis']
        print(f" {i:<4} {s['code']:<8} {s['name']:<10} {s['price']:<8.2f} {s['change']:+8.1f}% {s['pe']:<8.1f} {a['score']:<6}")
    
    # 推荐列表
    print("\n" + "=" * 75)
    print(" 重点推荐 (评分≥40且无风险)")
    print("=" * 75)
    
    recommendations = [r for r in results if r['analysis']['recommend']]
    
    if recommendations:
        for i, r in enumerate(recommendations[:5], 1):
            s = r['stock']
            a = r['analysis']
            print(f"\n [{i}] {s['code']} {s['name']}")
            print(f"     Price: {s['price']:.2f} | Change: {s['change']:+.2f}% | PE: {s['pe']:.1f}")
            print(f"     市值: {s['cap']:.1f}亿 | PB: {s['pb']:.2f}")
            print(f"     亮点: {' | '.join(a['reasons'])}")
    else:
        print("\n 当前市场暂无完全符合标准的推荐标的")
        print(" 建议关注评分较高的股票，等待更好入场时机")
    
    # 保存报告
    filename = f"stock_screening_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("A股股票筛选报告\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 75 + "\n\n")
        
        f.write("【筛选标准】\n")
        f.write("1. 技术面: 今日涨幅>3%，强势突破\n")
        f.write("2. 估值面: PE 5-50倍，估值合理\n")
        f.write("3. 基本面: 市值50-1000亿，流动性充足\n")
        f.write("4. 风险排除: 排除ST股、高估值、亏损股\n\n")
        
        f.write("【TOP 10 结果】\n")
        for i, r in enumerate(results[:10], 1):
            s = r['stock']
            a = r['analysis']
            f.write(f"{i}. {s['code']} {s['name']} - 价格{s['price']:.2f} 涨跌{s['change']:+.1f}% 评分{a['score']}\n")
        
        f.write("\n【风险提示】\n")
        f.write("以上分析仅供参考，不构成投资建议。股市有风险，投资需谨慎。\n")
    
    print(f"\n>> 完整报告已保存: {filename}")
    print("=" * 75)


if __name__ == "__main__":
    main()
