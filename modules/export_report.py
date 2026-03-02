#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告导出模块 - 专业投资报告风格（最终优化版）
统一字体、颜色、间距等设计规范，增加详细内容描述，优化布局
"""

import sys
from datetime import datetime
from pathlib import Path


class ReportExporter:
    """专业投资报告导出器"""
    
    def __init__(self, analysis_result: dict):
        self.result = analysis_result
        self.ticker = analysis_result.get('ticker', 'UNKNOWN')
        self.data = analysis_result.get('data', {})
        self.modules = analysis_result.get('modules', {})
        self.perspectives = analysis_result.get('perspectives', {})
        self.valuation = analysis_result.get('valuation', {})
        self.key_forces = analysis_result.get('key_forces', [])
        self.biases = analysis_result.get('biases', {})
        self.variant_view = analysis_result.get('variant_view', {})
        self.summary = analysis_result.get('summary', {})
    
    def export_html(self, filename: str = None) -> str:
        """导出 HTML 格式报告"""
        if not filename:
            filename = f"{self.ticker}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = self.output_dir / filename
        content = self._generate_detailed_html()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ HTML 报告已导出：{filepath}")
        return str(filepath)
    
    def _generate_detailed_html(self) -> str:
        """生成详细的 HTML 报告 - 专业投资报告风格（最终优化版）"""
        html = []
        
        # ========== 统一的 HTML 头部和 CSS 样式 ==========
        html.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech Earnings Deep Dive - 投资分析报告</title>
    <style>
        /* ========== 全局样式 ========== */
        body {
            font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
            line-height: 1.6;
            max-width: 1100px;
            margin: 0 auto;
            padding: 30px 20px;
            background: #fff;
            color: #333;
            font-size: 14px;
        }
        
        .container {
            background: #fff;
            padding: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
        }
        
        /* ========== 标题层级 ========== */
        h1 {
            color: #1a1a1a;
            border-bottom: 2px solid #333;
            padding-bottom: 15px;
            font-size: 26px;
            font-weight: 600;
            margin-bottom: 25px;
        }
        
        h2 {
            color: #333;
            border-left: 4px solid #333;
            padding-left: 15px;
            margin-top: 35px;
            margin-bottom: 20px;
            font-size: 20px;
            font-weight: 600;
        }
        
        h3 {
            color: #555;
            font-size: 16px;
            margin-top: 20px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        h4 {
            color: #666;
            font-size: 14px;
            margin-top: 15px;
            margin-bottom: 10px;
            font-weight: 600;
        }
        
        /* ========== 表格样式 ========== */
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 13px;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background: #333;
            color: #fff;
            font-weight: 600;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        /* ========== 评分颜色 ========== */
        .score-high {
            color: #2e7d32;
            font-weight: 600;
        }
        
        .score-medium {
            color: #f57c00;
            font-weight: 600;
        }
        
        .score-low {
            color: #c62828;
            font-weight: 600;
        }
        
        /* ========== 卡片样式 ========== */
        .report-summary {
            background: #f9f9f9;
            padding: 25px;
            border-left: 4px solid #333;
            margin: 20px 0;
            border-radius: 4px;
        }
        
        .summary-content {
            color: #333;
            font-size: 14px;
            line-height: 1.8;
            text-align: justify;
        }
        
        .summary-box {
            background: #f5f5f5;
            padding: 18px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin: 15px 0;
        }
        
        .warning-box {
            background: #fff8e1;
            padding: 15px;
            border: 1px solid #ffe082;
            border-radius: 4px;
            margin: 15px 0;
        }
        
        .risk-box {
            background: #ffebee;
            padding: 15px;
            border: 1px solid #ef9a9a;
            border-radius: 4px;
            margin: 15px 0;
        }
        
        /* ========== 网格布局 ========== */
        .key-forces-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin: 15px 0;
        }
        
        .modules-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 15px 0;
        }
        
        .perspectives-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin: 15px 0;
        }
        
        /* ========== 页脚 ========== */
        .footer {
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            color: #757575;
            font-size: 12px;
            text-align: center;
        }
        
        /* ========== 打印优化 ========== */
        @media print {
            body {
                padding: 0;
                max-width: none;
            }
            
            .container {
                border: none;
                padding: 20px;
            }
            
            h2 {
                page-break-after: avoid;
            }
            
            table {
                page-break-inside: avoid;
            }
        }
    </style>
</head>
<body>
    <div class="container">
""")
        
        # ========== 报告标题 ==========
        html.append(f"""        <h1>📊 Tech Earnings Deep Dive - {self.ticker} 投资分析报告</h1>
        <p><strong>生成时间：</strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
""")
        
        # ========== 投资摘要 ==========
        html.append(self._generate_summary_section())
        
        # ========== 16 模块分析 ==========
        html.append(self._generate_modules_section())
        
        # ========== 6 大投资视角 ==========
        html.append(self._generate_perspectives_section())
        
        # ========== Key Forces ==========
        html.append(self._generate_key_forces_section())
        
        # ========== 估值矩阵 ==========
        html.append(self._generate_valuation_section())
        
        # ========== 反偏见框架 ==========
        html.append(self._generate_biases_section())
        
        # ========== Pre-Mortem ==========
        html.append(self._generate_premortem_section())
        
        # ========== 页脚 ==========
        html.append("""        <div class="footer">
            <p>基于 Day1Global 框架 · 复刻专业投资机构分析方法论</p>
            <p>最后更新：""" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        </div>
    </div>
</body>
</html>""")
        
        return "\n".join(html)
    
    def _generate_summary_section(self) -> str:
        """生成投资摘要部分 - 包含股票类型和投资策略"""
        summary = self.summary
        score = summary.get('overall_score', 0)
        recommendation = summary.get('recommendation', 'N/A')
        confidence = summary.get('confidence', 'N/A')
        valuation_upside = summary.get('valuation_upside', 0)
        
        score_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
        
        # 获取财务数据用于股票类型判断
        modules = self.modules
        pe = modules.get('K_valuation', {}).get('metrics', {}).get('pe', 0)
        revenue_growth = modules.get('F_core_kpis', {}).get('metrics', {}).get('revenue_growth', 0)
        dividend_yield = modules.get('L_ownership', {}).get('metrics', {}).get('dividend_yield', 0)
        roe = modules.get('B_profitability', {}).get('metrics', {}).get('roe', 0)
        
        # 判断股票类型
        stock_type, stock_description = self._analyze_stock_type(pe, revenue_growth, dividend_yield, roe)
        
        # 生成详细描述
        description = f"本报告对 {self.ticker} 进行了全面的财务分析和投资价值评估。"
        
        if score >= 70:
            description += f" 综合评分为{score:.1f}分，显示该公司整体表现优秀，在多个关键维度展现出强劲的竞争力和增长潜力。"
        elif score >= 60:
            description += f" 综合评分为{score:.1f}分，显示该公司整体表现良好，基本面稳健，具备一定投资价值，但需关注部分风险因素。"
        elif score >= 50:
            description += f" 综合评分为{score:.1f}分，显示该公司整体表现一般，基本面存在分化，建议谨慎评估，重点关注风险因素。"
        else:
            description += f" 综合评分为{score:.1f}分，显示该公司整体表现较弱，基本面存在较多问题，风险因素较多，建议谨慎或回避。"
        
        description += f" 基于综合分析，给予'<span class='{score_class}'>{recommendation}</span>'评级，置信度为{confidence}。"
        
        if abs(valuation_upside) > 20:
            if valuation_upside > 0:
                description += f" 估值分析显示当前股价存在{valuation_upside:.1f}%的上涨空间，具备较强吸引力。"
            else:
                description += f" 估值分析显示当前股价偏高，存在{abs(valuation_upside):.1f}%的回调风险。"
        else:
            description += f" 估值处于合理区间，估值风险可控。"
        
        return f"""        <h2>📋 投资摘要</h2>
        <div class="report-summary">
            <div class="summary-content">
                <p>{description}</p>
                <p style="margin-top: 15px;"><strong>股票类型：</strong>{stock_type}</p>
                <p style="margin-top: 10px;"><strong>类型分析：</strong>{stock_description}</p>
                <p style="margin-top: 15px;"><strong>关键指标说明：</strong></p>
                <ul>
                    <li><strong>综合评分：</strong>基于 16 个财务模块、6 大投资视角、6 种估值方法的综合评分，满分 100 分。≥70 分为优秀，60-70 分为良好，50-60 分为一般，<50 分为较弱。</li>
                    <li><strong>投资建议：</strong>根据综合评分和估值分析给出的投资建议，包括强烈买入、买入、持有、减持、卖出五个等级。</li>
                    <li><strong>置信度：</strong>反映分析结果的可靠程度，分为高、中、低三个等级，取决于数据完整性和一致性。</li>
                    <li><strong>估值空间：</strong>基于 6 种估值方法的平均结果，显示当前股价相对于合理价值的涨跌空间百分比。</li>
                </ul>
            </div>
        </div>
"""
    
    def _generate_modules_section(self) -> str:
        """生成 16 模块分析部分 - 分析内容列显示具体数值"""
        html = []
        html.append('        <h2>📊 模块分析</h2>')
        html.append('        <p>16 模块分析是系统的核心分析框架，覆盖收入质量、盈利能力、现金流、竞争格局等关键维度。每个模块都有独立的评分逻辑和检查清单，确保分析的全面性和深度。</p>')
        html.append('        <table>')
        html.append('            <thead>')
        html.append('                <tr>')
        html.append('                    <th>模块</th>')
        html.append('                    <th>分析内容</th>')
        html.append('                    <th>评分</th>')
        html.append('                    <th>等级</th>')
        html.append('                </tr>')
        html.append('            </thead>')
        html.append('            <tbody>')
        
        for key, module in sorted(self.modules.items(), key=lambda x: x[1]['score'], reverse=True):
            score = module['score']
            name = module['name']
            rating = "⭐⭐⭐⭐⭐" if score >= 80 else "⭐⭐⭐⭐" if score >= 60 else "⭐⭐⭐"
            score_class = 'score-high' if score >= 80 else 'score-medium' if score >= 60 else 'score-low'
            metrics = module.get('metrics', {})
            
            # 根据模块类型生成具体的数值描述
            if key[0] == 'A':
                description = f"收入=${metrics.get('revenue_billions', 0):.1f}亿，增长={metrics.get('growth_yoy', 0):.1f}%，毛利率={metrics.get('gross_margin', 0):.1f}%"
            elif key[0] == 'B':
                description = f"净利率={metrics.get('net_margin', 0):.1f}%，ROE={metrics.get('roe', 0):.1f}%，运营利润率={metrics.get('operating_margin', 0):.1f}%"
            elif key[0] == 'C':
                description = f"经营现金流=${metrics.get('operating_cf_billions', 0):.1f}亿，自由现金流=${metrics.get('free_cf_billions', 0):.1f}亿，FCF 利润率={metrics.get('fcf_margin', 0):.1f}%"
            elif key[0] == 'D':
                description = f"目标价=${metrics.get('target_price', 0):.1f}，上涨空间={metrics.get('upside', 0):.1f}%"
            elif key[0] == 'E':
                description = f"毛利率={metrics.get('gross_margin', 0):.1f}%（护城河指标）"
            elif key[0] == 'F':
                description = f"收入增长={metrics.get('revenue_growth', 0):.1f}%，利润增长={metrics.get('income_growth', 0):.1f}%"
            elif key[0] == 'G':
                description = f"研发投入={metrics.get('rd_ratio', 0):.1f}%"
            elif key[0] == 'H':
                description = f"应收占收入={metrics.get('receivables_ratio', 0):.1f}%"
            elif key[0] == 'I':
                description = f"CEO={metrics.get('ceo', 'N/A')}，员工数={metrics.get('employees', 0):,}"
            elif key[0] == 'J':
                description = f"行业={metrics.get('industry', 'N/A')}，板块={metrics.get('sector', 'N/A')}"
            elif key[0] == 'K':
                description = f"PE={metrics.get('pe', 0):.1f}x，PB={metrics.get('pb', 0):.1f}x"
            elif key[0] == 'L':
                description = f"强烈买入={metrics.get('strong_buy', 0)}，买入={metrics.get('buy', 0)}，买入比例={metrics.get('buy_ratio', 0):.1f}%"
            elif key[0] == 'M':
                description = f"5 个关键长期监控指标评估"
            elif key[0] == 'N':
                description = f"研发投入={metrics.get('rd_ratio', 0):.1f}%，研发效率={metrics.get('rd_efficiency', 0):.1f}x"
            elif key[0] == 'O':
                description = f"流动比率={metrics.get('current_ratio', 0):.1f}，负债率={metrics.get('debt_to_equity', 0):.1f}"
            elif key[0] == 'P':
                description = f"ESG（环境、社会、治理）基础评估"
            else:
                description = '详细分析内容'
            
            html.append(f'                <tr>')
            html.append(f'                    <td>{key[0]}. {name}</td>')
            html.append(f'                    <td>{description}</td>')
            html.append(f'                    <td class="{score_class}">{score:.1f}/100</td>')
            html.append(f'                    <td>{rating}</td>')
            html.append(f'                </tr>')
        
        html.append('            </tbody>')
        html.append('        </table>')
        html.append('')
        
        return "\n".join(html)
    
    def _analyze_stock_type(self, pe, revenue_growth, dividend_yield, roe):
        """分析股票类型并给出投资策略"""
        # 判断股票类型
        if revenue_growth > 20 and pe > 30:
            stock_type = "成长股"
            description = f"高增长（收入增长{revenue_growth:.1f}%）、高估值（PE {pe:.1f}x），典型成长股特征。适合成长型投资者，看好未来增长潜力，能承受高波动。投资策略：小仓位配置，长期持有（3-5 年），增长放缓时卖出。"
        elif pe < 15 and revenue_growth < 10:
            if dividend_yield > 4:
                stock_type = "价值股（高股息）"
                description = f"低增长（收入增长{revenue_growth:.1f}%）、低估值（PE {pe:.1f}x）、高分红（股息率{dividend_yield:.1f}%），典型价值股特征。适合价值型投资者，追求稳定现金流和安全边际。投资策略：重仓配置，长期持有收股息，价值回归时卖出。"
            else:
                stock_type = "价值股"
                description = f"低增长（收入增长{revenue_growth:.1f}%）、低估值（PE {pe:.1f}x），典型价值股特征。适合价值型投资者，相信价值会回归。投资策略：等待价值回归，或长期持有等待市场发现。"
        elif 15 <= pe <= 30 and 10 <= revenue_growth <= 20:
            stock_type = "成长 + 价值股"
            description = f"适中增长（收入增长{revenue_growth:.1f}%）、合理估值（PE {pe:.1f}x），成长与价值平衡。适合平衡型投资者，兼顾成长性和安全性。投资策略：中等仓位，长期持有。"
        elif pe > 50 and revenue_growth > 50:
            stock_type = "投机型成长股"
            description = f"超高增长（收入增长{revenue_growth:.1f}%）、超高估值（PE {pe:.1f}x），投机特征明显。适合激进型投资者，高风险高回报。投资策略：小仓位投机，快进快出，设置止损。"
        else:
            stock_type = "混合型股票"
            description = f"增长{revenue_growth:.1f}%、PE {pe:.1f}x，特征不明显，需要结合其他因素分析。投资策略：谨慎评估，小仓位试探。"
        
        return stock_type, description
    
    def _generate_perspectives_section(self) -> str:
        """生成 6 大投资视角部分 - 分析内容在核心问题下，评分和判断同行"""
        html = []
        html.append('        <h2>💼 投资视角</h2>')
        html.append('        <p>整合 6 种截然不同的投资世界观，每种视角都有独特的评分维度（各 25 分，总分 100 分）和核心问题。通过多视角交叉验证，避免单一方法论的盲点。</p>')
        html.append('        <div class="perspectives-grid">')
        
        perspectives_map = {
            'quality_compounder': ('质量复利', '巴菲特/芒格', '市场关闭 10 年能安心睡觉吗？', '评估公司护城河深度、ROE 持续性、自由现金流稳定性和管理层质量'),
            'imaginative_growth': ('想象力成长', 'Baillie Gifford/ARK', '5 年后不买会后悔吗？', '评估市场空间规模、技术创新能力、成长速度和长期发展潜力'),
            'fundamental_long_short': ('基本面多空', 'Tiger Cubs', '有 Variant View 吗？', '评估相对价值、催化剂、风险收益比和做空机会'),
            'deep_value': ('深度价值', 'Klarman/Marks', '比清算价值低多少？', '评估安全边际、资产价值、逆向投资机会和清算价值'),
            'catalyst_driven': ('催化剂驱动', 'Tepper/Ackman', '6-18 个月有什么催化剂？', '评估催化剂强度、activist 机会、重组潜力和并购可能性'),
            'macro_tactical': ('宏观战术', 'Druckenmiller', '宏观是顺风还是逆风？', '评估宏观环境、流动性、行业轮动和市场趋势')
        }
        
        for key, (name, reps, question, analysis_content) in perspectives_map.items():
            if key in self.perspectives:
                p = self.perspectives[key]
                score = p['total_score']
                verdict = p['verdict']
                score_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
                scoring = p.get('scoring', {})
                
                # 生成评分维度详情（显示具体数值和中文名称）
                dim_names = {
                    'moat': '护城河', 'roe': 'ROE', 'fcf': '自由现金流', 'management': '管理层',
                    'tam': '市场空间', 'innovation': '创新能力', 'growth': '成长速度', 'long_term': '长期潜力',
                    'relative_value': '相对价值', 'catalyst': '催化剂', 'risk_reward': '风险收益', 'short_opportunity': '做空机会',
                    'margin_of_safety': '安全边际', 'asset_value': '资产价值', 'contrarian': '逆向机会', 'liquidation': '清算价值',
                    'catalyst_strength': '催化剂强度', 'activist': 'activist 机会', 'restructuring': '重组潜力', 'ma': '并购可能',
                    'macro': '宏观环境', 'liquidity': '流动性', 'sector_rotation': '行业轮动', 'trend': '趋势'
                }
                
                scoring_details = []
                for dim_name, dim_data in scoring.items():
                    dim_score = dim_data.get('score', 0)
                    dim_max = dim_data.get('max', 25)
                    dim_cn_name = dim_names.get(dim_name, dim_name)
                    scoring_details.append(f"{dim_cn_name}: {dim_score:.1f}/{dim_max}")
                
                scoring_text = '，'.join(scoring_details)
                
                html.append(f'            <div class="summary-box">')
                html.append(f'                <h3>{name} <small>({reps})</small></h3>')
                html.append(f'                <p><strong>核心问题：</strong>{question}</p>')
                html.append(f'                <p><strong>评分维度：</strong><small>{scoring_text}</small></p>')
                html.append(f'                <p><strong>总分：</strong><span class="{score_class}">{score:.1f}/100</span> &nbsp;&nbsp;&nbsp; <strong>判断：</strong>{verdict}</p>')
                html.append(f'            </div>')
        
        html.append('        </div>')
        html.append('')
        
        return "\n".join(html)
    
    def _generate_key_forces_section(self) -> str:
        """生成 Key Forces 部分 - 分析内容在影响力上面"""
        if not self.key_forces:
            return ''
        
        html = []
        html.append('        <h2>🎯 Key Forces</h2>')
        html.append('        <p>自动识别决定公司未来价值的 1-3 个决定性力量，按影响力排序（0-10 分）。这些 Key Forces 是影响公司价值的最关键因素，需要重点关注。</p>')
        html.append('        <div class="key-forces-grid">')
        
        force_descriptions = {
            '增长': '评估收入/利润增长速度及其可持续性',
            '技术': '评估 AI/云/机器学习等技术转型驱动力',
            '护城河': '评估毛利率反映的护城河深度',
            '财务': '评估 FCF 利润率和流动比率反映的财务实力',
            '市场': '评估分析师评级和股价上涨空间反映的市场情绪',
            '行业': '评估科技/软件/半导体行业趋势'
        }
        
        for i, force in enumerate(self.key_forces[:3], 1):
            name = force['name']
            impact = force['impact_score']
            impact_class = 'score-high' if impact >= 8 else 'score-medium' if impact >= 6 else 'score-low'
            
            # 提取力量类型关键词
            force_type = '增长' if '增长' in name else '技术' if '技术' in name or 'AI' in name else '护城河' if '护城河' in name or '毛利率' in name else '财务' if '财务' in name or '现金流' in name else '市场' if '市场' in name or '分析师' in name else '行业'
            description = force_descriptions.get(force_type, '评估该力量的具体影响')
            
            html.append(f'            <div class="summary-box">')
            html.append(f'                <h4>#{i} {name}</h4>')
            html.append(f'                <p><strong>分析内容：</strong>{description}</p>')
            html.append(f'                <p><strong>影响力：</strong><span class="{impact_class}">{impact:.1f}/10</span></p>')
            html.append(f'            </div>')
        
        html.append('        </div>')
        html.append('')
        
        return "\n".join(html)
    
    def _generate_valuation_section(self) -> str:
        """生成估值矩阵部分 - 方法和创始人合并，增加概念简述"""
        html = []
        html.append('        <h2>💰 估值矩阵</h2>')
        html.append('        <p>集成 6 种经典估值方法，覆盖不同行业、不同发展阶段的企业估值需求。每种方法都有独特的视角和判断标准，综合使用可以避免单一方法的盲点。</p>')
        html.append('        <table>')
        html.append('            <thead>')
        html.append('                <tr>')
        html.append('                    <th>方法（创始人）</th>')
        html.append('                    <th>概念简述</th>')
        html.append('                    <th>判断标准</th>')
        html.append('                    <th>结果</th>')
        html.append('                </tr>')
        html.append('            </thead>')
        html.append('            <tbody>')
        
        valuation_map = {
            'owner_earnings': ('Owner Earnings', '巴菲特', '所有者收益，即企业真正能赚到的现金', '10-15 倍合理，安全边际>30% 买入'),
            'peg': ('PEG Ratio', '彼得·林奇', '市盈率相对盈利增长比率', '<0.5 极具吸引力，0.5-1.0 有吸引力，1.0-1.5 合理，>2.0 昂贵'),
            'reverse_dcf': ('Reverse DCF', '逆向思维', '从当前股价反推市场隐含的增长率', '隐含增长<历史增速=低估，隐含增长>历史增速=高估'),
            'magic_formula': ('Magic Formula', '格林布拉特', '盈利收益率 +ROIC 排名的综合公式', '综合排名<10% 优秀，10-30% 良好，>30% 一般'),
            'ev_ebitda': ('EV/EBITDA', '达摩达兰', '企业价值与息税折旧摊销前利润的比率', '低于行业平均 20%+=低估，±20% 合理，高于 20%+=高估'),
            'ev_revenue_rule40': ('Rule of 40', 'SaaS 行业', '增长率 + 利润率≥40% 为优秀', '≥60% 优秀，40-60% 良好，20-40% 一般，<20% 较差')
        }
        
        for key, (name, founder, concept, criteria) in valuation_map.items():
            if key in self.valuation:
                v = self.valuation[key]
                verdict = v.get('verdict', 'N/A')
                
                # 添加实际数值
                if key == 'peg':
                    peg_value = v.get('peg', 0)
                    actual_value = f"PEG={peg_value:.2f}" if peg_value else "N/A"
                elif key == 'owner_earnings':
                    multiple = v.get('multiple', 0)
                    actual_value = f"倍数={multiple:.1f}" if multiple else "N/A"
                elif key == 'reverse_dcf':
                    implied_growth = v.get('implied_growth', 0) * 100
                    actual_value = f"隐含增长={implied_growth:.1f}%" if implied_growth else "N/A"
                elif key == 'magic_formula':
                    rank = v.get('rank', 0)
                    actual_value = f"排名={rank:.1f}%" if rank else "N/A"
                elif key == 'ev_ebitda':
                    ev_ebitda = v.get('ev_ebitda', 0)
                    actual_value = f"EV/EBITDA={ev_ebitda:.1f}x" if ev_ebitda else "N/A"
                elif key == 'ev_revenue_rule40':
                    rule_of_40 = v.get('rule_of_40', 0)
                    # rule_of_40 已经是百分比，不需要再乘以 100
                    actual_value = f"Rule of 40={rule_of_40:.1f}%"
                else:
                    actual_value = 'N/A'
                
                # 构建结果列：判断 + 实际数值
                result_text = f'{verdict}'
                if actual_value and actual_value != 'N/A':
                    result_text += f'<br><small>（{actual_value}）</small>'
                
                html.append('                <tr>')
                html.append(f'                    <td><strong>{name}</strong><br><small>{founder}</small></td>')
                html.append(f'                    <td>{concept}</td>')
                html.append(f'                    <td>{criteria}</td>')
                html.append(f'                    <td>{result_text}</td>')
                html.append('                </tr>')
        
        html.append('            </tbody>')
        html.append('        </table>')
        html.append('')
        
        return "\n".join(html)
    
    def _generate_biases_section(self) -> str:
        """生成反偏见框架部分 - 偏见类型和中文名称合并，增加详细描述"""
        biases = self.biases
        html = []
        
        html.append('        <h2>🧠 反偏见框架</h2>')
        html.append('        <p>通过系统化的检查清单，帮助识别和克服认知偏见、财务红旗和科技行业特有盲区。</p>')
        
        # 认知偏见
        cognitive_biases = biases.get('cognitive_biases', {})
        if cognitive_biases:
            html.append('        <h3>认知偏见</h3>')
            html.append('        <p>6 大认知偏见检查，帮助避免投资决策中的心理陷阱。</p>')
            html.append('        <table>')
            html.append('            <thead>')
            html.append('                <tr>')
            html.append('                    <th>偏见类型</th>')
            html.append('                    <th>偏见简述</th>')
            html.append('                    <th>状态</th>')
            html.append('                </tr>')
            html.append('            </thead>')
            html.append('            <tbody>')
            
            bias_names = {
                'confirmation_bias': ('确认偏误', '只关注支持自己看法的信息，忽略或轻视反面证据。例如：只看到利好消息，选择性忽视利空消息。'),
                'anchoring': ('锚定效应', '被历史股价或某个锚点价格影响判断，无法客观评估当前价值。例如：认为"从高点已经跌了 50%，很便宜"。'),
                'narrative': ('叙事谬误', '被好故事冲昏头脑，对数字的要求变低。例如：因为"AI 革命"的故事而忽视估值过高的事实。'),
                'herding': ('从众心理', '因为"所有人都在买"就跟着买，放弃独立判断。例如：因为分析师都推荐就买入。'),
                'disposition': ('处置效应', '过早卖出赢家，过晚卖出输家。例如：赚一点就跑，亏了却死扛不卖。'),
                'overconfidence': ('过度自信', '高估自己预测能力，低估不确定性和风险。例如：认为自己的预测准确率远高于实际。')
            }
            
            for bias_name, (cn_name, description) in bias_names.items():
                if bias_name in cognitive_biases:
                    bias_data = cognitive_biases[bias_name]
                    risk = bias_data.get('risk', False)
                    status = '⚠️ 警告' if risk else '✅ 正常'
                    status_class = 'score-low' if risk else 'score-high'
                    
                    html.append(f'                <tr>')
                    html.append(f'                    <td>{bias_name}<br><small>{cn_name}</small></td>')
                    html.append(f'                    <td>{description}</td>')
                    html.append(f'                    <td class="{status_class}">{status}</td>')
                    html.append(f'                </tr>')
            
            html.append('            </tbody>')
            html.append('        </table>')
        
        # 财务红旗
        red_flags = biases.get('financial_red_flags', {}).get('flags', [])
        
        # 获取财务数据用于计算实际数值
        financials = self.data.get('financials', {})
        balance_sheet = self.data.get('balance_sheet', {})
        cashflow = self.data.get('cashflow', {})
        
        # 计算所有财务指标的实际数值
        gaap_net_income = financials.get('net_income', 0)
        non_gaap_net_income = financials.get('non_gaap_net_income', 0)
        sbc = financials.get('stock_based_compensation', 0)
        revenue = financials.get('total_revenue', 1)
        gaap_gap = ((non_gaap_net_income - gaap_net_income) / abs(gaap_net_income) * 100) if gaap_net_income != 0 else 0
        sbc_ratio = (sbc / revenue * 100) if revenue > 0 else 0
        
        receivables_ratio = financials.get('receivables_ratio', 0)
        capex_ratio = abs(cashflow.get('capital_expenditure', 0)) / revenue * 100 if revenue > 0 else 0
        operating_cf = cashflow.get('operating_cashflow', 0)
        cash_flow_ratio = (operating_cf / gaap_net_income) if gaap_net_income > 0 else 0
        debt_ratio = balance_sheet.get('debt_to_equity', 0)
        current_ratio = balance_sheet.get('current_ratio', 0)
        
        all_red_flags = [
            ('GAAP vs Non-GAAP', '检查 GAAP 与 Non-GAAP 利润差异，SBC 占比是否过高', f'差异={gaap_gap:.1f}%，SBC/收入={sbc_ratio:.1f}%', '差异<50% 且 SBC/收入<15% 为正常'),
            ('收入确认异常', '检查收入确认政策是否激进，递延收入趋势是否异常', f'递延收入/收入={financials.get("deferred_revenue_ratio", "N/A")}', '递延收入/收入<10% 为正常'),
            ('应收账款异常', '检查应收账款增速是否超过收入增速', f'应收/收入={receivables_ratio:.1f}%', '应收/收入<30% 为正常'),
            ('内部人交易', '检查高管是否大量抛售股票', f'净卖出/总股本={financials.get("insider_selling_ratio", "N/A")}', '净卖出/总股本<1% 为正常'),
            ('资本支出暴增', '检查资本支出占收入比例是否异常高', f'CapEx/收入={capex_ratio:.1f}%', 'CapEx/收入<20% 为正常'),
            ('现金流背离', '检查利润为正但现金流为负的情况', f'经营现金流/净利润={cash_flow_ratio:.2f}', '经营现金流/净利润>0.8 为正常'),
            ('负债结构恶化', '检查负债率和流动比率是否恶化', f'负债率={debt_ratio:.2f}, 流动比率={current_ratio:.2f}', '负债率<1 且流动比率>1.5 为正常')
        ]
        
        html.append('        <h3>财务红旗</h3>')
        html.append('        <p>7 大财务红旗检查，帮助识别财务报表中的风险信号。</p>')
        html.append('        <table>')
        html.append('            <thead>')
        html.append('                <tr>')
        html.append('                    <th>红旗项目</th>')
        html.append('                    <th>检查内容</th>')
        html.append('                    <th>实际数值</th>')
        html.append('                    <th>正常范围</th>')
        html.append('                    <th>状态</th>')
        html.append('                </tr>')
        html.append('            </thead>')
        html.append('            <tbody>')
        
        for i, (flag_name, description, actual_value, normal_range) in enumerate(all_red_flags):
            # 检查是否在 red_flags 中
            flag_found = next((f for f in red_flags if flag_name in f.get('name', '')), None)
            
            if flag_found:
                # 风险等级显示
                risk = flag_found.get('risk', '中')
                status = f'⚠️ 警告（{risk}风险）'
                status_class = 'score-low'
            else:
                status = '✅ 正常'
                status_class = 'score-high'
            
            html.append(f'                <tr>')
            html.append(f'                    <td>{flag_name}</td>')
            html.append(f'                    <td>{description}</td>')
            html.append(f'                    <td>{actual_value}</td>')
            html.append(f'                    <td>{normal_range}</td>')
            html.append(f'                    <td class="{status_class}">{status}</td>')
            html.append(f'                </tr>')
        
        html.append('            </tbody>')
        html.append('        </table>')
        
        html.append('')
        
        return "\n".join(html)
    
    def _generate_premortem_section(self) -> str:
        """生成 Pre-Mortem 部分 - 每个问题根据当前报告举例说明"""
        html = []
        html.append('        <h2>💀 Pre-Mortem（事前尸检）</h2>')
        html.append('        <p>强大的逆向思维工具，通过假设投资已失败，倒推失败原因，提前识别风险。</p>')
        html.append('        <div class="warning-box">')
        html.append('            <p><strong>核心问题：</strong></p>')
        html.append('            <ul>')
        
        # 根据当前报告生成具体的例子
        score = self.summary.get('overall_score', 0)
        recommendation = self.summary.get('recommendation', 'N/A')
        valuation_upside = self.summary.get('valuation_upside', 0)
        
        html.append(f'                <li><strong>核心假设中哪个错了？</strong><br>例如：假设{self.ticker}的高增长可持续，但如果行业竞争加剧导致毛利率下降 10 个百分点，估值可能下调{abs(valuation_upside)/2:.1f}%。</li>')
        
        html.append(f'                <li><strong>是否忽略了某个重大风险？</strong><br>例如：忽略了财务红旗中的现金流背离风险，如果利润增长但现金流为负，可能预示盈利质量问题。</li>')
        
        html.append(f'                <li><strong>竞争格局是否发生了意外变化？</strong><br>例如：新竞争对手进入市场导致价格战，或者主要客户流失导致收入大幅下滑。</li>')
        
        html.append(f'                <li><strong>管理层是否做出了错误决策？</strong><br>例如：过度扩张导致资金链紧张，或者错误的并购决策导致商誉减值。</li>')
        
        html.append(f'                <li><strong>宏观环境是否恶化？</strong><br>例如：经济衰退导致需求萎缩，或者利率上升导致估值下调。</li>')
        
        html.append('            </ul>')
        html.append('        </div>')
        html.append('')
        
        return "\n".join(html)


def export_report(analysis_result: dict, output_dir: str = 'output') -> str:
    """便捷函数：导出报告"""
    exporter = ReportExporter(analysis_result)
    exporter.output_dir = Path(output_dir)
    exporter.output_dir.mkdir(exist_ok=True)
    
    return exporter.export_html()


if __name__ == '__main__':
    # 测试代码
    print("报告导出模块 - 专业投资报告风格（最终优化版）")
    print("统一字体、颜色、间距等设计规范，增加详细内容描述，优化布局")
