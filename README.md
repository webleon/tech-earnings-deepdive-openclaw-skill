# Tech Earnings Deep Dive Skill

科技股财报深度分析与多视角投资备忘录系统

---

## 📦 安装完成

**位置：** `~/.openclaw/workspace/skills/tech-earnings-deepdive/`

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

## 📊 功能特性

### 16 大分析模块（A-P）

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

### 6 大投资哲学视角

| 视角 | 代表人物 | 关注点 |
|------|---------|--------|
| 质量复利 | 巴菲特/芒格 | 护城河、ROE、自由现金流 |
| 想象力成长 | Baillie Gifford/ARK | TAM、颠覆性创新、成长速度 |
| 基本面多空 | Tiger Cubs | 相对价值、催化剂、风险收益比 |
| 深度价值 | Klarman/Marks | 安全边际、资产价值 |
| 催化剂驱动 | Tepper/Ackman | 事件驱动、activist 机会 |
| 宏观战术 | Druckenmiller | 宏观环境、流动性、行业轮动 |

### 多方法估值矩阵

- Owner Earnings（所有者收益）
- PEG（成长调整市盈率）
- 反向 DCF（隐含增长率）
- 魔法公式（Greenblatt）
- EV/EBITDA 行业对标
- EV/Revenue + Rule of 40

---

## 📁 目录结构

```
tech-earnings-deepdive/
├── SKILL.md              # Skill 配置文件
├── config.json           # 运行时配置
├── run.sh                # 主脚本
├── modules/              # 分析模块
│   ├── fetch_data.py     # 数据获取
│   ├── analyze.py        # 16 模块分析
│   ├── perspectives.py   # 6 大视角分析
│   ├── valuation.py      # 估值分析
│   └── report.py         # 报告生成
├── templates/            # 报告模板
├── cache/                # 数据缓存
└── log/                  # 日志目录
```

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

## 📝 输出示例

报告将包含以下部分：

1. ⚡ 执行摘要 (TL;DR)
2. 🎯 Key Forces（决定性力量）
3. 📐 16 大模块分析
4. 💰 估值矩阵
5. 👁️ 6 大投资哲学视角
6. 🎯 Variant View（变异视角）
7. ⚠️ 反偏见框架
8. 📋 长期监控变量
9. 🎯 决策框架

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

## 🔄 版本

- **v3.0.0** - OpenClaw 适配版
  - 完整复刻原项目功能、逻辑和方法论
  - 与现有 memory 和脚本隔离
  - 独立配置和缓存
