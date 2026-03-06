#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心分析引擎
提供单股和批量分析的共用功能
"""

import os
import sys
import statistics
from pathlib import Path
from typing import Dict, Optional

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from fetch_data import fetch_stock_data
from analyze_full import analyze_16_modules
from perspectives_full import analyze_perspectives_full
from valuation_full import ValuationCalculator
from key_forces import identify_key_forces
from bias_framework import check_biases
from variant_view import generate_variant_view


def calculate_summary(modules: dict, perspectives: dict, valuation: dict, biases: dict) -> dict:
    """
    计算综合评分和摘要信息
    
    Args:
        modules: 16 模块分析结果
        perspectives: 6 大视角分析结果
        valuation: 估值分析结果
        biases: 反偏见框架结果
    
    Returns:
        包含综合评分、MSCI Barra、置信度等的字典
    """
    # ========== 16 模块基础评分 ==========
    module_scores = [
        m['score'] for m in modules.values() 
        if isinstance(m, dict) and 'score' in m
    ]
    avg_module_score = sum(module_scores) / len(module_scores) if module_scores else 0
    
    # ========== 6 大视角评分 ==========
    perspective_keys = [
        'quality_compounder', 'imaginative_growth', 'fundamental_long_short', 
        'deep_value', 'catalyst_driven', 'macro_tactical'
    ]
    perspective_scores = [
        perspectives[k]['total_score'] 
        for k in perspective_keys 
        if k in perspectives and isinstance(perspectives[k], dict) and 'total_score' in perspectives[k]
    ]
    avg_perspective_score = sum(perspective_scores) / len(perspective_scores) if perspective_scores else 0
    
    # ========== 估值评分转换 ==========
    upside = valuation.get('summary', {}).get('upside_downside', 0)
    valuation_score = min(100, max(0, 75 + upside * 1.25))
    
    # ========== 综合评分 ==========
    base_score = (
        avg_module_score * 0.50 + 
        avg_perspective_score * 0.20 + 
        valuation_score * 0.30
    )
    
    # ========== 红旗罚分 ==========
    red_flags_data = biases.get('financial_red_flags', {})
    red_flags = red_flags_data.get('flags', []) if isinstance(red_flags_data, dict) else []
    red_flag_penalty = sum(
        15 if flag.get('risk') == '高' else
        8 if flag.get('risk') == '中' else
        3 if flag.get('risk') == '低' else 0
        for flag in red_flags
    )
    
    overall_score = max(0, base_score - red_flag_penalty)
    
    # ========== MSCI Barra 6 大因子 ==========
    # 质量因子（30%）- 7 个模块
    quality_modules = [
        'A_revenue_quality', 'B_profitability', 'C_cash_flow', 
        'E_competitive_landscape', 'H_partners', 'I_management', 'O_accounting'
    ]
    quality_score = sum(
        modules.get(m, {}).get('score', 0) for m in quality_modules if modules.get(m)
    ) / 7
    
    # 成长因子（25%）- 3 个模块
    growth_modules = ['F_core_kpis', 'G_products', 'N_rd_efficiency']
    growth_score = sum(
        modules.get(m, {}).get('score', 0) for m in growth_modules if modules.get(m)
    ) / 3
    
    # 价值因子（20%）
    value_score = modules.get('K_valuation', {}).get('score', 0)
    
    # 情绪因子（10%）
    sentiment_modules = ['D_forward_guidance', 'L_ownership']
    sentiment_score = sum(
        modules.get(m, {}).get('score', 0) for m in sentiment_modules if modules.get(m)
    ) / 2
    
    # 宏观因子（10%）
    macro_score = modules.get('J_macro', {}).get('score', 0)
    
    # ESG 因子（5%）
    esg_score = modules.get('P_esg', {}).get('score', 0)
    
    barra_score = (
        quality_score * 0.30 + 
        growth_score * 0.25 + 
        value_score * 0.20 +
        sentiment_score * 0.10 + 
        macro_score * 0.10 + 
        esg_score * 0.05
    )
    
    # ========== 置信度计算 ==========
    # 投资视角分歧度
    if len(perspective_scores) >= 2:
        perspective_std = statistics.stdev(perspective_scores)
        perspective_conf = 100 if perspective_std < 10 else 70 if perspective_std < 20 else 40
    else:
        perspective_conf = 50
    
    # 估值方法分歧度
    valuation_methods = valuation.get('methods', {})
    upside_values = [
        m.get('upside_downside', 0) 
        for m in valuation_methods.values() 
        if isinstance(m, dict) and 'upside_downside' in m
    ]
    
    if len(upside_values) >= 2:
        upside_std = statistics.stdev(upside_values)
        upside_conf = 100 if upside_std < 15 else 70 if upside_std < 30 else 40
    else:
        upside_conf = 50
    
    confidence_score = (perspective_conf + upside_conf) / 2
    confidence = '高' if confidence_score >= 80 else '中' if confidence_score >= 60 else '低'
    
    # ========== 投资建议 ==========
    if overall_score >= 80:
        recommendation = '强烈买入'
    elif overall_score >= 70:
        recommendation = '买入'
    elif overall_score >= 60:
        recommendation = '持有'
    elif overall_score >= 50:
        recommendation = '减持'
    else:
        recommendation = '卖出'
    
    return {
        'overall_score': overall_score,
        'recommendation': recommendation,
        'confidence': confidence,
        'valuation_upside': upside,
        'barra_score': barra_score,
        'barra_factors': {
            'quality': quality_score,
            'growth': growth_score,
            'value': value_score,
            'sentiment': sentiment_score,
            'macro': macro_score,
            'esg': esg_score
        }
    }


def analyze_single_stock(ticker: str, use_cache: bool = True) -> dict:
    """
    分析单只股票（完整流程，始终包含 Variant View）
    
    Args:
        ticker: 股票代码
        use_cache: 是否使用缓存（默认 True）
    
    Returns:
        完整的分析结果字典
    """
    # 1. 获取数据
    data = fetch_stock_data(ticker, use_cache=use_cache)
    
    # 2. 16 模块分析
    modules_result = analyze_16_modules(data)
    
    # 3. 6 大视角分析
    perspectives_result = analyze_perspectives_full(ticker, data)
    
    # 4. 估值分析
    valuation_result = ValuationCalculator(data).calculate_all()
    
    # 5. Key Forces
    forces = identify_key_forces(data)
    
    # 6. 反偏见框架
    biases = check_biases(data)
    
    # 7. Variant View（始终执行）
    variant_view = generate_variant_view(ticker, data)
    
    # 8. 综合评分
    summary = calculate_summary(modules_result, perspectives_result, valuation_result, biases)
    
    # 9. 整合结果
    return {
        'ticker': ticker,
        'data': data,
        'modules': modules_result,
        'perspectives': perspectives_result,
        'valuation': valuation_result,
        'key_forces': forces,
        'biases': biases,
        'variant_view': variant_view,
        'summary': summary
    }


def export_report(result: dict, output_dir: Optional[str] = None) -> str:
    """
    导出 HTML 报告
    
    Args:
        result: 分析结果
        output_dir: 输出目录（默认使用环境变量或默认路径）
    
    Returns:
        报告文件路径
    """
    from export_report import ReportExporter
    
    if output_dir is None:
        output_dir = os.environ.get('OUTPUT_DIR', str(Path.home() / '.openclaw' / 'tech-earnings-output'))
    
    exporter = ReportExporter(result, output_dir)
    return exporter.export_html()
