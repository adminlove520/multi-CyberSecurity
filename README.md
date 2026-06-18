# multi-CyberSecurity

> AI驱动的网络安全技能框架 — 融合MITRE ATT&CK + NIST CSF标准

[![技能数量](https://img.shields.io/badge/skills-199-blue)](skills_index.json)
[![ATT&CK覆盖](https://img.shields.io/badge/ATT%26CK-97%20techniques-green)](mappings/attack-navigator-layer.json)
[![MIT License](https://img.shields.io/badge/license-Apache--2.0-yellow)](LICENSE)

## 核心能力

- **39个安全分类**，覆盖渗透测试、安全审计、应急响应、云安全、代码审计等全领域
- **MITRE ATT&CK** 标准化映射，147个skill已关联97个ATT&CK技术ID
- **NIST CSF** 全覆盖，每个skill均标注对应的CSF控制措施
- **YAML标准格式**，机器可读，便于AI Agent动态调用

## 目录结构

```
00-09/  信息搜集 · 漏洞扫描 · 漏洞利用
10-19/  权限提升 · 后渗透 · 横向移动 · 持久化
20-29/  痕迹清除 · 报告撰写 · 移动安全 · 区块链 · IoT
30-39/  SOC运营 · 威胁狩猎 · 数字取证 · 容器安全 · API安全
framework/  红队框架（jailbreak技能分级体系）
mappings/   ATT&CK Navigator可视化层
tools/      标准化脚本集
```

## 快速使用

```bash
# 搜索特定ATT&CK技术的相关skill
grep -l "T1059" */skills/*.md

# 验证所有skill的frontmatter格式
python3 tools/validate_skills.py

# 重新标准化skill格式
python3 tools/transform_skills.py

# 查看ATT&CK覆盖仪表盘
# 在 https://mitre-attack.github.io/attack-navigator/ 加载 mappings/attack-navigator-layer.json
```

## 格式标准

每个skill采用统一YAML frontmatter：

```yaml
---
name: skill-name-kebab-case
description: 简短描述（150-200字符）
domain: cybersecurity
subdomain: category-subdomain
tags:
  - technique
  - tool-name
version: '1.0.0'
author: multi-cybersecurity
license: Apache-2.0
nist_csf:
  - PR.AC-01
mitre_attack:
  - T1190
---
```

## 与源仓库的差异化

| 特性 | Anthropic-Cybersecurity-Skills | multi-CyberSecurity |
|------|-------------------------------|----------------------|
| 语言 | 英文 | 中文为主，标注英文术语 |
| 分类 | 扁平（~20类） | 层级（39类垂直分类） |
| Agent | 无 | 7个专用Agent + 8阶段pipeline |
| 框架 | 无 | 红队jailbreak分级框架 |
| NIST CSF | 部分 | 100%覆盖 |
| 索引 | JSON | JSON + Navigator Layer |
