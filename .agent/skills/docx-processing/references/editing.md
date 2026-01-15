# 基础文档编辑

## 概述

本指南介绍如何使用 Python 和 OOXML 直接编辑现有 Word 文档的 XML 结构。

**适用场景**: 自己的文档 + 简单修改

**如需追踪更改**: 查看 [tracking.md](tracking.md)

---

## 工作流程

### 1. 解压文档

```bash
# 使用提供的脚本
python scripts/unpack.py document.docx unpacked/

# 或使用系统工具
unzip document.docx -d unpacked/
```

### 2. 编辑 XML

有两种方式:

#### 方式 A: 直接编辑 XML 文件 (大师级规则)

> [!CAUTION]
> **XML 元素顺序严格性 (Critical)**
> 在 `<w:pPr>` (段落属性) 中,子元素必须遵循严格的先后顺序,否则 Word 会判定文档损坏。
> **法定顺序**:
> 1. `<w:pStyle>` (样式)
> 2. `<w:numPr>` (编号)
> 3. `<w:spacing>` (间距)
> 4. `<w:ind>` (缩进)
> 5. `<w:jc>` (对齐方式)
>
> 如果你手动插入这些标签,请务必检查顺序。


```bash
# 编辑主文档
vim unpacked/word/document.xml

# 或使用 sed 批量替换
sed -i 's/旧文本/新文本/g' unpacked/word/document.xml
```

#### 方式 B: 使用 Python 脚本

```python
import xml.etree.ElementTree as ET

# 加载文档
tree = ET.parse('unpacked/word/document.xml')
root = tree.getroot()

# 命名空间
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# 查找并修改文本
for t in root.findall('.//w:t', ns):
    if t.text == '旧文本':
        t.text = '新文本'

# 保存
tree.write('unpacked/word/document.xml', encoding='utf-8', xml_declaration=True)
```

### 3. 重新打包

```bash
# 使用提供的脚本
python scripts/pack.py unpacked/ output.docx

# 或使用系统工具
cd unpacked && zip -r ../output.docx * && cd ..
```

---

## 常见编辑任务

### 替换文本

```python
import xml.etree.ElementTree as ET

def replace_text(xml_file, old_text, new_text):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    for t in root.findall('.//w:t', ns):
        if t.text and old_text in t.text:
            t.text = t.text.replace(old_text, new_text)
    
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

# 使用
replace_text('unpacked/word/document.xml', '公司名称', '新公司名称')
```

### 删除段落

```python
def delete_paragraph_containing(xml_file, text):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    for p in root.findall('.//w:p', ns):
        para_text = ''.join(p.itertext())
        if text in para_text:
            parent = root.find('.//*[w:p]', ns)
            if parent is not None:
                parent.remove(p)
    
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
```

### 添加段落

