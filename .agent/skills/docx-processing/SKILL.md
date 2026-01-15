---
description: 如何创建、编辑和分析 Word 文档(.docx)-1.0
---

# Word 文档处理工作流

## 概述

此工作流指导如何处理 Word 文档(.docx 文件),包括创建新文档、编辑现有文档、提取内容和管理追踪更改。

## 决策树:选择正确的工作流

```
你的任务是什么?
├─ 读取/分析文档内容
│   → 查看 references/reading.md
│
├─ 创建新文档
│   → 查看 references/creating.md
│
└─ 编辑现有文档
    ├─ 自己的文档 + 简单修改
    │   → 查看 references/editing.md
    │
    └─ 他人的文档/正式文档(需要追踪更改)
        → 查看 references/tracking.md
```

## 快速参考

### 常用命令

```bash
# 读取文档内容
pandoc document.docx -o output.md

# 解压文档(用于编辑)
python scripts/unpack.py document.docx unpacked/

# 打包文档(编辑后)
python scripts/pack.py unpacked/ output.docx
```

### 前置条件

**必需工具**:
- `pandoc` - 文本提取和格式转换
- `docx` (npm) - 创建新文档
- `python` + `defusedxml` - OOXML 编辑

**安装**:
```bash
brew install pandoc
npm install -g docx
pip install defusedxml
```

## 详细指南

根据你的任务选择对应的详细指南:

- **[reading.md](references/reading.md)** - 读取和分析文档内容
  - 文本提取(pandoc)
  - 访问原始 XML
  - 查看文档结构

- **[creating.md](references/creating.md)** - 创建新 Word 文档
  - 使用 docx-js 库
  - JavaScript/TypeScript 示例
  - 常用组件和格式

- **[editing.md](references/editing.md)** - 基础文档编辑
  - 解压和打包文档
  - 使用 Python 编辑 XML
  - 简单修改示例

- **[tracking.md](references/tracking.md)** - 追踪更改工作流(推荐用于正式文档)
  - 完整的追踪更改流程
  - 批量处理策略
  - 最小化精确编辑原则

- **[converting.md](references/converting.md)** - 文档格式转换
  - DOCX → PDF
  - PDF → 图片
  - 其他格式转换

## 辅助脚本

- **[scripts/unpack.py](scripts/unpack.py)** - 解压 .docx 文件为 XML
- **[scripts/pack.py](scripts/pack.py)** - 将 XML 打包为 .docx 文件

## 常见问题

### Q: 何时使用追踪更改 vs 直接编辑?
- **追踪更改**: 编辑他人文档、正式文档、需要审核历史
- **直接编辑**: 自己的文档、简单修改、不需要审核历史

### Q: 如何快速查看文档内容?
```bash
pandoc document.docx -o - | head -n 50
```

### Q: 文档损坏了怎么办?
1. 尝试用 pandoc 提取文本
2. 解压文档检查 XML 结构
3. 查看 `word/document.xml` 是否有语法错误

---

**提示**: 这是主工作流文件,提供快速导航。详细的步骤和示例请查看 `references/` 目录中的对应文件。