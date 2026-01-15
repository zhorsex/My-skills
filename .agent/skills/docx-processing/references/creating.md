# 创建新 Word 文档

## 概述

本指南介绍如何使用 `docx` JavaScript 库从零创建 Word 文档。

---

## 前置条件

### 安装 docx 库

```bash
# 全局安装
npm install -g docx

# 或在项目中安装
npm install docx
```

---

## 基础示例

### ⚠️ 核心准则 (防坑指南)

> [!IMPORTANT]
> **1. 严禁使用 `\n` 进行换行**
> Word XML 不识别 `\n`。如果需要换行,必须创建新的 `Paragraph` 元素。
> - ❌ 错误: `new TextRun("第一行\n第二行")`
> - ✅ 正确: `new Paragraph({ children: [new TextRun("第一行")] }), new Paragraph({ children: [new TextRun("第二行")] })`
>
> **2. `ImageRun` 必需参数**
> 创建图片时,`type` 和 `altText` 的所有子字段都是必需的,否则文档可能损坏。
> - `type`: 必须指定 ("png", "jpg", "jpeg" 等)
> - `altText`: 必须包含 `title`、`description` 和 `name`


### 最简单的文档

```javascript
const { Document, Packer, Paragraph, TextRun } = require("docx");
const fs = require("fs");

// 创建文档
const doc = new Document({
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        children: [
          new TextRun("Hello World!")
        ]
      })
    ]
  }]
});

// 导出为 .docx
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("output.docx", buffer);
  console.log("文档已创建!");
});
```

**运行**:
```bash
node create-document.js
```

---

## 常用组件

### 1. 段落(Paragraph)

```javascript
// 基础段落
new Paragraph({
  text: "这是一个段落"
})

// 带格式的段落
new Paragraph({
  children: [
    new TextRun({
      text: "粗体文本",
      bold: true
    }),
    new TextRun({
      text: " 普通文本 "
    }),
    new TextRun({
      text: "斜体文本",
      italics: true
    })
  ]
})

// 标题
new Paragraph({
  text: "一级标题",
  heading: HeadingLevel.HEADING_1
})
```

### 2. 文本格式(TextRun)

```javascript
new TextRun({
  text: "格式化文本",
  bold: true,           // 粗体
  italics: true,        // 斜体
  underline: {},        // 下划线
  color: "FF0000",      // 红色
  size: 28,             // 字号(半点,28 = 14pt)
  font: "Arial"         // 字体
})
```

### 3. 列表

```javascript
// 无序列表
new Paragraph({
  text: "列表项 1",
  bullet: {
    level: 0
  }
})

// 有序列表
new Paragraph({
  text: "列表项 1",
  numbering: {
    reference: "my-numbering",
    level: 0
  }
})
```

### 4. 表格

```javascript
const { Table, TableCell, TableRow } = require("docx");

new Table({
  rows: [
    new TableRow({
      children: [
        new TableCell({
          children: [new Paragraph("单元格 1")]
        }),
        new TableCell({
          children: [new Paragraph("单元格 2")]
        })
      ]
    })
  ]
})
```

### 5. 图片 (大师级要求)

```javascript
const { ImageRun } = require("docx");
const fs = require("fs");

new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [
    new ImageRun({
      data: fs.readFileSync("image.png"),
      type: "png", // ⭐ 必需:指定图片类型
      transformation: {
        width: 100, // 注意: Word 内部使用 EMU,此处库会自动转换,但建议保持比例
        height: 100
      },
      // ⭐ 必需:完整描述信息(防止 Word 报错)
      altText: { 
        title: "图片标题", 
        description: "图片描述", 
        name: "图片文件名称" 
      }
    })
  ]
})
```

---

## 完整示例

### 创建格式化报告

