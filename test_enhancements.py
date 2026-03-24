#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强功能测试脚本
测试：错误处理、速率限制、触发条件
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from exceptions import DataFetchError, InsufficientDataError, AnalysisError
from core import analyze_single_stock


def test_exception_classes():
    """测试异常类"""
    print("=" * 70)
    print("🧪 测试 1: 异常类")
    print("=" * 70)
    
    # DataFetchError
    try:
        raise DataFetchError("AAPL", "yahoo", "Connection timeout")
    except DataFetchError as e:
        print(f"✅ DataFetchError: {e}")
        assert e.ticker == "AAPL"
        assert e.source == "yahoo"
    
    # InsufficientDataError
    try:
        raise InsufficientDataError("TSLA", "quarterly_revenue")
    except InsufficientDataError as e:
        print(f"✅ InsufficientDataError: {e}")
        assert e.ticker == "TSLA"
        assert e.missing_data == "quarterly_revenue"
    
    # AnalysisError
    try:
        raise AnalysisError("NVDA", "module_A", "Invalid data format")
    except AnalysisError as e:
        print(f"✅ AnalysisError: {e}")
        assert e.ticker == "NVDA"
        assert e.module == "module_A"
    
    print()


def test_error_handling():
    """测试错误处理"""
    print("=" * 70)
    print("🧪 测试 2: 错误处理")
    print("=" * 70)
    
    # 测试无效股票代码（应该返回错误而不是崩溃）
    print("测试无效股票代码...")
    result = analyze_single_stock("INVALID_STOCK_12345", use_cache=False)
    
    assert 'success' in result, "结果应包含 success 字段"
    assert 'ticker' in result, "结果应包含 ticker 字段"
    print(f"✅ 无效股票返回格式正确：success={result.get('success')}")
    
    if not result.get('success'):
        print(f"   错误类型：{result.get('error_type')}")
        print(f"   错误信息：{result.get('error')}")
    
    print()


def test_success_case():
    """测试成功案例"""
    print("=" * 70)
    print("🧪 测试 3: 成功案例 (使用缓存)")
    print("=" * 70)
    
    # 测试有效股票代码（使用缓存避免 API 调用）
    print("测试 AAPL (使用缓存)...")
    result = analyze_single_stock("AAPL", use_cache=True)
    
    assert 'success' in result, "结果应包含 success 字段"
    assert result['ticker'] == "AAPL", "ticker 应匹配"
    
    if result.get('success'):
        print(f"✅ 分析成功")
        print(f"   综合评分：{result['summary']['overall_score']:.1f}/100")
        print(f"   投资建议：{result['summary']['recommendation']}")
        print(f"   置信度：{result['summary']['confidence']}")
    else:
        print(f"⚠️ 分析失败（可能是数据问题）")
        print(f"   错误类型：{result.get('error_type')}")
        print(f"   错误信息：{result.get('error')}")
    
    print()


def test_rate_limit_config():
    """测试速率限制配置"""
    print("=" * 70)
    print("🧪 测试 4: 速率限制配置")
    print("=" * 70)
    
    # 检查 config.json
    import json
    config_path = Path(__file__).parent / 'config.json'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    assert 'batch_analysis' in config, "config.json 应包含 batch_analysis"
    assert 'rate_limit' in config['batch_analysis'], "应包含 rate_limit"
    assert 'rate_period' in config['batch_analysis'], "应包含 rate_period"
    
    print(f"✅ 速率限制配置:")
    print(f"   最大并发：{config['batch_analysis']['max_workers']}")
    print(f"   速率限制：{config['batch_analysis']['rate_limit']} 请求/{config['batch_analysis']['rate_period']}秒")
    print(f"   超时时间：{config['batch_analysis']['timeout_per_stock']}秒")
    
    # 检查 analyze_batch.py
    batch_path = Path(__file__).parent / 'analyze_batch.py'
    with open(batch_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert '_enforce_rate_limit' in content, "analyze_batch.py 应包含速率限制方法"
    assert 'rate_limit' in content, "analyze_batch.py 应支持 rate_limit 参数"
    
    print(f"✅ analyze_batch.py 包含速率限制逻辑")
    print()


def test_trigger_conditions():
    """测试触发条件文档"""
    print("=" * 70)
    print("🧪 测试 5: 触发条件文档")
    print("=" * 70)
    
    skill_path = Path(__file__).parent / 'SKILL.md'
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert '## 触发条件' in content, "SKILL.md 应包含触发条件章节"
    assert '财报分析类' in content, "应包含财报分析类触发条件"
    assert '投资决策类' in content, "应包含投资决策类触发条件"
    assert '投资视角类' in content, "应包含投资视角类触发条件"
    assert '联动触发' in content, "应包含联动触发说明"
    
    print(f"✅ 触发条件文档完整")
    print(f"   - 财报分析类触发条件 ✓")
    print(f"   - 投资决策类触发条件 ✓")
    print(f"   - 投资视角类触发条件 ✓")
    print(f"   - 联动触发说明 ✓")
    print()


def test_output_format_config():
    """测试输出格式配置"""
    print("=" * 70)
    print("🧪 测试 6: 输出格式配置")
    print("=" * 70)
    
    # 检查主技能
    skill_path = Path(__file__).parent / 'SKILL.md'
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert 'formats: ["html", "md"]' in content, "主技能应配置 HTML 优先"
    print(f"✅ 主技能输出格式：HTML 优先")
    
    # 检查子技能
    sub_skills = [
        'us-value-investing/SKILL.md',
        'macro-liquidity/SKILL.md',
        'btc-bottom-model/SKILL.md',
        'us-market-sentiment/SKILL.md'
    ]
    
    for sub_skill in sub_skills:
        sub_path = Path(__file__).parent / sub_skill
        with open(sub_path, 'r', encoding='utf-8') as f:
            sub_content = f.read()
        
        assert 'formats: ["html", "md"]' in sub_content, f"{sub_skill} 应配置 HTML 优先"
        print(f"✅ {sub_skill.split('/')[0]} 输出格式：HTML 优先")
    
    print()


def run_all_tests():
    """运行所有测试"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "tech-earnings-deepdive 增强功能测试" + " " * 16 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    start_time = datetime.now()
    
    try:
        test_exception_classes()
        test_error_handling()
        test_success_case()
        test_rate_limit_config()
        test_trigger_conditions()
        test_output_format_config()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("=" * 70)
        print("✅ 所有测试通过！")
        print("=" * 70)
        print(f"测试耗时：{duration:.2f}秒")
        print()
        
        return True
        
    except AssertionError as e:
        print()
        print("=" * 70)
        print("❌ 测试失败！")
        print("=" * 70)
        print(f"错误：{e}")
        print()
        return False
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ 测试异常！")
        print("=" * 70)
        print(f"错误：{e}")
        import traceback
        traceback.print_exc()
        print()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
