# 追踪更改工作流

## 概述

本指南介绍如何在 Word 文档中实施追踪更改(Track Changes / Redlining),这是编辑正式文档的推荐方法。

**适用场景**:
- ✅ 编辑他人的文档
- ✅ 法律、学术、商业或政府文档
- ✅ 需要审核历史的任何文档
- ✅ 协作编辑

---

## 核心原则

### 最小化、精确编辑

**只标记实际更改的文本**,保留未更改部分的原始格式。

> [!CAUTION]
> **嵌套追踪更改 (Master Level)**
> 如果你要修改另一个作者已经“插入”(`w:ins`) 的内容:
> 1. **严禁**直接修改原有 `<w:t>` 文本。
> 2. **必须**在原作者的 `<w:ins>` 标签内部嵌套你自己的 `<w:del>`。
>
> ❌ **错误示例** (直接覆盖他人的追踪更改):
> `<w:ins w:author="张三"><w:r><w:t>新文本</w:t></w:r></w:ins>` (你直接把张三的删了改成了你的)
>
> ✅ **正确示例** (保留责任链):
> ```xml
> <w:ins w:author="张三">
>   <w:del w:author="Claude"><w:r><w:delText>张三原来的内容</w:delText></w:r></w:del>
>   <w:r><w:t>你修改的内容</w:t></w:r>
> </w:ins>
> ```


❌ **错误示例** - 替换整个句子:
```xml
<w:del><w:r><w:delText>合同期限为 30 天。</w:delText></w:r></w:del>
<w:ins><w:r><w:t>合同期限为 60 天。</w:t></w:r></w:ins>
```

✅ **正确示例** - 只标记更改的部分:
```xml
<w:r><w:t>合同期限为 </w:t></w:r>
<w:del><w:r><w:delText>30</w:delText></w:r></w:del>
<w:ins><w:r><w:t>60</w:t></w:r></w:ins>
<w:r><w:t> 天。</w:t></w:r>
```

---

## 完整工作流程

### 步骤 1: 获取 Markdown 表示

```bash
# 转换文档为 Markdown,保留追踪更改
pandoc --track-changes=all document.docx -o current.md

# 查看现有更改
cat current.md
```

### 步骤 2: 识别并分组更改

将所有需要的更改组织成逻辑批次(每批 3-10 个更改)。

#### 定位方法

**推荐**:
- 📍 章节/标题编号(如"第 3.2 节"、"第四条")
- 📍 段落标识符(如果有编号)
- 📍 使用唯一周围文本的 grep 模式
- 📍 文档结构(如"第一段"、"签名块")

**不推荐**:
- ❌ Markdown 行号(不对应 XML 结构)

#### 批次组织策略

**按章节**:
- 批次 1: 第 2 节修订
- 批次 2: 第 5 节更新

**按类型**:
- 批次 1: 日期更正
- 批次 2: 当事人名称更改

**按复杂度**:
- 批次 1: 简单文本替换
- 批次 2: 复杂结构更改

**按顺序**:
- 批次 1: 第 1-3 页
- 批次 2: 第 4-6 页

### 步骤 3: 解压文档

```bash
# 解压
python scripts/unpack.py document.docx unpacked/

# 注意脚本输出的建议 RSID
# 例如: "建议使用 RSID: 00AB12CD"
# 记下这个 RSID,在步骤 4 中使用
```

### 步骤 4: 批量实施更改

对于每批相关更改:

#### 4a. 将文本映射到 XML

```bash
# 在 word/document.xml 中搜索文本
grep -n "要修改的文本" unpacked/word/document.xml

# 查看上下文
grep -C 5 "要修改的文本" unpacked/word/document.xml
```

#### 4b. 创建并运行 Python 脚本

```python
from defusedxml import ElementTree as ET

# 加载文档
tree = ET.parse('unpacked/word/document.xml')
root = tree.getroot()
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# 使用步骤 3 中的 RSID
RSID = "00AB12CD"  # 替换为实际的 RSID

# 查找要修改的段落
for p in root.findall('.//w:p', ns):
    para_text = ''.join(p.itertext())
    
    if '要修改的文本' in para_text:
        # 实施追踪更改
        # (见下面的具体示例)
        pass

# 保存
tree.write('unpacked/word/document.xml', encoding='utf-8', xml_declaration=True)
```

