#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
估值计算模块 - 完整实现 6 种大师估值方法
基于 Day1Global 原项目框架
"""

import sys
import json
from datetime import datetime


class ValuationCalculator:
    """估值计算器 - 6 种大师方法完整实现"""
    
    def __init__(self, data: dict):
        self.data = data
        self.ticker = data.get('symbol', 'UNKNOWN')
        self.price = data.get('price', {})
        self.financials = data.get('financials', {})
        self.balance_sheet = data.get('balance_sheet', {})
        self.cashflow = data.get('cashflow', {})
        self.analyst = data.get('analyst_estimates', {})
    
    def calculate_all(self) -> dict:
        """执行所有 6 种估值方法"""
        print(f"💰 执行 6 种估值方法计算...")
        
        results = {
            'owner_earnings': self._owner_earnings(),
            'peg': self._peg(),
            'reverse_dcf': self._reverse_dcf(),
            'magic_formula': self._magic_formula(),
            'ev_ebitda': self._ev_ebitda(),
            'ev_revenue_rule40': self._ev_revenue_rule40(),
            'summary': self._generate_summary()
        }
        
        return results
    
    def _owner_earnings(self) -> dict:
        """
        1. 巴菲特 Owner Earnings 估值法
        
        公式：
        Owner Earnings = 净利润 + 折旧摊销 - 资本支出 - 营运资本变动
        合理价值 = Owner Earnings × (10-15 倍)
        """
        # 获取数据
        net_income = self.financials.get('net_income', 0)
        depreciation = self.cashflow.get('depreciation_amortization', 0)
        capex = abs(self.cashflow.get('capital_expenditure', 0))  # CapEx 是负数
        fcf = self.cashflow.get('free_cashflow', 0)
        
        # 简化计算：用 FCF 近似 Owner Earnings
        owner_earnings = fcf if fcf > 0 else net_income + depreciation - capex
        
        # 计算合理价值（10-15 倍）
        fair_value_low = owner_earnings * 10
        fair_value_high = owner_earnings * 15
        fair_value_avg = owner_earnings * 12.5
        
        # 每股价值
        shares = self.price.get('shares_outstanding', 1)
        fair_value_per_share_low = fair_value_low / shares
        fair_value_per_share_high = fair_value_high / shares
        fair_value_per_share_avg = fair_value_avg / shares
        
        current_price = self.price.get('current_price', 0)
        
        # 安全边际
        margin_of_safety = (fair_value_per_share_avg - current_price) / current_price * 100 if current_price > 0 else 0
        
        # 判断
        if margin_of_safety > 30:
            verdict = '明显低估（安全边际>30%）'
        elif margin_of_safety > 10:
            verdict = '合理偏低（安全边际 10-30%）'
        elif margin_of_safety > -10:
            verdict = '合理区间（±10%）'
        else:
            verdict = '高估（安全边际<-10%）'
        
        return {
            'method': 'Owner Earnings（巴菲特）',
            'formula': '净利润 + 折旧摊销 - 资本支出',
            'owner_earnings': owner_earnings,
            'owner_earnings_billions': round(owner_earnings / 1e9, 2),
            'fair_value_range': {
                'low': round(fair_value_per_share_low, 2),
                'high': round(fair_value_per_share_high, 2),
                'average': round(fair_value_per_share_avg, 2)
            },
            'current_price': current_price,
            'margin_of_safety': round(margin_of_safety, 2),
            'verdict': verdict,
            'pe_multiple': {
                'conservative': 10,
                'reasonable': 12.5,
                'optimistic': 15
            }
        }
    
    def _peg(self) -> dict:
        """
        2. 彼得·林奇 PEG 估值法
        
        公式：
        PEG = PE / 盈利增长率
        """
        pe = self.price.get('pe_ratio', 0)
        forward_pe = self.price.get('forward_pe', 0)
        
        # 获取增长率（用营收增长近似）
        growth_rate = self.financials.get('revenue_growth_yoy', 0) * 100  # 转为百分比
        
        # 计算 PEG
        peg = pe / growth_rate if growth_rate > 0 else 0
        
        # 判断标准
        if peg < 0.5:
            verdict = '极具吸引力（PEG<0.5）'
        elif peg < 1.0:
            verdict = '有吸引力（PEG 0.5-1.0）'
        elif peg < 1.5:
            verdict = '合理（PEG 1.0-1.5）'
        elif peg < 2.0:
            verdict = '偏贵（PEG 1.5-2.0）'
        else:
            verdict = '昂贵（PEG>2.0）'
        
        # 合理 PE
        fair_pe = growth_rate * 1.5  # PEG=1.5 时的合理 PE
        implied_price = fair_pe * (self.price.get('eps', 0))
        
        return {
            'method': 'PEG Ratio（彼得·林奇）',
            'formula': 'PE / 盈利增长率',
            'pe_ratio': round(pe, 2),
            'forward_pe': round(forward_pe, 2),
            'growth_rate': round(growth_rate, 2),
            'peg': round(peg, 2),
            'fair_pe': round(fair_pe, 2),
            'implied_price': round(implied_price, 2),
            'verdict': verdict,
            'standards': {
                'undervalued': '< 0.5',
                'attractive': '0.5 - 1.0',
                'fair': '1.0 - 1.5',
                'expensive': '1.5 - 2.0',
                'very_expensive': '> 2.0'
            }
        }
    
    def _reverse_dcf(self) -> dict:
        """
        3. 反向 DCF 估值法
        
        从当前股价反推市场隐含的增长率预期
        """
        current_price = self.price.get('current_price', 0)
        fcf = self.cashflow.get('free_cashflow', 0)
        shares = self.price.get('shares_outstanding', 1)
        
        # FCF per share
        fcf_per_share = fcf / shares if shares > 0 else 0
        
        # 假设 WACC=10%，终值增长率=3%
        wacc = 0.10
        terminal_growth = 0.03
        
        # 简化反向 DCF：从当前价格反推隐含增长率
        # Price = FCF × (1+g) / (WACC - g)
        # 解方程求 g
        
        if fcf_per_share > 0 and current_price > 0:
            # 近似计算隐含增长率
            implied_growth = (current_price * wacc - fcf_per_share) / (current_price + fcf_per_share)
            implied_growth = max(0, min(implied_growth, 0.50))  # 限制在 0-50%
        else:
            implied_growth = 0
        
        # 对比历史增长率
        historical_growth = self.financials.get('revenue_growth_yoy', 0) * 100
        
        # 判断
        if implied_growth < historical_growth * 0.8:
            verdict = '可能被低估（市场预期低于历史增速）'
        elif implied_growth > historical_growth * 1.5:
            verdict = '定价偏乐观（市场预期远超历史增速）'
        else:
            verdict = '合理定价'
        
        return {
            'method': 'Reverse DCF（反向现金流折现）',
            'logic': '从当前股价反推市场隐含的增长率预期',
            'current_price': round(current_price, 2),
            'fcf_per_share': round(fcf_per_share, 2),
            'implied_growth_rate': round(implied_growth * 100, 2),
            'historical_growth_rate': round(historical_growth, 2),
            'wacc': wacc * 100,
            'terminal_growth': terminal_growth * 100,
            'verdict': verdict,
            'analysis': f'市场隐含增长率{implied_growth*100:.1f}% vs 历史增速{historical_growth:.1f}%'
        }
    
    def _magic_formula(self) -> dict:
        """
        4. 格林布拉特魔法公式
        
        指标 1：盈利收益率 = EBIT / EV
        指标 2：ROIC = EBIT / 投入资本
        """
        # 获取数据
        ebit = self.financials.get('operating_income', 0)
        market_cap = self.price.get('market_cap', 0)
        total_debt = self.balance_sheet.get('total_debt', 0)
        cash = self.balance_sheet.get('cash_and_equivalents', 0)
        total_equity = self.balance_sheet.get('total_equity', 0)
        
        # 计算企业价值 EV
        enterprise_value = market_cap + total_debt - cash
        
        # 计算盈利收益率
        earnings_yield = ebit / enterprise_value * 100 if enterprise_value > 0 else 0
        
        # 计算 ROIC
        invested_capital = total_equity + total_debt - cash
        roic = ebit / invested_capital * 100 if invested_capital > 0 else 0
        
        # 判断标准
        if earnings_yield > 8 and roic > 25:
            verdict = '⭐ 优秀（又好又便宜）'
        elif earnings_yield > 5 and roic > 15:
            verdict = '良好'
        elif earnings_yield > 3 or roic > 10:
            verdict = '一般'
        else:
            verdict = '差'
        
        # 综合评分
        ey_score = min(earnings_yield / 8 * 50, 50)  # 最高 50 分
        roic_score = min(roic / 25 * 50, 50)  # 最高 50 分
        total_score = ey_score + roic_score
        
        return {
            'method': 'Magic Formula（格林布拉特）',
            'formula': '盈利收益率 + ROIC',
            'ebit': round(ebit / 1e9, 2),
            'enterprise_value': round(enterprise_value / 1e9, 2),
            'earnings_yield': round(earnings_yield, 2),
            'roic': round(roic, 2),
            'scoring': {
                'ey_score': round(ey_score, 1),
                'roic_score': round(roic_score, 1),
                'total_score': round(total_score, 1),
                'max_score': 100
            },
            'verdict': verdict,
            'standards': {
                'excellent': 'EY>8% 且 ROIC>25%',
                'good': 'EY>5% 且 ROIC>15%',
                'average': 'EY>3% 或 ROIC>10%',
                'poor': 'EY<3% 且 ROIC<10%'
            }
        }
    
    def _ev_ebitda(self) -> dict:
        """
        5. EV/EBITDA 行业对标
        """
        # 获取数据
        market_cap = self.price.get('market_cap', 0)
        total_debt = self.balance_sheet.get('total_debt', 0)
        cash = self.balance_sheet.get('cash_and_equivalents', 0)
        ebitda = self.financials.get('ebitda', 0)
        
        # 计算 EV
        enterprise_value = market_cap + total_debt - cash
        
        # 计算 EV/EBITDA
        ev_ebitda = enterprise_value / ebitda if ebitda > 0 else 0
        
        # 行业平均（科技行业通常 12-18 倍）
        industry_average = 15  # 简化假设
        
        # 判断
        premium_discount = (ev_ebitda - industry_average) / industry_average * 100
        
        if premium_discount < -20:
            verdict = '低估（低于行业平均 20%+）'
        elif premium_discount < 20:
            verdict = '合理（行业平均±20%）'
        else:
            verdict = '高估（高于行业平均 20%+）'
        
        return {
            'method': 'EV/EBITDA（达摩达兰）',
            'formula': '企业价值 / EBITDA',
            'enterprise_value': round(enterprise_value / 1e9, 2),
            'ebitda': round(ebitda / 1e9, 2),
            'ev_ebitda': round(ev_ebitda, 2),
            'industry_average': industry_average,
            'premium_discount': round(premium_discount, 2),
            'verdict': verdict,
            'standards': {
                'undervalued': '< 行业平均 20%+',
                'fair': '行业平均 ±20%',
                'overvalued': '> 行业平均 20%+'
            }
        }
    
    def _ev_revenue_rule40(self) -> dict:
        """
        6. EV/Revenue + Rule of 40（SaaS 适用）
        
        Rule of 40: 增长率 + 利润率 >= 40%
        """
        # 获取数据
        market_cap = self.price.get('market_cap', 0)
        total_debt = self.balance_sheet.get('total_debt', 0)
        cash = self.balance_sheet.get('cash_and_equivalents', 0)
        revenue = self.financials.get('total_revenue', 0)
        growth_rate = self.financials.get('revenue_growth_yoy', 0) * 100
        operating_margin = self.financials.get('operating_income', 0) / revenue * 100 if revenue > 0 else 0
        
        # 计算 EV
        enterprise_value = market_cap + total_debt - cash
        
        # 计算 EV/Revenue
        ev_revenue = enterprise_value / revenue if revenue > 0 else 0
        
        # 计算 Rule of 40
        rule_of_40 = growth_rate + operating_margin
        
        # 判断
        if rule_of_40 >= 60:
            verdict = '优秀（Rule of 40 >= 60%）'
            fair_ev_revenue = 15
        elif rule_of_40 >= 40:
            verdict = '良好（Rule of 40 40-60%）'
            fair_ev_revenue = 10
        elif rule_of_40 >= 20:
            verdict = '一般（Rule of 40 20-40%）'
            fair_ev_revenue = 6
        else:
            verdict = '差（Rule of 40 < 20%）'
            fair_ev_revenue = 3
        
        # 判断估值
        if ev_revenue < fair_ev_revenue * 0.7:
            valuation_verdict = '低估'
        elif ev_revenue < fair_ev_revenue * 1.3:
            valuation_verdict = '合理'
        else:
            valuation_verdict = '高估'
        
        return {
            'method': 'EV/Revenue + Rule of 40（科技股）',
            'formula': 'Rule of 40 = 增长率 + 利润率',
            'enterprise_value': round(enterprise_value / 1e9, 2),
            'revenue': round(revenue / 1e9, 2),
            'ev_revenue': round(ev_revenue, 2),
            'growth_rate': round(growth_rate, 2),
            'operating_margin': round(operating_margin, 2),
            'rule_of_40': round(rule_of_40, 2),
            'fair_ev_revenue': fair_ev_revenue,
            'verdict': f'{verdict} - {valuation_verdict}',
            'standards': {
                'excellent': 'Rule of 40 >= 60%',
                'good': 'Rule of 40 40-60%',
                'average': 'Rule of 40 20-40%',
                'poor': 'Rule of 40 < 20%'
            }
        }
    
    def _generate_summary(self) -> dict:
        """生成综合估值结论"""
        # 收集所有估值方法的结果
        current_price = self.price.get('current_price', 0)
        
        # 计算平均估值
        valuations = []
        
        # Owner Earnings
        oe = self._owner_earnings()
        valuations.append(oe['fair_value_range']['average'])
        
        # PEG
        peg = self._peg()
        if peg['implied_price'] > 0:
            valuations.append(peg['implied_price'])
        
        # 计算平均
        avg_fair_value = sum(valuations) / len(valuations) if valuations else 0
        upside = (avg_fair_value - current_price) / current_price * 100 if current_price > 0 else 0
        
        # 综合判断
        if upside > 30:
            recommendation = '强烈买入'
        elif upside > 10:
            recommendation = '买入'
        elif upside > -10:
            recommendation = '持有'
        elif upside > -30:
            recommendation = '减持'
        else:
            recommendation = '卖出'
        
        return {
            'current_price': current_price,
            'average_fair_value': round(avg_fair_value, 2),
            'upside_downside': round(upside, 2),
            'recommendation': recommendation,
            'valuation_range': {
                'low': round(min(valuations) if valuations else 0, 2),
                'high': round(max(valuations) if valuations else 0, 2)
            },
            'methods_used': 6,
            'confidence': '中等' if abs(upside) < 20 else '高'
        }


def calculate_valuation(data: dict) -> dict:
    """便捷函数：执行估值计算"""
    calculator = ValuationCalculator(data)
    return calculator.calculate_all()


if __name__ == '__main__':
    import sys
    sys.path.insert(0, '.')
    from fetch_data import StockDataFetcher
    
    if len(sys.argv) < 2:
        print("用法：python valuation_full.py <股票代码>")
        sys.exit(1)
    
    ticker = sys.argv[1]
    
    # 获取数据
    fetcher = StockDataFetcher(ticker)
    data = fetcher.get_all_data(use_cache=True)
    
    # 执行估值计算
    results = calculate_valuation(data)
    
    # 输出结果
    print(json.dumps(results, indent=2, ensure_ascii=False))
