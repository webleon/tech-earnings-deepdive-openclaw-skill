# Tech Earnings Deep Dive Skill

机构级科技股财报深度分析与多视角投资备忘录系统

---

## 功能特性

- **投资摘要**：专业投资报告风格，包含核心优势、关键驱动、风险提示、估值判断、综合建议
- **模块分析**：16 个独立分析模块，三列网格显示 Top 3 核心优势
- **投资视角**：6 大投资哲学视角评分（巴菲特、芒格、彼得·林奇等）
- **关键驱动因素**：自动识别 1-3 个决定性力量
- **认知偏见检测**：6 大认知偏见完整检测表
- **财务红旗**：GAAP vs Non-GAAP、股票期权稀释等风险分析
- **Pre-Mortem**：事前尸检，识别潜在风险

---

## 安装

```bash
# 克隆到 OpenClaw Skills 目录
cd ~/.openclaw/workspace/skills/
git clone https://github.com/webleon/tech-earnings-deepdive-skill.git tech-earnings-deepdive

# 安装依赖
cd tech-earnings-deepdive
python3 -m venv venv
source venv/bin/activate
pip install yfinance
```

---

## 使用

```bash
# 激活虚拟环境
source venv/bin/activate

# 分析单只股票
python3 modules/batch_analysis.py NVDA

# 分析多只股票
python3 modules/batch_analysis.py AAPL MSFT GOOGL

# 查看报告
open output/NVDA_analysis.html
```

---

## 报告结构

1. **投资摘要** - 详细描述性总结（核心优势、驱动因素、风险、估值、建议）
2. **模块分析** - 16 个模块详细评分
3. **投资视角** - 6 大投资哲学视角
4. **关键驱动因素** - Top 3 关键力量（三列布局）
5. **认知偏见检测** - 完整 6 项检测表
6. **财务红旗** - 风险警示
7. **Pre-Mortem** - 事前检查

---

## 版本

当前版本：1.0.0

详细变更历史请查看 [CHANGELOG.md](CHANGELOG.md)

---

## 待优化

- [ ] 对比报告优化（应用单体报告样式）
- [ ] PDF 导出功能
- [ ] 图表可视化
- [ ] 数据导出（CSV/Excel）

---

*基于 Day1Global 框架开发*
