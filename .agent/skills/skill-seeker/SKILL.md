---
name: skill-seeker
description: 将文档网站、GitHub 仓库和 PDF 文件转换为 Claude AI 技能，支持多源数据合并、冲突检测和多平台输出
license: MIT License. See LICENSE.txt for details
---

# Skill Seeker

## 概述

Skill Seeker 是一个通用 AI 数据预处理工具，可将以下数据源转换为生产就绪的 AI 技能：

- **文档网站** - 任何文档网站的自动化抓取
- **GitHub 仓库** - 深度代码分析和 API 提取
- **PDF 文件** - 文本、代码、表格和图像提取

支持输出到 4 个主流 AI 平台：Claude AI、Google Gemini、OpenAI ChatGPT 和通用 Markdown。

### 核心特性

- **多源合并** - 将文档 + GitHub + PDF 合并为统一技能
- **冲突检测** - 自动发现文档与代码实现之间的差异
- **智能分类** - 自动按主题组织内容
- **AI 增强** - 使用 Claude API 自动提升技能质量
- **RAG 集成** - 导出为 LangChain、LlamaIndex、Pinecone 格式

## 快速开始

### 安装

```bash
# 基础安装
pip install skill-seekers

# 包含 MCP 集成
pip install skill-seekers[mcp]

# 包含所有 LLM 平台支持
pip install skill-seekers[all-llms]
```

### 基础用法

#### 1. 抓取文档网站

```bash
# 使用预设配置
skill-seekers scrape --config configs/react.json

# 快速命令
skill-seekers scrape --name react --url https://react.dev/
```

#### 2. 分析 GitHub 仓库

```bash
# 基础分析
skill-seekers github --repo facebook/react

# 包含 Issues 和 Releases
skill-seekers github --repo django/django \
    --include-issues \
    --max-issues 100 \
    --include-changelog \
    --include-releases
```

#### 3. 提取 PDF 文件

```bash
# 基础提取
skill-seekers pdf --pdf docs/manual.pdf --name myskill

# 高级功能
skill-seekers pdf --pdf docs/manual.pdf --name myskill \
    --extract-tables \
    --parallel \
    --workers 8

# 扫描 PDF（需要 OCR）
skill-seekers pdf --pdf docs/scanned.pdf --name myskill --ocr
```

#### 4. 多源合并（统一抓取）

```bash
# 合并文档 + GitHub 仓库
skill-seekers unified --config configs/react_unified.json
```

### 一键安装工作流

```bash
# 从配置名到上传完成的完整流程
skill-seekers install --config react

# 仅打包不上传
skill-seekers install --config django --no-upload

# 无限制抓取
skill-seekers install --config godot --unlimited
```

## 配置说明

### 配置文件结构

```json
{
  "name": "framework-name",
  "description": "技能用途说明",
  "base_url": "https://docs.example.com/",
  "selectors": {
    "main_content": "article",
    "title": "h1",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": ["/docs"],
    "exclude": ["/blog"]
  },
  "categories": {
    "getting_started": ["intro", "quickstart"],
    "api": ["api", "reference"]
  },
  "rate_limit": 0.5,
  "max_pages": 500
}
```

### 配置字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 技能名称，用于输出目录和文件名 |
| `description` | string | 技能描述，用于识别何时使用该技能 |
| `base_url` | string | 文档网站基础 URL |
| `selectors` | object | CSS 选择器配置 |
| `url_patterns` | object | URL 包含/排除规则 |
| `categories` | object | 内容分类关键词 |
| `rate_limit` | number | 请求间隔（秒） |
| `max_pages` | number | 最大抓取页数 |

## AI 增强

### 本地增强（推荐）

使用 Claude Code Max 计划，无需 API 密钥：

```bash
# 基础增强
skill-seekers enhance output/react/

# 后台模式
skill-seekers enhance output/react/ --background

# 监控状态
skill-seekers enhance-status output/react/ --watch
```

### API 增强

使用 Claude API（需要 ANTHROPIC_API_KEY）：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
skill-seekers enhance output/react/
```

### 增强效果

- 质量从 3/10 提升到 9/10
- 添加故障排除指南
- 完善前置条件说明
- 提取最佳实践

## 多平台打包

### Claude AI（默认）

```bash
skill-seekers package output/react/
# 输出: react.zip
```

### Google Gemini

```bash
pip install skill-seekers[gemini]
skill-seekers package output/react/ --target gemini
# 输出: react-gemini.tar.gz
```

### OpenAI ChatGPT

```bash
pip install skill-seekers[openai]
skill-seekers package output/react/ --target openai
# 输出: react-openai.zip
```

### 通用 Markdown

```bash
skill-seekers package output/react/ --target markdown
# 输出: react-markdown/SKILL.md
```

## RAG 集成

### LangChain

```bash
skill-seekers package output/django --target langchain
# 输出: django-langchain.json
```

### LlamaIndex

```bash
skill-seekers package output/django --target llama-index
# 输出: django-llama-index.json
```

### Pinecone

```bash
skill-seekers package output/django --target pinecone
# 输出: pinecone-ready 格式
```

## MCP 集成

### 启动 MCP 服务器

```bash
# stdio 模式（Claude Code）
python -m skill_seekers.mcp.server_fastmcp