```python
def add_paragraph(xml_file, text, position='end'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    # 创建新段落
    p = ET.Element('{%s}p' % ns['w'])
    r = ET.SubElement(p, '{%s}r' % ns['w'])
    t = ET.SubElement(r, '{%s}t' % ns['w'])
    t.text = text
    
    # 找到 body
    body = root.find('.//w:body', ns)
    
    if position == 'end':
        body.append(p)
    elif position == 'start':
        body.insert(0, p)
    
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

### 表格与错误处理 (大师级)

#### 示例: 重置所有表格边框

修复表格格式混乱的终极方法。

```python
def reset_table_borders(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    for tbl in root.findall('.//w:tbl', ns):
        tblPr = tbl.find('w:tblPr', ns)
        # 获取或创建 tblBorders
        tblBorders = tblPr.find('w:tblBorders', ns)
        if tblBorders is None:
            tblBorders = ET.SubElement(tblPr, '{%s}tblBorders' % ns['w'])
            
        # 设置所有边框为单实线
        for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            border = tblBorders.find('w:%s' % side, ns)
            if border is None:
                border = ET.SubElement(tblBorders, '{%s}%s' % (ns['w'], side))
            border.set('{%s}val' % ns['w'], 'single')
            border.set('{%s}sz' % ns['w'], '4') # 1/2 pt
            border.set('{%s}color' % ns['w'], '000000')

    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
```

#### 示例: 识别并修正"错误格式" (Lint & Fix)

例如: 强制将所有使用"Comic Sans MS"的字体替换为"Arial"。

```python
def fix_bad_fonts(xml_file, bad_font, good_font):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    replacements = 0
    for rFonts in root.findall('.//w:rFonts', ns):
        for attr in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
            key = '{%s}%s' % (ns['w'], attr)
            if rFonts.get(key) == bad_font:
                rFonts.set(key, good_font)
                replacements += 1
                
    if replacements > 0:
        print(f"已修复 {replacements} 处错误字体")
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
```

```

### 修改格式 (大师级技巧)

> [!TIP]
> **保留 RSID 以维持“原生感”**
> 每次手动修改文本运行 (`<w:r>`) 时,尽量从原始节点中提取并保留 `w:rsidR` 属性。这能让文档看起来是由同一个作者连贯编辑的,而不是被脚本暴力插入的。

#### 示例: 批量标准化段落格式 (格式清洗)

此脚本用于统一行距和段落间距,常用于修复格式混乱的文档。

```python
def normalize_spacing(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    for p in root.findall('.//w:p', ns):
        pPr = p.find('w:pPr', ns)
        if pPr is None:
            pPr = ET.Element('{%s}pPr' % ns['w'])
            p.insert(0, pPr)
            
        # 强制设置间距: 段后 1行(240), 行距 1.5倍(360)
        spacing = pPr.find('w:spacing', ns)
        if spacing is None:
            spacing = ET.SubElement(pPr, '{%s}spacing' % ns['w'])
        
        # 清除旧属性并设置新标准
        spacing.attrib.clear()
        spacing.set('{%s}after' % ns['w'], '240')    # 段后 12磅
        spacing.set('{%s}line' % ns['w'], '360')     # 行距 1.5倍
        spacing.set('{%s}lineRule' % ns['w'], 'auto')

    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
```

#### 示例: 修改全局样式 (如将"标题"改为宋体 10号)

这需要修改 `word/styles.xml` 文件,是最高效的全局修改方式。

```python
def update_style_font(styles_xml_file, style_id, font_name, size_pt):
    tree = ET.parse(styles_xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    # 查找指定样式 (如 "Heading1")
    for style in root.findall('.//w:style', ns):
        if style.get('{%s}styleId' % ns['w']) == style_id:
            rPr = style.find('w:rPr', ns)
            if rPr is None:
                rPr = ET.SubElement(style, '{%s}rPr' % ns['w'])
            
            # 设置字体 (中西文同时设置)
            fonts = rPr.find('w:rFonts', ns)
            if fonts is None:
                fonts = ET.SubElement(rPr, '{%s}rFonts' % ns['w'])
            fonts.set('{%s}ascii' % ns['w'], font_name)
            fonts.set('{%s}eastAsia' % ns['w'], font_name)
            
            # 设置字号 (单位是半点, 所以 *2)
            sz = rPr.find('w:sz', ns)
            if sz is None:
                sz = ET.SubElement(rPr, '{%s}sz' % ns['w'])
            sz.set('{%s}val' % ns['w'], str(size_pt * 2))
            
            print(f"样式 {style_id} 已更新为 {font_name} {size_pt}pt")
            
    tree.write(styles_xml_file, encoding='utf-8', xml_declaration=True)
```

**使用提示**:
- 修改 `word/styles.xml` 可以一次性改变所有使用该样式的段落。
- 修改 `word/document.xml` 则是针对特定内容的"硬格式"覆盖。


---

## 使用 defusedxml(推荐)

为了安全地解析 XML,建议使用 `defusedxml`:

```python
from defusedxml import ElementTree as ET

# 其余代码相同
tree = ET.parse('unpacked/word/document.xml')
# ...
```

**安装**:
```bash
pip install defusedxml
```

---

## 完整示例:批量替换

```python
#!/usr/bin/env python3
"""
批量替换 Word 文档中的文本
"""
from defusedxml import ElementTree as ET
import sys

def replace_all(xml_file, replacements):
    """
    replacements: dict, {'旧文本': '新文本', ...}
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    count = 0
    for t in root.findall('.//w:t', ns):
        if t.text:
            for old, new in replacements.items():
                if old in t.text:
                    t.text = t.text.replace(old, new)
                    count += 1
    
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    return count

if __name__ == '__main__':
    replacements = {
        '旧公司名': '新公司名',
        '2023': '2024',
        '张三': '李四'
    }
    
    count = replace_all('unpacked/word/document.xml', replacements)
    print(f'完成 {count} 处替换')
```

**使用**:
```bash
python scripts/unpack.py document.docx unpacked/
python batch_replace.py
python scripts/pack.py unpacked/ output.docx
```

---

## 注意事项

### 1. 文本可能被分割

Word 可能将连续文本分割到多个 `<w:t>` 元素中:

```xml
<!-- "Hello World" 可能被分割为: -->
<w:r><w:t>Hel</w:t></w:r>
<w:r><w:t>lo Wor</w:t></w:r>
<w:r><w:t>ld</w:t></w:r>
```

**解决方案**: 先合并文本再搜索

```python
def get_paragraph_text(p, ns):
    """获取段落的完整文本"""
    return ''.join(t.text for t in p.findall('.//w:t', ns) if t.text)

def replace_in_paragraph(p, old, new, ns):
    """在段落中替换文本"""
    full_text = get_paragraph_text(p, ns)
    if old not in full_text:
        return False
    
    # 简单方法:清除所有 <w:r>,创建新的
    for r in p.findall('.//w:r', ns):
        p.remove(r)
    
    # 创建新的文本运行
    r = ET.SubElement(p, '{%s}r' % ns['w'])
    t = ET.SubElement(r, '{%s}t' % ns['w'])
    t.text = full_text.replace(old, new)
    
    return True
```

### 2. 保留 XML 声明

```python
tree.write(
    xml_file,
    encoding='utf-8',
    xml_declaration=True  # 重要!
)
```

### 3. 命名空间

始终使用正确的命名空间:

```python
ns = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
}
```

---

## 验证编辑结果

### 1. 检查 XML 语法

```bash
xmllint --noout unpacked/word/document.xml
```

### 2. 预览文档

```bash
# 打包后用 pandoc 预览
python scripts/pack.py unpacked/ temp.docx
pandoc temp.docx -o preview.md
cat preview.md
```

### 3. 在 Word 中打开

```bash
# macOS
open output.docx

# Linux
libreoffice output.docx
```

---

## 故障排查

### 文档损坏

如果编辑后文档无法打开:

1. **检查 XML 语法**:
   ```bash
   xmllint --noout unpacked/word/document.xml
   ```

2. **检查 ZIP 结构**:
   ```bash
   unzip -t output.docx
   ```

3. **恢复备份**:
   ```bash
   cp document.docx.backup document.docx
   ```

### 文本未替换

可能原因:
- 文本被分割到多个元素
- 大小写不匹配
- 包含特殊字符

**调试**:
```python
# 打印所有文本元素
for t in root.findall('.//w:t', ns):
    print(repr(t.text))
```

---

## 最佳实践

1. **始终备份原文件**:
   ```bash
   cp document.docx document.docx.backup
   ```

2. **使用版本控制**:
   ```bash
   git add unpacked/
   git commit -m "编辑前"
   # 进行编辑
   git diff
   ```

3. **测试小范围修改**:
   先在测试文档上验证脚本

4. **保留格式**:
   尽量不删除 `<w:rPr>` 等格式元素

---

## 下一步

- 如需追踪更改,查看 [tracking.md](tracking.md)
- 如需创建新文档,查看 [creating.md](creating.md)
- 如需读取文档,查看 [reading.md](reading.md)
