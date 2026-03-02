# tech-earnings-deepdive-openclaw-skill

科技股财报深度分析与多视角投资备忘录系统（v3.0）

---

## 作者

- [Ruby](https://x.com/Rubywang)
- [Star](https://x.com/starzq)
- 原项目：https://github.com/star23/Day1Global-Skills/

---

## 功能概述

一个为 AI 打造的科技股财报深度分析与多视角投资备忘录系统，覆盖：

- **16 大分析模块**（A-P）
- **6 大投资哲学视角**
- **多方法估值矩阵**
- **反偏见框架**
- **可执行决策体系**

---

## 触发条件

当用户询问以下类型问题时自动触发：

| 场景 | 示例提问 |
|------|---------|
| 财报分析 | "帮我看看 NVDA 最新财报" |
| 季报解读 | "META 这季度表现如何？" |
| 持仓决策 | "该不该继续持有 MSFT？" |
| 深度研究 | "帮我做个 AAPL 的 deep dive" |
| 估值判断 | "GOOGL 现在贵不贵？" |
| 多角度分析 | "投资大师怎么看 AMZN？" |

---

## 用法

```bash
# 命令行调用
~/.openclaw/workspace/skills/tech-earnings-deepdive-openclaw-skill/run.sh <股票代码>

# 示例
~/.openclaw/workspace/skills/tech-earnings-deepdive-openclaw-skill/run.sh NVDA
~/.openclaw/workspace/skills/tech-earnings-deepdive-openclaw-skill/run.sh TSLA
~/.openclaw/workspace/skills/tech-earnings-deepdive-openclaw-skill/run.sh MSFT
```

或在对话中直接询问：
- "帮我深度分析一下 NVDA 最新一季的财报"
- "TSLA 这季度财报出来了，帮我做个全面的 deep dive"
- "从多个投资大师的视角帮我看看 MSFT，现在值得买入吗？"

---

## 分析框架

### 1. Key Forces（决定性力量）

锚定 1-3 个决定公司未来价值的决定性力量

### 2. 16 大分析模块

| 模块 | 名称 | 说明 |
|------|------|------|
| A | 收入质量 | Revenue Quality |
| B | 盈利能力 | Profitability |
| C | 现金流 | Cash Flow |
| D | 前瞻指引 | Forward Guidance |
| E | 竞争格局 | Competitive Landscape |
| F | 核心 KPI | Core KPIs |
| G | 产品与新业务 | Products & New Businesses |
| H | 合作伙伴生态 | Partner Ecosystem |
| I | 高管团队 | Executive Team |
| J | 宏观政策 | Macro & Policy |
| K | 估值模型 | Valuation Models |
| L | 筹码分布 | Ownership Distribution |
| M | 长期监控变量 | Long-term Monitoring Variables |
| N | 研发效率 | R&D Efficiency |
| O | 会计质量 | Accounting Quality |
| P | ESG 筛查 | ESG Screening |

### 3. 6 大投资哲学视角

| 视角 | 代表人物 | 关注点 |
|------|---------|--------|
| 质量复利 | 巴菲特/芒格 | 护城河、ROE、自由现金流 |
| 想象力成长 | Baillie Gifford/ARK | TAM、颠覆性创新、成长速度 |
| 基本面多空 | Tiger Cubs | 相对价值、催化剂、风险收益比 |
| 深度价值 | Klarman/Marks | 安全边际、资产价值、逆向机会 |
| 催化剂驱动 | Tepper/Ackman | 事件驱动、 activist 机会 |
| 宏观战术 | Druckenmiller | 宏观环境、流动性、行业轮动 |

### 4. 多方法估值矩阵

- Owner Earnings（所有者收益）
- PEG（成长调整市盈率）
- 反向 DCF（隐含增长率）
- 魔法公式（Greenblatt）
- EV/EBITDA 行业对标
- EV/Revenue + Rule of 40

### 5. Variant View（变异视角）

找出市场共识的盲点

### 6. 反偏见框架

- 6 大认知陷阱自检
- 7 大财务红旗
- 5 大科技股盲区
- Pre-Mortem 事前尸检

### 7. 可执行决策

- Action Price（行动价格）
- 建仓节奏
- 加仓/减仓/清仓触发条件
- 长期监控清单

---

## 三层证据体系

| 层级 | 类型 | 举例 |
|------|------|------|
| 第一层 | 一手来源 | CEO 原话、员工评价、客户评价、GitHub 活跃度、专利、招聘动向 |
| 第二层 | 事实来源 | SEC 文件（10-K/10-Q/8-K）、财报数据、法庭文件 |
| 第三层 | 观点来源 | 卖方研报、新闻分析、价格目标汇总 |

---

## 依赖

- `web_search` 工具
- `web_fetch` 工具
- Python 3.x
- 网络连接

---

## 配置

编辑 `config.json` 设置：

```json
{
  "default_stock": "NVDA",
  "output_format": "markdown",
  "cache_ttl_hours": 24,
  "enable_modules": ["all"],
  "enable_perspectives": ["all"]
}
```

---

## 输出

Skill 生成的完整报告包含：

1. 执行摘要与 TL;DR
2. Key Forces（决定性力量）
3. 16 大模块分析（A-P）
4. 估值矩阵（多方法 + 敏感性 + 概率加权情景）
5. 筹码分布
6. Variant View（变异视角）
7. 6 大投资哲学视角汇总
8. Pre-Mortem 与反偏见检查
9. 长期监控变量与 Action Trigger
10. 决策框架（持仓分类 / Action Price / 建仓节奏 / 仓位建议）

---

## 协同技能

| 技能 | 协同方式 |
|------|---------|
| us-value-investing | 完成财报分析后，运行四维价值评分做交叉验证 |
| us-market-sentiment | 模块 J 涉及宏观情绪时联动 |
| macro-liquidity | 流动性环境是 Key Force 时联动 |

---

## 免责声明

此 Skill 生成的分析基于公开信息和模型推算，仅供研究参考，不构成投资建议。投资有风险，决策需谨慎。

---

## 版本

- v3.0 - 完整版（16 模块 + 6 视角 + 估值矩阵）
- 适配：OpenClaw
