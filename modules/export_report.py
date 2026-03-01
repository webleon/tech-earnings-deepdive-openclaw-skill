#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告导出模块
支持 Markdown、HTML 格式导出
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class ReportExporter:
    """报告导出器"""
    
    def __init__(self, analysis_result: dict):
        self.result = analysis_result
        self.ticker = analysis_result.get('ticker', 'UNKNOWN')
        
        # 如果 ticker 是 UNKNOWN，尝试从数据中获取
        if self.ticker == 'UNKNOWN':
            data = analysis_result.get('data', {})
            if data:
                # 尝试多种方式获取 symbol
                self.ticker = data.get('symbol', '')
                if not self.ticker:
                    # 尝试从 info 获取
                    info = data.get('info', {})
                    self.ticker = info.get('symbol', 'UNKNOWN')
        self.timestamp = analysis_result.get('timestamp', datetime.now().isoformat())
        self.data = analysis_result.get('data', {})
        self.modules = analysis_result.get('modules', {})
        self.valuation = analysis_result.get('valuation', {})
        self.biases = analysis_result.get('biases', {})
        self.variant_view = analysis_result.get('variant_view', {})
        self.key_forces = analysis_result.get('key_forces', [])
        self.perspectives = analysis_result.get('perspectives', {})
        self.summary = analysis_result.get('summary', {})
        
        self.output_dir = Path('output')
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_markdown(self, filename: str = None) -> str:
        """导出 Markdown 格式报告"""
        if not filename:
            filename = f"{self.ticker}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = self.output_dir / filename
        content = self._generate_markdown()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Markdown 报告已导出：{filepath}")
        return str(filepath)
    
    def export_html(self, filename: str = None) -> str:
        """导出 HTML 格式报告（详细版）"""
        if not filename:
            filename = f"{self.ticker}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = self.output_dir / filename
        content = self._generate_detailed_html()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ HTML 报告已导出：{filepath}")
        return str(filepath)
    
    def export_pdf(self, filename: str = None) -> str:
        """导出 PDF 格式报告"""
        if not filename:
            filename = f"{self.ticker}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = self.output_dir / filename
        
        try:
            from weasyprint import HTML, CSS
            
            # 生成 HTML 内容
            html_content = self._generate_detailed_html()
            
            # 添加 PDF 优化的 CSS
            pdf_css = CSS(string='''
                @page {
                    size: A4;
                    margin: 2cm 2.5cm;
                    @bottom-right {
                        content: "Page " counter(page) " of " counter(pages);
                        font-size: 9pt;
                        color: #666;
                    }
                }
                body {
                    font-family: "PingFang SC", "Microsoft YaHei", "Heiti SC", sans-serif !important;
                    font-size: 11pt;
                    line-height: 1.6;
                }
                h1 {
                    font-size: 24pt;
                    page-break-after: avoid;
                }
                h2 {
                    font-size: 18pt;
                    page-break-after: avoid;
                }
                h3 {
                    font-size: 14pt;
                    page-break-after: avoid;
                }
                table {
                    page-break-inside: avoid;
                    font-size: 12px;
                }
                .summary-box, .warning-box, .risk-box {
                    page-break-inside: avoid;
                }
                img {
                    max-width: 100%;
                    page-break-inside: avoid;
                }
            ''')
            
            # 生成 PDF
            HTML(string=html_content).write_pdf(str(filepath), stylesheets=[pdf_css])
            
            # 获取文件大小
            import os
            file_size = os.path.getsize(filepath)
            
            print(f"✅ PDF 报告已导出：{filepath}")
            print(f"   文件大小：{file_size/1024:.1f} KB")
            return str(filepath)
            
        except ImportError:
            print("⚠️ weasyprint 未安装，无法生成 PDF")
            print("   安装：pip install weasyprint")
            return None
        except Exception as e:
            print(f"⚠️ PDF 生成失败：{e}")
            print("   建议使用 HTML 打印为 PDF")
            return None
    
    def _generate_markdown(self) -> str:
        """生成 Markdown 报告内容"""
        md = []
        
        # 标题
        md.append(f"# 📊 {self.ticker} 投资分析报告")
        md.append(f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md.append("")
        
        # 综合结论
        md.append("## 📋 综合结论")
        md.append(f"- **综合评分：** {self.summary.get('overall_score', 0):.1f}/100")
        md.append(f"- **投资建议：** {self.summary.get('recommendation', 'N/A')}")
        md.append(f"- **置信度：** {self.summary.get('confidence', 'N/A')}")
        md.append("")
        
        # Key Forces
        if self.key_forces:
            md.append("## 🎯 Key Forces")
            for i, force in enumerate(self.key_forces[:3], 1):
                md.append(f"{i}. **{force['name']}** ({force['impact_score']:.1f}/10)")
            md.append("")
        
        # 16 模块
        md.append("## 🔍 16 模块分析")
        md.append("| 模块 | 评分 | 等级 |")
        md.append("|------|------|------|")
        for key, module in sorted(self.modules.items(), key=lambda x: x[1]['score'], reverse=True):
            score = module['score']
            rating = "⭐⭐⭐⭐⭐" if score >= 80 else "⭐⭐⭐⭐" if score >= 60 else "⭐⭐⭐"
            md.append(f"{key[0]}. {module['name']} | {score:.1f}/100 | {rating} |")
        md.append("")
        
        return "\n".join(md)
    
    def _generate_detailed_html(self) -> str:
        """生成详细的 HTML 报告"""
        html = []
        
        # HTML 头部
        html.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + self.ticker + """ 投资分析报告</title>
    <style>
        body { font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.5; max-width: 1100px; margin: 0 auto; padding: 30px 20px; background: #fff; }
        .container { background: #fff; padding: 40px; border: 1px solid #e0e0e0; }
        h1 { color: #1a1a1a; border-bottom: 2px solid #333; padding-bottom: 15px; font-size: 26px; font-weight: 600; }
        h2 { color: #333; border-left: 4px solid #333; padding-left: 15px; margin-top: 35px; font-size: 20px; font-weight: 600; }
        h3 { color: #555; font-size: 16px; margin-top: 20px; font-weight: 600; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 13px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #333; color: #fff; font-weight: 600; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .score-high { color: #2e7d32; font-weight: 600; }
        .score-medium { color: #f57c00; font-weight: 600; }
        .score-low { color: #c62828; font-weight: 600; }
        .report-summary { background: #f9f9f9; padding: 25px; border-left: 4px solid #333; margin: 20px 0; }
        .summary-intro { color: #555; padding-bottom: 15px; border-bottom: 1px solid #ddd; }
        .summary-content { color: #333; font-size: 14px; }
        .summary-box { background: #f5f5f5; padding: 18px; border: 1px solid #ddd; margin: 15px 0; }
        .warning-box { background: #fff8e1; padding: 15px; border: 1px solid #ffe082; margin: 15px 0; }
        .risk-box { background: #ffebee; padding: 15px; border: 1px solid #ef9a9a; margin: 15px 0; }
        .footer { margin-top: 40px; padding-top: 15px; border-top: 1px solid #ddd; color: #757575; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">""")
        
        # 标题
        company_name = self.data.get('company_info', {}).get('company_name', self.ticker)
        html.append(f"<h1>📊 {self.ticker} 投资分析报告</h1>")
        html.append(f"<p><strong>公司：</strong> {company_name}<br>")
        html.append(f"<strong>生成时间：</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        # 综合结论（专业投资报告风格 - 详细描述）
        score = self.summary.get('overall_score', 0)
        score_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
        recommendation = self.summary.get('recommendation', 'N/A')
        confidence = self.summary.get('confidence', 'N/A')
        valuation_upside = self.summary.get('valuation_upside', 0)
        
        # 生成详细摘要
        if score >= 70:
            rating = "优秀"
            intro = f"该公司整体表现<strong>优秀</strong>（{score:.1f}分），在多个关键维度展现出强劲的竞争力和可持续的增长潜力。"
        elif score >= 60:
            rating = "良好"
            intro = f"该公司整体表现<strong>良好</strong>（{score:.1f}分），基本面稳健，具备一定投资价值，但需关注部分风险因素。"
        elif score >= 50:
            rating = "一般"
            intro = f"该公司整体表现<strong>一般</strong>（{score:.1f}分），基本面存在分化，建议谨慎评估，重点关注风险因素。"
        else:
            rating = "较弱"
            intro = f"该公司整体表现<strong>较弱</strong>（{score:.1f}分），基本面存在较多问题，风险因素较多，建议谨慎或回避。"
        
        # 详细分析内容
        analysis_parts = []
        
        # 1. 核心优势
        top_modules = sorted(self.modules.items(), key=lambda x: x[1]['score'], reverse=True)[:3]
        strengths_detail = []
        for k, m in top_modules:
            if m['score'] >= 80:
                strengths_detail.append(f"{m['name']}（{m['score']:.1f}分，表现突出）")
            elif m['score'] >= 60:
                strengths_detail.append(f"{m['name']}（{m['score']:.1f}分，表现良好）")
        if strengths_detail:
            analysis_parts.append(f"<strong>核心优势方面，</strong>{'、'.join(strengths_detail)}。")
        
        # 2. 关键驱动因素
        if self.key_forces:
            forces_detail = []
            for f in self.key_forces[:3]:
                if f['impact_score'] >= 8:
                    forces_detail.append(f"{f['name']}（影响力{f['impact_score']:.1f}/10，强势驱动）")
                elif f['impact_score'] >= 6:
                    forces_detail.append(f"{f['name']}（影响力{f['impact_score']:.1f}/10，中等驱动）")
            if forces_detail:
                analysis_parts.append(f"<strong>关键驱动因素方面，</strong>{'、'.join(forces_detail)}。")
        
        # 3. 风险提示
        red_flags_count = len(self.biases.get('financial_red_flags', {}).get('flags', []))
        bias_count = self.biases['summary'].get('bias_warnings', 0)
        if red_flags_count > 0 or bias_count > 0:
            risk_parts = []
            if red_flags_count > 0:
                risk_parts.append(f"{red_flags_count}个财务红旗")
            if bias_count > 0:
                risk_parts.append(f"{bias_count}个认知偏见警示")
            analysis_parts.append(f"<strong>风险提示方面，</strong>需特别关注{'、'.join(risk_parts)}，建议深入分析相关风险因素。")
        
        # 4. 估值判断
        if abs(valuation_upside) > 30:
            if valuation_upside > 0:
                analysis_parts.append(f"<strong>估值方面，</strong>当前估值存在{valuation_upside:.1f}%的显著上涨空间，具备较强吸引力，建议重点关注。")
            else:
                analysis_parts.append(f"<strong>估值方面，</strong>当前估值偏高，存在{abs(valuation_upside):.1f}%的显著回调风险，建议谨慎对待。")
        elif abs(valuation_upside) > 15:
            if valuation_upside > 0:
                analysis_parts.append(f"<strong>估值方面，</strong>当前估值存在{valuation_upside:.1f}%的上涨空间，具备一定吸引力。")
            else:
                analysis_parts.append(f"<strong>估值方面，</strong>当前估值偏高，存在{abs(valuation_upside):.1f}%的回调风险。")
        else:
            analysis_parts.append(f"<strong>估值方面，</strong>当前估值处于合理区间，估值风险可控。")
        
        # 5. 综合建议
        if recommendation == "强烈买入":
            action_text = "建议积极配置，可作为核心持仓"
        elif recommendation == "买入":
            action_text = "建议逢低布局，逐步建仓"
        elif recommendation == "持有":
            action_text = "建议继续持有，密切关注基本面变化"
        elif recommendation == "减持":
            action_text = "建议适度减仓，控制风险敞口"
        else:
            action_text = "建议回避或清仓，等待更好的投资机会"
        
        analysis_parts.append(f"<strong>综合建议，</strong>基于以上分析，给予'<span class='{score_class}'>{recommendation}</span>'评级（置信度：{confidence}），{action_text}。")
        
        # 组合完整摘要
        full_summary = f"{intro}<br><br>" + "<br><br>".join(analysis_parts)
        
        html.append("<div class='report-summary'>")
        html.append("<h2>📋 投资摘要</h2>")
        html.append(f"<div class='summary-content' style='line-height: 1.8; text-align: justify; font-size: 14px;'>{full_summary}</div>")
        html.append("</div>")
        # 关键优势（Key Forces）- 三列紧凑布局
        if self.key_forces:
            html.append("<h2>✅ 关键驱动因素</h2>")
            html.append("<div class='key-forces-grid' style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 15px 0;'>")
            for i, force in enumerate(self.key_forces[:3], 1):
                impact_class = 'score-high' if force['impact_score'] >= 8 else 'score-medium' if force['impact_score'] >= 6 else 'score-low'
                html.append(f"<div style='background: #fff; padding: 15px; border: 1px solid #ddd; border-radius: 3px;'>")
                html.append(f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>")
                html.append(f"<span style='font-size: 12px; color: #757575;'>#{i}</span>")
                html.append(f"<span class='{impact_class}' style='font-size: 18px; font-weight: bold;'>{force['impact_score']:.1f}/10</span>")
                html.append(f"</div>")
                html.append(f"<div style='font-size: 14px; font-weight: 600; color: #333; margin-bottom: 8px; min-height: 40px;'>{force['name']}</div>")
                html.append(f"<div style='font-size: 12px; color: #757575;'><strong>类型：</strong>{force['type']}</div>")
                if force.get('description'):
                    html.append(f"<div style='font-size: 12px; color: #757575; margin-top: 5px;'><strong>说明：</strong>{force['description'][:50]}{'...' if len(force['description']) > 50 else ''}</div>")
                html.append(f"</div>")
            html.append("</div>")
        
        # 16 模块（紧凑两列布局）
        html.append("<h2>📊 模块分析</h2>")
        html.append("<div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;'>")
        for key, module in sorted(self.modules.items(), key=lambda x: x[1]['score'], reverse=True):
            score = module['score']
            name = module['name']
            rating = "⭐⭐⭐⭐⭐ 优秀" if score >= 80 else "⭐⭐⭐⭐ 良好" if score >= 60 else "⭐⭐⭐ 一般"
            rating_class = 'score-high' if score >= 80 else 'score-medium' if score >= 60 else 'score-low'
            
            html.append(f"<div class='summary-box'>")
            html.append(f"<h3>{key[0]}. {name} <span class='{rating_class}'>({score:.1f}/100 - {rating})</span></h3>")
            
            # 分析说明
            if 'analysis' in module and module['analysis']:
                html.append(f"<p><strong>📊 分析：</strong>{module['analysis']}</p>")
            
            # 关键指标
            if 'metrics' in module and module['metrics']:
                html.append(f"<p><strong>📈 关键指标：</strong></p>")
                html.append(f"<ul>")
                for metric_name, metric_value in module['metrics'].items():
                    if isinstance(metric_value, (int, float)):
                        if 'margin' in metric_name or 'ratio' in metric_name:
                            html.append(f"<li>{metric_name}: {metric_value:.1f}%</li>")
                        elif 'billions' in metric_name:
                            html.append(f"<li>{metric_name}: ${metric_value:.1f}亿</li>")
                        else:
                            html.append(f"<li>{metric_name}: {metric_value:.1f}</li>")
                html.append(f"</ul>")
            
            # 检查清单
            if 'checklist' in module and module['checklist']:
                html.append(f"<p><strong>✅ 检查项：</strong></p>")
                html.append(f"<ul>")
                for item in module['checklist']:
                    html.append(f"<li>{item}</li>")
                html.append(f"</ul>")
            
            # 风险标记
            if 'flags' in module and module['flags']:
                html.append(f"<p><strong>⚠️ 风险：</strong></p>")
                html.append(f"<ul>")
                for flag in module['flags']:
                    html.append(f"<li>{flag}</li>")
                html.append(f"</ul>")
            
            html.append(f"</div>")
        
        # 16 模块结束
        html.append("</div>")
        
        # 6 大视角（紧凑两列布局）
        html.append("<h2>💼 投资视角</h2>")
        html.append("<div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;'>")
        perspectives_map = {
            'quality_compounder': ('质量复利', '巴菲特/芒格', '市场关闭 10 年能安心睡觉吗？'),
            'imaginative_growth': ('想象力成长', 'Baillie Gifford/ARK', '5 年后不买会后悔吗？'),
            'fundamental_long_short': ('基本面多空', 'Tiger Cubs', '有 Variant View 吗？'),
            'deep_value': ('深度价值', 'Klarman/Marks', '比清算价值低多少？'),
            'catalyst_driven': ('催化剂驱动', 'Tepper/Ackman', '6-18 个月有什么催化剂？'),
            'macro_tactical': ('宏观战术', 'Druckenmiller', '宏观是顺风还是逆风？')
        }
        for key, (name, reps, core_question) in perspectives_map.items():
            if key in self.perspectives:
                p = self.perspectives[key]
                score = p['total_score']
                verdict = p['verdict']
                score_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
                verdict_class = 'score-high' if verdict == '买入' else 'score-medium' if verdict == '观望' else 'score-low'
                
                html.append(f"<div class='summary-box'>")
                html.append(f"<h3>{name} <small>({reps})</small> <span class='{rating_class}'>({score:.1f}/100 - {verdict})</span></h3>")
                html.append(f"<p><strong>🎯 核心问题：</strong>{core_question}</p>")
                
                
                # 评分维度（颜色圆点表示等级）
                if 'scoring' in p and p['scoring']:
                    html.append(f"<p><strong>📊 评分维度：</strong></p>")
                    html.append(f"<ul style='font-size: 12px; margin: 3px 0;'>")
                    for dim_name, dim_data in p['scoring'].items():
                        dim_score = dim_data.get('score', 0)
                        dim_max = dim_data.get('max', 25)
                        dim_criteria = dim_data.get('criteria', '')
                        percentage = (dim_score / dim_max * 100) if dim_max > 0 else 0
                        
                        # 颜色圆点表示等级
                        if percentage >= 80:
                            status_icon = "🟢"
                            status_text = "优秀"
                        elif percentage >= 60:
                            status_icon = "🟡"
                            status_text = "良好"
                        else:
                            status_icon = "🔴"
                            status_text = "待改进"
                        
                        # 中文维度名称映射
                        dim_name_cn = {
                            'moat': '护城河深度', 'roe': '净资产收益率', 'fcf': '自由现金流', 'management': '管理层质量',
                            'tam': '市场空间规模', 'innovation': '技术创新能力', 'growth': '收入成长速度', 'long_term': '长期发展潜力',
                            'relative_value': '相对估值水平', 'catalyst': '短期催化剂', 'risk_reward': '风险收益比',
                            'short_opportunity': '做空机会评估', 'margin_of_safety': '安全边际', 'asset_value': '资产重估价值',
                            'contrarian': '逆向投资机会', 'liquidation': '清算价值', 'catalyst_strength': '催化剂强度',
                            'activist': '主动投资者参与', 'restructuring': '业务重组潜力', 'ma': '并购可能性',
                            'macro': '宏观经济环境', 'liquidity': '市场流动性', 'sector_rotation': '行业轮动趋势', 'trend': '市场趋势'
                        }.get(dim_name, dim_name)
                        
                        html.append(f"<li style='margin: 3px 0;'>")
                        html.append(f"{status_icon} <strong>{dim_name_cn}</strong>: {dim_score}/{dim_max} ({status_text})")
                        if dim_criteria:
                            html.append(f"<br><small style='color: #666; margin-left: 25px;'>{dim_criteria}</small>")
                        html.append(f"</li>")
                    html.append(f"</ul>")
                html.append(f"</div>")
        
        # 6 视角结束
        html.append("</div>")
        
        # 财务红旗
        red_flags = self.biases.get('financial_red_flags', {}).get('flags', [])
        if red_flags:
            html.append("<h2>🚩 财务红旗</h2>")
            html.append("<div class='risk-box'>")
            html.append("<ul>")
            for flag in red_flags:
                html.append(f"<li><strong>{flag['name']}:</strong> {flag['description']} <em>(风险：{flag.get('risk', '中')})</em></li>")
            html.append("</ul>")
            html.append("</div>")
        
        # 认知偏见完整检测表
        cognitive_biases = self.biases.get('cognitive_biases', {})
        html.append("<h2>🧠 认知偏见检测</h2>")
        html.append("<div class='summary-box'>")
        html.append("<table>")
        html.append("<thead><tr><th>偏见类型</th><th>状态</th><th>检测说明</th></tr></thead>")
        html.append("<tbody>")
        
        biases_list = [
            ('confirmation_bias', '确认偏误', '是否只关注支持自己看法的信息？卖出评级<5% 则警告'),
            ('anchoring', '锚定效应', '是否被历史股价锚定？接近 52 周极值则警告'),
            ('narrative', '叙事谬误', '是否被好故事冲昏头脑？高增长低利润则警告'),
            ('herding', '从众心理', '是否因为"所有人都在买"就跟着买？买入>90% 则警告'),
            ('disposition', '处置效应', '是否过早卖出赢家，过晚卖出输家？'),
            ('overconfidence', '过度自信', '是否高估自己预测能力？'),
        ]
        
        for key, name, description in biases_list:
            if key in cognitive_biases:
                bias = cognitive_biases[key]
                risk = bias.get('risk', False)
                status = "⚠️ 警告" if risk else "✅ 正常"
                status_class = "score-low" if risk else "score-high"
                html.append(f"<tr>")
                html.append(f"<td><strong>{name}</strong></td>")
                html.append(f"<td class='{status_class}'>{status}</td>")
                html.append(f"<td>{description}</td>")
                html.append(f"</tr>")
        
        html.append("</tbody></table>")
        html.append("</div>")
        
        # 市场盲点
        blind_spots = self.variant_view.get('blind_spots', [])
        if blind_spots:
            html.append("<h2>🔍 市场盲点</h2>")
            html.append("<div class='warning-box'>")
            html.append("<ul>")
            for spot in blind_spots:
                html.append(f"<li><strong>{spot['type']}:</strong> {spot['description']} <em>(含义：{spot.get('implication', 'N/A')})</em></li>")
            html.append("</ul>")
            html.append("</div>")
        
        # Pre-Mortem
        pre_mortem = self.biases.get('pre_mortem', {})
        if pre_mortem:
            html.append("<h2>💀 Pre-Mortem（事前尸检）</h2>")
            html.append("<div class='warning-box'>")
            html.append(f"<p><em>{pre_mortem.get('exercise', '假设 1 年后投资失败，原因可能是：')}</em></p>")
            html.append("<p><strong>💡 使用说明：</strong> 先自己思考每个问题的答案，然后再看提示。</p>")
            
            hints = [
                '💡 <strong>提示：</strong>思考：收入增长/利润率假设是否过于乐观？如果实际情况只有预期的一半会怎样？',
                '💡 <strong>提示：</strong>思考：是否有未定价的重大风险？政策变化？技术颠覆？供应链问题？',
                '💡 <strong>提示：</strong>思考：新竞争对手？价格战？替代品出现？客户流失？',
                '💡 <strong>提示：</strong>思考：战略失误？过度扩张？人才流失？财务造假？',
                '💡 <strong>提示：</strong>思考：经济衰退？利率上升？汇率波动？地缘政治？'
            ]
            
            html.append("<table>")
            html.append("<thead><tr><th>问题</th><th>思考方向</th></tr></thead>")
            html.append("<tbody>")
            questions = pre_mortem.get('questions', [])
            for i, q in enumerate(questions[:5], 1):
                hint = hints[i-1] if i <= len(hints) else '💡 <strong>提示：</strong>思考：最坏情况是什么？如何对冲？'
                html.append(f"<tr><td>{i}. {q}</td><td>{hint}</td></tr>")
            html.append("</tbody></table>")
            
            html.append("<p><strong>✅ 行动建议：</strong></p>")
            html.append("<ol>")
            html.append("<li>针对每个风险，评估发生概率（高/中/低）</li>")
            html.append("<li>针对每个风险，评估影响程度（致命/严重/轻微）</li>")
            html.append("<li>制定应对方案：如何对冲或缓解？</li>")
            html.append("<li>设定监控指标：什么信号出现时需要警惕？</li>")
            html.append("</ol>")
            html.append("</div>")
        
        # 页脚
        html.append("<div class='footer'>")
        html.append("<p>⚠️ <strong>免责声明：</strong> 本报告基于公开信息和模型推算，仅供参考，不构成投资建议。</p>")
        html.append(f"<p>报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        html.append("</div>")
        
        # 结束
        html.append("    </div>")
        html.append("</body>")
        html.append("</html>")
        
        return "\n".join(html)


def export_report(analysis_result: dict, formats: list = ['html']) -> dict:
    """便捷函数：导出报告"""
    exporter = ReportExporter(analysis_result)
    
    results = {}
    if 'html' in formats:
        results['html'] = exporter.export_html()
    if 'md' in formats:
        results['markdown'] = exporter.export_markdown()
    
    return results


if __name__ == '__main__':
    print("报告导出模块 - 通过 batch_analysis.py 调用")
