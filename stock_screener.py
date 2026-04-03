#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票筛选分析工具 - 基础版
使用标准库实现，无需第三方依赖
"""

import csv
import json
import urllib.request
import urllib.parse
import ssl
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import os

# 禁用SSL验证（部分数据源需要）
ssl._create_default_https_context = ssl._create_unverified_context


@dataclass
class Stock:
    """股票数据类"""
    code: str
    name: str
    industry: str
    price: float
    change_pct: float  # 涨跌幅
    volume: float
    pe_ratio: float = 0  # 市盈率
    pb_ratio: float = 0  # 市净率
    market_cap: float = 0  # 市值(亿)
    
    # 技术指标
    ma5: float = 0
    ma10: float = 0
    ma20: float = 0
    ma60: float = 0
    
    @property
    def is_bullish_arrangement(self) -> bool:
        """判断是否多头排列：MA5 > MA10 > MA20 > MA60"""
        return self.ma5 > self.ma10 > self.ma20 > ma60 > 0
    
    @property
    def is_breakout(self) -> bool:
        """判断是否突破：价格创近期新高"""
        # 简化判断：价格高于MA20且涨幅较大
        return self.price > self.ma20 and self.change_pct > 3


class StockScreener:
    """股票筛选器"""
    
    def __init__(self):
        self.stocks: List[Stock] = []
        self.hot_sectors = [
            "人工智能", "机器人", "芯片", "新能源", "储能",
            "生物医药", "军工", "数字经济", "云计算", "大数据"
        ]
    
    def fetch_stock_list(self) -> List[Dict]:
        """
        获取股票列表
        使用东方财富免费API
        """
        try:
            # 东方财富A股列表API
            url = "http://81.push2.eastmoney.com/api/qt/clist/get"
            params = {
                "pn": 1,
                "pz": 100,  # 先取前100只
                "po": 1,
                "np": 1,
                "fltt": 2,
                "invt": 2,
                "fid": "f20",
                "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23",
                "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f20,f21,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100"
            }
            
            full_url = f"{url}?{urllib.parse.urlencode(params)}"
            
            req = urllib.request.Request(
                full_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            if data.get('data') and data['data'].get('diff'):
                return data['data']['diff']
            return []
            
        except Exception as e:
            print(f"获取数据失败: {e}")
            return []
    
    def parse_stock_data(self, raw_data: List[Dict]) -> List[Stock]:
        """解析原始数据为Stock对象"""
        stocks = []
        
        for item in raw_data:
            try:
                # 字段映射（东方财富字段编码）
                code = item.get('f12', '')  # 股票代码
                name = item.get('f14', '')  # 股票名称
                price = float(item.get('f2', 0)) / 100 if item.get('f2') else 0  # 最新价
                change_pct = float(item.get('f3', 0)) / 100 if item.get('f3') else 0  # 涨跌幅
                volume = float(item.get('f5', 0)) / 10000 if item.get('f5') else 0  # 成交量(万手)
                pe_ratio = float(item.get('f9', 0)) / 100 if item.get('f9') else 0  # 市盈率
                pb_ratio = float(item.get('f23', 0)) / 100 if item.get('f23') else 0  # 市净率
                market_cap = float(item.get('f20', 0)) / 100000000 if item.get('f20') else 0  # 总市值
                
                stock = Stock(
                    code=code,
                    name=name,
                    industry="",  # 需要另外获取
                    price=price,
                    change_pct=change_pct,
                    volume=volume,
                    pe_ratio=pe_ratio,
                    pb_ratio=pb_ratio,
                    market_cap=market_cap
                )
                stocks.append(stock)
                
            except (ValueError, TypeError) as e:
                continue
        
        return stocks
    
    def filter_by_performance(self, stocks: List[Stock]) -> List[Stock]:
        """
        条件②：筛选业绩增长或估值合理的股票
        - PE < 50（估值合理）
        - 或近期涨幅 > 5%（业绩驱动）
        """
        result = []
        for stock in stocks:
            # 估值合理：PE在5-50之间，PB < 8
            reasonable_valuation = 5 < stock.pe_ratio < 50 and stock.pb_ratio < 8
            # 业绩驱动：今日涨幅较大
            strong_performance = stock.change_pct > 5
            
            if reasonable_valuation or strong_performance:
                result.append(stock)
        return result
    
    def filter_by_technical(self, stocks: List[Stock]) -> List[Stock]:
        """
        条件③④：筛选多头排列、突破走势
        - 涨幅 > 3%
        - 价格创近期新高（简化判断）
        """
        result = []
        for stock in stocks:
            # 强势突破特征
            strong_momentum = stock.change_pct > 3
            high_volume = stock.volume > 10  # 成交量大于10万手
            
            if strong_momentum and high_volume:
                result.append(stock)
        return result
    
    def risk_assessment(self, stock: Stock) -> Dict:
        """
        条件⑤：风险评估
        返回风险评分和警告信息
        """
        risks = []
        score = 100  # 满分100
        
        # 估值风险
        if stock.pe_ratio > 100:
            risks.append("PE过高，估值泡沫风险")
            score -= 20
        elif stock.pe_ratio < 0:
            risks.append("亏损股，业绩风险")
            score -= 30
        
        if stock.pb_ratio > 10:
            risks.append("PB过高，估值偏高")
            score -= 15
        
        # 流动性风险
        if stock.market_cap < 50:
            risks.append("小市值股票，流动性风险")
            score -= 10
        
        # 波动风险
        if abs(stock.change_pct) > 10:
            risks.append("波动剧烈，注意追高风险")
            score -= 10
        
        return {
            "score": max(score, 0),
            "risks": risks,
            "is_safe": score >= 70
        }
    
    def screen_stocks(self) -> List[Dict]:
        """
        主筛选流程
        """
        print("=" * 60)
        print("股票筛选系统启动")
        print("=" * 60)
        
        # 步骤1：获取数据
        print("\n[1/4] 正在获取股票数据...")
        raw_data = self.fetch_stock_list()
        if not raw_data:
            print("获取数据失败，请检查网络连接")
            return []
        
        self.stocks = self.parse_stock_data(raw_data)
        print(f"获取到 {len(self.stocks)} 只股票数据")
        
        # 步骤2：估值和业绩筛选
        print("\n[2/4] 筛选估值合理/业绩增长的股票...")
        step2 = self.filter_by_performance(self.stocks)
        print(f"符合条件②的股票: {len(step2)} 只")
        
        # 步骤3：技术面筛选
        print("\n[3/4] 筛选多头排列/突破走势的股票...")
        step3 = self.filter_by_technical(step2)
        print(f"符合条件③④的股票: {len(step3)} 只")
        
        # 步骤4：风险评估
        print("\n[4/4] 进行风险评估...")
        results = []
        for stock in step3[:20]:  # 只评估前20只
            risk = self.risk_assessment(stock)
            results.append({
                "stock": stock,
                "risk": risk
            })
        
        # 按风险评分排序
        results.sort(key=lambda x: x["risk"]["score"], reverse=True)
        
        return results
    
    def print_results(self, results: List[Dict]):
        """打印筛选结果"""
        print("\n" + "=" * 80)
        print("筛选结果 TOP 10")
        print("=" * 80)
        print(f"{'排名':<4} {'代码':<8} {'名称':<10} {'价格':<8} {'涨幅%':<8} {'PE':<8} {'风险分':<8} {'风险提示'}")
        print("-" * 80)
        
        for i, item in enumerate(results[:10], 1):
            s = item["stock"]
            r = item["risk"]
            risk_text = ";".join(r["risks"]) if r["risks"] else "低风险"
            print(f"{i:<4} {s.code:<8} {s.name:<10} {s.price:<8.2f} {s.change_pct:<8.2f} {s.pe_ratio:<8.1f} {r['score']:<8} {risk_text[:20]}")
        
        print("\n" + "=" * 80)
        print("推荐关注（风险评分≥70）:")
        safe_stocks = [r for r in results if r["risk"]["is_safe"]]
        if safe_stocks:
            for item in safe_stocks[:3]:
                s = item["stock"]
                print(f"  • {s.code} {s.name} - 涨幅{s.change_pct:.2f}% PE{s.pe_ratio:.1f}")
        else:
            print("  当前没有符合条件的低风险股票")
        print("=" * 80)


def main():
    """主程序"""
    screener = StockScreener()
    results = screener.screen_stocks()
    
    if results:
        screener.print_results(results)
        
        # 保存结果到文件
        output_file = f"stock_screening_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"股票筛选报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 80 + "\n")
            for i, item in enumerate(results[:10], 1):
                s = item["stock"]
                r = item["risk"]
                f.write(f"{i}. {s.code} {s.name} - 价格{s.price:.2f} 涨幅{s.change_pct:.2f}% 风险分{r['score']}\n")
        print(f"\n结果已保存到: {output_file}")
    else:
        print("筛选失败，未能获取数据")


if __name__ == "__main__":
    main()
