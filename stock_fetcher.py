#!/usr/bin/env python3
"""
东方财富数据抓取脚本
使用 AKShare 库获取 A 股数据
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


def get_stock_list():
    """获取所有 A 股股票列表"""
    print("正在获取股票列表...")
    stock_df = ak.stock_zh_a_spot_em()
    print(f"共获取到 {len(stock_df)} 只股票")
    return stock_df


def get_stock_kline(stock_code, period="daily", start_date=None, end_date=None):
    """
    获取股票 K 线数据
    
    参数:
        stock_code: 股票代码 (如 "000001")
        period: 周期 (daily/weekly/monthly)
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=60)).strftime("%Y%m%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y%m%d")
    
    print(f"正在获取 {stock_code} 的 K 线数据...")
    
    # 判断是沪股还是深股
    if stock_code.startswith('6'):
        stock_code = f"{stock_code}.sh"
    else:
        stock_code = f"{stock_code}.sz"
    
    df = ak.stock_zh_a_hist(
        symbol=stock_code.split('.')[0],
        period=period,
        start_date=start_date,
        end_date=end_date,
        adjust="qfq"  # 前复权
    )
    return df


def get_stock_financial(stock_code):
    """获取股票财务数据"""
    print(f"正在获取 {stock_code} 的财务数据...")
    
    try:
        # 主要财务指标
        financial_df = ak.stock_financial_report_sina(stock=stock_code)
        return financial_df
    except Exception as e:
        print(f"获取财务数据失败: {e}")
        return None


def get_hot_sectors():
    """获取热门板块/概念"""
    print("正在获取热门板块...")
    
    # 行业板块涨幅
    sector_df = ak.stock_board_industry_name_em()
    print(f"共获取到 {len(sector_df)} 个行业板块")
    
    return sector_df


def get_sector_stocks(sector_name):
    """获取某个板块下的所有股票"""
    print(f"正在获取 {sector_name} 板块的股票...")
    
    try:
        stocks_df = ak.stock_board_industry_cons_em(symbol=sector_name)
        return stocks_df
    except Exception as e:
        print(f"获取板块股票失败: {e}")
        return None


def screen_stocks_basic():
    """
    基础选股筛选
    条件：
    1. 市值大于 50 亿
    2. 成交额大于 1 亿
    3. 近期有上涨
    """
    print("正在进行基础筛选...")
    
    df = get_stock_list()
    
    # 转换数值类型
    df['总市值'] = pd.to_numeric(df['总市值'], errors='coerce')
    df['成交额'] = pd.to_numeric(df['成交额'], errors='coerce')
    df['涨跌幅'] = pd.to_numeric(df['涨跌幅'], errors='coerce')
    
    # 筛选条件
    filtered = df[
        (df['总市值'] > 50e8) &  # 市值 > 50亿
        (df['成交额'] > 1e8) &    # 成交额 > 1亿
        (df['涨跌幅'] > -5)      # 跌幅不太大
    ].copy()
    
    # 按涨跌幅排序
    filtered = filtered.sort_values('涨跌幅', ascending=False)
    
    print(f"筛选后剩余 {len(filtered)} 只股票")
    
    return filtered[['代码', '名称', '最新价', '涨跌幅', '成交额', '总市值', '所属行业']]


def main():
    """主函数"""
    print("=" * 50)
    print("东方财富数据抓取工具")
    print("=" * 50)
    
    # 示例 1: 获取股票列表并筛选
    print("\n【1】基础选股筛选")
    screened = screen_stocks_basic()
    print(screened.head(20).to_string())
    
    # 保存到 CSV
    screened.head(100).to_csv("screened_stocks.csv", index=False, encoding='utf-8-sig')
    print("\n已保存筛选结果到 screened_stocks.csv")
    
    # 示例 2: 获取热门板块
    print("\n【2】热门板块")
    sectors = get_hot_sectors()
    print(sectors.head(10).to_string())
    
    # 示例 3: 获取单只股票 K 线（示例：贵州茅台）
    print("\n【3】示例：获取贵州茅台 K 线数据")
    kline = get_stock_kline("600519", start_date="20250101")
    print(kline.tail(10).to_string())
    kline.to_csv("600519_kline.csv", index=False, encoding='utf-8-sig')
    print("已保存到 600519_kline.csv")
    
    print("\n" + "=" * 50)
    print("数据抓取完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
