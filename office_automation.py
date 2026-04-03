#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
办公文档自动化工具
支持: Word文档生成、Excel报表、PDF处理
无需安装Microsoft Office，纯Python实现
"""

import os
import json
from datetime import datetime


class DocumentGenerator:
    """文档生成器基类"""
    
    def __init__(self, output_dir="documents"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)


class WordGenerator(DocumentGenerator):
    """Word文档生成器（使用HTML格式）"""
    
    def create_document(self, title, content, filename=None):
        """创建Word文档（HTML格式）"""
        if not filename:
            filename = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: "Microsoft YaHei", SimSun, serif; line-height: 1.6; margin: 40px; }}
        h1 {{ color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        p {{ text-align: justify; margin: 10px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #007acc; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .footer {{ text-align: center; margin-top: 50px; font-size: 12px; color: #666; }}
        .highlight {{ background-color: #fff3cd; padding: 2px 5px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    {content}
    
    <div class="footer">
        <p>本报告由办公文档自动化工具生成</p>
    </div>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Word文档已生成: {filepath}")
        print("提示: 可用Word或浏览器打开此HTML文件")
        return filepath
    
    def create_stock_report(self, stock_data, filename=None):
        """创建股票分析报告"""
        title = f"{stock_data.get('name', '股票')}分析报告"
        
        content = f"""
        <h2>一、基本信息</h2>
        <table>
            <tr><th>项目</th><th>数值</th></tr>
            <tr><td>股票代码</td><td>{stock_data.get('code', '-')}</td></tr>
            <tr><td>股票名称</td><td>{stock_data.get('name', '-')}</td></tr>
            <tr><td>当前价格</td><td>{stock_data.get('price', '-')} 元</td></tr>
            <tr><td>涨跌幅</td><td class="{'highlight' if stock_data.get('change_pct', 0) < 0 else ''}">{stock_data.get('change_pct', '-'):.2f}%</td></tr>
            <tr><td>主力净流入</td><td>{stock_data.get('main_inflow', 0)/10000:+.0f} 万元</td></tr>
            <tr><td>主力控盘度</td><td>{stock_data.get('main_control', '-'):.3f}</td></tr>
        </table>
        
        <h2>二、资金流向分析</h2>
        <p>根据最新监控数据，该股票主力资金呈现<span class="highlight">{'流出' if stock_data.get('main_inflow', 0) < 0 else '流入'}</span>状态。</p>
        
        <h2>三、风险提示</h2>
        <ul>
            <li>主力控盘度较低，筹码分散</li>
            <li>近期波动较大，注意风险控制</li>
            <li>建议持续关注资金流向变化</li>
        </ul>
        
        <h2>四、操作建议</h2>
        <p>基于当前技术面和资金面分析，建议投资者:</p>
        <ul>
            <li>密切关注主力资金动向</li>
            <li>设置合理止损位</li>
            <li>等待企稳信号后再考虑操作</li>
        </ul>
        """
        
        return self.create_document(title, content, filename)


class ExcelGenerator(DocumentGenerator):
    """Excel表格生成器（使用CSV格式）"""
    
    def create_csv(self, data, headers, filename=None):
        """创建CSV表格"""
        if not filename:
            filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            # 写入表头
            f.write(','.join(headers) + '\n')
            
            # 写入数据
            for row in data:
                # 处理逗号和引号
                formatted_row = []
                for cell in row:
                    cell_str = str(cell)
                    if ',' in cell_str or '"' in cell_str:
                        cell_str = '"' + cell_str.replace('"', '""') + '"'
                    formatted_row.append(cell_str)
                f.write(','.join(formatted_row) + '\n')
        
        print(f"Excel表格已生成: {filepath}")
        print("提示: 可用Excel或WPS打开此CSV文件")
        return filepath
    
    def create_stock_monitor_table(self, stock_history, filename=None):
        """创建股票监控数据表"""
        headers = ['时间', '股票代码', '股票名称', '价格', '涨跌幅', '主力净流入(万)', '控盘度']
        
        data = []
        for record in stock_history:
            data.append([
                record.get('time', '-'),
                record.get('code', '-'),
                record.get('name', '-'),
                f"{record.get('price', 0):.2f}",
                f"{record.get('change_pct', 0):+.2f}%",
                f"{record.get('main_inflow', 0)/10000:+.0f}",
                f"{record.get('main_control', 0):.3f}"
            ])
        
        return self.create_csv(data, headers, filename)


class ReportGenerator:
    """综合报告生成器"""
    
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.word_gen = WordGenerator(output_dir)
        self.excel_gen = ExcelGenerator(output_dir)
    
    def generate_stock_analysis_report(self, stock_code, stock_name, current_data, history_data):
        """生成完整的股票分析报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 生成Word报告
        word_file = self.word_gen.create_stock_report(
            current_data,
            f"stock_report_{stock_code}_{timestamp}.html"
        )
        
        # 生成Excel数据表
        excel_file = self.excel_gen.create_stock_monitor_table(
            history_data,
            f"stock_data_{stock_code}_{timestamp}.csv"
        )
        
        # 生成JSON原始数据
        json_file = os.path.join(self.output_dir, f"stock_raw_{stock_code}_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'current': current_data,
                'history': history_data,
                'generated_at': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n报告生成完成!")
        print(f"Word报告: {word_file}")
        print(f"Excel表格: {excel_file}")
        print(f"原始数据: {json_file}")
        
        return {
            'word': word_file,
            'excel': excel_file,
            'json': json_file
        }


def main():
    """演示"""
    print("=" * 70)
    print(" 办公文档自动化工具")
    print("=" * 70)
    
    # 创建报告生成器
    report_gen = ReportGenerator()
    
    # 示例数据
    current_data = {
        'code': '301117',
        'name': '佳缘科技',
        'price': 47.64,
        'change_pct': -9.17,
        'main_inflow': -78830000,
        'main_control': 0.153
    }
    
    history_data = [
        {'time': '11:23', 'code': '301117', 'name': '佳缘科技', 'price': 47.30, 'change_pct': -9.82, 'main_inflow': -78830000, 'main_control': 0.153},
        {'time': '14:27', 'code': '301117', 'name': '佳缘科技', 'price': 47.64, 'change_pct': -9.17, 'main_inflow': -78830000, 'main_control': 0.153},
    ]
    
    # 生成报告
    print("\n正在生成股票分析报告...")
    files = report_gen.generate_stock_analysis_report(
        '301117',
        '佳缘科技',
        current_data,
        history_data
    )
    
    print("\n" + "=" * 70)
    print("所有文件已保存到 'reports' 目录")
    print("=" * 70)


if __name__ == "__main__":
    main()
