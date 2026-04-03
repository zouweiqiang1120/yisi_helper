#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tavily AI 搜索工具
需要 API Key: https://tavily.com/
"""

import urllib.request
import urllib.parse
import json
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context


class TavilySearch:
    """Tavily AI 搜索引擎"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('TAVILY_API_KEY')
        self.base_url = "https://api.tavily.com/search"
    
    def search(self, query, search_depth="basic", max_results=5):
        """
        执行搜索
        
        Args:
            query: 搜索关键词
            search_depth: "basic" 或 "advanced"
            max_results: 返回结果数量 (1-10)
        """
        if not self.api_key:
            return {'error': '请提供 Tavily API Key'}
        
        data = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "max_results": max_results,
            "include_answer": True,
            "include_images": False,
            "include_raw_content": False
        }
        
        try:
            req = urllib.request.Request(
                self.base_url,
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            return result
            
        except Exception as e:
            return {'error': f'搜索失败: {str(e)}'}
    
    def display_results(self, results):
        """显示搜索结果"""
        if 'error' in results:
            print(f"错误: {results['error']}")
            return
        
        print("\n" + "=" * 70)
        print(" Tavily AI 搜索结果")
        print("=" * 70)
        
        # 显示 AI 回答
        if results.get('answer'):
            print(f"\n[AI 回答]\n{results['answer']}\n")
        
        # 显示搜索结果
        print("-" * 70)
        print("[相关网页]")
        print("-" * 70)
        
        for i, result in enumerate(results.get('results', []), 1):
            print(f"\n[{i}] {result.get('title', '无标题')}")
            print(f"    链接: {result.get('url', '无链接')}")
            print(f"    内容: {result.get('content', '无内容')[:150]}...")
            if result.get('score'):
                print(f"    相关度: {result.get('score'):.2f}")
        
        print("\n" + "=" * 70)


def main():
    """主程序"""
    import sys
    
    print("=" * 70)
    print(" Tavily AI 搜索引擎")
    print(" 官网: https://tavily.com")
    print("=" * 70)
    
    # 获取 API Key
    api_key = os.environ.get('TAVILY_API_KEY')
    
    if not api_key:
        print("\n请先设置 Tavily API Key:")
        print("1. 访问 https://tavily.com 注册获取免费 API Key")
        print("2. 设置环境变量: set TAVILY_API_KEY=your_key_here")
        print("3. 或在代码中直接传入 api_key 参数")
        print("\n免费额度: 每月 1000 次搜索")
        
        # 尝试从用户输入获取
        api_key = input("\n请输入 API Key (或按回车跳过): ").strip()
        
        if not api_key:
            print("\n未提供 API Key，演示模式")
            print("示例搜索结果格式:\n")
            
            # 显示示例
            demo_result = {
                'answer': '这是一个 AI 生成的回答示例。实际使用时需要提供 API Key。',
                'results': [
                    {
                        'title': '示例结果 1',
                        'url': 'https://example.com/1',
                        'content': '这是搜索结果的示例内容...',
                        'score': 0.95
                    },
                    {
                        'title': '示例结果 2',
                        'url': 'https://example.com/2',
                        'content': '这是另一个搜索结果的示例内容...',
                        'score': 0.85
                    }
                ]
            }
            
            searcher = TavilySearch(api_key="demo")
            searcher.display_results(demo_result)
            return
    
    # 获取搜索关键词
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = input("\n请输入搜索关键词: ").strip()
    
    if not query:
        print("搜索关键词不能为空")
        return
    
    # 执行搜索
    print(f"\n正在搜索: {query}")
    print("-" * 70)
    
    searcher = TavilySearch(api_key=api_key)
    results = searcher.search(query, search_depth="advanced", max_results=5)
    
    # 显示结果
    searcher.display_results(results)
    
    # 保存结果
    from datetime import datetime
    filename = f"tavily_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n完整结果已保存到: {filename}")


if __name__ == "__main__":
    main()
