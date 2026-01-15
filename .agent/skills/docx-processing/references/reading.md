# 读取和分析 Word 文档

## 概述

本指南介绍如何读取和分析 Word 文档(.docx)的内容,包括文本提取和访问原始 XML 结构。

---

## 方法 1: 文本提取(推荐用于简单阅读)

### 使用 pandoc 转换为 Markdown

**基础转换**:
```bash
pandoc document.docx -o output.md
```

**保留追踪更改**:
```bash
# 显示所有更改
pandoc --track-changes=all document.docx -o output.md

# 接受所有更改
pandoc --track-changes=accept document.docx -o output.md

# 拒绝所有更改
pandoc --track-changes=reject document.docx -o output.md
```

**快速预览**(不保存文件):
```bash
pandoc document.docx -o - | less
```

### 适用场景

✅ 只需要读取文本内容  
✅ 需要快速预览文档  
✅ 想要查看追踪更改  
✅ 需要转换为其他格式

### 💡 进阶: 提取带图片的内容 (拆分素材必备)

如果需要将文档拆分为素材,并保留**图片与文本的对应关系**:

```bash
# 这会将图片提取到 ./images 目录,并在 Markdown 中生成正确的引用
pandoc document.docx --extract-media=./images -o content.md
```

这样你就可以通过解析 Markdown 轻松获取"文本段落 + 对应的图片路径",用于生成新文档。


---

## 方法 2: 访问原始 XML(用于复杂分析)

### 何时需要访问 XML

当你需要以下信息时:
- 📝 评论(comments)
- 🎨 复杂格式(字体、颜色、样式)
- 📊 文档结构(章节、表格)
- 🖼️ 嵌入媒体(图片、视频)
- 📋 元数据(作者、创建时间)

### 解压文档

```bash
# 使用提供的脚本
python scripts/unpack.py document.docx unpacked/

# 或使用系统 unzip
unzip document.docx -d unpacked/
```

### 关键文件结构

解压后的目录结构:

```
unpacked/
├── word/
│   ├── document.xml       # 主文档内容 ⭐
│   ├── comments.xml       # 评论
│   ├── styles.xml         # 样式定义
│   ├── settings.xml       # 文档设置
│   ├── numbering.xml      # 编号格式
│   ├── media/             # 嵌入的图片和媒体
│   └── _rels/             # 关系文件
├── docProps/
│   ├── core.xml           # 核心元数据
│   └── app.xml            # 应用程序属性
└── [Content_Types].xml    # 内容类型定义
```

### 查看主文档内容

```bash
# 查看文档 XML
cat unpacked/word/document.xml | xmllint --format - | less

# 搜索特定文本
grep "要查找的文本" unpacked/word/document.xml

# 查看评论
cat unpacked/word/comments.xml
```

### XML 结构示例

**段落和文本**:
```xml
<w:p>                          <!-- 段落 -->
  <w:r>                        <!-- 文本运行 -->
    <w:t>Hello World!</w:t>    <!-- 文本内容 -->
  </w:r>
</w:p>
```

**追踪更改**:
```xml
<!-- 插入 -->
<w:ins w:id="1" w:author="张三" w:date="2024-01-01T10:00:00Z">
  <w:r><w:t>新增文本</w:t></w:r>
</w:ins>

<!-- 删除 -->
<w:del w:id="2" w:author="李四" w:date="2024-01-02T11:00:00Z">
  <w:r><w:delText>删除文本</w:delText></w:r>
</w:del>
```

---

## 提取特定信息

### 提取所有评论

```bash
# 如果有 comments.xml
python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('unpacked/word/comments.xml')
for comment in tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}comment'):
    author = comment.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}author')
    text = ''.join(comment.itertext())
    print(f'{author}: {text}')
"
```

### 提取嵌入图片

```bash
# 图片位于 word/media/ 目录
ls -lh unpacked/word/media/

# 复制所有图片
cp unpacked/word/media/* ./extracted-images/
```

### 查看文档元数据

```bash
# 查看核心属性
cat unpacked/docProps/core.xml | xmllint --format -

# 提取作者和标题
grep -E "(creator|title)" unpacked/docProps/core.xml
```

---

## 常见任务

### 统计字数

```bash
# 方法 1: 使用 pandoc
pandoc document.docx -t plain | wc -w

# 方法 2: 从 XML 提取
grep -oP '(?<=<w:t>)[^<]+' unpacked/word/document.xml | wc -w
```

### 查找特定文本

```bash
# 在文档中搜索
grep -n "关键词" unpacked/word/document.xml

# 带上下文
grep -C 3 "关键词" unpacked/word/document.xml
```

### 检查追踪更改

```bash
# 查看是否有追踪更改
grep -E "(w:ins|w:del)" unpacked/word/document.xml

# 统计更改数量
echo "插入: $(grep -c 'w:ins' unpacked/word/document.xml)"
echo "删除: $(grep -c 'w:del' unpacked/word/document.xml)"
```

---

## 故障排查

### 文档无法打开

```bash
# 1. 检查文件是否是有效的 ZIP
file document.docx

# 2. 尝试解压
unzip -t document.docx

# 3. 提取可能的文本
strings document.docx | less
```

### XML 格式错误

```bash
# 验证 XML 语法
xmllint --noout unpacked/word/document.xml

# 格式化 XML(便于阅读)
xmllint --format unpacked/word/document.xml > formatted.xml
```

---

## 下一步

- 如需创建新文档,查看 [creating.md](creating.md)
- 如需编辑文档,查看 [editing.md](editing.md)
- 如需追踪更改,查看 [tracking.md](tracking.md)
