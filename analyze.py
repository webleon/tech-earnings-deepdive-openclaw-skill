#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单股分析入口
用法：python analyze.py AAPL
"""

import sys
from modules.core import analyze_single_stock, export_report

def main():
    if len(sys.argv) < 2:
        print("用法：python analyze.py <股票代码>")
        print("示例：python analyze.py AAPL")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    print(f"🚀 开始分析 {ticker}...")
    
    # 调用核心分析（完整流程）
    result = analyze_single_stock(ticker, use_cache=True)
    
    # 打印结果
    summary = result['summary']
    print(f"📊 综合评分：{summary['overall_score']:.1f}/100")
    print(f"💰 MSCI Barra: {summary['barra_score']:.1f}/100")
    print(f"📈 投资建议：{summary['recommendation']}")
    print(f"🎯 置信度：{summary['confidence']}")
    
    # 导出报告
    print("📝 生成报告...")
    html_file = export_report(result)
    print(f"✅ 报告已生成：{html_file}")

if __name__ == '__main__':
    main()