# HTTP 模式（Cursor、Windsurf）
python -m skill_seekers.mcp.server_fastmcp --transport http --port 8765
```

### MCP 工具列表

1. `list_configs` - 列出预设配置
2. `generate_config` - 从 URL 生成配置
3. `validate_config` - 验证配置结构
4. `estimate_pages` - 估算页数
5. `scrape_docs` - 抓取文档
6. `scrape_github` - 分析 GitHub 仓库
7. `scrape_pdf` - 提取 PDF
8. `unified_scrape` - 多源合并
9. `detect_conflicts` - 检测冲突
10. `package_skill` - 打包技能
11. `upload_skill` - 上传到平台
12. `enhance_skill` - AI 增强
13. `install_skill` - 完整安装流程
14. `add_config_source` - 添加配置源
15. `fetch_config` - 获取配置
16. `split_config` - 拆分大型配置
17. `generate_router` - 生成路由技能
18. `merge_sources` - 合并多个源

## 环境变量

```bash
# Claude AI / 兼容 API
export ANTHROPIC_API_KEY=sk-ant-...
export ANTHROPIC_BASE_URL=https://api.anthropic.com  # 可选，用于兼容 API

# Google Gemini
export GOOGLE_API_KEY=AIza...

# OpenAI
export OPENAI_API_KEY=sk-...

# GitHub（提高速率限制）
export GITHUB_TOKEN=ghp_...
```

## 命令参考

| 命令 | 说明 | 示例 |
|------|------|------|
| `scrape` | 抓取文档网站 | `skill-seekers scrape --config react.json` |
| `github` | 分析 GitHub 仓库 | `skill-seekers github --repo owner/repo` |
| `pdf` | 提取 PDF | `skill-seekers pdf --pdf file.pdf --name skill` |
| `unified` | 多源合并 | `skill-seekers unified --config unified.json` |
| `analyze` | 本地代码分析 | `skill-seekers analyze --directory .` |
| `enhance` | AI 增强 | `skill-seekers enhance output/skill/` |
| `package` | 打包技能 | `skill-seekers package output/skill/` |
| `upload` | 上传到平台 | `skill-seekers upload skill.zip` |
| `install` | 完整安装流程 | `skill-seekers install --config react` |
| `config` | 配置向导 | `skill-seekers config --github` |

## 输出结构

```
output/
├── {name}_data/          # 原始抓取数据（可复用）
│   └── pages/
│       └── *.json
└── {name}/               # 生成的技能
    ├── SKILL.md          # 主技能文档
    ├── references/       # 分类参考文件
    │   ├── getting_started.md
    │   ├── api_reference.md
    │   └── examples.md
    └── metadata/         # 元数据
        └── info.json
```

## 使用场景

### 框架学习

为任何框架创建全面的学习技能：

```bash
skill-seekers install --config godot
skill-seekers install --config react
skill-seekers install --config django
```

### 团队内部文档

合并内部文档和代码库：

```bash
# 创建统一配置
cat > configs/team_unified.json << 'EOF'
{
  "name": "team-docs",
  "description": "团队内部文档和代码库",
  "merge_mode": "rule-based",
  "sources": [
    {
      "type": "documentation",
      "base_url": "https://wiki.company.com/",
      "max_pages": 200
    },
    {
      "type": "github",
      "repo": "company/internal-repo",
      "include_code": true
    }
  ]
}
EOF

skill-seekers unified --config configs/team_unified.json
```

### API 文档分析

发现文档与代码之间的差异：

```bash
skill-seekers unified --config configs/react_unified.json
# 自动检测：文档中记录但未实现的功能
# 自动检测：已实现但未文档化的功能
```

## 故障排除

### 速率限制

```bash
# 配置多个 GitHub 账号
skill-seekers config --github

# 使用特定配置文件
skill-seekers github --repo owner/repo --profile work
```

### 恢复中断的任务

```bash
# 列出可恢复的任务
skill-seekers resume --list

# 恢复特定任务
skill-seekers resume github_react_20260117_143022
```

### 检查配置

```bash
# 显示当前配置
skill-seekers config --show

# 测试连接
skill-seekers config --test
```

## Python 库

### 基本用法

```python
from skill_seekers.cli.doc_scraper import scrape_all

# 抓取文档
result = scrape_all(
    base_url="https://docs.example.com/",
    max_pages=100,
    rate_limit=0.5
)
```

### GitHub 分析

```python
from skill_seekers.cli.unified_codebase_analyzer import UnifiedCodebaseAnalyzer

analyzer = UnifiedCodebaseAnalyzer()
result = analyzer.analyze(
    source="https://github.com/facebook/react",
    depth="c3x",
    fetch_github_metadata=True
)
```

## 进阶功能

### C3.x 代码分析

- **C3.1** - 设计模式检测（10 种常见模式）
- **C3.2** - 测试示例提取
- **C3.3** - 操作指南生成
- **C3.4** - 配置模式提取
- **C3.5** - 架构概述生成
- **C3.10** - Godot 信号流分析

### 异步模式

```bash
# 异步抓取（速度提升 2-3 倍）
skill-seekers scrape --config react.json --async --workers 8
```

### 检查点恢复

```bash
# 支持断点续传
skill-seekers scrape --config large-docs.json --checkpoint-interval 60
```

## 相关资源

- **官方仓库**: https://github.com/yusufkaraaslan/Skill_Seekers
- **文档网站**: https://skillseekersweb.com/
- **PyPI**: https://pypi.org/project/skill-seekers/
- **完整文档**: 参见 reference.md

## 许可证

MIT License - 详见 LICENSE.txt