**重要**: 每次运行脚本前都要重新 grep,因为行号会变化!

### 步骤 5: 打包文档

```bash
python scripts/pack.py unpacked/ reviewed-document.docx
```

### 步骤 6: 最终验证

```bash
# 转换为 Markdown 验证
pandoc --track-changes=all reviewed-document.docx -o verification.md

# 验证更改已应用
grep "原始文本" verification.md  # 应该不存在
grep "新文本" verification.md     # 应该存在

# 检查追踪更改标记
grep -E "\[.*\]{\.insertion}" verification.md  # 插入
grep -E "\[.*\]{\.deletion}" verification.md   # 删除
```

---

## 追踪更改 XML 模式

### 插入文本

```xml
<w:ins w:id="1" w:author="作者名" w:date="2024-01-01T10:00:00Z">
  <w:r>
    <w:t>新增的文本</w:t>
  </w:r>
</w:ins>
```

### 删除文本

```xml
<w:del w:id="2" w:author="作者名" w:date="2024-01-01T10:00:00Z">
  <w:r>
    <w:delText>删除的文本</w:delText>
  </w:r>
</w:del>
```

### 替换文本(删除 + 插入)

```xml
<!-- 保留未更改的文本 -->
<w:r w:rsidR="00AB12CD">
  <w:t>合同期限为 </w:t>
</w:r>

<!-- 删除旧值 -->
<w:del w:id="1" w:author="张三" w:date="2024-01-01T10:00:00Z">
  <w:r>
    <w:delText>30</w:delText>
  </w:r>
</w:del>

<!-- 插入新值 -->
<w:ins w:id="2" w:author="张三" w:date="2024-01-01T10:00:00Z">
  <w:r>
    <w:t>60</w:t>
  </w:r>
</w:ins>

<!-- 保留未更改的文本 -->
<w:r w:rsidR="00AB12CD">
  <w:t> 天。</w:t>
</w:r>
```

---

## Python 实现示例

### 示例 1: 简单文本替换

```python
from defusedxml import ElementTree as ET
from datetime import datetime

def track_replace(xml_file, old_text, new_text, author="编辑者", rsid="00AB12CD"):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    change_id = 1
    timestamp = datetime.now().isoformat()
    
    for p in root.findall('.//w:p', ns):
        # 查找包含旧文本的段落
        for r in p.findall('.//w:r', ns):
            t = r.find('w:t', ns)
            if t is not None and t.text and old_text in t.text:
                # 分割文本
                parts = t.text.split(old_text)
                
                # 清除原有内容
                p.remove(r)
                
                # 重建:前文 + 删除 + 插入 + 后文
                # 前文
                if parts[0]:
                    r1 = ET.SubElement(p, '{%s}r' % ns['w'])
                    r1.set('{%s}rsidR' % ns['w'], rsid)
                    t1 = ET.SubElement(r1, '{%s}t' % ns['w'])
                    t1.text = parts[0]
                
                # 删除
                del_elem = ET.SubElement(p, '{%s}del' % ns['w'])
                del_elem.set('{%s}id' % ns['w'], str(change_id))
                del_elem.set('{%s}author' % ns['w'], author)
                del_elem.set('{%s}date' % ns['w'], timestamp)
                change_id += 1
                
                r_del = ET.SubElement(del_elem, '{%s}r' % ns['w'])
                t_del = ET.SubElement(r_del, '{%s}delText' % ns['w'])
                t_del.text = old_text
                
                # 插入
                ins_elem = ET.SubElement(p, '{%s}ins' % ns['w'])
                ins_elem.set('{%s}id' % ns['w'], str(change_id))
                ins_elem.set('{%s}author' % ns['w'], author)
                ins_elem.set('{%s}date' % ns['w'], timestamp)
                change_id += 1
                
                r_ins = ET.SubElement(ins_elem, '{%s}r' % ns['w'])
                t_ins = ET.SubElement(r_ins, '{%s}t' % ns['w'])
                t_ins.text = new_text
                
                # 后文
                if parts[1]:
                    r2 = ET.SubElement(p, '{%s}r' % ns['w'])
                    r2.set('{%s}rsidR' % ns['w'], rsid)
                    t2 = ET.SubElement(r2, '{%s}t' % ns['w'])
                    t2.text = parts[1]
    
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

# 使用
track_replace('unpacked/word/document.xml', '30 天', '60 天', author='张三')
```

