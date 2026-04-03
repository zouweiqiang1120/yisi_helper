#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多搜索引擎聚合工具
支持: 百度搜索、Bing搜索、DuckDuckGo（通过网页抓取）
"""

import urllib.request
import urllib.parse
import json
import ssl
import re
from urllib.error import HTTPError, URLError
import time

ssl._create_default_https_context = ssl._create_unverified_context


class MultiSearchEngine:
    """多搜索引擎聚合"""
    
    def __init__(self):
        self.results = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    def search_baidu(self, query, num=5):
        """百度搜索"""
        try:
            url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            # 简单提取搜索结果
            results = []
            # 提取标题和链接（简化版）
            title_pattern = r'<div[^>]*class="[^"]*c-container[^"]*"[^>]*>.*?<h3[^>]*>(.*?)</h3>'
            titles = re.findall(title_pattern, html, re.DOTALL)[:num]
            
            for i, title in enumerate(titles, 1):
                # 清理HTML标签
                clean_title = re.sub(r'<[^>]+>', '', title)
                if clean_title:
                    results.append({
                        'rank': i,
                        'title': clean_title.strip(),
                        'source': '百度'
                    })
            
            return results
        except Exception as e:
            return [{'error': f'百度搜索失败: {str(e)}'}]
    
    def search_bing(self, query, num=5):
        """Bing搜索"""
        try:
            url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            results = []
            # 提取Bing搜索结果
            title_pattern = r'<li class="b_algo"[^>]*>.*?<h2[^>]*>(.*?)</h2>'
            titles = re.findall(title_pattern, html, re.DOTALL)[:num]
            
            for i, title in enumerate(titles, 1):
                clean_title = re.sub(r'<[^>]+>', '', title)
                if clean_title:
                    results.append({
                        'rank': i,
                        'title': clean_title.strip(),
                        'source': 'Bing'
                    })
            
            return results
        except Exception as e:
            return [{'error': f'Bing搜索失败: {str(e)}'}]
    
    def search_duckduckgo(self, query, num=5):
        """DuckDuckGo搜索"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers=self.headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            results = []
            # 提取DDG搜索结果
            title_pattern = r'<a[^>]*class="result__a"[^>]*>(.*?)</a>'
            titles = re.findall(title_pattern, html, re.DOTALL)[:num]
            
            for i, title in enumerate(titles, 1):
                clean_title = re.sub(r'<[^>]+>', '', title)
                if clean_title:
                    results.append({
                        'rank': i,
                        'title': clean_title.strip(),
                        'source': 'DuckDuckGo'
                    })
            
            return results
        except Exception as e:
            return [{'error': f'DuckDuckGo搜索失败: {str(e)}'}]
    
    def search_all(self, query, num=5):
        """同时搜索所有引擎"""
        print(f"\n正在搜索: {query}")
        print("=" * 70)
        
        all_results = {}
        
        # 百度搜索
        print("\n[1/3] 百度搜索中...")
        baidu_results = self.search_baidu(query, num)
        all_results['百度'] = baidu_results
        time.sleep(0.5)
        
        # Bing搜索
        print("[2/3] Bing搜索中...")
        bing_results = self.search_bing(query, num)
        all_results['Bing'] = bing_results
        time.sleep(0.5)
        
        # DuckDuckGo搜索
        print("[3/3] DuckDuckGo搜索中...")
        ddg_results = self.search_duckduckgo(query, num)
        all_results['DuckDuckGo'] = ddg_results
        
        return all_results
    
    def display_results(self, results):
        """显示搜索结果"""
        for engine, items in results.items():
            print(f"\n{'='*70}")
            print(f" {engine} 搜索结果")
            print('='*70)
            
            if not items:
                print("  无结果")
                continue
            
            for item in items:
                if 'error' in item:
                    print(f"  {item['error']}")
                else:
                    print(f"  [{item['rank']}] {item['title']}")
        
        print("\n" + "="*70)


def main():
    """主程序"""
    import sys
    
    print("=" * 70)
    print(" 多搜索引擎聚合工具")
    print(" 支持: 百度 | Bing | DuckDuckGo")
    print("=" * 70)
    
    # 获取搜索关键词
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = input("\n请输入搜索关键词: ").strip()
    
    if not query:
        print("搜索关键词不能为空")
        return
    
    # 执行搜索
    searcher = MultiSearchEngine()
    results = searcher.search_all(query, num=5)
    
    # 显示结果
    searcher.display_results(results)
    
    # 保存结果
    import os
    from datetime import datetime
    
    filename = f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"搜索关键词: {query}\n")
        f.write(f"搜索时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n")
        
        for engine, items in results.items():
            f.write(f"\n{engine} 搜索结果:\n")
            f.write("-" * 70 + "\n")
            for item in items:
                if 'error' in item:
                    f.write(f"  {item['error']}\n")
                else:
                    f.write(f"  [{item['rank']}] {item['title']}\n")
    
    print(f"\n结果已保存到: {filename}")


if __name__ == "__main__":
    main()
