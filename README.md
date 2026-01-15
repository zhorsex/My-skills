# My-skills

这是一个个人/自定义的代理（Agent）技能仓库，包含了一系列用于增强 AI 代理能力的工具（Skills）和配置。

## 核心技能预览

该仓库集成了多种领域的专业技能，主要分布在 `.agent/skills` 目录下：

### 📄 文档处理
- **Word (docx)**: 深入支持 `.docx` 文档的创建、编辑、分析及格式转换。
- **PDF (pdf)**: 提供 PDF 文本提取、表格分析以及表单填充能力。
- **PowerPoint (pptx)**: 自动生成演示文稿，支持幻灯片布局调整和内容更新。
- **Excel (xlsx)**: 强大的电子表格自动化，支持公式、格式设置和数据透视分析。

### 📓 Obsidian 集成
- **Obsidian Markdown**: 支持 Wikilinks、Callouts 和 Properties 等 Obsidian 特有语法。
- **JSON Canvas**: 创建和编辑 `.canvas` 可视化脑图/流程图文件。
- **Obsidian Bases**: 允许通过数据库视图管理笔记内容。
- **Docx to Obsidian**: 智能将 Word 文档转换为 Obsidian 格式。

### 🛠️ 开发工具
- **Skill Creator**: 快速构建和扩展新技能的标准化指南。

## 项目结构

```text
.
├── .agent/
│   ├── skills/          # 核心代码：存放所有可用的 Agent 技能
│   └── rules/           # 行为准则：定义 Agent 的工作边界
├── README.md            # 项目自述文件
└── .gitignore           # Git 忽略配置
```

## 如何使用

这些技能被设计为可由支持工具调用的 AI 代理直接加载。在使用时，确保代理有权限访问 `.agent/skills` 目录下的相应模块。

---
*Created by Antigravity.*