```javascript
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require("docx");
const fs = require("fs");

const doc = new Document({
  sections: [{
    properties: {},
    children: [
      // 标题
      new Paragraph({
        text: "项目报告",
        heading: HeadingLevel.HEADING_1,
        alignment: AlignmentType.CENTER
      }),
      
      // 空行
      new Paragraph({ text: "" }),
      
      // 正文
      new Paragraph({
        children: [
          new TextRun({
            text: "项目概述: ",
            bold: true
          }),
          new TextRun({
            text: "本项目旨在..."
          })
        ]
      }),
      
      // 二级标题
      new Paragraph({
        text: "主要成果",
        heading: HeadingLevel.HEADING_2
      }),
      
      // 列表
      new Paragraph({
        text: "完成功能 A",
        bullet: { level: 0 }
      }),
      new Paragraph({
        text: "完成功能 B",
        bullet: { level: 0 }
      }),
      
      // 页脚
      new Paragraph({
        text: "报告日期: 2024-01-01",
        alignment: AlignmentType.RIGHT
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("report.docx", buffer);
  console.log("报告已生成!");
});
```

---

## 高级功能

### 页眉和页脚

```javascript
const doc = new Document({
  sections: [{
    properties: {
      page: {
        pageNumbers: {
          start: 1,
          formatType: NumberFormat.DECIMAL
        }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            text: "页眉内容",
            alignment: AlignmentType.CENTER
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            text: "页脚内容",
            alignment: AlignmentType.CENTER
          })
        ]
      })
    },
    children: [
      // 文档内容
    ]
  }]
});
```

### 多个章节

```javascript
const doc = new Document({
  sections: [
    {
      properties: {},
      children: [
        new Paragraph({ text: "第一章节" })
      ]
    },
    {
      properties: {
        page: {
          pageNumbers: {
            start: 1  // 重新开始页码
          }
        }
      },
      children: [
        new Paragraph({ text: "第二章节" })
      ]
    }
  ]
});
```

### 样式定义

```javascript
const doc = new Document({
  styles: {
    paragraphStyles: [
      {
        id: "MyCustomStyle",
        name: "My Custom Style",
        basedOn: "Normal",
        next: "Normal",
        run: {
          color: "FF0000",
          size: 26
        },
        paragraph: {
          spacing: {
            after: 120
          }
        }
      }
    ]
  },
  sections: [{
    children: [
      new Paragraph({
        text: "使用自定义样式",
        style: "MyCustomStyle"
      })
    ]
  }]
});
```

---

## 实用技巧

### 1. 从模板数据生成文档

```javascript
const data = {
  title: "月度报告",
  items: ["项目 A", "项目 B", "项目 C"]
};

const children = [
  new Paragraph({
    text: data.title,
    heading: HeadingLevel.HEADING_1
  }),
  ...data.items.map(item => 
    new Paragraph({
      text: item,
      bullet: { level: 0 }
    })
  )
];

const doc = new Document({
  sections: [{ children }]
});
```

### 2. 异步生成文档

```javascript
async function createDocument() {
  const doc = new Document({
    sections: [{
      children: [
        new Paragraph({ text: "异步生成的文档" })
      ]
    }]
  });
  
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync("async-doc.docx", buffer);
}

createDocument().then(() => {
  console.log("完成!");
});
```

### 3. 导出为 Blob(浏览器环境)

```javascript
Packer.toBlob(doc).then(blob => {
  // 在浏览器中下载
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'document.docx';
  link.click();
});
```

---

## 常见问题

### Q: 如何设置页面大小和边距?

```javascript
sections: [{
  properties: {
    page: {
      margin: {
        top: 1440,    // 1 英寸 = 1440 twips
        right: 1440,
        bottom: 1440,
        left: 1440
      },
      size: {
        width: 12240,   // A4 宽度
        height: 15840   // A4 高度
      }
    }
  },
  children: [...]
}]
```

### Q: 如何添加换行?

```javascript
// 段落内换行
new Paragraph({
  children: [
    new TextRun("第一行"),
    new TextRun({ text: "第二行", break: 1 })
  ]
})

// 分页符
new Paragraph({
  children: [
    new PageBreak()
  ]
})
```

### Q: 支持哪些字体?

docx 库支持所有系统字体。常用中文字体:
- `"宋体"` (SimSun)
- `"黑体"` (SimHei)
- `"微软雅黑"` (Microsoft YaHei)
- `"楷体"` (KaiTi)

---

## 参考资源

- **官方文档**: https://docx.js.org/
- **GitHub**: https://github.com/dolanmiu/docx
- **示例**: https://github.com/dolanmiu/docx/tree/master/demo

---

## 下一步

- 如需编辑现有文档,查看 [editing.md](editing.md)
- 如需读取文档,查看 [reading.md](reading.md)
