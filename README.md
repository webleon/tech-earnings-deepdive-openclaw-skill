# Tech Earnings Deep Dive Skill

科技股财报深度分析与多视角投资备忘录系统

Institutional-Grade Tech Stock Earnings Analysis & Multi-Perspective Investment Memo System

基于 Day1Global 框架 · 复刻专业投资机构分析方法论

Based on Day1Global Framework · Replicating Professional Investment Analysis Methodology

---

## 🌐 语言切换 / Language Switch

| 中文版本 | English Version |
|---------|-----------------|
| [🇨🇳 跳转到中文](#-中文版本) | [🇺🇸 Jump to English](#-english-version) |

---

# 🇨🇳 中文版本

## 🎯 系统概述

Tech Earnings Deep Dive 是一个为 AI 助手打造的机构级投资分析系统，专为科技股财报深度分析设计。系统完整复刻了专业投资机构的研究方法论，提供从数据获取、多维度分析到报告生成的全流程自动化解决方案。

通过整合 **16 大分析模块**、**6 大投资哲学视角**、**6 种估值方法**，配合反偏见框架和 Pre-Mortem 事前尸检工具，帮助投资者做出更理性、更全面、更可靠的投资决策。

**功能完成率：94%**

---

## 🚀 快速开始

### 方法 1：命令行调用

```bash
# 基本用法
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh NVDA

# 完整报告
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh TSLA --full

# 指定投资视角
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh MSFT --perspective buffett
```

### 方法 2：在对话中使用

直接在对话中询问：
- "帮我深度分析一下 NVDA 最新一季的财报"
- "TSLA 这季度财报出来了，帮我做个全面的 deep dive"
- "从多个投资大师的视角帮我看看 MSFT，现在值得买入吗？"

---

## 📁 模块架构

```
tech-earnings-deepdive/
├── modules/
│   ├── fetch_data.py          # 数据获取（yfinance + SEC EDGAR）
│   ├── analyze_full.py        # 16 模块分析引擎
│   ├── perspectives_full.py   # 6 大投资哲学视角评分
│   ├── valuation_full.py      # 6 种估值方法计算
│   ├── key_forces.py          # Key Forces 识别引擎
│   ├── bias_framework.py      # 反偏见框架检查
│   ├── variant_view.py        # Variant View 生成器
│   ├── batch_analysis.py      # 批量分析引擎
│   └── export_report.py       # HTML/Markdown 报告导出
├── SKILL.md                   # Skill 配置文件
├── config.json                # 运行时配置
└── run.sh                     # 命令行入口
```

---

## 🔍 核心功能

### 1️⃣ 数据获取层

系统通过 yfinance API 获取实时市场数据，配合本地缓存机制，确保数据获取的高效性和可靠性。所有财务数据均来自权威来源，确保分析的准确性和可信度。

| 数据类型 | 数据源 | 获取内容 | 状态 |
|---------|--------|---------|------|
| **股价数据** | yfinance API | 当前股价、市值、PE、52 周区间、Beta 系数 | ✅ 已实现 |
| **财报数据** | yfinance API | 营收、净利润、毛利率、运营利润、EBITDA | ✅ 已实现 |
| **资产负债表** | yfinance API | 总资产、总负债、现金、应收账款、存货 | ✅ 已实现 |
| **现金流量表** | yfinance API | 经营现金流、自由现金流、资本支出 | ✅ 已实现 |
| **分析师评级** | yfinance API | 买入/持有/卖出评级、目标价、评级分布 | ✅ 已实现 |
| **数据缓存** | 本地 JSON 文件 | 24 小时缓存，避免重复请求，提升效率 | ✅ 已实现 |

---

### 2️⃣ 16 模块分析引擎

16 模块分析是系统的核心分析框架，覆盖收入质量、盈利能力、现金流、竞争格局等关键维度。每个模块都有独立的评分逻辑和检查清单，确保分析的全面性和深度。

| 模块 | 分析方法 | 核心指标 | 评分逻辑 |
|------|---------|---------|---------|
| **A. 收入质量** | 增长率分析 | YoY 增长、QoQ 增长、毛利率 | 增长>20% 且毛利>50% 得高分 |
| **B. 盈利能力** | 利润率分析 | 净利率、ROE、运营利润率 | ROE>20% 且净利率>20% 得高分 |
| **C. 现金流** | 现金流质量 | FCF 利润率、现金转化率 | FCF 利润率>25% 得高分 |
| **D. 前瞻指引** | 分析师预期 | 目标价上涨空间 | 上涨>30% 得高分 |
| **E. 竞争格局** | 护城河分析 | 毛利率（定价权代理） | 毛利率>60% 得高分 |
| **F. 核心 KPI** | 增长质量 | 收入增长 vs 利润增长 | 双增长>20% 得高分 |
| **G. 产品与新业务** | 创新能力 | 研发投入占比 | 研发>15% 得高分 |
| **H. 合作伙伴生态** | 渠道健康度 | 应收账款占比 | 应收<20% 得高分 |
| **I. 高管团队** | 管理层评估 | CEO 信息、员工数 | 基础信息展示 |
| **J. 宏观政策** | 行业分析 | 行业分类 | 科技行业默认中等 |
| **K. 估值模型** | 估值水平 | PE、PB | PE<15 得高分 |
| **L. 筹码分布** | 分析师评级 | 买入比例 | 买入>80% 得高分 |
| **M. 长期监控变量** | 风险识别 | 5 个关键指标 | 固定 80 分 |
| **N. 研发效率** | 研发 ROI | 利润增长/研发投入 | 效率>2x 得高分 |
| **O. 会计质量** | 财务健康度 | 流动比率、负债率 | 流动>1.5 且负债<0.5 得高分 |
| **P. ESG 筛查** | ESG 评估 | 基础评估 | 默认 65 分 |

---

### 3️⃣ 6 大投资哲学视角

整合 6 种截然不同的投资世界观，每种视角都有独特的评分维度（各 25 分，总分 100 分）和核心问题。

| 视角 | 代表人物 | 评分维度 | 核心问题 |
|------|----------|---------|---------|
| **质量复利** | 巴菲特/芒格 | 护城河、ROE、自由现金流、管理层 | 市场关闭 10 年能安心睡觉吗？ |
| **想象力** | Baillie Gifford/ARK | TAM、创新能力、成长速度、长期潜力 | 5 年后不买会后悔吗？ |
| **基本面** | Tiger Cubs | 相对价值、催化剂、风险收益、做空机会 | 有 Variant View 吗？ |
| **深度价值** | Klarman/Marks | 安全边际、资产价值、逆向机会、清算价值 | 比清算价值低多少？ |
| **催化剂** | Tepper/Ackman | 催化剂强度、activist 机会、重组、并购 | 6-18 个月有什么催化剂？ |
| **宏观战术** | Druckenmiller | 宏观环境、流动性、行业轮动、趋势 | 宏观是顺风还是逆风？ |

---

### 4️⃣ 多方法估值矩阵

集成 6 种经典估值方法，覆盖不同行业、不同发展阶段的企业估值需求。

| 方法 | 创始人 | 计算公式 | 判断标准 |
|------|-------|---------|---------|
| **Owner Earnings** | 巴菲特 | 净利润 + 折旧 - 资本支出 | 10-15 倍合理 |
| **PEG Ratio** | 彼得·林奇 | PE / 盈利增长率 | <0.5 极具吸引力 |
| **Reverse DCF** | 逆向思维 | 从股价反推隐含增长率 | 隐含增长<历史=低估 |
| **Magic Formula** | 格林布拉特 | 盈利收益率 + ROIC 排名 | 综合排名<10% 优秀 |
| **EV/EBITDA** | 达摩达兰 | 企业价值 / EBITDA | 低于行业 20%+=低估 |
| **Rule of 40** | SaaS 行业 | 增长率 + 利润率 | ≥40% 优秀 |

---

### 5️⃣ 反偏见框架

通过系统化的检查清单，帮助识别和克服认知偏见、财务红旗和科技行业特有盲区。

#### 认知偏见（6 个）

| 偏见 | 检测方法 | 警告条件 |
|------|---------|---------|
| **确认偏误** | 卖出评级比例 | <5% 则警告 |
| **锚定效应** | 股价位置（52 周区间） | 接近极值则警告 |
| **叙事谬误** | 增长 vs 利润 | 高增长低利润则警告 |
| **从众心理** | 买入评级比例 | >90% 则警告 |
| **处置效应** | 通用检查 | 针对持仓场景 |
| **过度自信** | 通用检查 | 区间估计场景 |

#### 财务红旗（7 个）

| 红旗 | 检测方法 | 警告条件 |
|------|---------|---------|
| **收入确认异常** | 待实现 | - |
| **GAAP vs Non-GAAP** | 待实现 | - |
| **应收账款异常** | 应收/收入 | >30% 则标记 |
| **内部人交易** | 待接入 SEC Form 4 | - |
| **资本支出暴增** | CapEx/收入 | >20% 则标记 |
| **现金流背离** | 利润 vs 现金流 | 利润正但现金流负 |
| **负债结构恶化** | 负债率、流动比率 | 负债>1 或流动<1 |

#### 科技盲区（5 个）

| 盲区 | 检测方法 | 警告条件 |
|------|---------|---------|
| **TAM 幻觉** | 待实现 | - |
| **AI 收入真实性** | AI 关键词 | AI 相关则提示核实 |
| **股票期权稀释** | 待实现 | - |
| **CAC 拐点** | 待实现 | - |
| **监管尾部风险** | 市值 | >1 万亿则警告 |

---

### 6️⃣ Key Forces 识别

自动识别决定公司未来价值的 1-3 个决定性力量，按影响力排序（0-10 分）。

| 类型 | 判断逻辑 | 影响力评分 |
|------|---------|-----------|
| **增长驱动** | 收入/利润增长>20% | 增长率/5（最高 10 分） |
| **技术变革** | AI/云/机器学习关键词 | 关键词数×2+4（最高 10 分） |
| **护城河加深** | 毛利率>60% | 毛利率/8（最高 10 分） |
| **财务实力** | FCF 利润率>20% 且流动>1.5 | FCF/3 + 流动×2 |
| **市场情绪** | 分析师买入>80% 或上涨>30% | 买入%/15 + 上涨/5 |
| **行业趋势** | 科技/软件/半导体行业 | 固定 6 分 |

---

### 7️⃣ Variant View 生成器

识别市场共识盲点，生成独特的投资观点。

| 功能 | 实现方法 | 输出内容 |
|------|---------|---------|
| **市场共识** | 分析师评级汇总 | 买入比例、目标价、上涨空间 |
| **盲点识别** | 数据对比分析 | 现金流、增长质量、共识盲点 |
| **变异认知** | 盲点方向分析 | 看多/看空/中性 |
| **置信度评估** | 盲点数量及严重程度 | 高/中/低 |
| **可执行观点** | 根据方向生成建议 | 做多/做空/观望 + 理由 |

---

### 8️⃣ Pre-Mortem（事前尸检）

强大的逆向思维工具，通过假设投资已失败，倒推失败原因，提前识别风险。

| 组件 | 内容 |
|------|------|
| **核心问题** | 5 个标准化问题（核心假设、风险、竞争、管理层、宏观） |
| **静态提示** | 每个问题配思考方向提示 |
| **行动建议** | 4 步风险评估（概率、影响、应对、监控） |

---

## 📝 输出示例

报告将包含以下部分：

1. **📋 投资摘要** - 详细描述性总结（核心优势、驱动因素、风险、估值、建议）
2. **📊 模块分析** - 16 个模块详细评分（两列紧凑布局）
3. **💼 投资视角** - 6 大投资哲学视角（两列布局，含评分维度）
4. **✅ 关键驱动因素** - Top 3 关键力量（三列网格布局）
5. **🧠 认知偏见检测** - 完整 6 项检测表
6. **🚩 财务红旗** - 风险警示
7. **💀 Pre-Mortem** - 事前检查

---

## ⚙️ 配置

编辑 `config.json` 自定义：

```json
{
  "default_stock": "NVDA",
  "output_format": "markdown",
  "cache_ttl_hours": 24,
  "enable_modules": "all",
  "enable_perspectives": "all"
}
```

---

## 🔌 协同技能

| 技能 | 协同方式 |
|------|---------|
| us-value-investing | 四维价值评分交叉验证 |
| us-market-sentiment | 宏观情绪联动 |
| macro-liquidity | 流动性环境分析 |

---

## ⚠️ 免责声明

此 Skill 生成的分析基于公开信息和模型推算，仅供研究参考，不构成投资建议。投资有风险，决策需谨慎。

---

## 📄 许可证

基于 Day1Global 开源项目改编  
原项目：https://github.com/star23/Day1Global-Skills/

---

**[⬆ 返回顶部](#tech-earnings-deep-dive-skill)** | **[🇺🇸 Switch to English](#-english-version)**

---

# 🇺🇸 English Version

## 🎯 System Overview

Tech Earnings Deep Dive is an institutional-grade investment analysis system built for AI assistants, specifically designed for deep analysis of tech stock earnings. The system fully replicates professional investment research methodologies, providing a fully automated solution from data acquisition to multi-dimensional analysis and report generation.

By integrating **16 Analysis Modules**, **6 Investment Philosophy Perspectives**, and **6 Valuation Methods**, along with anti-bias frameworks and Pre-Mortem tools, it helps investors make more rational, comprehensive, and reliable investment decisions.

**Completion Rate: 94%**

---

## 🚀 Quick Start

### Method 1: Command Line

```bash
# Basic Usage
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh NVDA

# Full Report
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh TSLA --full

# Specify Investment Perspective
~/.openclaw/workspace/skills/tech-earnings-deepdive/run.sh MSFT --perspective buffett
```

### Method 2: In Conversation

Ask directly in conversation:
- "Analyze NVDA's latest quarterly earnings in depth"
- "TSLA just reported earnings, do a comprehensive deep dive"
- "Analyze MSFT from multiple investment masters' perspectives, is it worth buying now?"

---

## 📁 Module Architecture

```
tech-earnings-deepdive/
├── modules/
│   ├── fetch_data.py          # Data Acquisition (yfinance + SEC EDGAR)
│   ├── analyze_full.py        # 16-Module Analysis Engine
│   ├── perspectives_full.py   # 6 Investment Perspectives Scoring
│   ├── valuation_full.py      # 6 Valuation Methods Calculation
│   ├── key_forces.py          # Key Forces Identification Engine
│   ├── bias_framework.py      # Anti-Bias Framework Check
│   ├── variant_view.py        # Variant View Generator
│   ├── batch_analysis.py      # Batch Analysis Engine
│   └── export_report.py       # HTML/Markdown Report Export
├── SKILL.md                   # Skill Configuration
├── config.json                # Runtime Configuration
└── run.sh                     # Command Line Entry
```

---

## 🔍 Core Features

### 1️⃣ Data Acquisition Layer

The system acquires real-time market data through yfinance API, with local caching mechanism to ensure efficient and reliable data acquisition. All financial data comes from authoritative sources to ensure accuracy and credibility.

| Data Type | Source | Content | Status |
|---------|--------|---------|--------|
| **Stock Price** | yfinance API | Current price, market cap, PE, 52-week range, Beta | ✅ Implemented |
| **Financials** | yfinance API | Revenue, net income, gross margin, operating income, EBITDA | ✅ Implemented |
| **Balance Sheet** | yfinance API | Total assets, liabilities, cash, receivables, inventory | ✅ Implemented |
| **Cash Flow** | yfinance API | Operating cash flow, free cash flow, capital expenditure | ✅ Implemented |
| **Analyst Ratings** | yfinance API | Buy/Hold/Sell ratings, target price, rating distribution | ✅ Implemented |
| **Data Cache** | Local JSON files | 24-hour cache, avoids repeated requests | ✅ Implemented |

---

### 2️⃣ 16-Module Analysis Engine

The 16-module analysis is the core analytical framework of the system, covering key dimensions such as revenue quality, profitability, cash flow, and competitive landscape. Each module has independent scoring logic and checklists to ensure comprehensiveness and depth of analysis.

| Module | Analysis Method | Core Metrics | Scoring Logic |
|------|---------|---------|---------|
| **A. Revenue Quality** | Growth Analysis | YoY, QoQ, Gross Margin | Growth>20% & Margin>50% |
| **B. Profitability** | Margin Analysis | Net Margin, ROE, Operating Margin | ROE>20% & Net Margin>20% |
| **C. Cash Flow** | Cash Flow Quality | FCF Margin, Cash Conversion | FCF Margin>25% |
| **D. Forward Guidance** | Analyst Expectations | Target Price Upside | Upside>30% |
| **E. Competitive Landscape** | Moat Analysis | Gross Margin (Pricing Power) | Gross Margin>60% |
| **F. Core KPIs** | Growth Quality | Revenue vs Profit Growth | Dual Growth>20% |
| **G. Products & New Business** | Innovation Capability | R&D Spending Ratio | R&D>15% |
| **H. Partner Ecosystem** | Channel Health | Receivables Ratio | Receivables<20% |
| **I. Management Team** | Management Assessment | CEO Info, Employee Count | Basic Info Display |
| **J. Macro & Policy** | Industry Analysis | Industry Classification | Tech Industry Default Medium |
| **K. Valuation Models** | Valuation Level | PE, PB | PE<15 |
| **L. Ownership Distribution** | Analyst Ratings | Buy Ratio | Buy>80% |
| **M. Long-term Monitoring** | Risk Identification | 5 Key Indicators | Fixed 80 Points |
| **N. R&D Efficiency** | R&D ROI | Profit Growth/R&D Investment | Efficiency>2x |
| **O. Accounting Quality** | Financial Health | Current Ratio, Debt Ratio | Current>1.5 & Debt<0.5 |
| **P. ESG Screening** | ESG Assessment | Basic Assessment | Default 65 Points |

---

### 3️⃣ 6 Investment Philosophy Perspectives

Integrates 6 distinct investment worldviews, each with unique scoring dimensions (25 points each, 100 total) and core questions.

| Perspective | Representatives | Scoring Dimensions | Core Question |
|------|----------|---------|---------|
| **Quality Compounder** | Buffett/Munger | Moat, ROE, FCF, Management | Can you sleep well if market closes for 10 years? |
| **Imaginative** | Baillie Gifford/ARK | TAM, Innovation, Growth, Long-term Potential | Will you regret not buying in 5 years? |
| **Fundamental** | Tiger Cubs | Relative Value, Catalyst, Risk/Reward, Short Opportunity | Do you have a Variant View? |
| **Deep Value** | Klarman/Marks | Margin of Safety, Asset Value, Contrarian, Liquidation Value | How much below liquidation value? |
| **Catalyst** | Tepper/Ackman | Catalyst Strength, Activist, Restructuring, M&A | What catalyst in 6-18 months? |
| **Macro Tactical** | Druckenmiller | Macro Environment, Liquidity, Sector Rotation, Trend | Is macro a tailwind or headwind? |

---

### 4️⃣ Multi-Method Valuation Matrix

Integrates 6 classic valuation methods, covering valuation needs for different industries and development stages.

| Method | Founder | Formula | Criteria |
|------|-------|---------|---------|
| **Owner Earnings** | Buffett | Net Income + D&A - CapEx | 10-15x reasonable |
| **PEG Ratio** | Peter Lynch | PE / Earnings Growth | <0.5 very attractive |
| **Reverse DCF** | Reverse Thinking | Implied growth from stock price | Implied growth < historical = undervalued |
| **Magic Formula** | Greenblatt | Earnings Yield + ROIC Rank | Combined rank <10% excellent |
| **EV/EBITDA** | Damodaran | Enterprise Value / EBITDA | <Industry -20% = undervalued |
| **Rule of 40** | SaaS Industry | Growth Rate + Profit Margin | ≥40% excellent |

---

### 5️⃣ Anti-Bias Framework

Systematic checklists to help identify and overcome cognitive biases, financial red flags, and tech-specific blind spots.

#### Cognitive Biases (6)

| Bias | Detection | Warning Condition |
|------|---------|---------|
| **Confirmation Bias** | Sell Rating Ratio | Warn if <5% |
| **Anchoring** | Stock Price Position (52-week) | Warn if near extremes |
| **Narrative Fallacy** | Growth vs Profit | Warn if high growth low profit |
| **Herding** | Buy Rating Ratio | Warn if >90% |
| **Disposition Effect** | General Check | For holding scenarios |
| **Overconfidence** | General Check | Interval estimation scenarios |

#### Financial Red Flags (7)

| Red Flag | Detection | Warning Condition |
|------|---------|---------|
| **Revenue Recognition** | TBD | - |
| **GAAP vs Non-GAAP** | TBD | - |
| **Receivables Anomaly** | Receivables/Revenue | Flag if >30% |
| **Insider Trading** | SEC Form 4 | TBD |
| **CapEx Surge** | CapEx/Revenue | Flag if >20% |
| **Cash Flow Divergence** | Profit vs Cash Flow | Flag if profit positive but cash flow negative |
| **Debt Structure** | Debt Ratio, Current Ratio | Flag if debt>1 or current<1 |

#### Tech Blind Spots (5)

| Blind Spot | Detection | Warning Condition |
|------|---------|---------|
| **TAM Illusion** | TBD | - |
| **AI Revenue Authenticity** | AI Keywords | Prompt verification if AI-related |
| **Stock Option Dilution** | TBD | - |
| **CAC Inflection** | TBD | - |
| **Regulatory Tail Risk** | Market Cap | Warn if >1 trillion |

---

### 6️⃣ Key Forces Identification

Automatically identifies 1-3 decisive forces determining company future value, ranked by influence (0-10 points).

| Type | Logic | Influence Score |
|------|---------|-----------|
| **Growth Driver** | Revenue/Profit Growth>20% | Growth/5 (max 10) |
| **Technology Shift** | AI/Cloud/ML Keywords | Keywords×2+4 (max 10) |
| **Moat Deepening** | Gross Margin>60% | Margin/8 (max 10) |
| **Financial Strength** | FCF Margin>20% & Current>1.5 | FCF/3 + Current×2 |
| **Market Sentiment** | Analyst Buy>80% or Upside>30% | Buy%/15 + Upside/5 |
| **Industry Trend** | Tech/Software/Semiconductor | Fixed 6 Points |

---

### 7️⃣ Variant View Generator

Identifies market consensus blind spots and generates unique investment viewpoints.

| Function | Method | Output |
|------|---------|---------|
| **Market Consensus** | Analyst Rating Summary | Buy Ratio, Target Price, Upside |
| **Blind Spot ID** | Data Comparison | Cash Flow, Growth Quality, Consensus Blind Spots |
| **Variant Perception** | Blind Spot Direction | Bullish/Bearish/Neutral |
| **Confidence Assessment** | Blind Spot Count & Severity | High/Medium/Low |
| **Actionable View** | Generate Based on Direction | Long/Short/Hold + Reasoning |

---

### 8️⃣ Pre-Mortem

Powerful reverse thinking tool that identifies risks in advance by assuming investment failure and working backwards.

| Component | Content |
|------|------|
| **Core Questions** | 5 Standardized Questions (Assumptions, Risks, Competition, Management, Macro) |
| **Static Hints** | Thinking Direction Hints for Each Question |
| **Action Recommendations** | 4-Step Risk Assessment (Probability, Impact, Mitigation, Monitoring) |

---

## 📝 Output Example

Report includes:

1. **📋 Investment Summary** - Detailed descriptive summary (strengths, drivers, risks, valuation, recommendations)
2. **📊 Module Analysis** - 16 modules detailed scoring (two-column compact layout)
3. **💼 Investment Perspectives** - 6 investment philosophy perspectives (two-column layout with scoring dimensions)
4. **✅ Key Drivers** - Top 3 key forces (three-column grid layout)
5. **🧠 Cognitive Biases Detection** - Complete 6-item detection table
6. **🚩 Financial Red Flags** - Risk warnings
7. **💀 Pre-Mortem** - Pre-mortem check

---

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
  "default_stock": "NVDA",
  "output_format": "markdown",
  "cache_ttl_hours": 24,
  "enable_modules": "all",
  "enable_perspectives": "all"
}
```

---

## 🔌 Synergistic Skills

| Skill | Synergy |
|------|---------|
| us-value-investing | Four-dimensional value scoring cross-validation |
| us-market-sentiment | Macro sentiment linkage |
| macro-liquidity | Liquidity environment analysis |

---

## ⚠️ Disclaimer

Analysis generated by this Skill is based on public information and model calculations, for research reference only, does not constitute investment advice. Investment involves risks, make decisions cautiously.

---

## 📄 License

Based on Day1Global open source project  
Original Project: https://github.com/star23/Day1Global-Skills/

---

**[⬆ Back to Top](#tech-earnings-deep-dive-skill)** | **[🇨🇳 切换到中文](#-中文版本)**

---

*Last Updated: 2026-03-02*
