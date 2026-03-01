#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Variant View 生成模块
识别市场共识的盲点，生成变异认知
"""

import sys
import json
from datetime import datetime


class VariantViewGenerator:
    """Variant View 生成器"""
    
    def __init__(self, ticker: str, data: dict):
        self.ticker = ticker
        self.data = data
        self.price = data.get('price', {})
        self.financials = data.get('financials', {})
        self.balance_sheet = data.get('balance_sheet', {})
        self.cashflow = data.get('cashflow', {})
        self.analyst = data.get('analyst_estimates', {})
        self.company_info = data.get('company_info', {})
    
    def generate(self) -> dict:
        """生成 Variant View"""
        print("🔍 生成 Variant View...")
        
        # 1. 获取市场共识
        consensus = self._get_market_consensus()
        
        # 2. 识别盲点
        blind_spots = self._identify_blind_spots()
        
        # 3. 生成变异认知
        variant_perception = self._generate_variant_perception(blind_spots)
        
        # 4. 评估置信度
        confidence = self._assess_confidence(variant_perception)
        
        # 5. 生成可执行观点
        actionable_view = self._generate_actionable_view(variant_perception)
        
        result = {
            'consensus': consensus,
            'blind_spots': blind_spots,
            'variant_perception': variant_perception,
            'confidence': confidence,
            'actionable_view': actionable_view
        }
        
        print(f"✅ Variant View 生成完成")
        print(f"   市场共识：{consensus['summary']}")
        print(f"   变异认知：{variant_perception['summary']}")
        print(f"   置信度：{confidence}")
        
        return result
    
    def _get_market_consensus(self) -> dict:
        """获取市场共识"""
        # 分析师评级
        strong_buy = self.analyst.get('strong_buy', 0)
        buy = self.analyst.get('buy', 0)
        hold = self.analyst.get('hold', 0)
        sell = self.analyst.get('sell', 0)
        strong_sell = self.analyst.get('strong_sell', 0)
        
        total = strong_buy + buy + hold + sell + strong_sell
        buy_ratio = (strong_buy + buy) / total * 100 if total > 0 else 0
        
        # 目标价
        target_price = self.analyst.get('target_price_mean', 0)
        current_price = self.price.get('current_price', 1)
        upside = (target_price - current_price) / current_price * 100 if current_price > 0 else 0
        
        # 估值水平
        pe = self.price.get('pe_ratio', 0)
        market_cap = self.price.get('market_cap', 0)
        
        # 生成共识总结
        if buy_ratio > 80:
            sentiment = '极度乐观'
        elif buy_ratio > 60:
            sentiment = '乐观'
        elif buy_ratio > 40:
            sentiment = '中性'
        elif buy_ratio > 20:
            sentiment = '悲观'
        else:
            sentiment = '极度悲观'
        
        summary = f'分析师{sentiment}（{buy_ratio:.1f}%买入），目标价${target_price:.2f}（{upside:+.1f}%）'
        
        return {
            'analyst_ratings': {
                'strong_buy': strong_buy,
                'buy': buy,
                'hold': hold,
                'sell': sell,
                'strong_sell': strong_sell,
                'buy_ratio': round(buy_ratio, 1)
            },
            'price_target': {
                'mean': target_price,
                'high': self.analyst.get('target_price_high', 0),
                'low': self.analyst.get('target_price_low', 0),
                'upside': round(upside, 1)
            },
            'valuation': {
                'pe': pe,
                'market_cap': market_cap
            },
            'sentiment': sentiment,
            'summary': summary
        }
    
    def _identify_blind_spots(self) -> list:
        """识别市场盲点"""
        blind_spots = []
        
        # 盲点 1：现金流被忽视
        fcf = self.cashflow.get('free_cashflow', 0)
        revenue = self.financials.get('total_revenue', 1)
        fcf_margin = fcf / revenue * 100 if revenue > 0 else 0
        
        net_income = self.financials.get('net_income', 0)
        income_margin = net_income / revenue * 100 if revenue > 0 else 0
        
        if fcf_margin < income_margin * 0.5:
            blind_spots.append({
                'type': '现金流盲点',
                'description': '市场关注利润增长，但自由现金流利润率偏低',
                'data': {
                    'fcf_margin': round(fcf_margin, 1),
                    'income_margin': round(income_margin, 1)
                },
                'implication': '利润质量可能有问题',
                'severity': '高' if fcf_margin < 5 else '中'
            })
        
        # 盲点 2：研发投入被低估
        rd_expense = self.financials.get('research_development', 0)
        if rd_expense > 0:
            rd_ratio = rd_expense / revenue * 100
            if rd_ratio > 15:
                blind_spots.append({
                    'type': '研发价值盲点',
                    'description': '高研发投入的长期价值未被充分定价',
                    'data': {
                        'rd_ratio': round(rd_ratio, 1)
                    },
                    'implication': '未来竞争力被低估',
                    'severity': '中'
                })
        
        # 盲点 3：增长质量
        revenue_growth = self.financials.get('revenue_growth_yoy', 0) * 100
        income_growth = self.financials.get('net_income_growth_yoy', 0) * 100
        
        if income_growth > revenue_growth * 2:
            blind_spots.append({
                'type': '增长质量盲点',
                'description': '利润增长远超收入增长，可能来自一次性因素',
                'data': {
                    'revenue_growth': round(revenue_growth, 1),
                    'income_growth': round(income_growth, 1)
                },
                'implication': '增长可持续性存疑',
                'severity': '中'
            })
        
        # 盲点 4：估值对比
        pe = self.price.get('pe_ratio', 0)
        if pe > 30:
            blind_spots.append({
                'type': '估值盲点',
                'description': '高估值下，市场可能忽视了下行风险',
                'data': {
                    'pe': round(pe, 1)
                },
                'implication': '估值容错空间小',
                'severity': '高' if pe > 40 else '中'
            })
        
        # 盲点 5：分析师过度一致
        buy_ratio = self.analyst.get('strong_buy', 0) + self.analyst.get('buy', 0)
        total = sum([
            self.analyst.get('strong_buy', 0),
            self.analyst.get('buy', 0),
            self.analyst.get('hold', 0),
            self.analyst.get('sell', 0),
            self.analyst.get('strong_sell', 0)
        ])
        consensus_buy = buy_ratio / total * 100 if total > 0 else 0
        
        if consensus_buy > 90:
            blind_spots.append({
                'type': '共识盲点',
                'description': '分析师观点过度一致，可能存在群体思维',
                'data': {
                    'consensus_buy_ratio': round(consensus_buy, 1)
                },
                'implication': '预期反转风险大',
                'severity': '高'
            })
        
        return blind_spots
    
    def _generate_variant_perception(self, blind_spots: list) -> dict:
        """生成变异认知"""
        if not blind_spots:
            return {
                'summary': '未发现明显市场盲点',
                'points': [],
                'direction': '中性'
            }
        
        # 分析盲点方向
        bullish_count = 0
        bearish_count = 0
        
        points = []
        for spot in blind_spots:
            if '低估' in spot.get('implication', ''):
                bullish_count += 1
                direction = '看多'
            elif '高估' in spot.get('implication', '') or '风险' in spot.get('implication', ''):
                bearish_count += 1
                direction = '看空'
            else:
                direction = '中性'
            
            points.append({
                'blind_spot': spot['type'],
                'market_thinks': f'市场认为{spot["description"].split("，")[0]}',
                'we_think': f'我们认为{spot["implication"]}',
                'direction': direction,
                'severity': spot['severity']
            })
        
        # 总体方向
        if bullish_count > bearish_count:
            overall_direction = '看多'
            summary = f'发现{bullish_count}个看多盲点，{bearish_count}个看空盲点 - 总体看多'
        elif bearish_count > bullish_count:
            overall_direction = '看空'
            summary = f'发现{bearish_count}个看空盲点，{bullish_count}个看多盲点 - 总体看空'
        else:
            overall_direction = '中性'
            summary = f'发现{len(blind_spots)}个盲点，多空因素相当 - 保持中性'
        
        return {
            'summary': summary,
            'points': points,
            'direction': overall_direction,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count
        }
    
    def _assess_confidence(self, variant_perception: dict) -> str:
        """评估置信度"""
        if not variant_perception.get('points'):
            return '低'
        
        # 根据盲点数量和严重程度评估
        high_severity_count = sum(1 for p in variant_perception['points'] if p.get('severity') == '高')
        total_points = len(variant_perception['points'])
        
        if high_severity_count >= 2 or total_points >= 4:
            return '高'
        elif high_severity_count >= 1 or total_points >= 2:
            return '中'
        else:
            return '低'
    
    def _generate_actionable_view(self, variant_perception: dict) -> dict:
        """生成可执行观点"""
        direction = variant_perception.get('direction', '中性')
        
        if direction == '看多':
            action = {
                'recommendation': '做多',
                'rationale': '市场低估了某些关键因素',
                'catalyst': '等待市场认识到这些盲点',
                'position_sizing': '可根据置信度适当放大仓位',
                'risk_management': '设置止损，防止判断错误'
            }
        elif direction == '看空':
            action = {
                'recommendation': '做空或减持',
                'rationale': '市场忽视了某些重大风险',
                'catalyst': '等待风险暴露',
                'position_sizing': '做空仓位不宜过大',
                'risk_management': '严格止损，做空风险无限'
            }
        else:
            action = {
                'recommendation': '观望',
                'rationale': '多空因素相当，缺乏明确方向',
                'catalyst': '等待新的催化剂',
                'position_sizing': '保持中性仓位',
                'risk_management': '观望为主'
            }
        
        return {
            **action,
            'variant_direction': direction,
            'key_monitoring_points': [p['blind_spot'] for p in variant_perception.get('points', [])]
        }


def generate_variant_view(ticker: str, data: dict) -> dict:
    """便捷函数：生成 Variant View"""
    generator = VariantViewGenerator(ticker, data)
    return generator.generate()


if __name__ == '__main__':
    sys.path.insert(0, 'modules')
    from fetch_data import StockDataFetcher
    
    if len(sys.argv) < 2:
        print("用法：python variant_view.py <股票代码>")
        sys.exit(1)
    
    ticker = sys.argv[1]
    
    # 获取数据
    fetcher = StockDataFetcher(ticker)
    data = fetcher.get_all_data(use_cache=True)
    
    # 生成 Variant View
    result = generate_variant_view(ticker, data)
    
    print("\n" + "=" * 60)
    print(f"{ticker} Variant View 分析")
    print("=" * 60)
    
    print(f"\n📊 市场共识:")
    print(f"   {result['consensus']['summary']}")
    
    print(f"\n🔍 市场盲点 ({len(result['blind_spots'])}个):")
    for i, spot in enumerate(result['blind_spots'], 1):
        print(f"   {i}. {spot['type']} ({spot['severity']}风险)")
        print(f"      描述：{spot['description']}")
        print(f"      含义：{spot['implication']}")
    
    print(f"\n💡 变异认知:")
    print(f"   {result['variant_perception']['summary']}")
    
    if result['variant_perception'].get('points'):
        print(f"\n   详细观点:")
        for i, point in enumerate(result['variant_perception']['points'], 1):
            print(f"   {i}. {point['blind_spot']}")
            print(f"      市场认为：{point['market_thinks']}")
            print(f"      我们认为：{point['we_think']}")
            print(f"      方向：{point['direction']}")
    
    print(f"\n🎯 置信度：{result['confidence']}")
    
    print(f"\n📋 可执行观点:")
    action = result['actionable_view']
    print(f"   建议：{action['recommendation']}")
    print(f"   理由：{action['rationale']}")
    print(f"   催化剂：{action['catalyst']}")
    print(f"   仓位：{action['position_sizing']}")
    print(f"   风控：{action['risk_management']}")
    
    print("\n" + "=" * 60)
