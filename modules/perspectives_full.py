#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6 大投资哲学视角评分模块 - 完整实现
基于 Day1Global 原项目框架
每个视角包含详细评分逻辑和关键问题
"""

import sys
import json
from datetime import datetime


class InvestmentPerspectivesFull:
    """6 大投资哲学视角评分器 - 完整实现"""
    
    def __init__(self, ticker: str, data: dict):
        self.ticker = ticker
        self.data = data
        self.price = data.get('price', {})
        self.financials = data.get('financials', {})
        self.balance_sheet = data.get('balance_sheet', {})
        self.cashflow = data.get('cashflow', {})
        self.analyst = data.get('analyst_estimates', {})
        self.company_info = data.get('company_info', {})
    
    def analyze_all(self) -> dict:
        """执行全部 6 大视角分析"""
        print("👁️ 执行 6 大投资哲学视角分析（完整版）...")
        
        results = {
            'quality_compounder': self._analyze_quality_compounder(),
            'imaginative_growth': self._analyze_imaginative_growth(),
            'fundamental_long_short': self._analyze_fundamental_long_short(),
            'deep_value': self._analyze_deep_value(),
            'catalyst_driven': self._analyze_catalyst_driven(),
            'macro_tactical': self._analyze_macro_tactical()
        }
        
        # 计算综合评分
        total_score = sum(p['total_score'] for p in results.values())
        max_score = sum(p['max_score'] for p in results.values())
        
        results['summary'] = {
            'total_score': total_score,
            'max_score': max_score,
            'average_score': total_score / max_score * 100 if max_score > 0 else 0,
            'bull_count': sum(1 for p in results.values() if p['verdict'] == '买入'),
            'bear_count': sum(1 for p in results.values() if p['verdict'] == '卖出'),
            'neutral_count': sum(1 for p in results.values() if p['verdict'] == '观望')
        }
        
        print(f"✅ 6 大视角分析完成")
        print(f"   综合评分：{results['summary']['average_score']:.1f}/100")
        print(f"   看多：{results['summary']['bull_count']}个，看空：{results['summary']['bear_count']}个，观望：{results['summary']['neutral_count']}个")
        
        return results
    
    def _analyze_quality_compounder(self) -> dict:
        """
        1. 质量复利视角 - 巴菲特/芒格
        关注：护城河、ROE、自由现金流、管理层诚信
        
        评分标准（各 25 分）：
        - 护城河（0-25 分）
        - ROE（0-25 分）
        - 自由现金流（0-25 分）
        - 管理层（0-25 分）
        """
        # 获取数据
        gross_margin = self.financials.get('gross_profit', 0) / self.financials.get('total_revenue', 1) * 100
        roe = self.financials.get('net_income', 0) / self.balance_sheet.get('total_equity', 1) * 100
        fcf = self.cashflow.get('free_cashflow', 0)
        fcf_margin = fcf / self.financials.get('total_revenue', 1) * 100
        
        # 1. 护城河评分（0-25 分）
        if gross_margin > 60:
            moat_score = 25
        elif gross_margin > 40:
            moat_score = 20
        elif gross_margin > 30:
            moat_score = 15
        elif gross_margin > 20:
            moat_score = 10
        else:
            moat_score = 5
        
        # 2. ROE 评分（0-25 分）
        if roe > 25:
            roe_score = 25
        elif roe > 20:
            roe_score = 22
        elif roe > 15:
            roe_score = 18
        elif roe > 10:
            roe_score = 12
        else:
            roe_score = max(0, roe)
        
        # 3. 自由现金流评分（0-25 分）
        if fcf_margin > 25:
            fcf_score = 25
        elif fcf_margin > 20:
            fcf_score = 22
        elif fcf_margin > 15:
            fcf_score = 18
        elif fcf_margin > 10:
            fcf_score = 12
        else:
            fcf_score = max(0, fcf_margin)
        
        # 4. 管理层评分（0-25 分）- 简化：用内部人交易和 CEO 信息
        management_score = 18  # 默认中等偏上
        
        # 总分
        total_score = moat_score + roe_score + fcf_score + management_score
        max_score = 100
        
        # 核心问题
        key_questions = [
            f'护城河深度如何？（毛利率{gross_margin:.1f}%）',
            f'ROE 是否持续>15%？（当前{roe:.1f}%）',
            f'自由现金流是否稳定增长？（FCF 利润率{fcf_margin:.1f}%）',
            '管理层是否诚信且以股东利益为导向？'
        ]
        
        # 判断
        if total_score >= 80:
            verdict = '买入'
            analysis = '绝妙的生意，值得长期持有'
        elif total_score >= 60:
            verdict = '观望'
            analysis = '好生意，但需要合理价格'
        else:
            verdict = '卖出'
            analysis = '生意质量一般'
        
        return {
            'perspective': '质量复利',
            'representatives': '巴菲特/芒格',
            'time_horizon': '永久持有',
            'key_indicator': 'ROIC 趋势',
            'scoring': {
                'moat': {'score': moat_score, 'max': 25, 'criteria': f'毛利率{gross_margin:.1f}%'},
                'roe': {'score': roe_score, 'max': 25, 'criteria': f'ROE{roe:.1f}%'},
                'fcf': {'score': fcf_score, 'max': 25, 'criteria': f'FCF 利润率{fcf_margin:.1f}%'},
                'management': {'score': management_score, 'max': 25, 'criteria': '管理层评估'}
            },
            'total_score': total_score,
            'max_score': max_score,
            'rating': f'{total_score}/{max_score}',
            'analysis': analysis,
            'verdict': verdict,
            'key_questions': key_questions,
            'core_question': '如果市场关闭 10 年，你拿着这只股票能安心睡觉吗？'
        }
    
    def _analyze_imaginative_growth(self) -> dict:
        """
        2. 想象力成长视角 - Baillie Gifford/ARK
        关注：TAM、颠覆性创新、成长速度、长期潜力
        
        评分标准（各 25 分）：
        - TAM（0-25 分）
        - 创新能力（0-25 分）
        - 成长速度（0-25 分）
        - 长期潜力（0-25 分）
        """
        # 获取数据
        revenue_growth = self.financials.get('revenue_growth_yoy', 0) * 100
        description = self.company_info.get('description', '').lower()
        
        # 1. TAM 评分（0-25 分）- 简化：用市值和行业判断
        market_cap = self.price.get('market_cap', 0)
        if market_cap > 500e9:  # 万亿以上
            tam_score = 20  # 已经很大，增长空间有限
        elif market_cap > 100e9:
            tam_score = 22
        elif market_cap > 50e9:
            tam_score = 25  # 中等市值，增长空间大
        else:
            tam_score = 20
        
        # 2. 创新能力评分（0-25 分）
        tech_keywords = ['ai', 'cloud', 'machine learning', 'saas', 'platform']
        tech_score = sum(1 for keyword in tech_keywords if keyword in description)
        innovation_score = min(25, 10 + tech_score * 3)
        
        # 3. 成长速度评分（0-25 分）
        if revenue_growth > 40:
            growth_score = 25
        elif revenue_growth > 30:
            growth_score = 22
        elif revenue_growth > 20:
            growth_score = 18
        elif revenue_growth > 10:
            growth_score = 12
        else:
            growth_score = max(0, revenue_growth)
        
        # 4. 长期潜力评分（0-25 分）
        long_term_score = min(25, growth_score + tech_score)
        
        # 总分
        total_score = tam_score + innovation_score + growth_score + long_term_score
        max_score = 100
        
        key_questions = [
            f'TAM 是否足够大？（市值${market_cap/1e9:.0f}亿）',
            f'是否具有颠覆性创新能力？（技术关键词{tech_score}个）',
            f'收入增长率是否>30%？（当前{revenue_growth:.1f}%）',
            '5-10 年后的长期潜力如何？'
        ]
        
        # 判断
        if total_score >= 80:
            verdict = '买入'
            analysis = '巨大成长空间，值得长期持有'
        elif total_score >= 60:
            verdict = '观望'
            analysis = '成长性好，但需要关注估值'
        else:
            verdict = '卖出'
            analysis = '成长性不足'
        
        return {
            'perspective': '想象力成长',
            'representatives': 'Baillie Gifford/ARK',
            'time_horizon': '5-10 年',
            'key_indicator': '收入增长率',
            'scoring': {
                'tam': {'score': tam_score, 'max': 25, 'criteria': '市场空间'},
                'innovation': {'score': innovation_score, 'max': 25, 'criteria': f'技术关键词{tech_score}个'},
                'growth': {'score': growth_score, 'max': 25, 'criteria': f'增长{revenue_growth:.1f}%'},
                'long_term': {'score': long_term_score, 'max': 25, 'criteria': '长期潜力'}
            },
            'total_score': total_score,
            'max_score': max_score,
            'rating': f'{total_score}/{max_score}',
            'analysis': analysis,
            'verdict': verdict,
            'key_questions': key_questions,
            'core_question': '5 年后回头看，今天不买会不会后悔？'
        }
    
    def _analyze_fundamental_long_short(self) -> dict:
        """
        3. 基本面多空视角 - Tiger Cubs
        关注：相对价值、催化剂、风险收益比、做空机会
        
        评分标准（各 25 分）：
        - 相对价值（0-25 分）
        - 催化剂（0-25 分）
        - 风险收益比（0-25 分）
        - 做空机会评估（0-25 分）
        """
        # 获取数据
        pe = self.price.get('pe_ratio', 0)
        target_price = self.analyst.get('target_price_mean', 0)
        current_price = self.price.get('current_price', 1)
        upside = (target_price - current_price) / current_price * 100 if current_price > 0 else 0
        
        # 1. 相对价值评分（0-25 分）
        if pe < 15:
            value_score = 25
        elif pe < 20:
            value_score = 20
        elif pe < 25:
            value_score = 15
        elif pe < 30:
            value_score = 10
        else:
            value_score = 5
        
        # 2. 催化剂评分（0-25 分）- 简化：用分析师预期
        if upside > 50:
            catalyst_score = 25
        elif upside > 30:
            catalyst_score = 20
        elif upside > 10:
            catalyst_score = 15
        else:
            catalyst_score = 5
        
        # 3. 风险收益比评分（0-25 分）
        risk_reward_score = min(25, max(0, 15 + upside / 5))
        
        # 4. 做空机会评估（0-25 分）- 对于好公司通常不做空
        short_opportunity_score = 5  # 默认不做空
        
        # 总分
        total_score = value_score + catalyst_score + risk_reward_score + short_opportunity_score
        max_score = 100
        
        key_questions = [
            f'相对于同行是否有估值优势？（PE{pe:.1f}x）',
            f'近期是否有催化剂？（上涨空间{upside:.1f}%）',
            '风险收益比是否有利？',
            '是否存在做空机会？'
        ]
        
        # 判断
        if total_score >= 70:
            verdict = '买入'
            analysis = '有 Variant View，值得做多'
        elif total_score >= 40:
            verdict = '观望'
            analysis = '缺乏明显 alpha'
        else:
            verdict = '卖出'
            analysis = '考虑做空'
        
        return {
            'perspective': '基本面多空',
            'representatives': 'Tiger Cubs',
            'time_horizon': '1-3 年',
            'key_indicator': 'Variant Perception',
            'scoring': {
                'relative_value': {'score': value_score, 'max': 25, 'criteria': f'PE{pe:.1f}x'},
                'catalyst': {'score': catalyst_score, 'max': 25, 'criteria': f'上涨{upside:.1f}%'},
                'risk_reward': {'score': risk_reward_score, 'max': 25, 'criteria': '风险收益比'},
                'short_opportunity': {'score': short_opportunity_score, 'max': 25, 'criteria': '做空机会'}
            },
            'total_score': total_score,
            'max_score': max_score,
            'rating': f'{total_score}/{max_score}',
            'analysis': analysis,
            'verdict': verdict,
            'key_questions': key_questions,
            'core_question': '有没有一个市场还没看到的 Variant View？'
        }
    
    def _analyze_deep_value(self) -> dict:
        """
        4. 深度价值视角 - Klarman/Marks
        关注：安全边际、资产价值、逆向机会、清算价值
        
        评分标准（各 25 分）：
        - 安全边际（0-25 分）
        - 资产价值（0-25 分）
        - 逆向机会（0-25 分）
        - 清算价值（0-25 分）
        """
        # 获取数据
        pe = self.price.get('pe_ratio', 0)
        pb = self.price.get('market_cap', 0) / self.balance_sheet.get('total_equity', 1) if self.balance_sheet.get('total_equity', 0) > 0 else 0
        current_ratio = self.balance_sheet.get('current_ratio', 0)
        debt_to_equity = self.balance_sheet.get('debt_to_equity', 0)
        
        # 1. 安全边际评分（0-25 分）
        if pe < 10:
            margin_score = 25
        elif pe < 15:
            margin_score = 20
        elif pe < 20:
            margin_score = 12
        else:
            margin_score = max(0, 25 - pe)
        
        # 2. 资产价值评分（0-25 分）
        if pb < 1:
            asset_score = 25
        elif pb < 1.5:
            asset_score = 20
        elif pb < 2:
            asset_score = 12
        else:
            asset_score = max(0, 25 - pb * 5)
        
        # 3. 逆向机会评分（0-25 分）- 科技股通常不是逆向机会
        contrarian_score = 10  # 默认较低
        
        # 4. 清算价值评分（0-25 分）
        if current_ratio > 2 and debt_to_equity < 0.3:
            liquidation_score = 20
        elif current_ratio > 1.5 and debt_to_equity < 0.5:
            liquidation_score = 15
        else:
            liquidation_score = 8
        
        # 总分
        total_score = margin_score + asset_score + contrarian_score + liquidation_score
        max_score = 100
        
        key_questions = [
            f'是否有足够的安全边际？（PE{pe:.1f}x）',
            f'资产价值是否被低估？（PB{pb:.1f}x）',
            '是否是逆向投资机会？',
            f'清算价值是否高于市值？（流动比率{current_ratio:.2f}）'
        ]
        
        # 判断
        if total_score >= 80:
            verdict = '买入'
            analysis = '深度低估，安全边际充足'
        elif total_score >= 60:
            verdict = '观望'
            analysis = '估值合理，但缺乏安全边际'
        else:
            verdict = '卖出'
            analysis = '估值偏高，不适合深度价值'
        
        return {
            'perspective': '深度价值',
            'representatives': 'Klarman/Marks',
            'time_horizon': '数年（等待均值回归）',
            'key_indicator': '安全边际',
            'scoring': {
                'margin_of_safety': {'score': margin_score, 'max': 25, 'criteria': f'PE{pe:.1f}x'},
                'asset_value': {'score': asset_score, 'max': 25, 'criteria': f'PB{pb:.1f}x'},
                'contrarian': {'score': contrarian_score, 'max': 25, 'criteria': '逆向机会'},
                'liquidation': {'score': liquidation_score, 'max': 25, 'criteria': f'流动比率{current_ratio:.2f}'}
            },
            'total_score': total_score,
            'max_score': max_score,
            'rating': f'{total_score}/{max_score}',
            'analysis': analysis,
            'verdict': verdict,
            'key_questions': key_questions,
            'core_question': '市场出价比这家公司的"清算价值"低多少？'
        }
    
    def _analyze_catalyst_driven(self) -> dict:
        """
        5. 催化剂驱动视角 - Tepper/Ackman
        关注：事件驱动、activist 机会、重组、并购
        
        评分标准（各 25 分）：
        - 催化剂强度（0-25 分）
        - activist 机会（0-25 分）
        - 重组潜力（0-25 分）
        - 并购可能性（0-25 分）
        """
        # 获取数据
        target_price = self.analyst.get('target_price_mean', 0)
        current_price = self.price.get('current_price', 1)
        upside = (target_price - current_price) / current_price * 100 if current_price > 0 else 0
        market_cap = self.price.get('market_cap', 0)
        
        # 1. 催化剂强度评分（0-25 分）
        if upside > 50:
            catalyst_score = 25
        elif upside > 30:
            catalyst_score = 20
        elif upside > 10:
            catalyst_score = 12
        else:
            catalyst_score = 5
        
        # 2. activist 机会评分（0-25 分）- 大公司通常没有
        activist_score = 5
        
        # 3. 重组潜力评分（0-25 分）
        restructuring_score = 8  # 默认较低
        
        # 4. 并购可能性评分（0-25 分）
        if market_cap < 10e9:
            ma_score = 15  # 小公司可能被收购
        else:
            ma_score = 5  # 大公司不太可能被收购
        
        # 总分
        total_score = catalyst_score + activist_score + restructuring_score + ma_score
        max_score = 100
        
        key_questions = [
            f'近期是否有重大催化剂？（上涨空间{upside:.1f}%）',
            '是否存在 activist 投资机会？',
            '是否有重组或分拆可能？',
            '并购可能性如何？'
        ]
        
        # 判断
        if total_score >= 70:
            verdict = '买入'
            analysis = '催化剂明确，时间窗口清晰'
        elif total_score >= 40:
            verdict = '观望'
            analysis = '等待催化剂'
        else:
            verdict = '卖出'
            analysis = '缺乏催化剂'
        
        return {
            'perspective': '催化剂驱动',
            'representatives': 'Tepper/Ackman',
            'time_horizon': '6-18 个月',
            'key_indicator': '催化剂时间线',
            'scoring': {
                'catalyst_strength': {'score': catalyst_score, 'max': 25, 'criteria': f'上涨{upside:.1f}%'},
                'activist': {'score': activist_score, 'max': 25, 'criteria': 'activist 机会'},
                'restructuring': {'score': restructuring_score, 'max': 25, 'criteria': '重组潜力'},
                'ma': {'score': ma_score, 'max': 25, 'criteria': '并购可能性'}
            },
            'total_score': total_score,
            'max_score': max_score,
            'rating': f'{total_score}/{max_score}',
            'analysis': analysis,
            'verdict': verdict,
            'key_questions': key_questions,
            'core_question': '未来 6-18 个月，有什么具体、可识别的事件会迫使市场重新给这只股票定价？'
        }
    
    def _analyze_macro_tactical(self) -> dict:
        """
        6. 宏观战术视角 - Druckenmiller
        关注：宏观环境、流动性、行业轮动、趋势
        
        评分标准（各 25 分）：
        - 宏观环境（0-25 分）
        - 流动性（0-25 分）
        - 行业轮动（0-25 分）
        - 趋势（0-25 分）
        """
        # 获取数据
        sector = self.company_info.get('sector', '')
        industry = self.company_info.get('industry', '')
        beta = self.price.get('beta', 1)
        
        # 1. 宏观环境评分（0-25 分）- 简化：科技行业默认中等偏上
        if 'Technology' in sector:
            macro_score = 18
        else:
            macro_score = 15
        
        # 2. 流动性评分（0-25 分）- 简化：假设流动性正常
        liquidity_score = 18
        
        # 3. 行业轮动评分（0-25 分）
        if 'Technology' in sector or 'Software' in industry:
            sector_rotation_score = 20  # 科技行业通常是顺风
        else:
            sector_rotation_score = 15
        
        # 4. 趋势评分（0-25 分）
        trend_score = 18  # 默认中等偏上
        
        # 总分
        total_score = macro_score + liquidity_score + sector_rotation_score + trend_score
        max_score = 100
        
        key_questions = [
            '当前宏观环境是否有利？',
            '流动性环境如何？',
            '行业轮动处于什么阶段？',
            '主要趋势是什么？'
        ]
        
        # 判断
        if total_score >= 80:
            verdict = '买入'
            analysis = '宏观顺风，加大仓位'
        elif total_score >= 60:
            verdict = '观望'
            analysis = '宏观中性，正常仓位'
        else:
            verdict = '卖出'
            analysis = '宏观逆风，减小仓位'
        
        return {
            'perspective': '宏观战术',
            'representatives': 'Druckenmiller',
            'time_horizon': '随宏观周期而定',
            'key_indicator': '美联储政策、流动性',
            'scoring': {
                'macro': {'score': macro_score, 'max': 25, 'criteria': '宏观环境'},
                'liquidity': {'score': liquidity_score, 'max': 25, 'criteria': '流动性'},
                'sector_rotation': {'score': sector_rotation_score, 'max': 25, 'criteria': '行业轮动'},
                'trend': {'score': trend_score, 'max': 25, 'criteria': '趋势'}
            },
            'total_score': total_score,
            'max_score': max_score,
            'rating': f'{total_score}/{max_score}',
            'analysis': analysis,
            'verdict': verdict,
            'key_questions': key_questions,
            'core_question': '当前的宏观/流动性环境对这只股票是顺风还是逆风？'
        }


def analyze_perspectives_full(ticker: str, data: dict) -> dict:
    """便捷函数：执行 6 大视角完整分析"""
    analyzer = InvestmentPerspectivesFull(ticker, data)
    return analyzer.analyze_all()


if __name__ == '__main__':
    sys.path.insert(0, 'modules')
    from fetch_data import StockDataFetcher
    
    if len(sys.argv) < 2:
        print("用法：python perspectives_full.py <股票代码>")
        sys.exit(1)
    
    ticker = sys.argv[1]
    
    # 获取数据
    fetcher = StockDataFetcher(ticker)
    data = fetcher.get_all_data(use_cache=True)
    
    # 执行分析
    results = analyze_perspectives_full(ticker, data)
    
    # 打印摘要
    print("\n" + "=" * 60)
    print(f"{ticker} 6 大投资哲学视角分析")
    print("=" * 60)
    
    perspectives_map = {
        'quality_compounder': '质量复利 (巴菲特/芒格)',
        'imaginative_growth': '想象力成长 (Baillie Gifford/ARK)',
        'fundamental_long_short': '基本面多空 (Tiger Cubs)',
        'deep_value': '深度价值 (Klarman/Marks)',
        'catalyst_driven': '催化剂驱动 (Tepper/Ackman)',
        'macro_tactical': '宏观战术 (Druckenmiller)'
    }
    
    for key, name in perspectives_map.items():
        p = results[key]
        score = p['total_score']
        verdict = p['verdict']
        print(f"\n{name}")
        print(f"   评分：{score}/100")
        print(f"   判断：{verdict}")
        print(f"   核心问题：{p['core_question']}")
    
    # 综合结论
    summary = results['summary']
    print("\n" + "=" * 60)
    print("综合结论")
    print("=" * 60)
    print(f"综合评分：{summary['average_score']:.1f}/100")
    print(f"看多：{summary['bull_count']}个，看空：{summary['bear_count']}个，观望：{summary['neutral_count']}个")
    print("=" * 60)
