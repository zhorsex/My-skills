# Skill Seeker 参考文档

## 目录

- [架构概述](#架构概述)
- [平台适配器](#平台适配器)
- [数据流](#数据流)
- [配置详解](#配置详解)
- [MCP 工具](#mcp-工具)
- [C3.x 代码分析](#c3x-代码分析)
- [故障排除](#故障排除)

## 架构概述

Skill Seeker 采用**策略模式**架构，通过工厂方法支持多个 LLM 平台：

```
src/skill_seekers/cli/adaptors/
├── __init__.py          # 工厂：get_adaptor(target)
├── base_adaptor.py      # 抽象基类
├── claude_adaptor.py    # Claude AI (ZIP + YAML)
├── gemini_adaptor.py    # Google Gemini (tar.gz)
├── openai_adaptor.py    # OpenAI ChatGPT (ZIP + Vector Store)
└── markdown_adaptor.py  # 通用 Markdown (ZIP)
```

### 核心设计模式

1. **平台适配器模式** - 统一接口支持多平台
2. **策略模式** - 不同抓取策略（文档/GitHub/PDF）
3. **工厂模式** - 动态创建适配器实例
4. **观察者模式** - MCP 工具的事件驱动

## 平台适配器

### 基类接口

```python
class BaseAdaptor(ABC):
    @abstractmethod
    def package(self, skill_dir: str, output_path: str) -> str:
        """将技能目录打包为平台特定格式"""
        pass
    
    @abstractmethod
    def upload(self, package_path: str, api_key: str) -> dict:
        """上传到目标平台"""
        pass
    
    @abstractmethod
    def enhance(self, skill_dir: str, mode: str) -> None:
        """AI 增强技能内容"""
        pass
```

### 平台对比

| 平台 | 格式 | 上传方式 | 增强模型 |
|------|------|----------|----------|
| Claude | ZIP + YAML | API | Sonnet 4 |
| Gemini | tar.gz | API | Gemini 2.0 Flash |
| OpenAI | ZIP + Vector | API | GPT-4o |
| Markdown | ZIP | 手动 | 无 |

## 数据流

### 五阶段处理流程

```
1. 抓取阶段 (Scrape Phase)
   ├── 文档抓取：BFS 遍历从 base_url 开始
   ├── GitHub 分析：AST 解析代码结构
   └── PDF 提取：PyMuPDF + OCR
   
2. 构建阶段 (Build Phase)
   ├── 加载页面
   ├── 智能分类
   ├── 提取模式
   └── 生成 SKILL.md
   
3. 增强阶段 (Enhancement Phase)
   ├── LLM 分析参考文件
   ├── 重写 SKILL.md
   └── 平台特定优化
   
4. 打包阶段 (Package Phase)
   ├── 平台适配器选择
   ├── 格式转换
   └── 元数据添加
   
5. 上传阶段 (Upload Phase)
   ├── API 认证
   ├── 文件上传
   └── 验证响应
```

## 配置详解

### 完整配置示例

```json
{
  "name": "my-framework",
  "description": "My Framework 完整文档",
  "base_url": "https://docs.myframework.com/",
  "version": "1.0.0",
  
  "selectors": {
    "main_content": "article.main-content",
    "title": "h1.article-title",
    "code_blocks": "pre code",
    "navigation": "nav.sidebar",
    "exclude": [".ads", ".cookie-banner"]
  },
  
  "url_patterns": {
    "include": [
      "/docs/",
      "/api/",
      "/guide/"
    ],
    "exclude": [
      "/blog/",
      "/changelog/",
      "*.pdf"
    ]
  },
  
  "categories": {
    "getting_started": {
      "keywords": ["intro", "quickstart", "tutorial", "beginner"],
      "weight": 3
    },
    "api_reference": {
      "keywords": ["api", "reference", "function", "method", "class"],
      "weight": 2
    },
    "advanced": {
      "keywords": ["advanced", "performance", "optimization"],
      "weight": 1
    }
  },
  
  "rate_limit": 0.5,
  "max_pages": 500,
  "timeout": 30,
  "retry_attempts": 3,
  
  "github": {
    "repo": "owner/my-framework",
    "include_code": true,
    "code_analysis_depth": "deep",
    "include_issues": true,
    "max_issues": 50
  },
  
  "enhancement": {
    "enabled": true,
    "mode": "local",
    "sections": ["overview", "examples", "troubleshooting"]
  }
}
```

### 配置字段详解

#### 基础字段

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `name` | string | 是 | - | 技能名称，用于输出目录 |
| `description` | string | 是 | - | 技能描述 |
| `base_url` | string | 是 | - | 文档网站 URL |
| `version` | string | 否 | "1.0.0" | 技能版本 |

#### 选择器配置

| 字段 | 类型 | 说明 |
|------|------|------|
| `main_content` | string | 主内容区域 CSS 选择器 |
| `title` | string | 标题选择器 |
| `code_blocks` | string | 代码块选择器 |
| `navigation` | string | 导航栏选择器（可选） |
| `exclude` | array | 排除的元素选择器 |

#### URL 模式

| 字段 | 类型 | 说明 |
|------|------|------|
| `include` | array | 只包含匹配的 URL 路径 |
| `exclude` | array | 排除匹配的 URL 路径 |

#### 分类配置

分类使用权重系统：
- URL 匹配：3 分
- 标题匹配：2 分
- 内容匹配：1 分
- 阈值：2 分以上归类

#### 性能配置

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `rate_limit` | number | 0.5 | 请求间隔（秒） |
| `max_pages` | number | 500 | 最大抓取页数 |
| `timeout` | number | 30 | 单页超时（秒） |
| `retry_attempts` | number | 3 | 失败重试次数 |

## MCP 工具

### 核心工具（9 个）

#### 1. list_configs

列出所有可用的预设配置。

**参数**：无

**返回**：
```json
{
  "configs": [
    {
      "name": "react",
      "description": "React 官方文档",
      "url": "https://react.dev/"
    }
  ]
}
```

#### 2. generate_config

从文档 URL 自动生成配置。

**参数**：
```json
{
  "url": "https://docs.example.com/",
  "name": "example",
  "max_pages": 100
}
```

**返回**：配置文件路径

#### 3. validate_config

验证配置文件结构。

**参数**：
```json
{
  "config_path": "configs/myconfig.json"
}
```

**返回**：验证结果和错误列表

#### 4. estimate_pages

估算文档网站的总页数。

**参数**：
```json
{
  "config_path": "configs/react.json"
}
```

**返回**：估算页数和时间

#### 5. scrape_docs

抓取文档网站。

**参数**：
```json
{
  "config": "react",
  "async": true,
  "workers": 8
}
```

**返回**：输出目录路径

#### 6. package_skill

将技能打包为平台特定格式。

**参数**：
```json
{
  "skill_dir": "output/react/",
  "target": "claude"
}
```

**返回**：包文件路径

#### 7. upload_skill

上传技能到平台。

**参数**：
```json
{
  "package_path": "output/react.zip",
  "target": "claude",
  "api_key": "sk-ant-..."
}
```

**返回**：上传状态和 URL

#### 8. enhance_skill

AI 增强技能内容。

**参数**：
```json
{
  "skill_dir": "output/react/",
  "mode": "local",
  "background": false
}
```

**返回**：增强状态

#### 9. install_skill

完整安装流程（抓取 → 增强 → 打包 → 上传）。

**参数**：
```json
{
  "config": "react",
  "target": "claude",
  "no_upload": false
}
```

### 扩展工具（9 个）

#### 10. scrape_github

分析 GitHub 仓库。

**参数**：
```json
{
  "repo": "facebook/react",
  "include_issues": true,
  "include_releases": true
}
```

#### 11. scrape_pdf

提取 PDF 文件内容。

**参数**：
```json
{
  "pdf_path": "docs/manual.pdf",
  "name": "manual",
  "ocr": false
}
```

#### 12. unified_scrape

多源合并抓取。

**参数**：
```json
{
  "config_path": "configs/react_unified.json"
}
```

#### 13. detect_conflicts

检测文档与代码之间的冲突。

**参数**：
```json
{
  "skill_dir": "output/react/"
}
```

**冲突类型**：
- 🔴 Missing in code：文档记录但未实现
- 🟡 Missing in docs：实现但未记录
- ⚠️ Signature mismatch：参数签名不一致
- ℹ️ Description mismatch：描述不一致

#### 14. add_config_source

添加私有配置源。

**参数**：
```json
{
  "name": "team",
  "git_url": "https://github.com/company/configs.git",
  "token_env": "GITHUB_TOKEN"
}
```

#### 15. fetch_config

从配置源获取配置。

**参数**：
```json
{
  "source": "team",
  "config_name": "internal-api"
}
```

#### 16. split_config

拆分大型配置为多个小配置。

**参数**：
```json
{
  "config_path": "configs/large.json",
  "max_pages_per_skill": 100
}
```

#### 17. generate_router

为大型文档生成路由技能。

**参数**：
```json
{
  "skills_dir": "output/",
  "name": "framework-router"
}
```

#### 18. merge_sources

合并多个数据源。

**参数**：
```json
{
  "sources": [
    {"type": "docs", "path": "output/docs/"},
    {"type": "github", "path": "output/github/"}
  ],
  "merge_mode": "rule-based"
}
```

## C3.x 代码分析

### C3.1 设计模式检测

检测 10 种常见设计模式：

| 模式 | 描述 | 检测方法 |
|------|------|----------|
| Singleton | 单例模式 | 类变量 + 私有构造函数 |
| Factory | 工厂模式 | 创建方法返回接口 |
| Observer | 观察者模式 | 订阅/通知机制 |
| Strategy | 策略模式 | 可互换算法 |
| Decorator | 装饰器模式 | 包装类 |
| Builder | 建造者模式 | 分步构建 |
| Adapter | 适配器模式 | 接口转换 |
| Command | 命令模式 | 请求封装 |
| Template Method | 模板方法 | 算法骨架 |
| Chain of Responsibility | 责任链 | 请求传递链 |

支持 9 种语言：Python、JavaScript、TypeScript、C++、C、C#、Go、Rust、Java

### C3.2 测试示例提取

从测试文件中提取真实使用示例：

**类别**：
- Instantiation - 实例化示例
- Method Call - 方法调用
- Configuration - 配置示例
- Setup - 初始化设置
- Workflow - 完整工作流程

### C3.3 操作指南生成

将测试工作流转换为教育性指南：

**AI 增强的 5 个方面**：
1. Step Descriptions - 步骤的自然语言说明
2. Troubleshooting - 故障诊断和解决方案
3. Prerequisites - 前置条件和设置说明
4. Next Steps - 相关指南和学习路径
5. Use Cases - 实际应用场景

### C3.4 配置模式提取

提取 9 种配置格式：
- JSON
- YAML
- TOML
- ENV
- INI
- Python
- JavaScript
- Dockerfile
- Docker Compose

### C3.5 架构概述生成

生成 ARCHITECTURE.md 文件，包含：
- 系统架构图
- 组件关系
- 数据流
- 依赖关系

### C3.10 Godot 信号流分析

专为 Godot 引擎设计的信号分析：

**功能**：
- Signal 声明提取
- Connection 映射（.connect() 调用）
- Emission 跟踪（.emit() 调用）
- Event Chain 检测
- Pattern 识别（EventBus、Observer）

**输出**：
- `signal_flow.json` - 结构化数据
- `signal_flow.mmd` - Mermaid 图表
- `signal_reference.md` - 参考文档
- `signal_how_to_guides.md` - 使用指南

## 故障排除

### 常见问题

#### 1. ImportError: No module named 'skill_seekers'

**原因**：未安装包（src/ 布局要求）

**解决**：
```bash
pip install -e .
```

#### 2. 403 Forbidden from GitHub

**原因**：GitHub API 速率限制

**解决**：
```bash
# 配置 GitHub Token
export GITHUB_TOKEN=ghp_...

# 或配置多个配置文件
skill-seekers config --github
```

#### 3. 增强功能不工作

**原因**：未设置 API 密钥或 Claude Code 未安装

**解决**：
```bash
# 检查 API 密钥
echo $ANTHROPIC_API_KEY

# 或使用本地模式（无需 API 密钥）
skill-seekers enhance output/skill/ --mode LOCAL
```

#### 4. 测试失败

**原因**：包未安装或依赖缺失

**解决**：
```bash
# 确保安装包
pip install -e .

# 安装测试依赖
pip install pytest pytest-asyncio pytest-cov coverage

# 运行测试
pytest tests/ -v
```

#### 5. 配置验证失败

**原因**：配置文件结构错误

**解决**：
```bash
# 验证配置
skill-seekers validate-config configs/myconfig.json
```

### 调试技巧

#### 启用详细日志

```bash
skill-seekers scrape --config react.json --verbose
```

#### 检查中间输出

```bash
# 查看原始数据
ls output/react_data/pages/

# 查看提取的内容
cat output/react_data/pages/page_001.json
```

#### 测试选择器

```python
from skill_seekers.cli.doc_scraper import extract_content

# 测试单个页面
result = extract_content(
    url="https://react.dev/learn",
    selectors={"main_content": "article"}
)
print(result)
```

### 性能优化

#### 异步模式

```bash
# 使用异步模式（速度提升 2-3 倍）
skill-seekers scrape --config react.json --async --workers 8
```

#### 增量更新

```bash
# 跳过已抓取的页面
skill-seekers scrape --config react.json --skip-scrape
```

#### 限制页面数

```json
{
  "max_pages": 50  // 测试时使用小数量
}
```

### 获取帮助

```bash
# 查看命令帮助
skill-seekers --help
skill-seekers scrape --help

# 查看配置示例
cat configs/react.json

# 访问文档网站
open https://skillseekersweb.com/
```
