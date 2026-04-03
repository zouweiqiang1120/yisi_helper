#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票自动监控脚本 - 定时运行版
每30分钟运行一次，记录资金流向变化
"""

import json
import urllib.request
import ssl
from datetime import datetime
import os

ssl._create_default_https_context = ssl._create_unverified_context


def fetch_stock_data(code):
    """获取单只股票数据"""
    secid = f"0.{code}" if code.startswith(('0', '3')) else f"1.{code}"
    
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f59,f60,f170,f171,f103,f104,f105,f106,f108,f162,f167"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data.get('data'):
            d = data['data']
            return {
                'code': code,
                'name': d.get('f58', ''),
                'time': datetime.now().strftime('%H:%M'),
                'price': float(d.get('f43', 0)) / 100,
                'open': float(d.get('f46', 0)) / 100,
                'high': float(d.get('f44', 0)) / 100,
                'low': float(d.get('f45', 0)) / 100,
                'prev_close': float(d.get('f60', 0)) / 100,
                'change_pct': float(d.get('f170', 0)) / 100,
                'volume': float(d.get('f47', 0)),
                'amount': float(d.get('f48', 0)),
                'turnover': float(d.get('f59', 0)) / 100 if d.get('f59') else 0,
                'main_inflow': float(d.get('f103', 0)),
                'super_inflow': float(d.get('f104', 0)),
                'big_inflow': float(d.get('f105', 0)),
                'main_control': float(d.get('f108', 0)),
                'pe': float(d.get('f162', 0)) / 100 if d.get('f162') else 0,
                'pb': float(d.get('f167', 0)) / 100 if d.get('f167') else 0,
            }
    except Exception as e:
        print(f"Error fetching {code}: {e}")
    return None


def analyze_trend(history):
    """分析资金流向趋势"""
    if len(history) < 2:
        return "数据不足"
    
    # 最近3条数据
    recent = history[-3:]
    
    # 计算主力流向趋势
    flows = [h.get('main_inflow', 0) for h in recent]
    avg_flow = sum(flows) / len(flows)
    
    # 判断趋势
    outflow_count = sum(1 for f in flows if f < 0)
    
    if outflow_count >= 2:
        return f"主力连续流出，累计{sum(flows)/10000:+.0f}万"
    elif avg_flow > 10000000:
        return f"主力持续流入，累计{sum(flows)/10000:+.0f}万"
    else:
        return "资金流向平稳"


def auto_monitor():
    """自动监控主函数"""
    
    # 监控的股票列表
    stocks = [
        ('301117', '佳缘科技'),
        ('301136', '招标股份'),
    ]
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_str = datetime.now().strftime('%Y%m%d')
    
    # 日志文件
    log_file = f"auto_monitor_{date_str}.log"
    
    # 读取历史数据
    history_file = "monitor_history.json"
    history = {}
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = {}
    
    # 获取最新数据
    results = []
    for code, name in stocks:
        data = fetch_stock_data(code)
        if data:
            results.append(data)
            
            # 保存到历史
            if code not in history:
                history[code] = []
            history[code].append(data)
            
            # 只保留最近50条
            history[code] = history[code][-50:]
    
    # 保存历史
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    # 写入日志
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*70}\n")
        f.write(f"监控时间: {timestamp}\n")
        f.write(f"{'='*70}\n")
        
        for data in results:
            code = data['code']
            trend = analyze_trend(history.get(code, []))
            
            f.write(f"\n[{data['code']}] {data['name']}\n")
            f.write(f"  时间: {data['time']} | 价格: {data['price']:.2f} | 涨跌: {data['change_pct']:+.2f}%\n")
            f.write(f"  主力: {data['main_inflow']/10000:+.0f}万 | 控盘: {data['main_control']:.3f}\n")
            f.write(f"  趋势: {trend}\n")
            
            # 警报判断
            alerts = []
            if data['main_inflow'] < -50000000:
                alerts.append("主力大幅流出")
            if data['main_control'] < 0.1:
                alerts.append("筹码极度分散")
            if abs(data['change_pct']) > 7:
                alerts.append("价格大幅波动")
            
            if alerts:
                f.write(f"  [ALERT] {'; '.join(alerts)}\n")
        
        f.write(f"\n")
    
    # 输出到控制台
    print(f"\n监控完成: {timestamp}")
    print(f"数据已保存到: {log_file}")
    print(f"历史数据: {history_file}")
    
    return results


if __name__ == "__main__":
    auto_monitor()
