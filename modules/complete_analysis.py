#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整投资分析模块 - 整合所有功能
1. 数据获取
2. 16 模块分析
3. 6 大视角评分
4. 估值计算
5. 自动生成报告
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 导入各模块
sys.path.insert(0, 'modules')
from fetch_data import StockDataFetcher
from analyze_full import analyze_16_modules
from perspectives_full import analyze_perspectives_full
from valuation_full import ValuationCalculator
from key_forces import identify_key_forces
from bias_framework import check_biases
from variant_view import generate_variant_view
from evidence_search import search_evidence


class CompleteAnalysis:
    """完整投资分析器"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.data = None
        self.modules_result = None
        self.perspectives_result = None
        self.valuation_result = None
    
    def run(self, use_cache=True, full_analysis=True, p2_features=False) -> dict:
        """执行完整分析流程"""
        print("=" * 60)
        print(f"🚀 {self.ticker} 完整投资分析")
        print("=" * 60)
        print()
        
        # 步骤 1：获取数据
        print("📊 步骤 1：获取真实数据...")
        fetcher = StockDataFetcher(self.ticker)
        self.data = fetcher.get_all_data(use_cache=use_cache)
        print(f"✅ 数据获取完成")
        print()
        
        # 步骤 0:Key Forces 识别
        if full_analysis:
            print("🎯 步骤 0:Key Forces 识别...")
            self.key_forces = identify_key_forces(self.data)
            print()
        else:
            self.key_forces = []
        
        # 步骤 2:16 模块分析
        print("🔍 步骤 2:16 模块分析...")
        self.modules_result = analyze_16_modules(self.data)
        avg_module_score = sum(m.get('score', 0) for m in self.modules_result.values()) / 16
        print(f"✅ 16 模块分析完成，平均评分：{avg_module_score:.1f}/100")
        print()
        
        # 步骤 3:6 大视角评分
        print("👁️ 步骤 3:6 大投资哲学视角...")
        self.perspectives_result = analyze_perspectives_full(self.ticker, self.data)
        print(f"✅ 6 大视角分析完成")
        print()
        
        # 步骤 4：估值计算
        print("💰 步骤 4：多方法估值...")
        calc = ValuationCalculator(self.data)
        self.valuation_result = calc.calculate_all()
        print(f"✅ 估值分析完成")
        print()
        
        # 步骤 5：反偏见检查
        if full_analysis:
            print("⚠️ 步骤 5：反偏见检查...")
            self.bias_result = check_biases(self.data)
            print()
        
        # 步骤 6:Variant View（P2 功能）
        if p2_features:
            print("💡 步骤 6:Variant View 生成...")
            self.variant_view_result = generate_variant_view(self.ticker, self.data)
            print()
            
            print("📚 步骤 7：证据搜索...")
            self.evidence_result = search_evidence(self.ticker, self.data.get('company_info', {}).get('company_name', ''))
            print()
        else:
            self.variant_view_result = {}
            self.evidence_result = {}
        
        # 步骤 8：生成综合结论
        print(f"📋 步骤{'7' if not p2_features else '8'}：生成综合结论...")
        summary = self._generate_summary()
        print(f"✅ 综合结论生成完成")
        print()
        
        result = {
            'ticker': self.ticker,
            'timestamp': datetime.now().isoformat(),
            'data': self.data,
            'key_forces': self.key_forces if full_analysis else [],
            'modules': self.modules_result,
            'perspectives': self.perspectives_result,
            'valuation': self.valuation_result,
            'biases': self.bias_result if full_analysis else {},
            'variant_view': self.variant_view_result,
            'evidence': self.evidence_result,
            'summary': summary
        }
        
        return result
    
    def _generate_summary(self) -> dict:
        """生成综合投资结论"""
        # 计算 16 模块平均分
        avg_module_score = sum(m.get('score', 0) for m in self.modules_result.values()) / 16
        
        # 6 大视角评分（使用完整评分）
        perspectives = self.perspectives_result
        perspective_summary = perspectives.get('summary', {})
        perspective_pct = perspective_summary.get('average_score', 0)
        
        # 估值结论
        valuation_summary = self.valuation_result.get('summary', {})
        recommendation = valuation_summary.get('recommendation', '持有')
        upside = valuation_summary.get('upside_downside', 0)
        
        # 综合评分
        overall_score = (avg_module_score * 0.5 + perspective_pct * 0.2 + (100 + upside) / 2 * 0.3)
        
        # 最终建议
        if overall_score >= 80 and upside > 20:
            final_recommendation = '强烈买入'
        elif overall_score >= 70 and upside > 10:
            final_recommendation = '买入'
        elif overall_score >= 60:
            final_recommendation = '持有'
        elif overall_score >= 50:
            final_recommendation = '减持'
        else:
            final_recommendation = '卖出'
        
        return {
            'overall_score': round(overall_score, 1),
            'module_score': round(avg_module_score, 1),
            'perspective_score': round(perspective_pct, 1),
            'valuation_upside': round(upside, 1),
            'recommendation': final_recommendation,
            'confidence': '高' if overall_score >= 70 else '中等' if overall_score >= 50 else '低'
        }
    
    def print_report(self):
        """打印投资分析报告"""
        if not self.modules_result:
            print("❌ 请先运行 run() 方法")
            return
        
        print("=" * 60)
        print(f"📊 {self.ticker} 投资分析报告")
        print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print()
        
        # 公司基本信息
        data = self.data
        print(f"🏢 {data['company_info']['company_name']}")
        print(f"📊 行业：{data['company_info']['sector']} - {data['company_info']['industry']}")
        print(f"💰 股价：${data['price']['current_price']:.2f}")
        print(f"📈 市值：${data['price']['market_cap']/1e12:.2f} 万亿")
        print(f"📊 PE: {data['price']['pe_ratio']:.1f}x")
        print()
        
        # 财务摘要
        print("💵 财务摘要")
        print(f"   营收：${data['financials']['total_revenue']/1e9:.1f} 亿 (+{data['financials']['revenue_growth_yoy']*100:.1f}%)")
        print(f"   净利润：${data['financials']['net_income']/1e9:.1f} 亿")
        print(f"   自由现金流：${data['cashflow']['free_cashflow']/1e9:.1f} 亿")
        print()
        
        # 16 模块评分
        print("🔍 16 模块分析")
        for key, module in self.modules_result.items():
            score = module.get('score', 0)
            name = module.get('name', key)
            bar = '█' * int(score / 10)
            print(f"   {key[0]}. {name}: {score:.1f}/100 {bar}")
        print()
        
        # 6 大视角
        print("👁️ 6 大投资哲学视角")
        perspectives_map = {
            'quality_compounder': '质量复利 (巴菲特/芒格)',
            'imaginative_growth': '想象力成长 (Baillie Gifford/ARK)',
            'fundamental_long_short': '基本面多空 (Tiger Cubs)',
            'deep_value': '深度价值 (Klarman/Marks)',
            'catalyst_driven': '催化剂驱动 (Tepper/Ackman)',
            'macro_tactical': '宏观战术 (Druckenmiller)'
        }
        for key, name in perspectives_map.items():
            if key in self.perspectives_result:
                p = self.perspectives_result[key]
                score = p.get('total_score', 0)
                verdict = p.get('verdict', '')
                bar = '█' * int(score / 10)
                print(f"   {name}: {score:.1f}/100 {bar} [{verdict}]")
        print()
        
        # 估值结论
        print("💰 估值结论")
        valuation_summary = self.valuation_result.get('summary', {})
        print(f"   当前股价：${valuation_summary.get('current_price', 0):.2f}")
        print(f"   平均合理价值：${valuation_summary.get('average_fair_value', 0):.2f}")
        print(f"   上涨/下跌空间：{valuation_summary.get('upside_downside', 0):.1f}%")
        print()
        
        # 综合结论
        summary = self._generate_summary()
        print("=" * 60)
        print("📋 综合投资结论")
        print("=" * 60)
        print(f"综合评分：{summary['overall_score']:.1f}/100")
        print(f"16 模块评分：{summary['module_score']:.1f}/100")
        print(f"6 大视角评分：{summary['perspective_score']:.1f}/100")
        print(f"估值上涨空间：{summary['valuation_upside']:.1f}%")
        print()
        print(f"投资建议：{summary['recommendation']}")
        print(f"置信度：{summary['confidence']}")
        print("=" * 60)


def analyze_stock(ticker: str, use_cache=True) -> dict:
    """便捷函数：执行完整分析"""
    analyzer = CompleteAnalysis(ticker)
    return analyzer.run(use_cache=use_cache)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python complete_analysis.py <股票代码>")
        print("示例：python complete_analysis.py MSFT")
        sys.exit(1)
    
    ticker = sys.argv[1]
    
    analyzer = CompleteAnalysis(ticker)
    analyzer.run(use_cache=True)
    analyzer.print_report()
