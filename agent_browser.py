#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Browser - 浏览器自动化工具（简化版）
使用标准库实现网页抓取和解析
完整版需要 Selenium + WebDriver
"""

import urllib.request
import urllib.parse
import ssl
import json
import re
from urllib.error import HTTPError, URLError
from datetime import datetime
import os

ssl._create_default_https_context = ssl._create_unverified_context


class AgentBrowser:
    """Agent 浏览器"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        self.session_cookies = {}
        self.history = []
    
    def navigate(self, url, params=None, method='GET'):
        """导航到指定URL"""
        try:
            # 添加参数
            if params:
                if method == 'GET':
                    url = f"{url}?{urllib.parse.urlencode(params)}"
                
            # 创建请求
            req = urllib.request.Request(
                url,
                headers=self.headers,
                method=method
            )
            
            # 添加cookies
            if self.session_cookies:
                cookie_str = '; '.join([f"{k}={v}" for k, v in self.session_cookies.items()])
                req.add_header('Cookie', cookie_str)
            
            # 发送请求
            with urllib.request.urlopen(req, timeout=30) as response:
                # 保存cookies
                if 'Set-Cookie' in response.headers:
                    self._parse_cookies(response.headers['Set-Cookie'])
                
                # 读取内容
                content = response.read()
                
                # 尝试解压gzip
                try:
                    import gzip
                    content = gzip.decompress(content)
                except:
                    pass
                
                # 解码
                try:
                    html = content.decode('utf-8')
                except:
                    try:
                        html = content.decode('gbk')
                    except:
                        html = content.decode('utf-8', errors='ignore')
                
                # 记录历史
                self.history.append({
                    'url': url,
                    'time': datetime.now().isoformat(),
                    'status': response.status
                })
                
                return {
                    'url': url,
                    'status': response.status,
                    'headers': dict(response.headers),
                    'html': html,
                    'success': True
                }
                
        except HTTPError as e:
            return {'error': f'HTTP Error {e.code}: {e.reason}', 'success': False}
        except URLError as e:
            return {'error': f'URL Error: {e.reason}', 'success': False}
        except Exception as e:
            return {'error': f'Error: {str(e)}', 'success': False}
    
    def _parse_cookies(self, cookie_str):
        """解析cookies"""
        for cookie in cookie_str.split(','):
            parts = cookie.strip().split(';')
            if parts:
                kv = parts[0].split('=')
                if len(kv) == 2:
                    self.session_cookies[kv[0].strip()] = kv[1].strip()
    
    def extract_data(self, html, pattern, multiple=False):
        """从HTML中提取数据"""
        if multiple:
            return re.findall(pattern, html, re.DOTALL)
        else:
            match = re.search(pattern, html, re.DOTALL)
            return match.group(1) if match else None
    
    def extract_stock_data_from_eastmoney(self, code):
        """从东方财富提取股票数据"""
        print(f"正在访问东方财富 {code}...")
        
        # 访问个股页面
        url = f"https://quote.eastmoney.com/concept/sh{code}.html"
        if code.startswith('3') or code.startswith('0'):
            url = f"https://quote.eastmoney.com/concept/sz{code}.html"
        
        result = self.navigate(url)
        
        if not result['success']:
            return result
        
        html = result['html']
        
        # 提取股票名称
        name_pattern = r'<h1[^>]*>(.*?)</h1>'
        name = self.extract_data(html, name_pattern)
        if name:
            name = re.sub(r'<[^>]+>', '', name).strip()
        
        # 提取价格
        price_pattern = r'id="price9"[^>]*>([\d.]+)</span>'
        price = self.extract_data(html, price_pattern)
        
        # 提取涨跌幅
        change_pattern = r'id="km2"[^>]*>([\d.-]+)</span>'
        change = self.extract_data(html, change_pattern)
        
        return {
            'success': True,
            'code': code,
            'name': name or '未知',
            'price': price or '未知',
            'change': change or '未知',
            'source_url': url
        }
    
    def screenshot(self, url, filename=None):
        """截图（简化版：保存HTML）"""
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        result = self.navigate(url)
        
        if result['success']:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result['html'])
            return {'success': True, 'file': filename}
        else:
            return result
    
    def get_history(self):
        """获取浏览历史"""
        return self.history
    
    def clear_history(self):
        """清除历史"""
        self.history = []
        self.session_cookies = {}


def main():
    """演示"""
    print("=" * 70)
    print(" Agent Browser - 浏览器自动化工具")
    print("=" * 70)
    
    browser = AgentBrowser()
    
    # 示例1: 访问百度
    print("\n[示例1] 访问百度...")
    result = browser.navigate("https://www.baidu.com")
    if result['success']:
        print(f"成功! 状态码: {result['status']}")
        print(f"页面标题: {browser.extract_data(result['html'], r'<title>(.*?)</title>')}")
    else:
        print(f"失败: {result.get('error')}")
    
    # 示例2: 访问东方财富
    print("\n[示例2] 访问东方财富...")
    stock_data = browser.extract_stock_data_from_eastmoney('301117')
    if stock_data['success']:
        print(f"股票: {stock_data['name']} ({stock_data['code']})")
        print(f"价格: {stock_data['price']}")
        print(f"涨跌: {stock_data['change']}")
    else:
        print(f"失败: {stock_data.get('error')}")
    
    # 示例3: 搜索
    print("\n[示例3] 百度搜索...")
    search_result = browser.navigate(
        "https://www.baidu.com/s",
        params={'wd': 'Python 教程'}
    )
    if search_result['success']:
        # 提取搜索结果标题
        titles = browser.extract_data(
            search_result['html'],
            r'<h3[^>]*class="t"[^>]*>(.*?)</h3>',
            multiple=True
        )
        print(f"找到 {len(titles)} 个搜索结果")
        for i, title in enumerate(titles[:3], 1):
            clean_title = re.sub(r'<[^>]+>', '', title)
            print(f"  {i}. {clean_title[:50]}...")
    
    # 显示历史
    print("\n[浏览历史]")
    for item in browser.get_history():
        print(f"  {item['time']}: {item['url'][:60]}...")
    
    print("\n" + "=" * 70)
    print("功能:")
    print("  - 网页访问和导航")
    print("  - Cookie 会话管理")
    print("  - 数据提取和解析")
    print("  - 浏览历史记录")
    print("=" * 70)
    print("\n提示: 完整版需要安装 Selenium + ChromeDriver")
    print("      可实现真正的浏览器控制和截图")


if __name__ == "__main__":
    main()
