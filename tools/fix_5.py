#!/usr/bin/env python3
"""Fix 5 files whose description contains YAML-special chars."""
import os, re, yaml

def sq(s):
    return "'" + str(s).replace("'", "''") + "'"

files = {
    "/tmp/our/09-报告撰写-Reporting/skills/安全报告模板-HTML.md": {
        "name": "安全报告模板-HTML格式",
        "description": "HTML报告模板基于Bootstrap 5，支持响应式设计、Chart.js图表，暗色模式、侧边栏导航、打印和PDF导出功能，可快速生成专业的渗透测试安全评估报告。",
        "subdomain": "reporting",
    },
    "/tmp/our/09-报告撰写-Reporting/skills/安全报告模板-Markdown.md": {
        "name": "安全报告模板-Markdown格式",
        "description": "Markdown格式安全报告模板，兼容CVSS 3.1/4.0、OWASP Top 10 2021、CWE、PCI DSS、等保2.0等标准格式，可导出为HTML、PDF、DOCX多种格式。",
        "subdomain": "reporting",
    },
    "/tmp/our/09-报告撰写-Reporting/skills/安全报告模板-Word.md": {
        "name": "安全报告模板-Word-PDF格式",
        "description": "Word格式安全报告模板，基于python-docx库生成，支持自动化填充漏洞信息、图片插入、目录生成，可直接导出为.docx或转换为PDF格式。",
        "subdomain": "reporting",
    },
    "/tmp/our/16-大模型安全-LLMSecurity/skills/AI Agent权限与访问控制-AgentAuthorization.md": {
        "name": "AI-Agent权限与访问控制",
        "description": "AI智能体（AI Agent）具有执行工具调用、访问外部资源、处理敏感数据的能力。不当的权限控制可能导致Agent越权操作，造成严重安全事件。本技能覆盖Agent权限模型设计、工具函数授权、最小权限原则、人机确认机制等核心议题。",
        "subdomain": "llm-security",
    },
    "/tmp/our/16-大模型安全-LLMSecurity/skills/模型输出安全与幻觉检测-OutputSafetyHallucination.md": {
        "name": "大模型输出安全与幻觉检测",
        "description": "LLM输出安全涵盖有害内容生成、事实幻觉、版权侵权等问题。本技能覆盖输出过滤、幻觉检测、事实一致性验证、内容安全审核等关键技术。",
        "subdomain": "llm-security",
    },
}

for fp, info in files.items():
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('---', 2)
    if len(parts) < 3:
        print("Unexpected format in " + os.path.basename(fp))
        continue

    preserve_and_body = parts[2]

    new_fm = "\n".join([
        "---",
        "name: " + sq(info['name']),
        "description: " + sq(info['description']),
        "domain: cybersecurity",
        "subdomain: " + info['subdomain'],
        "tags:",
        "  - " + info['subdomain'],
        "  - security",
        "version: '1.0.0'",
        "author: multi-cybersecurity",
        "license: Apache-2.0",
        "nist_csf:",
        "  []",
        "mitre_attack:",
        "  []",
        "---",
    ])

    new_content = new_fm + "\n" + preserve_and_body

    try:
        yaml.safe_load(new_fm + "\n---")
        print("Valid: " + os.path.basename(fp))
    except Exception as e:
        print("Still invalid: " + os.path.basename(fp) + ": " + str(e))
        continue

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("All done")
