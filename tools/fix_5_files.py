#!/usr/bin/env python3
"""Fix 5 files whose description contains YAML-special chars."""
import os, re, yaml

def safe_yaml_value(s):
    s = str(s)
    if any(c in s for c in '*:#>|[],{}!%&\'"@`'):
        return "'" + s.replace("'", "''") + "'"
    return s

files = [
    "/tmp/our/09-报告撰写-Reporting/skills/安全报告模板-HTML.md",
    "/tmp/our/09-报告撰写-Reporting/skills/安全报告模板-Markdown.md",
    "/tmp/our/09-报告撰写-Reporting/skills/安全报告模板-Word.md",
    "/tmp/our/16-大模型安全-LLMSecurity/skills/AI Agent权限与访问控制-AgentAuthorization.md",
    "/tmp/our/16-大模型安全-LLMSecurity/skills/模型输出安全与幻觉检测-OutputSafetyHallucination.md",
]

descriptions = {
    "安全报告模板-HTML.md": "HTML报告模板基于Bootstrap 5，支持响应式设计、Chart.js图表，暗色模式、侧色栏导航、打印和PDF导出功能，可快速生成专业的渗透测试安全评估报告。",
    "安全报告模板-Markdown.md": "Markdown格式安全报告模板，兼容CVSS 3.1/4.0、OWASP Top 10 2021、CWE、PCI DSS、等保2.0等标准格式，可导出为HTML、PDF、DOCX多种格式。",
    "安全报告模板-Word.md": "Word格式安全报告模板，基于python-docx库生成，支持自动化填充漏洞信息、图片插入、目录生成，可直接导出为.docx或转换为PDF格式。",
    "AI Agent权限与访问控制-AgentAuthorization.md": "AI智能体（AI Agent）具有执行工具调用、访问外部资源、处理敏感数据的能力。不当的权限控制可能导致Agent越权操作，造成严重安全事件。本技能覆盖Agent权限模型设计、工具函数授权、最小权限原则、人机确认机制等核心议题。",
    "模型输出安全与幻觉检测-OutputSafetyHallucination.md": "LLM输出安全涵盖有害内容生成、事实幻觉、版权侵权等问题。本技能覆盖输出过滤、幻觉检测、事实一致性验证、内容安全审核等关键技术。",
}

subdomains = {
    "安全报告模板-HTML.md": "reporting",
    "安全报告模板-Markdown.md": "reporting",
    "安全报告模板-Word.md": "reporting",
    "AI Agent权限与访问控制-AgentAuthorization.md": "llm-security",
    "模型输出安全与幻觉检测-OutputSafetyHallucination.md": "llm-security",
}

for fp in files:
    fname = os.path.basename(fp)
    desc = descriptions.get(fname, "安全技能文档")
    subdom = subdomains.get(fname, "cybersecurity")

    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find body - content starting with # heading
    body_match = re.search(r'\n---\n(# .*)', content, re.DOTALL)
    if not body_match:
        print("Cannot find body in " + fname)
        continue

    body = body_match.group(1)

    name = fname.replace('.md', '')
    name = '-'.join(re.sub(r'[^\w\s-]', ' ', name).split())

    new_fm_lines = [
        "---",
        "name: " + name,
        "description: " + safe_yaml_value(desc),
        "domain: cybersecurity",
        "subdomain: " + subdom,
        "tags:",
        "  - " + subdom,
        "  - security",
        "version: '1.0.0'",
        "author: multi-cybersecurity",
        "license: Apache-2.0",
        "nist_csf:",
        "  []",
        "mitre_attack:",
        "  []",
        "---",
    ]

    new_content = "\n".join(new_fm_lines) + "\n" + body

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed: " + fname)

print("All done")
