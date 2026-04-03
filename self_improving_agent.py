#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自我改进 Agent
自动执行股票监控、分析、报告生成任务
根据历史数据优化策略
"""

import json
import os
from datetime import datetime, timedelta
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class SelfImprovingAgent:
    """自我改进 Agent"""
    
    def __init__(self, name="StockAgent"):
        self.name = name
        self.memory_file = f"{name}_memory.json"
        self.config_file = f"{name}_config.json"
        self.log_file = f"{name}_log.txt"
        
        self.memory = self.load_memory()
        self.config = self.load_config()
        
        # 初始化默认配置
        if not self.config:
            self.config = {
                'version': 1.0,
                'created_at': datetime.now().isoformat(),
                'strategies': {
                    'alert_threshold': -50000000,  # 主力流出超5000万报警
                    'monitor_interval': 30,  # 监控间隔30分钟
                    'max_history_days': 30,  # 保留30天历史
                },
                'improvements': []
            }
    
    def load_memory(self):
        """加载记忆"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            'interactions': [],
            'stock_alerts': [],
            'performance': []
        }
    
    def save_memory(self):
        """保存记忆"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def load_config(self):
        """加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        print(log_entry.strip())
    
    def fetch_stock_data(self, code):
        """获取股票数据"""
        secid = f"0.{code}" if code.startswith(('0', '3')) else f"1.{code}"
        url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f57,f58,f60,f170,f103,f108"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if data.get('data'):
                d = data['data']
                return {
                    'code': code,
                    'name': d.get('f58', ''),
                    'price': float(d.get('f43', 0)) / 100,
                    'prev_close': float(d.get('f60', 0)) / 100,
                    'change_pct': float(d.get('f170', 0)) / 100,
                    'main_inflow': float(d.get('f103', 0)),
                    'main_control': float(d.get('f108', 0)),
                    'time': datetime.now().isoformat()
                }
        except Exception as e:
            self.log(f"获取 {code} 数据失败: {e}")
        return None
    
    def analyze_stock(self, data):
        """分析股票"""
        if not data:
            return None
        
        alerts = []
        score = 50  # 基础分
        
        # 1. 价格异动
        if abs(data['change_pct']) > 7:
            alerts.append(f"价格大幅波动: {data['change_pct']:+.2f}%")
            score -= 20
        
        # 2. 资金流向
        threshold = self.config['strategies']['alert_threshold']
        if data['main_inflow'] < threshold:
            alerts.append(f"主力大幅流出: {data['main_inflow']/10000:.0f}万")
            score -= 30
        elif data['main_inflow'] > abs(threshold):
            alerts.append(f"主力大幅流入: {data['main_inflow']/10000:.0f}万")
            score += 20
        
        # 3. 控盘度
        if data['main_control'] < 0.2:
            alerts.append(f"筹码分散，控盘度: {data['main_control']:.3f}")
            score -= 10
        elif data['main_control'] > 0.5:
            alerts.append(f"高度控盘: {data['main_control']:.3f}")
            score += 10
        
        # 保存到记忆
        self.memory['stock_alerts'].append({
            'time': data['time'],
            'code': data['code'],
            'alerts': alerts,
            'score': score
        })
        
        return {
            'data': data,
            'alerts': alerts,
            'score': score,
            'recommendation': '卖出' if score < 30 else '观望' if score < 60 else '关注'
        }
    
    def learn_from_history(self):
        """从历史数据学习，优化策略"""
        self.log("开始自我改进分析...")
        
        if len(self.memory['stock_alerts']) < 10:
            self.log("历史数据不足，跳过优化")
            return
        
        # 分析历史警报效果
        recent_alerts = self.memory['stock_alerts'][-20:]
        
        # 统计警报类型
        alert_types = {}
        for alert in recent_alerts:
            for a in alert.get('alerts', []):
                alert_type = a.split(':')[0] if ':' in a else a
                alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
        
        # 根据统计优化阈值
        improvements = []
        
        # 如果主力流出警报太频繁，提高阈值
        outflow_alerts = alert_types.get('主力大幅流出', 0)
        if outflow_alerts > 10:
            old_threshold = self.config['strategies']['alert_threshold']
            new_threshold = old_threshold * 1.2  # 提高20%
            self.config['strategies']['alert_threshold'] = new_threshold
            improvements.append(f"主力流出阈值调整: {old_threshold/10000:.0f}万 -> {new_threshold/10000:.0f}万")
        
        # 记录改进
        if improvements:
            self.config['improvements'].append({
                'time': datetime.now().isoformat(),
                'changes': improvements
            })
            self.log(f"策略优化完成: {', '.join(improvements)}")
        else:
            self.log("当前策略无需优化")
        
        self.save_config()
    
    def generate_report(self, analysis_results):
        """生成分析报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"agent_report_{timestamp}.html"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Agent分析报告</title>
    <style>
        body {{ font-family: Microsoft YaHei; margin: 40px; }}
        h1 {{ color: #333; }}
        .stock {{ border: 1px solid #ddd; margin: 20px 0; padding: 15px; border-radius: 5px; }}
        .alert {{ color: #d9534f; }}
        .score {{ font-size: 24px; font-weight: bold; }}
        .recommendation {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .sell {{ background: #f2dede; color: #a94442; }}
        .hold {{ background: #fcf8e3; color: #8a6d3b; }}
        .buy {{ background: #dff0d8; color: #3c763d; }}
    </style>
</head>
<body>
    <h1>Agent 股票分析报告</h1>
    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>Agent版本: {self.config['version']}</p>
    
    <h2>分析结果</h2>
"""
        
        for result in analysis_results:
            if result:
                data = result['data']
                rec_class = 'sell' if result['score'] < 30 else 'hold' if result['score'] < 60 else 'buy'
                
                html += f"""
    <div class="stock">
        <h3>{data['name']} ({data['code']})</h3>
        <p>价格: {data['price']:.2f} | 涨跌: {data['change_pct']:+.2f}%</p>
        <p>主力: {data['main_inflow']/10000:+.0f}万 | 控盘: {data['main_control']:.3f}</p>
        <p class="score">评分: {result['score']}</p>
        <div class="recommendation {rec_class}">建议: {result['recommendation']}</div>
        <ul>
"""
                for alert in result['alerts']:
                    html += f"            <li class='alert'>{alert}</li>\n"
                
                html += "        </ul>\n    </div>\n"
        
        html += """
</body>
</html>
"""
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        self.log(f"报告已生成: {report_file}")
        return report_file
    
    def run(self, stock_codes=None):
        """运行 Agent"""
        self.log(f"=== {self.name} 开始运行 ===")
        
        if not stock_codes:
            stock_codes = ['301117', '301136']  # 默认监控股票
        
        # 1. 获取数据
        self.log(f"正在监控 {len(stock_codes)} 只股票...")
        analysis_results = []
        
        for code in stock_codes:
            data = self.fetch_stock_data(code)
            if data:
                result = self.analyze_stock(data)
                if result:
                    analysis_results.append(result)
                    self.log(f"{data['name']}: 评分{result['score']}, 建议{result['recommendation']}")
        
        # 2. 生成报告
        if analysis_results:
            report_file = self.generate_report(analysis_results)
        
        # 3. 自我改进
        self.learn_from_history()
        
        # 4. 保存记忆
        self.save_memory()
        
        self.log(f"=== {self.name} 运行完成 ===")
        
        return analysis_results


def main():
    """主程序"""
    print("=" * 70)
    print(" 自我改进 Agent")
    print("=" * 70)
    
    # 创建 Agent
    agent = SelfImprovingAgent(name="StockMonitorAgent")
    
    # 运行
    results = agent.run(['301117', '301136'])
    
    print("\n" + "=" * 70)
    print("Agent 功能:")
    print("  - 自动获取股票数据")
    print("  - 智能分析资金流向")
    print("  - 自动生成报告")
    print("  - 自我学习优化策略")
    print("=" * 70)


if __name__ == "__main__":
    main()
