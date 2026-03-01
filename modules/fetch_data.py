#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据获取模块 - 使用 yfinance + SEC EDGAR
无需 API Key，完全免费
"""

import yfinance as yf
import requests
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 缓存配置
CACHE_DIR = Path(__file__).parent / '..' / 'cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_TTL_HOURS = 24  # 缓存有效期 24 小时


class StockDataFetcher:
    """免费股票数据获取器（yfinance + SEC EDGAR）"""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(ticker)
        self.cache_file = CACHE_DIR / f"{self.ticker}_data.json"
        
        # SEC User-Agent（必须设置）
        self.sec_headers = {
            'User-Agent': 'Tech Earnings Deepdive your@email.com'  # 替换为你的邮箱
        }
    
    def is_cache_valid(self) -> bool:
        """检查缓存是否有效"""
        if not self.cache_file.exists():
            return False
        
        try:
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            
            cached_at = datetime.fromisoformat(cache['fetched_at'])
            if datetime.now() - cached_at < timedelta(hours=CACHE_TTL_HOURS):
                return True
        except:
            pass
        
        return False
    
    def load_cache(self) -> dict:
        """加载缓存数据"""
        with open(self.cache_file, 'r') as f:
            return json.load(f)
    
    def save_cache(self, data: dict):
        """保存缓存数据"""
        with open(self.cache_file, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_price_data(self) -> dict:
        """获取价格数据"""
        try:
            history = self.stock.history(period="1y")
            info = self.stock.info
            
            return {
                'current_price': info.get('currentPrice', history['Close'].iloc[-1]),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', history['High'].max()),
                '52_week_low': info.get('fiftyTwoWeekLow', history['Low'].min()),
                'volume': info.get('volume', history['Volume'].iloc[-1]),
                'avg_volume': info.get('averageVolume', 0),
                'market_cap': info.get('marketCap', 0),
                'beta': info.get('beta', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'forward_pe': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'eps': info.get('trailingEps', 0),
                'shares_outstanding': info.get('sharesOutstanding', 0)
            }
        except Exception as e:
            print(f"⚠️ 获取价格数据失败：{e}")
            return {}
    
    def get_financials(self) -> dict:
        """获取利润表数据"""
        try:
            financials = self.stock.financials
            cashflow = self.stock.cashflow
            info = self.stock.info
            
            # 获取最新年度数据
            def get_latest(series):
                if len(series) > 0:
                    return series.iloc[0]
                return 0
            
            # 获取股票期权费用 (SBC)
            def get_sbc():
                try:
                    if 'Stock Based Compensation' in cashflow.index:
                        return get_latest(cashflow.loc['Stock Based Compensation'])
                except:
                    pass
                return 0
            
            # 获取股本数据
            def get_shares_outstanding():
                try:
                    # 当前流通股数
                    current = info.get('sharesOutstanding', 0)
                    
                    # 尝试获取历史股数（简化：用当前代替）
                    # 完整实现需要查询历史数据
                    return {
                        'current': current,
                        'previous_year': current * 0.98,  # 估算：假设年稀释 2%
                        'change_rate': 0.02  # 估算稀释率
                    }
                except:
                    return {
                        'current': 0,
                        'previous_year': 0,
                        'change_rate': 0
                    }
            
            sbc = get_sbc()
            net_income = get_latest(financials.loc['Net Income']) if 'Net Income' in financials.index else 0
            revenue = get_latest(financials.loc['Total Revenue']) if 'Total Revenue' in financials.index else 1
            
            # 估算 Non-GAAP 净利润（GAAP + SBC）
            non_gaap_net_income = net_income + sbc if sbc > 0 else net_income
            
            # 计算稀释相关指标
            shares = get_shares_outstanding()
            dilution_rate = shares['change_rate']
            sbc_to_revenue_ratio = (sbc / revenue) * 100 if revenue > 0 else 0
            
            return {
                'total_revenue': revenue,
                'cost_of_revenue': get_latest(financials.loc['Cost Of Revenue']) if 'Cost Of Revenue' in financials.index else 0,
                'gross_profit': get_latest(financials.loc['Gross Profit']) if 'Gross Profit' in financials.index else 0,
                'operating_expenses': get_latest(financials.loc['Total Operating Expenses']) if 'Total Operating Expenses' in financials.index else 0,
                'operating_income': get_latest(financials.loc['Operating Income']) if 'Operating Income' in financials.index else 0,
                'net_income': net_income,
                'ebitda': get_latest(financials.loc['EBITDA']) if 'EBITDA' in financials.index else 0,
                'research_development': get_latest(financials.loc['Research Development']) if 'Research Development' in financials.index else 0,
                'stock_based_compensation': sbc,
                'non_gaap_net_income': non_gaap_net_income,
                'shares_outstanding': shares['current'],
                'shares_dilution_rate': dilution_rate,
                'sbc_to_revenue_ratio': sbc_to_revenue_ratio,
                # 增长率计算
                'revenue_growth_yoy': self._calculate_growth(financials.loc['Total Revenue']) if 'Total Revenue' in financials.index else 0,
                'net_income_growth_yoy': self._calculate_growth(financials.loc['Net Income']) if 'Net Income' in financials.index else 0
            }
        except Exception as e:
            print(f"⚠️ 获取利润表失败：{e}")
            return {}
    
    def get_balance_sheet(self) -> dict:
        """获取资产负债表数据"""
        try:
            bs = self.stock.balance_sheet
            
            def get_latest(series):
                if len(series) > 0:
                    return series.iloc[0]
                return 0
            
            return {
                'total_assets': get_latest(bs.loc['Total Assets']) if 'Total Assets' in bs.index else 0,
                'total_liabilities': get_latest(bs.loc['Total Liabilities Net Minority Interest']) if 'Total Liabilities Net Minority Interest' in bs.index else 0,
                'total_equity': get_latest(bs.loc['Total Equity Gross Minority Interest']) if 'Total Equity Gross Minority Interest' in bs.index else 0,
                'cash_and_equivalents': get_latest(bs.loc['Cash And Cash Equivalents']) if 'Cash And Cash Equivalents' in bs.index else 0,
                'accounts_receivable': get_latest(bs.loc['Accounts Receivable']) if 'Accounts Receivable' in bs.index else 0,
                'inventory': get_latest(bs.loc['Inventory']) if 'Inventory' in bs.index else 0,
                'current_assets': get_latest(bs.loc['Current Assets']) if 'Current Assets' in bs.index else 0,
                'current_liabilities': get_latest(bs.loc['Current Liabilities']) if 'Current Liabilities' in bs.index else 0,
                'long_term_debt': get_latest(bs.loc['Long Term Debt']) if 'Long Term Debt' in bs.index else 0,
                'total_debt': get_latest(bs.loc['Total Debt']) if 'Total Debt' in bs.index else 0,
                # 计算指标
                'current_ratio': get_latest(bs.loc['Current Assets']) / get_latest(bs.loc['Current Liabilities']) if 'Current Assets' in bs.index and 'Current Liabilities' in bs.index and get_latest(bs.loc['Current Liabilities']) > 0 else 0,
                'debt_to_equity': get_latest(bs.loc['Total Debt']) / get_latest(bs.loc['Total Equity Gross Minority Interest']) if 'Total Equity Gross Minority Interest' in bs.index and get_latest(bs.loc['Total Equity Gross Minority Interest']) > 0 else 0
            }
        except Exception as e:
            print(f"⚠️ 获取资产负债表失败：{e}")
            return {}
    
    def get_cashflow(self) -> dict:
        """获取现金流量表数据"""
        try:
            cf = self.stock.cashflow
            
            def get_latest(series):
                if len(series) > 0:
                    return series.iloc[0]
                return 0
            
            return {
                'operating_cashflow': get_latest(cf.loc['Operating Cash Flow']) if 'Operating Cash Flow' in cf.index else 0,
                'investing_cashflow': get_latest(cf.loc['Investing Cash Flow']) if 'Investing Cash Flow' in cf.index else 0,
                'financing_cashflow': get_latest(cf.loc['Financing Cash Flow']) if 'Financing Cash Flow' in cf.index else 0,
                'free_cashflow': get_latest(cf.loc['Free Cash Flow']) if 'Free Cash Flow' in cf.index else 0,
                'capital_expenditure': get_latest(cf.loc['Capital Expenditure']) if 'Capital Expenditure' in cf.index else 0,
                'depreciation_amortization': get_latest(cf.loc['Depreciation And Amortization']) if 'Depreciation And Amortization' in cf.index else 0,
                # 计算指标
                'fcf_margin': get_latest(cf.loc['Free Cash Flow']) / get_latest(cf.loc['Operating Cash Flow']) if 'Operating Cash Flow' in cf.index and get_latest(cf.loc['Operating Cash Flow']) > 0 else 0,
                'cash_conversion': get_latest(cf.loc['Free Cash Flow']) / get_latest(cf.loc['Net Income']) if 'Net Income' in cf.index and get_latest(cf.loc['Net Income']) > 0 else 0
            }
        except Exception as e:
            print(f"⚠️ 获取现金流量表失败：{e}")
            return {}
    
    def get_analyst_estimates(self) -> dict:
        """获取分析师预期"""
        try:
            return {
                'target_price_mean': self.stock.analyst_price_targets.get('mean', 0),
                'target_price_high': self.stock.analyst_price_targets.get('high', 0),
                'target_price_low': self.stock.analyst_price_targets.get('low', 0),
                'recommendation': self.stock.recommendations.iloc[0]['period'] if len(self.stock.recommendations) > 0 else '',
                'strong_buy': int(self.stock.recommendations.iloc[0]['strongBuy']) if len(self.stock.recommendations) > 0 else 0,
                'buy': int(self.stock.recommendations.iloc[0]['buy']) if len(self.stock.recommendations) > 0 else 0,
                'hold': int(self.stock.recommendations.iloc[0]['hold']) if len(self.stock.recommendations) > 0 else 0,
                'sell': int(self.stock.recommendations.iloc[0]['sell']) if len(self.stock.recommendations) > 0 else 0,
                'strong_sell': int(self.stock.recommendations.iloc[0]['strongSell']) if len(self.stock.recommendations) > 0 else 0
            }
        except Exception as e:
            print(f"⚠️ 获取分析师预期失败：{e}")
            return {}
    
    def get_sec_filings(self) -> dict:
        """获取 SEC 文件列表"""
        try:
            # 获取 CIK 编号
            cik_url = f"https://data.sec.gov/submissions/CIK{self.ticker}.json"
            response = requests.get(cik_url, headers=self.sec_headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                recent = data.get('filings', {}).get('recent', {})
                return {
                    'accession_numbers': recent.get('accessionNumber', [])[:10],
                    'filing_dates': recent.get('filingDate', [])[:10],
                    'report_dates': recent.get('reportDate', [])[:10],
                    'form_types': recent.get('form', [])[:10],
                    'titles': recent.get('primaryDocument', [])[:10]
                }
        except Exception as e:
            print(f"⚠️ 获取 SEC 文件失败：{e}")
        return {}
    
    def get_company_info(self) -> dict:
        """获取公司基本信息"""
        try:
            info = self.stock.info
            return {
                'company_name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'website': info.get('website', ''),
                'description': info.get('longBusinessSummary', ''),
                'employees': info.get('fullTimeEmployees', 0),
                'headquarters': info.get('city', '') + ', ' + info.get('state', '') + ', ' + info.get('country', '') if info.get('city') else '',
                'founded': info.get('founded', 0),
                'ceo': info.get('companyOfficers', [{}])[0].get('name', '') if info.get('companyOfficers') else ''
            }
        except Exception as e:
            print(f"⚠️ 获取公司信息失败：{e}")
            return {}
    
    def _calculate_growth(self, series) -> float:
        """计算增长率（YoY）"""
        if len(series) >= 2:
            current = series.iloc[0]
            previous = series.iloc[1]
            if previous > 0:
                return (current - previous) / previous
        return 0
    
    def get_all_data(self, use_cache=True) -> dict:
        """获取所有数据"""
        # 检查缓存
        if use_cache and self.is_cache_valid():
            print(f"✅ 使用缓存数据：{self.ticker}")
            return self.load_cache()
        
        print(f"📊 获取 {self.ticker} 数据...")
        
        data = {
            'symbol': self.ticker,
            'fetched_at': datetime.now().isoformat(),
            'company_info': self.get_company_info(),
            'price': self.get_price_data(),
            'financials': self.get_financials(),
            'balance_sheet': self.get_balance_sheet(),
            'cashflow': self.get_cashflow(),
            'analyst_estimates': self.get_analyst_estimates(),
            'sec_filings': self.get_sec_filings()
        }
        
        # 保存到缓存
        self.save_cache(data)
        print(f"✅ 数据已缓存：{self.cache_file}")
        
        return data


def fetch_stock_data(ticker: str, use_cache=True) -> dict:
    """便捷函数：获取股票数据"""
    fetcher = StockDataFetcher(ticker)
    return fetcher.get_all_data(use_cache=use_cache)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python fetch_data.py <股票代码> [use_cache=true/false]")
        print("示例：python fetch_data.py NVDA")
        print("      python fetch_data.py TSLA false")
        sys.exit(1)
    
    ticker = sys.argv[1]
    use_cache = sys.argv[2].lower() != 'false' if len(sys.argv) > 2 else True
    
    data = fetch_stock_data(ticker, use_cache)
    print(json.dumps(data, indent=2, ensure_ascii=False))