### 示例 2: 批量更改

```python
def batch_track_changes(xml_file, changes, author="编辑者", rsid="00AB12CD"):
    """
    changes: list of (old_text, new_text) tuples
    """
    for old, new in changes:
        track_replace(xml_file, old, new, author, rsid)
        print(f'✓ 已标记: {old} → {new}')

# 使用
changes = [
    ('2023年', '2024年'),
    ('甲方', '乙方'),
    ('30天', '60天')
]

batch_track_changes('unpacked/word/document.xml', changes, author='李四')
```

---

## 高级技巧

### 1. 获取下一个可用的更改 ID

```python
def get_next_change_id(root, ns):
    """获取下一个可用的更改 ID"""
    max_id = 0
    for elem in root.findall('.//*[@w:id]', ns):
        try:
            change_id = int(elem.get('{%s}id' % ns['w']))
            max_id = max(max_id, change_id)
        except (ValueError, TypeError):
            pass
    return max_id + 1
```

### 2. 保留原始格式

```python
def preserve_formatting(original_r, new_r, ns):
    """将原始 <w:r> 的格式复制到新 <w:r>"""
    rPr = original_r.find('w:rPr', ns)
    if rPr is not None:
        new_rPr = ET.Element('{%s}rPr' % ns['w'])
        new_rPr[:] = rPr[:]
        new_r.insert(0, new_rPr)
```

### 3. 使用 grep 定位精确位置

```bash
# 查找包含特定文本的行号
grep -n "第三条" unpacked/word/document.xml

# 查看该行周围的内容
sed -n '150,160p' unpacked/word/document.xml
```

---

## 验证清单

完成每批更改后,验证:

- [ ] XML 语法正确: `xmllint --noout unpacked/word/document.xml`
- [ ] 文档可以打包: `python scripts/pack.py unpacked/ test.docx`
- [ ] 文档可以打开: `open test.docx`
- [ ] 更改正确显示: `pandoc --track-changes=all test.docx -o test.md`
- [ ] 所有更改都已标记
- [ ] 未更改的文本保持原样

---

## 常见问题

### Q: 如何设置更改的作者和时间?

```python
del_elem.set('{%s}author' % ns['w'], '张三')
del_elem.set('{%s}date' % ns['w'], '2024-01-01T10:00:00Z')
```

### Q: 如何处理跨多个 `<w:r>` 的文本?

先合并段落文本,再重建:

```python
# 获取完整段落文本
full_text = ''.join(t.text for t in p.findall('.//w:t', ns) if t.text)

# 清除所有 <w:r>
for r in p.findall('.//w:r', ns):
    p.remove(r)

# 重建段落(带追踪更改)
# ...
```

### Q: RSID 是什么?

RSID (Revision Save ID) 是 Word 用来跟踪修订的标识符。使用 `unpack.py` 脚本时会建议一个 RSID,保持一致即可。

### Q: 如何接受/拒绝所有更改?

```bash
# 接受所有更改
pandoc --track-changes=accept document.docx -o accepted.docx

# 拒绝所有更改
pandoc --track-changes=reject document.docx -o rejected.docx
```

---

## 最佳实践

1. **小批次处理**: 每批 3-10 个更改,便于调试
2. **增量验证**: 每批完成后立即验证
3. **保留备份**: 每批前备份 `word/document.xml`
4. **使用版本控制**: Git 跟踪每批更改
5. **详细注释**: 在脚本中注释每个更改的目的

---

## 下一步

- 如需基础编辑,查看 [editing.md](editing.md)
- 如需读取文档,查看 [reading.md](reading.md)
- 如需创建新文档,查看 [creating.md](creating.md)
