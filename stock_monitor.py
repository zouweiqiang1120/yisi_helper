#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票资金流向监控系统
监控个股主力资金流向，发现异常及时提醒
"""

import json
import urllib.request
import urllib.parse
import ssl
from datetime import datetime, timedelta
import os

ssl._create_default_https_context = ssl._create_unverified_context


class StockMonitor:
    """股票监控类"""
    
    def __init__(self, code, name=""):
        self.code = code
        self.name = name
        self.data_file = f"monitor_{code}.json"
        self.history = self.load_history()
    
    def load_history(self):
        """加载历史数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """保存历史数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.history[-100:], f, ensure_ascii=False, indent=2)  # 只保留最近100条
    
    def fetch_data(self):
        """获取实时数据"""
        # 判断是沪市还是深市
        secid = f"0.{self.code}" if self.code.startswith('3') or self.code.startswith('0') else f"1.{self.code}"
        
        url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f100,f101,f102,f103,f104,f105,f106,f107,f108,f109,f162,f163,f164,f165,f166,f167,f168,f169,f170"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if data.get('data'):
                d = data['data']
                return {
                    'code': self.code,
                    'name': d.get('f58', self.name),
                    'price': float(d.get('f43', 0)),
                    'open': float(d.get('f46', 0)),
                    'high': float(d.get('f44', 0)),
                    'low': float(d.get('f45', 0)),
                    'change_pct': float(d.get('f170', 0)),
                    'volume': float(d.get('f47', 0)),
                    'amount': float(d.get('f48', 0)),
                    'main_inflow': float(d.get('f103', 0)),  # 主力净流入
                    'super_inflow': float(d.get('f104', 0)),  # 超大单流入
                    'big_inflow': float(d.get('f105', 0)),  # 大单净流入
                    'retail_count': float(d.get('f106', 0)),  # 散户数量
                    'main_control': float(d.get('f108', 0)),  # 主力控盘度
                    'pe': float(d.get('f162', 0)),
                    'pb': float(d.get('f167', 0)),
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            return None
        except Exception as e:
            print(f"获取数据失败: {e}")
            return None
    
    def analyze(self, data):
        """分析数据，生成警报"""
        alerts = []
        
        # 1. 价格异动警报
        if abs(data['change_pct']) > 7:
            alerts.append(f"【价格异动】涨跌幅 {data['change_pct']:+.2f}%，大幅波动！")
        
        # 2. 主力资金警报
        if data['main_inflow'] < -50000000:  # 主力流出超5000万
            alerts.append(f"【主力出逃】主力资金净流出 {abs(data['main_inflow'])/10000:.0f} 万！")
        elif data['main_inflow'] > 50000000:  # 主力流入超5000万
            alerts.append(f"【主力进场】主力资金净流入 {data['main_inflow']/10000:.0f} 万！")
        
        # 3. 控盘度警报
        if data['main_control'] < 0.2:
            alerts.append(f"【筹码分散】主力控盘度仅 {data['main_control']:.2f}，无主力控盘")
        elif data['main_control'] > 0.6:
            alerts.append(f"【高度控盘】主力控盘度 {data['main_control']:.2f}，高度集中")
        
        # 4. 散户数量警报
        if len(self.history) > 0:
            last_retail = self.history[-1].get('retail_count', 0)
            if data['retail_count'] > last_retail * 1.1:  # 散户增加10%
                alerts.append(f"【散户增加】散户数量上升，筹码流向散户")
        
        # 5. 连续流出警报
        if len(self.history) >= 3:
            recent = self.history[-3:]
            outflow_count = sum(1 for h in recent if h.get('main_inflow', 0) < 0)
            if outflow_count >= 3:
                total_out = sum(h.get('main_inflow', 0) for h in recent)
                alerts.append(f"【连续流出】连续3次主力净流出，累计 {abs(total_out)/10000:.0f} 万")
        
        return alerts
    
    def run(self):
        """运行监控"""
        print("=" * 70)
        print(f"股票资金流向监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        data = self.fetch_data()
        if not data:
            print("获取数据失败")
            return
        
        # 保存数据
        self.history.append(data)
        self.save_history()
        
        # 显示基本信息
        print(f"\n股票: {data['code']} {data['name']}")
        print(f"时间: {data['time']}")
        print(f"价格: {data['price']:.2f} 元")
        print(f"涨跌: {data['change_pct']:+.2f}%")
        print("-" * 70)
        
        # 显示资金流向
        print("资金流向:")
        print(f"  主力净流入: {data['main_inflow']/10000:+.0f} 万元")
        print(f"  超大单流入: {data['super_inflow']/10000:.0f} 万元")
        print(f"  大单净流入: {data['big_inflow']/10000:+.0f} 万元")
        print(f"  主力控盘度: {data['main_control']:.2f}")
        print(f"  散户数量: {data['retail_count']:.0f}")
        print("-" * 70)
        
        # 分析并显示警报
        alerts = self.analyze(data)
        if alerts:
            print("[!] 警报:")
            for alert in alerts:
                print(f"  {alert}")
        else:
            print("[OK] 暂无异常")
        
        print("=" * 70)
        
        # 保存监控日志
        log_file = f"monitor_{self.code}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{data['time']} | 价格:{data['price']:.2f} | 涨跌:{data['change_pct']:+.2f}% | 主力:{data['main_inflow']/10000:+.0f}万\n")
            if alerts:
                for alert in alerts:
                    f.write(f"  ALERT: {alert}\n")
        
        return data, alerts


def monitor_multiple(stocks):
    """监控多只股票"""
    print("\n" + "=" * 70)
    print("批量股票监控")
    print("=" * 70)
    
    results = []
    for code, name in stocks:
        monitor = StockMonitor(code, name)
        try:
            data, alerts = monitor.run()
            results.append({
                'code': code,
                'name': name,
                'data': data,
                'alerts': alerts
            })
            print()  # 空行分隔
        except Exception as e:
            print(f"监控 {code} 失败: {e}\n")
    
    # 汇总警报
    all_alerts = [(r['code'], r['name'], r['alerts']) for r in results if r['alerts']]
    if all_alerts:
        print("=" * 70)
        print("【警报汇总】")
        print("=" * 70)
        for code, name, alerts in all_alerts:
            print(f"\n{code} {name}:")
            for alert in alerts:
                print(f"  - {alert}")
    
    return results


def main():
    """主程序"""
    import sys
    
    # 默认监控佳缘科技
    default_stocks = [
        ('301117', '佳缘科技'),
    ]
    
    # 可以添加更多股票
    my_stocks = [
        ('301117', '佳缘科技'),  # 你的套牢股
        # ('000001', '平安银行'),  # 示例：添加其他股票
        # ('600519', '贵州茅台'),  # 示例：添加其他股票
    ]
    
    print("股票资金流向监控系统")
    print("=" * 70)
    print("1. 监控单只股票 (佳缘科技)")
    print("2. 监控多只股票")
    print("=" * 70)
    
    # 运行监控
    if len(my_stocks) == 1:
        monitor = StockMonitor(my_stocks[0][0], my_stocks[0][1])
        monitor.run()
    else:
        monitor_multiple(my_stocks)
    
    print("\n提示:")
    print("- 数据已保存，可以对比历史资金流向")
    print("- 建议每天收盘后运行一次")
    print("- 可以添加到Windows计划任务定时执行")


if __name__ == "__main__":
    main()
