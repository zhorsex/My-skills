# Skill Seeker 示例配置

本目录包含 Skill Seeker 工具的示例配置文件，展示不同场景下的配置方法。

## 示例列表

### 1. react.json - 文档网站抓取

基础文档抓取配置，适用于大多数文档网站。

```bash
skill-seekers scrape --config examples/react.json
```

**特点**：
- 使用 CSS 选择器提取内容
- URL 包含/排除规则
- 智能分类配置
- 速率限制控制

### 2. react-unified.json - 多源合并

合并文档网站和 GitHub 仓库的高级配置。

```bash
skill-seekers unified --config examples/react-unified.json
```

**特点**：
- 多数据源（文档 + GitHub）
- 自动冲突检测
- 统一知识库
- 文档与代码差异分析

### 3. pdf-config.json - PDF 提取

从 PDF 文件提取内容的配置。

```bash
skill-seekers pdf --pdf manual.pdf --config examples/pdf-config.json
```

**特点**：
- 文本提取
- 表格识别
- 代码块检测
- 并行处理

### 4. github-config.json - 仓库分析

深度 GitHub 仓库分析配置。

```bash
skill-seekers github --config examples/github-config.json
```

**特点**：
- C3.x 代码分析
- 设计模式检测
- 测试示例提取
- 社区问题分析

## 使用方法

### 基础用法

1. 复制示例配置：
```bash
cp examples/react.json configs/my-framework.json
```

2. 编辑配置：
```bash
nano configs/my-framework.json
```

3. 运行抓取：
```bash
skill-seekers scrape --config configs/my-framework.json
```

### 验证配置

```bash
skill-seekers validate-config configs/my-framework.json
```

### 估算页数

```bash
skill-seekers estimate configs/my-framework.json
```

## 配置字段速查

### 通用字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | 技能名称 | `"react"` |
| `description` | 技能描述 | `"React 官方文档"` |
| `base_url` | 基础 URL | `"https://react.dev/"` |
| `max_pages` | 最大页数 | `300` |
| `rate_limit` | 请求间隔 | `0.5` |

### 选择器字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `selectors.main_content` | 主内容 | `"article"` |
| `selectors.title` | 标题 | `"h1"` |
| `selectors.code_blocks` | 代码块 | `"pre code"` |

### 分类字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `categories.{name}.keywords` | 关键词 | `["tutorial", "guide"]` |
| `categories.{name}.weight` | 权重 | `3` |

## 更多资源

- 完整文档：参见 `../SKILL.md`
- 技术参考：参见 `../reference.md`
- 官方仓库：https://github.com/yusufkaraaslan/Skill_Seekers
