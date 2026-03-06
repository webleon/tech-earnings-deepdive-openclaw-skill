#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量分析入口
用法：python analyze_batch.py AAPL MSFT GOOGL
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from core import analyze_single_stock, export_report


class BatchAnalyzer:
    """批量分析器"""
    
    def __init__(self, tickers: List[str], max_workers: int = 3):
        self.tickers = tickers
        self.max_workers = max_workers
        self.results = {}
        
        # 输出目录
        output_base = os.environ.get('OUTPUT_DIR', Path.home() / '.openclaw' / 'tech-earnings-output')
        self.output_dir = Path(output_base) / 'batch'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_all(self, use_cache: bool = True) -> Dict:
        """分析所有股票（完整流程）"""
        print("=" * 70)
        print(f"🚀 批量分析 {len(self.tickers)} 只股票")
        print("=" * 70)
        print(f"股票列表：{', '.join(self.tickers)}")
        print(f"并发数：{self.max_workers}")
        print(f"使用缓存：{'是' if use_cache else '否'}")
        print("=" * 70)
        print()
        
        # 多线程并行分析
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交任务（始终完整分析，包含 Variant View）
            future_to_ticker = {
                executor.submit(analyze_single_stock, ticker, use_cache): ticker
                for ticker in self.tickers
            }
            
            # 收集结果
            completed = 0
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    result = future.result()
                    self.results[ticker] = result
                    completed += 1
                    
                    # 显示进度
                    score = result['summary']['overall_score']
                    rec = result['summary']['recommendation']
                    print(f"✅ [{completed}/{len(self.tickers)}] {ticker}: "
                          f"{score:.1f}/100 - {rec}")
                except Exception as e:
                    print(f"❌ [{ticker}] 分析失败：{e}")
        
        print()
        print("=" * 70)
        print(f"✅ 批量分析完成：{len(self.results)}/{len(self.tickers)} 只股票")
        print("=" * 70)
        
        # 生成对比报告
        self.generate_comparison_report()
        
        return self.results
    
    def generate_comparison_report(self):
        """生成多股对比报告"""
        if not self.results:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"comparison_{timestamp}.html"
        filepath = self.output_dir / filename
        
        # 简单的对比表格
        html = ['<!DOCTYPE html>', '<html><head><meta charset="UTF-8">',
                '<title>批量分析对比报告</title>',
                '<style>',
                'body { font-family: Arial, sans-serif; padding: 40px; }',
                'table { border-collapse: collapse; width: 100%; margin: 20px 0; }',
                'th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }',
                'th { background: #333; color: white; }',
                'tr:nth-child(even) { background: #f5f5f5; }',
                '.score-high { color: #27ae60; font-weight: bold; }',
                '.score-medium { color: #f39c12; font-weight: bold; }',
                '.score-low { color: #c0392b; font-weight: bold; }',
                '</style>',
                '</head><body>',
                '<h1>📊 批量分析对比报告</h1>',
                f'<p>生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>',
                '<table>',
                '<tr><th>股票代码</th><th>综合评分</th><th>MSCI Barra</th>',
                '<th>投资建议</th><th>置信度</th></tr>']
        
        for ticker, result in sorted(self.results.items()):
            summary = result['summary']
            score = summary['overall_score']
            barra = summary['barra_score']
            rec = summary['recommendation']
            conf = summary['confidence']
            
            score_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
            
            html.append(f'<tr>'
                       f'<td>{ticker}</td>'
                       f'<td class="{score_class}">{score:.1f}/100</td>'
                       f'<td>{barra:.1f}</td>'
                       f'<td>{rec}</td>'
                       f'<td>{conf}</td>'
                       f'</tr>')
        
        html.extend(['</table>', '</body></html>'])
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html))
        
        print(f"📊 对比报告已生成：{filepath}")


def main():
    if len(sys.argv) < 2:
        print("用法：python analyze_batch.py <股票代码列表>")
        print("示例：python analyze_batch.py AAPL MSFT GOOGL")
        sys.exit(1)
    
    tickers = [t.upper() for t in sys.argv[1:]]
    analyzer = BatchAnalyzer(tickers, max_workers=3)
    analyzer.analyze_all(use_cache=True)


if __name__ == '__main__':
    main()
