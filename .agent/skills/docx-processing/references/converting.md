# 文档格式转换

## 概述

本指南介绍如何将 Word 文档转换为其他格式,特别是转换为图片用于视觉分析。

---

## DOCX → Markdown

### 使用 pandoc

```bash
# 基础转换
pandoc document.docx -o output.md

# 保留更多格式
pandoc document.docx -o output.md --wrap=none

# 提取纯文本
pandoc document.docx -t plain -o output.txt
```

---

## DOCX → PDF

### 方法 1: 使用 LibreOffice(推荐)

```bash
# 安装 LibreOffice
brew install libreoffice  # macOS
# sudo apt-get install libreoffice  # Linux

# 转换
soffice --headless --convert-to pdf document.docx

# 指定输出目录
soffice --headless --convert-to pdf --outdir ./output document.docx

# 批量转换
soffice --headless --convert-to pdf *.docx
```

### 方法 2: 使用 pandoc + LaTeX

```bash
# 需要安装 LaTeX
pandoc document.docx -o output.pdf
```

---

## DOCX → HTML

```bash
# 基础转换
pandoc document.docx -o output.html

# 独立 HTML(包含 CSS)
pandoc document.docx -o output.html --standalone

# 自定义 CSS
pandoc document.docx -o output.html --css=style.css
```

---

## PDF → 图片

### 使用 pdftoppm

```bash
# 安装 poppler
brew install poppler  # macOS
# sudo apt-get install poppler-utils  # Linux

# 转换为 JPEG
pdftoppm -jpeg -r 150 document.pdf page

# 这会创建: page-1.jpg, page-2.jpg, ...
```

### 参数说明

```bash
# 分辨率
-r 150    # 150 DPI(默认)
-r 300    # 300 DPI(高质量)

# 格式
-jpeg     # JPEG 格式
-png      # PNG 格式
-tiff     # TIFF 格式

# 页面范围
-f 2      # 起始页(第 2 页)
-l 5      # 结束页(第 5 页)

# 示例:仅转换第 2-5 页为高质量 PNG
pdftoppm -png -r 300 -f 2 -l 5 document.pdf page
```

---

## DOCX → 图片(两步法)

### 完整流程

```bash
# 步骤 1: DOCX → PDF
soffice --headless --convert-to pdf document.docx

# 步骤 2: PDF → JPEG
pdftoppm -jpeg -r 150 document.pdf page

# 结果: page-1.jpg, page-2.jpg, ...
```

### 自动化脚本

```bash
#!/bin/bash
# docx2images.sh - 将 DOCX 转换为图片

DOCX_FILE=$1
OUTPUT_PREFIX=${2:-page}
RESOLUTION=${3:-150}

# 检查文件
if [ ! -f "$DOCX_FILE" ]; then
    echo "错误: 文件不存在: $DOCX_FILE"
    exit 1
fi

# 转换为 PDF
echo "转换为 PDF..."
soffice --headless --convert-to pdf "$DOCX_FILE"

# 获取 PDF 文件名
PDF_FILE="${DOCX_FILE%.docx}.pdf"

# 转换为图片
echo "转换为图片..."
pdftoppm -jpeg -r "$RESOLUTION" "$PDF_FILE" "$OUTPUT_PREFIX"

# 清理临时 PDF
rm "$PDF_FILE"

echo "完成! 图片已保存为 ${OUTPUT_PREFIX}-*.jpg"
```

**使用**:
```bash
chmod +x docx2images.sh
./docx2images.sh document.docx output 300
```

---

## 其他格式转换

### DOCX → RTF

```bash
pandoc document.docx -o output.rtf
```

### DOCX → ODT(OpenDocument)

```bash
soffice --headless --convert-to odt document.docx
```

### DOCX → EPUB(电子书)

```bash
pandoc document.docx -o output.epub
```

---

## 批量转换

### 批量 DOCX → PDF

```bash
# 转换当前目录所有 DOCX
for file in *.docx; do
    soffice --headless --convert-to pdf "$file"
done

# 或使用 find
find . -name "*.docx" -exec soffice --headless --convert-to pdf {} \;
```

### 批量 DOCX → Markdown

```bash
for file in *.docx; do
    pandoc "$file" -o "${file%.docx}.md"
done
```

---

## 图片处理

### 调整图片大小

```bash
# 使用 ImageMagick
brew install imagemagick

# 调整为 50% 大小
mogrify -resize 50% page-*.jpg

# 调整为指定宽度
mogrify -resize 800x page-*.jpg
```

### 合并图片为 PDF

```bash
# 使用 ImageMagick
convert page-*.jpg output.pdf

# 使用 img2pdf
pip install img2pdf
img2pdf page-*.jpg -o output.pdf
```

### 添加水印

```bash
# 使用 ImageMagick
for img in page-*.jpg; do
    convert "$img" -pointsize 50 -fill "rgba(255,255,255,0.5)" \
        -gravity center -annotate +0+0 "DRAFT" "watermarked-$img"
done
```

---

## 质量对比

### 分辨率建议

| 用途 | DPI | 说明 |
|------|-----|------|
| 屏幕查看 | 72-96 | 最小文件大小 |
| 一般打印 | 150-200 | 平衡质量和大小 |
| 高质量打印 | 300 | 专业印刷 |
| 存档 | 600 | 最高质量 |

### 格式选择

| 格式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| JPEG | 小文件 | 有损压缩 | 照片、屏幕查看 |
| PNG | 无损、透明 | 较大文件 | 图表、截图 |
| TIFF | 无损、高质量 | 很大文件 | 存档、专业用途 |

---

## 故障排查

### LibreOffice 转换失败

```bash
# 检查 LibreOffice 是否安装
which soffice

# 查看详细错误
soffice --headless --convert-to pdf document.docx --verbose
```

### PDF 转换为空白图片

可能是权限问题:

```bash
# 检查 PDF 权限
pdfinfo document.pdf | grep Encrypted

# 如果加密,先解密
qpdf --decrypt document.pdf decrypted.pdf
```

### 图片质量不佳

增加分辨率:

```bash
# 使用更高 DPI
pdftoppm -jpeg -r 300 document.pdf page

# 或使用 PNG(无损)
pdftoppm -png -r 300 document.pdf page
```

---

## 实用工具

### 查看 PDF 信息

```bash
# 安装 poppler
pdfinfo document.pdf

# 查看页数
pdfinfo document.pdf | grep Pages
```

### 提取 PDF 特定页

```bash
# 使用 pdftk
pdftk document.pdf cat 2-5 output pages2-5.pdf

# 或使用 qpdf
qpdf document.pdf --pages . 2-5 -- output.pdf
```

---

## 下一步

- 如需读取文档,查看 [reading.md](reading.md)
- 如需编辑文档,查看 [editing.md](editing.md)
- 如需创建新文档,查看 [creating.md](creating.md)
