# 📦 Tech Earnings Deep Dive Skill - 分享指南

---

## 🎁 分享包位置

**文件位置：** `/tmp/tech-earnings-deepdive-openclaw-skill-skill.zip`
**文件大小：** 2.9MB（优化后）

---

## 📤 分享方式

### 方式 1：直接发送文件（推荐）⭐

**步骤：**
1. 找到文件：`/tmp/tech-earnings-deepdive-openclaw-skill-skill.zip`
2. 通过微信/QQ/邮件/AirDrop 发送

**优点：** 最简单直接，不需要第三方服务

---

### 方式 2：网盘分享链接

**iCloud Drive：**
```bash
cp /tmp/tech-earnings-deepdive-openclaw-skill-skill.zip ~/Library/Mobile\ Documents/com~apple~CloudDocs/
# 然后在 iCloud.com 生成分享链接
```

**百度网盘/Google Drive：**
1. 上传文件
2. 创建分享链接
3. 发送给朋友

---

### 方式 3：GitHub 仓库（最专业）🚀

**步骤：**
```bash
cd /tmp/tech-earnings-deepdive-openclaw-skill-share
rm -rf cache/ output/ .DS_Store

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/tech-earnings-deepdive-openclaw-skill-skill.git
git push -u origin main
```

**优点：** 可更新、有版本管理、支持开源

---

## 📋 给朋友的使用说明

### 3 步安装

```bash
# 1. 解压
unzip tech-earnings-deepdive-openclaw-skill-skill.zip

# 2. 复制
cp -r tech-earnings-deepdive-openclaw-skill-share ~/.openclaw/workspace/skills/tech-earnings-deepdive-openclaw-skill

# 3. 安装依赖
cd ~/.openclaw/workspace/skills/tech-earnings-deepdive-openclaw-skill
python3 -m venv venv
source venv/bin/activate
pip install yfinance markdown weasyprint
```

### 测试运行

```bash
python3 modules/batch_analysis.py AAPL
open output/AAPL_analysis.html
```

---

## ⚠️ 系统要求

- **Python：** 3.8+
- **系统：** macOS / Linux / Windows
- **内存：** 4GB+
- **磁盘：** 100MB+

---

## 📞 常见问题

**Q: 导入 yfinance 失败？**
```bash
source venv/bin/activate
pip install yfinance
```

**Q: 报告打不开？**
```bash
open output/AAPL_analysis.html  # Mac
```

---

*基于 Day1Global 框架 · 机构级投资分析系统*
