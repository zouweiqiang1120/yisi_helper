#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Browser Plus - 增强版浏览器工具
专为股票监控设计的功能
"""

import urllib.request
import urllib.parse
import ssl
import json
from datetime import datetime
import os

ssl._create_default_https_context = ssl._create_unverified_context


class AgentBrowserPlus:
    """增强版 Agent 浏览器"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_stock_realtime(self, code):
        """获取股票实时数据（使用东方财富API）"""
        secid = f"0.{code}" if code.startswith(('0', '3')) else f"1.{code}"
        url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f59,f60,f170,f171,f103,f104,f105,f106,f108,f162,f167"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if data.get('data'):
                d = data['data']
                return {
                    'success': True,
                    'code': code,
                    'name': d.get('f58', ''),
                    'price': float(d.get('f43', 0)) / 100,
                    'open': float(d.get('f46', 0)) / 100,
                    'high': float(d.get('f44', 0)) / 100,
                    'low': float(d.get('f45', 0)) / 100,
                    'prev_close': float(d.get('f60', 0)) / 100,
                    'change_pct': float(d.get('f170', 0)) / 100,
                    'change_amount': float(d.get('f171', 0)) / 100,
                    'volume': float(d.get('f47', 0)),
                    'amount': float(d.get('f48', 0)),
                    'turnover': float(d.get('f59', 0)) / 100 if d.get('f59') else 0,
                    'main_inflow': float(d.get('f103', 0)),
                    'super_inflow': float(d.get('f104', 0)),
                    'big_inflow': float(d.get('f105', 0)),
                    'main_control': float(d.get('f108', 0)),
                    'pe': float(d.get('f162', 0)) / 100 if d.get('f162') else 0,
                    'pb': float(d.get('f167', 0)) / 100 if d.get('f167') else 0,
                    'time': datetime.now().strftime('%H:%M:%S')
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_stock_kline(self, code, period='day', count=30):
        """获取股票K线数据"""
        secid = f"0.{code}" if code.startswith(('0', '3')) else f"1.{code}"
        
        # 1=分时, 5=5分钟, 15=15分钟, 30=30分钟, 60=60分钟, 101=日, 102=周, 103=月
        period_map = {'1min': 1, '5min': 5, '15min': 15, '30min': 30, '60min': 60, 'day': 101, 'week': 102, 'month': 103}
        klt = period_map.get(period, 101)
        
        url = f"http://push2.eastmoney.com/api/qt/stock/kline/get?secid={secid}&fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt={klt}&fqt=0&end=20500101&lmt={count}"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if data.get('data') and data['data'].get('klines'):
                klines = []
                for line in data['data']['klines']:
                    parts = line.split(',')
                    if len(parts) >= 6:
                        klines.append({
                            'date': parts[0],
                            'open': float(parts[1]),
                            'close': float(parts[2]),
                            'high': float(parts[3]),
                            'low': float(parts[4]),
                            'volume': float(parts[5])
                        })
                return {'success': True, 'code': code, 'klines': klines}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        return {'success': False, 'error': 'No data'}
    
    def get_stock_news(self, code, num=5):
        """获取股票相关新闻"""
        url = f"http://searchapi.eastmoney.com/api/suggest/get?input={code}&type=14&count={num}"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if data.get('QuotationCodeTable') and data['QuotationCodeTable'].get('Data'):
                items = data['QuotationCodeTable']['Data']
                return {'success': True, 'code': code, 'news': items}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        
        return {'success': False, 'error': 'No news'}
    
    def get_market_overview(self):
        """获取市场概况"""
        # 上证指数、深证成指、创业板指
        indices = ['000001', '399001', '399006']
        results = {}
        
        for code in indices:
            data = self.get_stock_realtime(code)
            if data['success']:
                results[code] = data
        
        return results
    
    def monitor_stocks(self, stock_list):
        """监控多只股票"""
        print(f"\n{'='*70}")
        print(f" 股票实时监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        print(f" {'代码':<8} {'名称':<10} {'价格':<8} {'涨跌%':<8} {'主力(万)':<10} {'状态'}")
        print(f"{'-'*70}")
        
        results = []
        for code in stock_list:
            data = self.get_stock_realtime(code)
            if data['success']:
                status = "DOWN" if data['change_pct'] < -5 else "UP" if data['change_pct'] > 5 else "-"
                print(f" {data['code']:<8} {data['name']:<10} {data['price']:<8.2f} {data['change_pct']:<+8.2f} {data['main_inflow']/10000:<+10.0f} {status}")
                results.append(data)
            else:
                print(f" {code:<8} {'获取失败':<10}")
        
        print(f"{'='*70}")
        return results


def main():
    """主程序"""
    print("=" * 70)
    print(" Agent Browser Plus - 增强版浏览器工具")
    print("=" * 70)
    
    browser = AgentBrowserPlus()
    
    # 1. 市场概况
    print("\n[1] 市场概况")
    market = browser.get_market_overview()
    for code, data in market.items():
        print(f"  {data['name']}: {data['price']:.2f} ({data['change_pct']:+.2f}%)")
    
    # 2. 监控股票
    print("\n[2] 股票监控")
    browser.monitor_stocks(['301117', '301136', '000001'])
    
    # 3. 获取K线数据
    print("\n[3] K线数据（最近5天）")
    kline = browser.get_stock_kline('301117', period='day', count=5)
    if kline['success']:
        for k in kline['klines']:
            print(f"  {k['date']}: 开{k['open']:.2f} 收{k['close']:.2f} 高{k['high']:.2f} 低{k['low']:.2f}")
    
    print("\n" + "=" * 70)
    print("功能:")
    print("  - 实时行情获取")
    print("  - K线历史数据")
    print("  - 多股同时监控")
    print("  - 市场概况")
    print("=" * 70)


if __name__ == "__main__":
    main()
