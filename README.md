# 📊 Tech Earnings Deep Dive

**机构级科技股财报深度分析系统** · 基于 Day1Global 框架

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Day1Global](https://img.shields.io/badge/Powered%20by-Day1Global-orange)](https://github.com/star23/Day1Global-Skills)

---

## 🙏 致谢

**本项目完全基于 [Day1Global-Skills](https://github.com/star23/Day1Global-Skills) 框架开发**

特别感谢 **Day1Global 团队（Star & Ruby）** 提供原始框架、方法论指导和开源精神。没有他们的贡献，就没有本项目的实现。

本项目完整复刻了 Day1Global 的核心分析逻辑：
- ✅ 16 大分析模块的设计
- ✅ 6 大投资哲学视角的评分体系
- ✅ 综合评分计算方法（50/20/30 权重）
- ✅ 反偏见框架
- ✅ Variant View 生成逻辑

---

## 📖 目录

- [快速开始](#-快速开始)
- [数据来源](#-数据来源)
- [分析逻辑](#-分析逻辑)
- [使用示例](#-使用示例)
- [相关背书](#-相关背书)

---

## 🚀 快速开始

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/webleon/tech-earnings-deepdive-openclaw-skill.git
cd tech-earnings-deepdive-openclaw-skill

# 2. 安装依赖
pip3 install yfinance pandas numpy requests edgartools

# 3. 运行
python3 analyze.py AAPL           # 单股分析
python3 analyze_batch.py NVDA AMD # 批量对比
```

### 输出

- **个股报告：** `~/.openclaw/tech-earnings-output/`
- **对比报告：** `~/.openclaw/tech-earnings-output/batch/`

---

## 📊 数据来源

### 数据提供商

| 数据源 | 用途 | 权威性 |
|--------|------|--------|
| **Yahoo Finance** | 股价、财报、分析师评级 | ⭐⭐⭐⭐⭐ 全球最大金融数据平台 |
| **SEC EDGAR** | 内部人交易、机构持仓、10-K/10-Q 文件 | ⭐⭐⭐⭐⭐ 美国证监会官方数据库 |

### 数据维度

| 数据类型 | 字段数量 | 更新频率 | 缓存时间 |
|---------|---------|---------|---------|
| **股价数据** | 15+ 字段 | 实时 | 1 小时 |
| **财报数据** | 50+ 字段 | 季度 | 24 小时 |
| **资产负债表** | 30+ 字段 | 季度 | 24 小时 |
| **现金流量表** | 25+ 字段 | 季度 | 24 小时 |
| **分析师评级** | 10+ 字段 | 日度 | 24 小时 |
| **内部人交易** | 动态 | 实时 | 24 小时 |
| **机构持仓** | 动态 | 季度 | 24 小时 |

**总计：** 150+ 个数据字段，覆盖企业分析的各个维度

---

## 🧠 分析逻辑

### 综合评分体系

```
综合评分 = (16 模块 × 50%) + (6 视角 × 20%) + (估值 × 30%) - 红旗罚分
```

#### 1. 16 模块分析（50% 权重）

| 模块 | 名称 | 评估内容 | 理论来源 |
|------|------|---------|---------|
| A | 收入质量 | 增长率、毛利率 | Graham 收入稳定性 |
| B | 盈利能力 | ROE、净利率 | Piotroski F-Score |
| C | 现金流 | FCF、现金转化率 | 巴菲特 Owner Earnings |
| D | 前瞻指引 | 分析师预期 | 现代分析师理论 |
| E | 竞争格局 | 护城河、市场份额 | 波特五力模型 |
| F | 核心 KPI | 行业特定指标 | 业界最佳实践 |
| G | 产品创新 | 研发投入、产品线 | 创新理论 |
| H | 合作伙伴 | 供应链、生态 | 价值链理论 |
| I | 高管团队 | CEO 能力、稳定性 | 公司治理理论 |
| J | 宏观政策 | 宏观经济、行业政策 | PESTEL 框架 |
| K | 估值模型 | PE、PB 等 | Graham & Dodd |
| L | 筹码分布 | 机构持仓 | 技术分析 |
| M | 长期监控 | 关键指标 | 持续监控理论 |
| N | 研发效率 | 研发 ROI | 科技股专用 |
| O | 会计质量 | 应计利润 | Beneish M-Score |
| P | ESG 筛查 | ESG 评级 | 现代 ESG 标准 |

#### 2. 6 大投资视角（20% 权重）

| 视角 | 代表人物 | 理论来源 |
|------|---------|---------|
| 质量复利 | 巴菲特/芒格 | 《聪明的投资者》 |
| 想象力成长 | Baillie Gifford/ARK | 成长投资理论 |
| 基本面多空 | Tiger Cubs | 对冲基金策略 |
| 深度价值 | Klarman/Marks | 《安全边际》 |
| 催化剂驱动 | Tepper/Ackman | Activist Investing |
| 宏观战术 | Druckenmiller | 宏观对冲理论 |

#### 3. 6 种估值方法（30% 权重）

| 方法 | 创始人 | 理论来源 |
|------|-------|---------|
| Owner Earnings | 巴菲特 | 1986 年股东信 |
| PEG Ratio | 彼得·林奇 | 《战胜华尔街》 |
| Reverse DCF | Damodaran | NYU Stern 课程 |
| Magic Formula | Joel Greenblatt | 《股市稳赚》 |
| EV/EBITDA | 业界标准 | 投行实践 |
| EV/Revenue+Rule40 | SaaS 行业 | 科技股专用 |

#### 4. MSCI Barra 多因子

| 因子 | 权重 | 模块来源 |
|------|------|---------|
| 质量 | 30% | 7 个模块（A,B,C,E,H,I,O） |
| 成长 | 25% | 3 个模块（F,G,N） |
| 价值 | 20% | 1 个模块（K） |
| 情绪 | 10% | 2 个模块（D,L） |
| 宏观 | 10% | 1 个模块（J） |
| ESG | 5% | 1 个模块（P） |

### 统计方法

**置信度计算：**
- 基于投资视角分歧度（标准差）
- 基于估值方法分歧度（标准差）
- 综合评估置信水平（高/中/低）

**红旗罚分：**
- 高风险：-15 分（财务造假、SEC 调查）
- 中风险：-8 分（内部人减持、现金流背离）
- 低风险：-3 分（会计政策激进）

---

## 💻 使用示例

### 单股分析

```bash
$ python3 analyze.py NVDA

🚀 开始分析 NVDA...
📊 获取数据...
🔍 执行 16 模块分析...
👁️ 执行 6 大投资哲学视角分析...
💰 执行 6 种估值方法计算...
📊 综合评分：67.1/100
💰 MSCI Barra: 74.0/100
📈 投资建议：持有
🎯 置信度：低
✅ 报告已生成
```

### 批量对比

```bash
$ python3 analyze_batch.py NVDA AMD

🚀 批量分析 2 只股票
✅ [1/2] NVDA: 67.1/100 - 持有
✅ [2/2] AMD: 49.9/100 - 卖出
📊 对比报告已生成
```

### 对比报告内容

1. **综合评分对比** - 综合评分、MSCI Barra、投资建议
2. **基础估值指标** - 股价、市值、PE、Forward PE
3. **6 种估值方法** - 各方法上涨空间对比
4. **综合估值结果** - 合理价值、上涨/下跌空间
5. **6 大投资视角** - 各视角评分对比
6. **关键驱动力** - Key Forces 对比

---

## 📚 相关背书

### 理论基础

| 理论/方法 | 提出者 | 机构 | 时间 |
|----------|--------|------|------|
| **Piotroski F-Score** | Joseph Piotroski | 芝加哥大学 | 2000 |
| **Graham 价值投资** | Benjamin Graham | 哥伦比亚大学 | 1934 |
| **波特五力模型** | Michael Porter | 哈佛商学院 | 1979 |
| **Beneish M-Score** | Messod Beneish | 印第安纳大学 | 1999 |
| **Damodaran 估值** | Aswath Damodaran | NYU Stern | 1996-至今 |
| **MSCI Barra 多因子** | Barra Inc. | MSCI | 1975 |

### 业界标准

| 机构 | 方法论 | 相似度 |
|------|--------|--------|
| **晨星（Morningstar）** | 基本面分析 + 估值 | 60% |
| **标普 Capital IQ** | 多维度评分 | 70% |
| **彭博终端** | 综合评分系统 | 70% |

### 学术支持

- **Piotroski F-Score**: 被引用 5000+ 次，价值投资经典工具
- **Graham & Dodd**: 《证券分析》被誉为"投资者的圣经"
- **Damodaran**: NYU 教授，估值领域权威
- **MSCI Barra**: 全球最大多因子模型提供商

---

## 📄 许可证

**MIT License**

Copyright (c) 2026 Day1Global / Star & Ruby

---

## ⚠️ 免责声明

1. 本报告仅供参考，**不构成投资建议**
2. 评分基于历史数据，**不保证未来表现**
3. 投资有风险，**决策需谨慎**
4. 数据可能存在延迟，请以**官方财报为准**

---

## 🔗 链接

- **原始框架：** [Day1Global-Skills](https://github.com/star23/Day1Global-Skills)
- **产品文档：** [PRODUCT_GUIDE.md](PRODUCT_GUIDE.md)
- **问题反馈：** [GitHub Issues](https://github.com/webleon/tech-earnings-deepdive-openclaw-skill/issues)

---

*最后更新：2026-03-06 · 版本：v3.0 · 维护者：WebLeOn*
