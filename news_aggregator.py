#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻聚合器
自动收集股票相关新闻，分类整理，生成简报
"""

import urllib.request
import urllib.parse
import json
import ssl
import re
from datetime import datetime
import os

ssl._create_default_https_context = ssl._create_unverified_context


class NewsAggregator:
    """新闻聚合器"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.output_dir = "news"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_baidu_news(self, keyword, num=10):
        """获取百度新闻"""
        try:
            url = f"https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word={urllib.parse.quote(keyword)}"
            req = urllib.request.Request(url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            # 提取新闻标题和链接
            news_list = []
            
            # 百度新闻结果匹配
            pattern = r'<div[^>]*class="[^"]*result[^"]*"[^>]*>.*?<h3[^>]*>(.*?)</h3>.*?<span[^>]*class="[^"]*c-color-gray[^"]*"[^>]*>(.*?)</span>'
            matches = re.findall(pattern, html, re.DOTALL)[:num]
            
            for title_html, source_time in matches:
                # 清理标题
                title = re.sub(r'<[^>]+>', '', title_html).strip()
                source_time = re.sub(r'<[^>]+>', '', source_time).strip()
                
                if title and len(title) > 10:
                    news_list.append({
                        'title': title,
                        'source_time': source_time,
                        'source': '百度新闻'
                    })
            
            return news_list
        except Exception as e:
            print(f"百度新闻获取失败: {e}")
            return []
    
    def fetch_36kr_news(self, num=5):
        """获取36氪财经新闻"""
        try:
            url = "https://36kr.com/api/search-column/mainsite?per_page=10"
            req = urllib.request.Request(url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            news_list = []
            if data.get('data'):
                for item in data['data'][:num]:
                    news_list.append({
                        'title': item.get('title', ''),
                        'source_time': item.get('published_at', ''),
                        'source': '36氪'
                    })
            
            return news_list
        except Exception as e:
            print(f"36氪新闻获取失败: {e}")
            return []
    
    def fetch_wallstreetcn_news(self, num=5):
        """获取华尔街见闻新闻"""
        try:
            url = "https://api.wallstreetcn.com/apiv1/content/articles?category=global&limit=10"
            req = urllib.request.Request(url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            news_list = []
            if data.get('data'):
                for item in data['data'][:num]:
                    news_list.append({
                        'title': item.get('title', ''),
                        'source_time': item.get('display_time', ''),
                        'source': '华尔街见闻'
                    })
            
            return news_list
        except Exception as e:
            print(f"华尔街见闻获取失败: {e}")
            return []
    
    def categorize_news(self, news_list, stock_keywords):
        """分类新闻"""
        categories = {
            '个股相关': [],
            '行业动态': [],
            '宏观经济': [],
            '其他': []
        }
        
        for news in news_list:
            title = news['title']
            
            # 检查是否个股相关
            is_stock_related = any(keyword in title for keyword in stock_keywords)
            
            if is_stock_related:
                categories['个股相关'].append(news)
            elif any(word in title for word in ['行业', '板块', '概念', '产业链']):
                categories['行业动态'].append(news)
            elif any(word in title for word in ['经济', '政策', '央行', 'GDP', 'CPI', '利率']):
                categories['宏观经济'].append(news)
            else:
                categories['其他'].append(news)
        
        return categories
    
    def generate_newsletter(self, stock_code, stock_name, all_news, categories):
        """生成新闻简报"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"news_{stock_code}_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{stock_name} 新闻简报</title>
    <style>
        body {{ font-family: Microsoft YaHei, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007acc; padding-bottom: 15px; }}
        h2 {{ color: #555; margin-top: 30px; border-left: 4px solid #007acc; padding-left: 10px; }}
        .meta {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
        .news-item {{ padding: 15px; margin: 10px 0; border-left: 3px solid #ddd; background: #fafafa; }}
        .news-item.important {{ border-left-color: #d9534f; background: #fdf2f2; }}
        .news-title {{ font-weight: bold; color: #333; margin-bottom: 5px; }}
        .news-meta {{ font-size: 12px; color: #999; }}
        .stats {{ background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .tag {{ display: inline-block; padding: 2px 8px; background: #007acc; color: white; font-size: 12px; border-radius: 3px; margin-right: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{stock_name} ({stock_code}) 新闻简报</h1>
        <div class="meta">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        
        <div class="stats">
            <strong>统计:</strong> 共收集 {len(all_news)} 条新闻
            <span class="tag">个股相关: {len(categories['个股相关'])}</span>
            <span class="tag">行业动态: {len(categories['行业动态'])}</span>
            <span class="tag">宏观经济: {len(categories['宏观经济'])}</span>
        </div>
"""
        
        # 个股相关新闻（重要）
        if categories['个股相关']:
            html += """
        <h2>🔴 个股相关新闻</h2>
"""
            for news in categories['个股相关'][:5]:
                html += f"""
        <div class="news-item important">
            <div class="news-title">{news['title']}</div>
            <div class="news-meta">{news['source']} | {news['source_time']}</div>
        </div>
"""
        
        # 行业动态
        if categories['行业动态']:
            html += """
        <h2>🟡 行业动态</h2>
"""
            for news in categories['行业动态'][:3]:
                html += f"""
        <div class="news-item">
            <div class="news-title">{news['title']}</div>
            <div class="news-meta">{news['source']} | {news['source_time']}</div>
        </div>
"""
        
        # 宏观经济
        if categories['宏观经济']:
            html += """
        <h2>🟢 宏观经济</h2>
"""
            for news in categories['宏观经济'][:3]:
                html += f"""
        <div class="news-item">
            <div class="news-title">{news['title']}</div>
            <div class="news-meta">{news['source']} | {news['source_time']}</div>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath
    
    def run(self, stock_code, stock_name, keywords):
        """运行新闻聚合"""
        print(f"\n正在收集 {stock_name} 相关新闻...")
        print("=" * 70)
        
        all_news = []
        
        # 1. 百度新闻
        print("[1/3] 获取百度新闻...")
        baidu_news = self.fetch_baidu_news(f"{stock_name} {stock_code}", num=10)
        all_news.extend(baidu_news)
        print(f"      获取 {len(baidu_news)} 条")
        
        # 2. 36氪
        print("[2/3] 获取36氪新闻...")
        kr_news = self.fetch_36kr_news(num=5)
        all_news.extend(kr_news)
        print(f"      获取 {len(kr_news)} 条")
        
        # 3. 华尔街见闻
        print("[3/3] 获取华尔街见闻...")
        wsc_news = self.fetch_wallstreetcn_news(num=5)
        all_news.extend(wsc_news)
        print(f"      获取 {len(wsc_news)} 条")
        
        print(f"\n共收集 {len(all_news)} 条新闻")
        
        # 分类
        categories = self.categorize_news(all_news, keywords)
        
        # 生成简报
        report_file = self.generate_newsletter(stock_code, stock_name, all_news, categories)
        
        print(f"\n新闻简报已生成: {report_file}")
        print("=" * 70)
        
        return {
            'total': len(all_news),
            'categories': {k: len(v) for k, v in categories.items()},
            'report': report_file
        }


def main():
    """主程序"""
    print("=" * 70)
    print(" 新闻聚合器")
    print("=" * 70)
    
    aggregator = NewsAggregator()
    
    # 示例：收集佳缘科技相关新闻
    result = aggregator.run(
        stock_code='301117',
        stock_name='佳缘科技',
        keywords=['佳缘科技', '301117', '网络安全', '信息安全']
    )
    
    print("\n功能:")
    print("  - 自动收集多源新闻")
    print("  - 智能分类整理")
    print("  - 生成精美简报")
    print("  - 突出个股相关信息")


if __name__ == "__main__":
    main()
