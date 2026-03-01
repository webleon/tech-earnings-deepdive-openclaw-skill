#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Key Forces 识别模块
识别未来 3-5 年决定公司价值的 1-3 个决定性力量
"""

import sys
import json
from datetime import datetime


class KeyForcesIdentifier:
    """Key Forces 识别器"""
    
    def __init__(self, data: dict):
        self.data = data
        self.ticker = data.get('symbol', 'UNKNOWN')
        self.financials = data.get('financials', {})
        self.balance_sheet = data.get('balance_sheet', {})
        self.cashflow = data.get('cashflow', {})
        self.price = data.get('price', {})
        self.company_info = data.get('company_info', {})
        self.analyst = data.get('analyst_estimates', {})
    
    def identify(self) -> list:
        """识别 Key Forces（1-3 个决定性力量）"""
        print("🎯 识别 Key Forces...")
        
        forces = []
        
        # 1. 检查增长驱动力
        growth_force = self._check_growth_driver()
        if growth_force:
            forces.append(growth_force)
        
        # 2. 检查技术变革
        tech_force = self._check_technology_shift()
        if tech_force:
            forces.append(tech_force)
        
        # 3. 检查竞争格局
        competition_force = self._check_competitive_moat()
        if competition_force:
            forces.append(competition_force)
        
        # 4. 检查财务健康度
        financial_force = self._check_financial_strength()
        if financial_force:
            forces.append(financial_force)
        
        # 5. 检查市场情绪
        sentiment_force = self._check_market_sentiment()
        if sentiment_force:
            forces.append(sentiment_force)
        
        # 6. 检查行业趋势
        industry_force = self._check_industry_trend()
        if industry_force:
            forces.append(industry_force)
        
        # 按影响力排序，返回最重要的 1-3 个
        forces.sort(key=lambda x: x['impact_score'], reverse=True)
        
        key_forces = forces[:3]
        
        print(f"✅ 识别到 {len(key_forces)} 个 Key Forces")
        for i, force in enumerate(key_forces, 1):
            print(f"   {i}. {force['name']} (影响力：{force['impact_score']}/10)")
        
        return key_forces
    
    def _check_growth_driver(self) -> dict:
        """检查增长驱动力"""
        revenue_growth = self.financials.get('revenue_growth_yoy', 0) * 100
        income_growth = self.financials.get('net_income_growth_yoy', 0) * 100
        
        if revenue_growth > 20 or income_growth > 20:
            return {
                'type': '增长驱动',
                'name': f'收入/利润高速增长（+{max(revenue_growth, income_growth):.1f}%）',
                'description': f'营收增长{revenue_growth:.1f}%，净利润增长{income_growth:.1f}%',
                'impact': '高' if max(revenue_growth, income_growth) > 30 else '中',
                'impact_score': min(10, max(revenue_growth, income_growth) / 5),
                'related_modules': ['A', 'B', 'F'],  # 收入质量、盈利能力、核心 KPI
                'evidence': [
                    f'营收同比增长{revenue_growth:.1f}%',
                    f'净利润同比增长{income_growth:.1f}%'
                ],
                'questions': [
                    '增长是否可持续？',
                    '增长质量如何（现金流匹配吗）？',
                    '增长来自哪里（现有业务还是新业务）？'
                ]
            }
        return None
    
    def _check_technology_shift(self) -> dict:
        """检查技术变革"""
        description = self.company_info.get('description', '').lower()
        industry = self.company_info.get('industry', '').lower()
        
        # 检查是否涉及 AI、云计算等技术变革
        tech_keywords = ['ai', 'artificial intelligence', 'cloud', 'machine learning', 'saas']
        tech_score = sum(1 for keyword in tech_keywords if keyword in description)
        
        rd_ratio = 15  # 假设科技行业平均研发投入
        
        if tech_score >= 2 or 'software' in industry or 'semiconductor' in industry:
            return {
                'type': '技术范式转移',
                'name': 'AI/技术转型驱动',
                'description': f'公司处于{industry}行业，正在经历技术变革',
                'impact': '高' if tech_score >= 3 else '中',
                'impact_score': min(10, tech_score * 2 + 4),
                'related_modules': ['G', 'N'],  # 产品与新业务、研发效率
                'evidence': [
                    f'行业：{industry}',
                    f'研发投入约{rd_ratio}%',
                    f'技术关键词提及{tech_score}次'
                ],
                'questions': [
                    '技术变革对公司是机会还是威胁？',
                    '公司在新技术领域的投入是否足够？',
                    '技术优势能否转化为商业优势？'
                ]
            }
        return None
    
    def _check_competitive_moat(self) -> dict:
        """检查竞争格局/护城河"""
        gross_margin = self.financials.get('gross_profit', 0) / self.financials.get('total_revenue', 1) * 100
        
        if gross_margin > 60:
            return {
                'type': '护城河加深',
                'name': f'强定价权（毛利率{gross_margin:.1f}%）',
                'description': f'毛利率{gross_margin:.1f}%，反映强大的竞争优势',
                'impact': '高' if gross_margin > 70 else '中',
                'impact_score': min(10, gross_margin / 8),
                'related_modules': ['E', 'K'],  # 竞争格局、估值
                'evidence': [
                    f'毛利率{gross_margin:.1f}%',
                    '高毛利率反映定价权和竞争优势'
                ],
                'questions': [
                    '护城河来源是什么（品牌/网络效应/转换成本）？',
                    '护城河是在加深还是被侵蚀？',
                    '竞争对手能否复制这个优势？'
                ]
            }
        return None
    
    def _check_financial_strength(self) -> dict:
        """检查财务健康度"""
        fcf = self.cashflow.get('free_cashflow', 0)
        revenue = self.financials.get('total_revenue', 1)
        fcf_margin = fcf / revenue * 100 if revenue > 0 else 0
        
        current_ratio = self.balance_sheet.get('current_ratio', 0)
        debt_to_equity = self.balance_sheet.get('debt_to_equity', 0)
        
        if fcf_margin > 20 and current_ratio > 1.5:
            return {
                'type': '财务实力',
                'name': f'强劲现金流（FCF 利润率{fcf_margin:.1f}%）',
                'description': f'自由现金流利润率{fcf_margin:.1f}%，流动比率{current_ratio:.2f}',
                'impact': '中',
                'impact_score': min(10, fcf_margin / 3 + current_ratio * 2),
                'related_modules': ['C', 'O'],  # 现金流、会计质量
                'evidence': [
                    f'自由现金流${fcf/1e9:.1f}亿',
                    f'FCF 利润率{fcf_margin:.1f}%',
                    f'流动比率{current_ratio:.2f}',
                    f'负债率{debt_to_equity:.2f}'
                ],
                'questions': [
                    '现金流能否支撑未来投资？',
                    '是否有并购或回购能力？',
                    '财务风险是否可控？'
                ]
            }
        return None
    
    def _check_market_sentiment(self) -> dict:
        """检查市场情绪"""
        target_price = self.analyst.get('target_price_mean', 0)
        current_price = self.price.get('current_price', 1)
        upside = (target_price - current_price) / current_price * 100 if current_price > 0 else 0
        
        strong_buy = self.analyst.get('strong_buy', 0)
        buy = self.analyst.get('buy', 0)
        hold = self.analyst.get('hold', 0)
        total = strong_buy + buy + hold
        buy_ratio = (strong_buy + buy) / total * 100 if total > 0 else 0
        
        if upside > 30 or buy_ratio > 80:
            return {
                'type': '市场情绪',
                'name': f'分析师强烈看好（{buy_ratio:.1f}%买入）',
                'description': f'分析师目标价${target_price:.2f}（上涨{upside:.1f}%），{buy_ratio:.1f}%给予买入评级',
                'impact': '中',
                'impact_score': min(10, upside / 5 + buy_ratio / 15),
                'related_modules': ['D', 'L'],  # 前瞻指引、筹码分布
                'evidence': [
                    f'分析师目标价${target_price:.2f}',
                    f'上涨空间{upside:.1f}%',
                    f'{strong_buy}强烈买入，{buy}买入，{hold}持有'
                ],
                'questions': [
                    '分析师预期是否过于乐观？',
                    '市场共识是否已经反映在股价中？',
                    '是否存在预期差？'
                ]
            }
        return None
    
    def _check_industry_trend(self) -> dict:
        """检查行业趋势"""
        sector = self.company_info.get('sector', '')
        industry = self.company_info.get('industry', '')
        
        # 科技行业通常处于增长趋势
        if 'Technology' in sector or 'Software' in industry or 'Semiconductor' in industry:
            return {
                'type': '行业趋势',
                'name': f'{industry}行业增长趋势',
                'description': f'公司处于{sector} - {industry}，行业整体增长',
                'impact': '中',
                'impact_score': 6,
                'related_modules': ['E', 'J'],  # 竞争格局、宏观政策
                'evidence': [
                    f'行业：{industry}',
                    '科技行业整体保持增长趋势'
                ],
                'questions': [
                    '行业增长是否可持续？',
                    '公司在行业中的地位如何？',
                    '是否有行业整合机会？'
                ]
            }
        return None


def identify_key_forces(data: dict) -> list:
    """便捷函数：识别 Key Forces"""
    identifier = KeyForcesIdentifier(data)
    return identifier.identify()


if __name__ == '__main__':
    sys.path.insert(0, 'modules')
    from fetch_data import StockDataFetcher
    
    if len(sys.argv) < 2:
        print("用法：python key_forces.py <股票代码>")
        sys.exit(1)
    
    ticker = sys.argv[1]
    
    # 获取数据
    fetcher = StockDataFetcher(ticker)
    data = fetcher.get_all_data(use_cache=True)
    
    # 识别 Key Forces
    forces = identify_key_forces(data)
    
    print("\n" + "=" * 60)
    print(f"{ticker} Key Forces 分析")
    print("=" * 60)
    
    for i, force in enumerate(forces, 1):
        print(f"\n{i}. {force['name']}")
        print(f"   类型：{force['type']}")
        print(f"   影响力：{force['impact']} ({force['impact_score']:.1f}/10)")
        print(f"   描述：{force['description']}")
        print(f"   相关模块：{', '.join(force['related_modules'])}")
        print(f"   关键问题：")
        for q in force['questions']:
            print(f"     - {q}")
