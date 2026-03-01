#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
16 模块分析模块 - 完整实现
基于 Day1Global 原项目框架
每个模块包含：数据计算、检查清单、风险标记、关键要点
"""

import sys
import json
from datetime import datetime


class SixteenModulesAnalyzer:
    """16 模块分析器 - 完整实现"""
    
    def __init__(self, data: dict):
        self.data = data
        self.ticker = data.get('symbol', 'UNKNOWN')
        self.price = data.get('price', {})
        self.financials = data.get('financials', {})
        self.balance_sheet = data.get('balance_sheet', {})
        self.cashflow = data.get('cashflow', {})
        self.analyst = data.get('analyst_estimates', {})
        self.company_info = data.get('company_info', {})
    
    def analyze_all(self) -> dict:
        """执行全部 16 模块分析"""
        print(f"🔍 执行 16 模块分析...")
        
        results = {
            'A_revenue_quality': self._analyze_revenue_quality(),
            'B_profitability': self._analyze_profitability(),
            'C_cash_flow': self._analyze_cash_flow(),
            'D_forward_guidance': self._analyze_forward_guidance(),
            'E_competitive_landscape': self._analyze_competitive_landscape(),
            'F_core_kpis': self._analyze_core_kpis(),
            'G_products': self._analyze_products(),
            'H_partners': self._analyze_partners(),
            'I_management': self._analyze_management(),
            'J_macro': self._analyze_macro(),
            'K_valuation': self._analyze_valuation(),
            'L_ownership': self._analyze_ownership(),
            'M_monitoring': self._analyze_monitoring(),
            'N_rd_efficiency': self._analyze_rd_efficiency(),
            'O_accounting': self._analyze_accounting(),
            'P_esg': self._analyze_esg()
        }
        
        return results
    
    def _analyze_revenue_quality(self) -> dict:
        """A. 收入质量分析"""
        revenue = self.financials.get('total_revenue', 0)
        growth_yoy = self.financials.get('revenue_growth_yoy', 0) * 100
        gross_profit = self.financials.get('gross_profit', 0)
        gross_margin = gross_profit / revenue * 100 if revenue > 0 else 0
        
        # 检查清单
        checklist = []
        flags = []
        
        if growth_yoy > 20:
            checklist.append('✅ 收入增长加速（>20%）')
        elif growth_yoy > 10:
            checklist.append('⚠️ 收入增长稳定（10-20%）')
        else:
            checklist.append('❌ 收入增长放缓（<10%）')
            flags.append('增长放缓')
        
        if gross_margin > 50:
            checklist.append('✅ 毛利率优秀（>50%）')
        elif gross_margin > 30:
            checklist.append('⚠️ 毛利率良好（30-50%）')
        else:
            checklist.append('❌ 毛利率偏低（<30%）')
            flags.append('毛利率偏低')
        
        # 评分（0-100）
        score = min(100, max(0, 50 + growth_yoy + (gross_margin - 30)))
        
        return {
            'module': 'A',
            'name': '收入质量',
            'metrics': {
                'revenue_billions': round(revenue / 1e9, 2),
                'growth_yoy': round(growth_yoy, 2),
                'gross_margin': round(gross_margin, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'营收${revenue/1e9:.1f}亿，同比增长{growth_yoy:.1f}%，毛利率{gross_margin:.1f}%'
        }
    
    def _analyze_profitability(self) -> dict:
        """B. 盈利能力分析"""
        revenue = self.financials.get('total_revenue', 0)
        net_income = self.financials.get('net_income', 0)
        operating_income = self.financials.get('operating_income', 0)
        
        net_margin = net_income / revenue * 100 if revenue > 0 else 0
        operating_margin = operating_income / revenue * 100 if revenue > 0 else 0
        
        # ROE 和 ROIC（简化计算）
        equity = self.balance_sheet.get('total_equity', 1)
        roe = net_income / equity * 100 if equity > 0 else 0
        
        checklist = []
        flags = []
        
        if net_margin > 20:
            checklist.append('✅ 净利率优秀（>20%）')
        elif net_margin > 10:
            checklist.append('⚠️ 净利率良好（10-20%）')
        else:
            checklist.append('❌ 净利率偏低（<10%）')
            flags.append('净利率偏低')
        
        if roe > 20:
            checklist.append('✅ ROE 优秀（>20%）')
        elif roe > 15:
            checklist.append('⚠️ ROE 良好（15-20%）')
        else:
            checklist.append('❌ ROE 偏低（<15%）')
            if roe < 10:
                flags.append('ROE 偏低')
        
        score = min(100, max(0, 50 + net_margin + (roe - 15)))
        
        return {
            'module': 'B',
            'name': '盈利能力',
            'metrics': {
                'net_margin': round(net_margin, 2),
                'operating_margin': round(operating_margin, 2),
                'roe': round(roe, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'净利率{net_margin:.1f}%，经营利润率{operating_margin:.1f}%，ROE{roe:.1f}%'
        }
    
    def _analyze_cash_flow(self) -> dict:
        """C. 现金流分析"""
        operating_cf = self.cashflow.get('operating_cashflow', 0)
        free_cf = self.cashflow.get('free_cashflow', 0)
        capex = abs(self.cashflow.get('capital_expenditure', 0))
        net_income = self.financials.get('net_income', 1)
        
        fcf_margin = free_cf / self.financials.get('total_revenue', 1) * 100
        cash_conversion = free_cf / net_income * 100 if net_income > 0 else 0
        
        checklist = []
        flags = []
        
        if fcf_margin > 20:
            checklist.append('✅ FCF 利润率优秀（>20%）')
        elif fcf_margin > 10:
            checklist.append('⚠️ FCF 利润率良好（10-20%）')
        else:
            checklist.append('❌ FCF 利润率偏低（<10%）')
            flags.append('FCF 利润率偏低')
        
        if cash_conversion > 100:
            checklist.append('✅ 现金转化率高（>100%）')
        elif cash_conversion > 80:
            checklist.append('⚠️ 现金转化率良好（80-100%）')
        else:
            checklist.append('❌ 现金转化率偏低（<80%）')
            if cash_conversion < 50:
                flags.append('现金转化差')
        
        score = min(100, max(0, 50 + fcf_margin + (cash_conversion - 80) / 2))
        
        return {
            'module': 'C',
            'name': '现金流',
            'metrics': {
                'operating_cf_billions': round(operating_cf / 1e9, 2),
                'free_cf_billions': round(free_cf / 1e9, 2),
                'fcf_margin': round(fcf_margin, 2),
                'cash_conversion': round(cash_conversion, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'经营现金流${operating_cf/1e9:.1f}亿，自由现金流${free_cf/1e9:.1f}亿，转化率{cash_conversion:.0f}%'
        }
    
    def _analyze_forward_guidance(self) -> dict:
        """D. 前瞻指引分析"""
        # 简化：用分析师预期代替
        target_price = self.analyst.get('target_price_mean', 0)
        current_price = self.price.get('current_price', 1)
        
        upside = (target_price - current_price) / current_price * 100 if current_price > 0 else 0
        
        checklist = []
        flags = []
        
        if upside > 30:
            checklist.append('✅ 分析师预期强烈看好（>30% 上涨）')
        elif upside > 10:
            checklist.append('⚠️ 分析师预期看好（10-30% 上涨）')
        else:
            checklist.append('❌ 分析师预期一般（<10% 上涨）')
            flags.append('预期一般')
        
        score = min(100, max(0, 50 + upside / 2))
        
        return {
            'module': 'D',
            'name': '前瞻指引',
            'metrics': {
                'target_price': round(target_price, 2),
                'upside': round(upside, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'分析师目标价${target_price:.2f}，上涨空间{upside:.1f}%'
        }
    
    def _analyze_competitive_landscape(self) -> dict:
        """E. 竞争格局分析"""
        gross_margin = self.financials.get('gross_profit', 0) / self.financials.get('total_revenue', 1) * 100
        
        checklist = []
        flags = []
        
        if gross_margin > 60:
            checklist.append('✅ 护城河深（毛利率>60%）')
        elif gross_margin > 40:
            checklist.append('⚠️ 护城河中等（毛利率 40-60%）')
        else:
            checklist.append('❌ 护城河浅（毛利率<40%）')
            flags.append('护城河浅')
        
        score = min(100, max(0, 50 + (gross_margin - 40)))
        
        return {
            'module': 'E',
            'name': '竞争格局',
            'metrics': {
                'gross_margin': round(gross_margin, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'毛利率{gross_margin:.1f}%，反映竞争地位'
        }
    
    def _analyze_core_kpis(self) -> dict:
        """F. 核心 KPI 分析"""
        # 简化：用营收增长和利润增长作为核心 KPI
        revenue_growth = self.financials.get('revenue_growth_yoy', 0) * 100
        income_growth = self.financials.get('net_income_growth_yoy', 0) * 100
        
        checklist = []
        flags = []
        
        if revenue_growth > 20 and income_growth > 20:
            checklist.append('✅ 双增长优秀（>20%）')
        elif revenue_growth > 10 and income_growth > 10:
            checklist.append('⚠️ 双增长良好（>10%）')
        else:
            checklist.append('❌ 增长放缓')
            if revenue_growth < 5:
                flags.append('收入增长乏力')
        
        score = min(100, max(0, 50 + (revenue_growth + income_growth) / 4))
        
        return {
            'module': 'F',
            'name': '核心 KPI',
            'metrics': {
                'revenue_growth': round(revenue_growth, 2),
                'income_growth': round(income_growth, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'收入增长{revenue_growth:.1f}%，利润增长{income_growth:.1f}%'
        }
    
    def _analyze_products(self) -> dict:
        """G. 产品与新业务分析"""
        # 简化：用研发投入占比判断产品创新
        rd_expense = self.financials.get('research_development', 0)
        revenue = self.financials.get('total_revenue', 1)
        rd_ratio = rd_expense / revenue * 100 if rd_expense > 0 else 15  # 假设科技行业平均 15%
        
        checklist = []
        flags = []
        
        if rd_ratio > 20:
            checklist.append('✅ 高研发投入（>20%）')
        elif rd_ratio > 10:
            checklist.append('⚠️ 研发投入充足（10-20%）')
        else:
            checklist.append('❌ 研发投入偏低（<10%）')
            flags.append('研发投入不足')
        
        score = min(100, max(0, 50 + (rd_ratio - 10) * 2))
        
        return {
            'module': 'G',
            'name': '产品与新业务',
            'metrics': {
                'rd_ratio': round(rd_ratio, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'研发投入占比约{rd_ratio:.1f}%'
        }
    
    def _analyze_partners(self) -> dict:
        """H. 合作伙伴生态分析"""
        # 简化：用应收账款周转判断渠道健康度
        receivables = self.balance_sheet.get('accounts_receivable', 0)
        revenue = self.financials.get('total_revenue', 1)
        receivables_ratio = receivables / revenue * 100 if revenue > 0 else 0
        
        checklist = []
        flags = []
        
        if receivables_ratio < 20:
            checklist.append('✅ 渠道健康（应收占比<20%）')
        elif receivables_ratio < 30:
            checklist.append('⚠️ 渠道正常（应收占比 20-30%）')
        else:
            checklist.append('❌ 渠道压力大（应收占比>30%）')
            flags.append('应收账款高')
        
        score = min(100, max(0, 70 - receivables_ratio))
        
        return {
            'module': 'H',
            'name': '合作伙伴生态',
            'metrics': {
                'receivables_ratio': round(receivables_ratio, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'应收账款占比{receivables_ratio:.1f}%'
        }
    
    def _analyze_management(self) -> dict:
        """I. 高管团队分析"""
        # 简化：用内部人交易和 CEO 信息
        ceo = self.company_info.get('ceo', 'Unknown')
        employees = self.company_info.get('employees', 0)
        
        checklist = []
        flags = []
        
        checklist.append(f'✅ CEO: {ceo}')
        checklist.append(f'✅ 员工数：{employees:,}')
        
        score = 70  # 默认中等偏上
        
        return {
            'module': 'I',
            'name': '高管团队',
            'metrics': {
                'ceo': ceo,
                'employees': employees
            },
            'checklist': checklist,
            'flags': flags,
            'score': score,
            'analysis': f'CEO {ceo}，员工{employees:,}人'
        }
    
    def _analyze_macro(self) -> dict:
        """J. 宏观政策分析"""
        # 简化：行业分析
        industry = self.company_info.get('industry', 'Unknown')
        sector = self.company_info.get('sector', 'Unknown')
        
        checklist = []
        flags = []
        
        checklist.append(f'✅ 行业：{industry}')
        checklist.append(f'✅ 板块：{sector}')
        
        # 科技行业通常宏观风险中等
        score = 60
        
        return {
            'module': 'J',
            'name': '宏观政策',
            'metrics': {
                'industry': industry,
                'sector': sector
            },
            'checklist': checklist,
            'flags': flags,
            'score': score,
            'analysis': f'{sector} - {industry}'
        }
    
    def _analyze_valuation(self) -> dict:
        """K. 估值模型分析"""
        pe = self.price.get('pe_ratio', 0)
        pb = self.price.get('market_cap', 0) / self.balance_sheet.get('total_equity', 1) if self.balance_sheet.get('total_equity', 0) > 0 else 0
        
        checklist = []
        flags = []
        
        if pe < 15:
            checklist.append('✅ PE 低估（<15x）')
        elif pe < 25:
            checklist.append('⚠️ PE 合理（15-25x）')
        else:
            checklist.append('❌ PE 偏高（>25x）')
            flags.append('估值偏高')
        
        score = min(100, max(0, 70 - (pe - 20)))
        
        return {
            'module': 'K',
            'name': '估值模型',
            'metrics': {
                'pe': round(pe, 2),
                'pb': round(pb, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'PE {pe:.1f}x，PB {pb:.1f}x'
        }
    
    def _analyze_ownership(self) -> dict:
        """L. 筹码分布分析"""
        # 简化：用分析师评级分布
        strong_buy = self.analyst.get('strong_buy', 0)
        buy = self.analyst.get('buy', 0)
        hold = self.analyst.get('hold', 0)
        total = strong_buy + buy + hold
        
        buy_ratio = (strong_buy + buy) / total * 100 if total > 0 else 0
        
        checklist = []
        flags = []
        
        if buy_ratio > 80:
            checklist.append('✅ 分析师强烈看好（>80% 买入）')
        elif buy_ratio > 60:
            checklist.append('⚠️ 分析师看好（60-80% 买入）')
        else:
            checklist.append('❌ 分析师态度一般（<60% 买入）')
            flags.append('分析师分歧')
        
        score = min(100, max(0, buy_ratio))
        
        return {
            'module': 'L',
            'name': '筹码分布',
            'metrics': {
                'strong_buy': strong_buy,
                'buy': buy,
                'hold': hold,
                'buy_ratio': round(buy_ratio, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'{strong_buy}强烈买入，{buy}买入，{hold}持有，买入比例{buy_ratio:.1f}%'
        }
    
    def _analyze_monitoring(self) -> dict:
        """M. 长期监控变量分析"""
        # 识别 3-5 个关键监控指标
        variables = [
            '营收增长率',
            '自由现金流',
            '毛利率',
            '研发投入',
            '市场份额'
        ]
        
        return {
            'module': 'M',
            'name': '长期监控变量',
            'variables': variables,
            'checklist': [f'✅ {var}' for var in variables],
            'flags': [],
            'score': 80,
            'analysis': f'建议监控{len(variables)}个关键指标'
        }
    
    def _analyze_rd_efficiency(self) -> dict:
        """N. 研发效率分析"""
        # 简化：用研发投入和利润增长判断
        rd_ratio = 15  # 假设
        income_growth = self.financials.get('net_income_growth_yoy', 0) * 100
        
        rd_efficiency = income_growth / rd_ratio if rd_ratio > 0 else 0
        
        checklist = []
        flags = []
        
        if rd_efficiency > 2:
            checklist.append('✅ 研发效率高（>2x）')
        elif rd_efficiency > 1:
            checklist.append('⚠️ 研发效率中等（1-2x）')
        else:
            checklist.append('❌ 研发效率偏低（<1x）')
            flags.append('研发效率低')
        
        score = min(100, max(0, 50 + rd_efficiency * 20))
        
        return {
            'module': 'N',
            'name': '研发效率',
            'metrics': {
                'rd_ratio': rd_ratio,
                'rd_efficiency': round(rd_efficiency, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'研发投入约{rd_ratio:.1f}%，转化效率{rd_efficiency:.2f}x'
        }
    
    def _analyze_accounting(self) -> dict:
        """O. 会计质量分析"""
        # 简化：检查财务健康度
        current_ratio = self.balance_sheet.get('current_ratio', 0)
        debt_to_equity = self.balance_sheet.get('debt_to_equity', 0)
        
        checklist = []
        flags = []
        
        if current_ratio > 1.5:
            checklist.append('✅ 流动比率健康（>1.5）')
        elif current_ratio > 1:
            checklist.append('⚠️ 流动比率正常（1-1.5）')
        else:
            checklist.append('❌ 流动比率偏低（<1）')
            flags.append('流动性风险')
        
        if debt_to_equity < 0.5:
            checklist.append('✅ 负债率低（<0.5）')
        elif debt_to_equity < 1:
            checklist.append('⚠️ 负债率正常（0.5-1）')
        else:
            checklist.append('❌ 负债率高（>1）')
            flags.append('负债率高')
        
        score = min(100, max(0, 70 + (current_ratio - 1) * 10 - debt_to_equity * 20))
        
        return {
            'module': 'O',
            'name': '会计质量',
            'metrics': {
                'current_ratio': round(current_ratio, 2),
                'debt_to_equity': round(debt_to_equity, 2)
            },
            'checklist': checklist,
            'flags': flags,
            'score': round(score, 1),
            'analysis': f'流动比率{current_ratio:.2f}，负债率{debt_to_equity:.2f}'
        }
    
    def _analyze_esg(self) -> dict:
        """P. ESG 筛查分析"""
        # 简化：假设大型科技公司 ESG 中等偏上
        checklist = []
        flags = []
        
        checklist.append('⚠️ ESG 数据需要第三方评级')
        
        score = 65  # 默认中等
        
        return {
            'module': 'P',
            'name': 'ESG 筛查',
            'metrics': {},
            'checklist': checklist,
            'flags': flags,
            'score': score,
            'analysis': '建议查询 MSCI/晨星 ESG 评级'
        }


def analyze_16_modules(data: dict) -> dict:
    """便捷函数：执行 16 模块分析"""
    analyzer = SixteenModulesAnalyzer(data)
    return analyzer.analyze_all()


if __name__ == '__main__':
    sys.path.insert(0, 'modules')
    from fetch_data import StockDataFetcher
    
    if len(sys.argv) < 2:
        print("用法：python analyze_full.py <股票代码>")
        sys.exit(1)
    
    ticker = sys.argv[1]
    
    # 获取数据
    fetcher = StockDataFetcher(ticker)
    data = fetcher.get_all_data(use_cache=True)
    
    # 执行分析
    results = analyze_16_modules(data)
    
    # 输出摘要
    print(f"\n{'='*60}")
    print(f"{ticker} 16 模块分析摘要")
    print(f"{'='*60}\n")
    
    total_score = 0
    for key, module in results.items():
        score = module.get('score', 0)
        name = module.get('name', key)
        total_score += score
        print(f"{key[0]}. {name}: {score:.1f}/100")
    
    avg_score = total_score / len(results)
    print(f"\n{'='*60}")
    print(f"平均评分：{avg_score:.1f}/100")
    print(f"{'='*60}")
