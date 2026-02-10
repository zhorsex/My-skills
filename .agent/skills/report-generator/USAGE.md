# 使用指南

---

## 🚀 交互式大纲生成功能（新增）

本功能允许您通过 AI 智能生成报告大纲，支持多种交互模式和增强建议。

### 快速开始（大纲生成）

#### 方式一：快速生成（推荐）

1. **启动大纲生成**：
   ```bash
   python scripts/generate_outline.py \
     --input "风电场地质调查报告" \
     --mode quick \
     --output outline-generated.md
   ```

2. **系统自动生成大纲**：
   - 智能选择合适的模板
   - 生成章+节结构（中等详细程度）
   - 提供增强建议（章节数量、配图、写作方向）

3. **查看生成的大纲**：
   ```bash
   # 查看大纲内容
   cat outline-generated.md
   
   # 使用大纲管理工具
   python scripts/outline_manager.py --show outline-generated.md
   ```

#### 方式二：逐章引导

适用于需要精细控制大纲结构的场景：

```bash
python scripts/generate_outline.py \
  --input "风电项目" \
  --mode chapter \
  --template OT101 \
  --output outline-generated.md
```

系统会逐个生成章节，每章生成后要求您确认和调整。

#### 方式三：要点扩展

适用于已有基础大纲结构，需要系统扩展详细内容的场景：

```bash
python scripts/generate_outline.py \
  --input "风电项目" \
  --mode keypoints \
  --reference reference.md \
  --output outline-generated.md
```

### 编辑生成的大纲

#### 交互式编辑

```bash
python scripts/outline_editor.py \
  --input outline-generated.md \
  --mode interactive
```

**编辑功能**：
- 添加章节
- 添加小节
- 删除章节
- 重命名章节
- 移动章节
- 重新编号所有章节

#### 命令式编辑

```bash
# 添加章节
python scripts/outline_editor.py \
  --add-chapter "项目投资估算" \
  --after 3 \
  --input outline-generated.md \
  --output outline-edited.md

# 删除章节
python scripts/outline_editor.py \
  --remove-chapter 4 \
  --input outline-generated.md \
  --output outline-edited.md

# 移动章节
python scripts/outline_editor.py \
  --move-chapter 5 \
  --after 3 \
  --input outline-generated.md \
  --output outline-edited.md
```

### 管理大纲

#### 列出所有大纲

```bash
python scripts/outline_manager.py --list
```

输出示例：
```
序号    文件名                         标题                          章节      大小(KB)
--------------------------------------------------------------------------------
1       outline-20260204_162000.md      风电场地质调查报告           7         12.5
2       outline-20260203_153045.md      工程设计方案                   9         15.2
3       outline-20260202_144500.md      环境影响评估报告               9         18.0
--------------------------------------------------------------------------------
总计: 3 个大纲文件
```

#### 查看大纲详情

```bash
python scripts/outline_manager.py --show outline-generated.md
```

#### 查看历史版本

```bash
python scripts/outline_manager.py --history outline-generated.md
```

#### 搜索大纲

```bash
python scripts/outline_manager.py --search "地质调查"
```

### 高级功能

#### 指定模板生成

```bash
python scripts/generate_outline.py \
  --input "风电场地质调查报告" \
  --mode quick \
  --template OT101 \
  --output outline-generated.md
```

**可用模板**：
- OT001：精简版快速报告（3-4章）
- OT002：标准版综合报告（5-6章）
- OT003：详细版深度报告（7-9章）
- OT101：地质调查报告模板
- OT102：工程设计方案模板
- OT103：环境影响评估报告模板

#### 使用参考文档

```bash
python scripts/generate_outline.py \
  --input "风电项目" \
  --mode quick \
  --reference doc1.md doc2.pdf \
  --output outline-generated.md
```

系统会从参考文档中提取结构信息，辅助生成大纲。

### 大纲生成流程图

```
┌─────────────┐
│  开始       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 选择生成模式 │
│ quick/chapter/ │
│ keypoints   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 输入项目信息 │
│ - 主题      │
│ - 关键词    │
│ - 模板（可选）│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ AI生成大纲   │
│ 或模板匹配   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 展示候选模板│
│ 用户选择     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 智能推荐     │
│ - 章节数量   │
│ - 配图建议   │
│ - 写作方向   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 用户编辑调整 │
│ 添加/删除/   │
│ 移动/重命名   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 确认最终大纲 │
│ 用于报告生成 │
└─────────────┘
```

### 常见问题

#### Q1: 如何选择合适的模板？

**A**: 系统会根据关键词自动推荐模板。您也可以手动指定：
- 地质调查 → 使用 OT101
- 工程设计 → 使用 OT102
- 环境评估 → 使用 OT103
- 快速报告 → 使用 OT001
- 标准报告 → 使用 OT002
- 详细报告 → 使用 OT003

#### Q2: 如何修改生成的大纲？

**A**: 两种方式：
1. **交互式编辑**（推荐）：`python scripts/outline_editor.py --input outline.md --mode interactive`
2. **命令式编辑**：使用 `--add-chapter`、`--remove-chapter` 等参数

#### Q3: 大纲保存到哪里了？

**A**: 
1. Markdown 文件：指定的输出路径（默认：outline-generated.md）
2. 历史记录：`iteration/outline-history/outline_时间戳.json`

#### Q4: 如何恢复历史版本？

**A**:
```bash
# 查看历史版本
python scripts/outline_manager.py --history outline-generated.md

# 历史记录保存在 iteration/outline-history/ 目录
```

#### Q5: 生成的大纲可以直接用于报告生成吗？

**A**: 可以！生成的大纲采用标准 Markdown 格式，符合 report-generator 的输入要求。直接使用 `--input outline-generated.md` 参数即可。

---

## 快速开始

### 第1步：启动技能

在Claude中启动 `report-generator` skill：

```
请使用 /report-generator skill
```

### 第2步：提供报告信息

根据skill的提示，提供以下信息：

1. **参考文档**：提供需要参考的文档路径列表
    ```
    请提供本次报告需要参考的文档路径列表：
    - F:/docs/标准规范.docx
    - F:/docs/技术报告.pdf
    - F:/docs/案例资料.md
    ```

2. **大纲文件**：提供大纲文件路径或直接输入大纲结构
    ```
    请提供大纲文件路径或直接输入大纲结构：
    - 第1章 项目背景与目标
    - 第2章 技术方案概述
    - 第3章 工程设计方案
    - ...
    ```

3. **基本信息**：确认报告基本信息
    ```
    请确认基本信息：
    - 报告标题：河南省沿黄流域风电场地质调查报告
    - 报告类型：工程技术报告
    - 目标读者：项目评审专家
    - 总体字数范围：约15000字
    - 输出文件路径：F:/output/报告.docx
    ```

### 第3步：逐章编写确认

skill会按章节逐个生成内容，每章完成后需要您确认：

1. **章节规划确认**：确认本章的资料搜集深度、图表需求、目标字数
    ```
    本章是否需要搜集专业资料？
   选项：工程规范、技术标准、行业数据、案例资料
   
   资料搜集的深度要求？
   A. 🔍 快速搜索 (1-2个来源, 3-5分钟)
   B. 📚 标准搜索 (3-5个来源, 8-10分钟)
   C. 🔬 深度搜索 (6-10个来源, 15-20分钟)
   D. 🌐 广泛搜索 (10-15个来源, 30-40分钟)
   
   本章需要生成哪些图表？
   选项：流程图、柱状图、折线图、饼图、表格
   
   本章的目标字数范围？
   例如：2000-2500字
   ```

2. **章节内容确认**：查看本章内容，确认是否需要修改
   ```
   本章内容是否符合要求？
   选项：
   A. 完全符合，继续下一章
   B. 需要修改（请说明修改意见）
   C. 需要重写（请说明重写方向）
   ```

3. **修改完成确认**：如需修改，查看修改后的内容，再次确认
   ```
   修改后的内容是否符合要求？
   选项：
   A. 完全符合，继续下一章
   B. 继续修改
   C. 需要重写
   ```

### 第4步：整合与完善

所有章节完成后，skill会进行整体整合和检查：

1. **术语一致性检查**：检查全文术语使用是否一致
   ```
   是否发现术语不一致？
   发现冲突项：
   - 术语A：风力发电机组
   - 术语B：风电设备
   是否需要统一方式？
   ```

2. **风格统一性检查**：检查全文风格是否统一
   ```
   是否发现风格不统一？
   需要调整的方面：
   - 标题层级
   - 段落长度
   - 技术语言
   ```

3. **逻辑连贯性检查**：检查章节间逻辑是否连贯
   ```
   是否发现逻辑不连贯？
   需要调整的方面：
   - 章节过渡
   - 内容重复
   - 信息缺失
   ```

### 第5步：最终预览和确认

查看完整报告预览，确认是否满意：

```
报告是否符合预期？
选项：
A. 完全符合，准备输出
B. 需要调整（请说明调整内容）
```

### 第6步：生成Word文档

skill会使用/docx skill生成Word文档，保存到指定路径：

```
文件已保存到：F:/output/河南省沿黄流域风电场地质调查报告.docx
```

## 示例

### 示例1：完整报告生成流程

```
用户：我需要写一份风电场建设方案，请根据大纲逐章编写

Skill：好的，请提供参考文档和大纲

用户：
参考文档：
- F:/docs/GB-T-31084-2014.docx
- F:/docs/风电技术规范.pdf
- F:/docs/生态修复技术导则.docx

大纲：
第1章 项目背景与目标
第2章 技术方案概述
第3章 工程设计方案
第4章 施工组织设计

Skill：好的，开始第1章...

[第1章规划]
Skill：当前章节：第1章 项目背景与目标
本章是否需要搜集专业资料？
用户：是，工程规范
资料搜集的深度要求？
用户：B. 标准搜索 (3-5个来源, 8-10分钟)
本章需要生成哪些图表？
用户：表格
本章的目标字数范围？
用户：2000字

Skill：好的，正在搜集资料...（8分钟）
资料搜集完成，开始编写内容...

[第1章内容确认]
Skill：第1章内容如下：
[展示第1章完整内容]

用户：完全符合，继续下一章

Skill：好的，开始第2章...

[重复第2-4章]

[整合与完善]
Skill：所有章节完成，开始术语一致性检查...
[检查结果]
发现术语不一致：
- "风力发电机组"和"风电设备"混用
是否统一为"风力发电机组"？
用户：是

Skill：已统一术语...

[最终预览]
Skill：报告预览如下：
[展示完整报告预览]

报告是否符合预期？
用户：完全符合，准备输出

Skill：正在生成Word文档...
文件已保存到：F:/output/风电场建设方案.docx
```

### 示例2：章节修改流程

```
[第2章内容确认]
Skill：第2章内容如下：
[展示第2章内容]

用户：需要修改。技术方案描述过于笼统，需要补充具体参数和技术细节

Skill：好的，正在修改第2章...
[修改后的内容]
Skill：修改后的内容如下：
[展示修改后的内容，补充具体参数]

用户：还是不够详细，需要补充与其他方案的对比数据

Skill：好的，正在补充对比数据...
[再次修改后的内容]
Skill：补充对比数据后的内容如下：
[展示包含对比数据的内容]

用户：完全符合，继续下一章
```

### 示例3：术语一致性检查

```
Skill：术语一致性检查发现冲突：

冲突项1：
- 术语A：风力发电机组（使用8次）
- 术语B：风电设备（使用3次）
- 建议统一为：风力发电机组

冲突项2：
- 术语A：生态修复（使用10次）
- 术语B：生态环境修复（使用2次）
- 建议统一为：生态修复

是否统一这些术语？
用户：全部统一

Skill：已统一术语，全文共替换11处...
```

## 模板管理与排版功能

report-generator skill 提供了完整的模板管理和文档排版功能，可以为已有Word文档应用专业格式模板。

### 功能概述

**1. 模板生成功能**
- 预定义模板：地质资料归档格式、通用工程技术报告
- 自定义模板：完全自定义页面设置、字体、字号、段落格式
- 预设管理：保存自定义配置供重复使用

**2. 文档排版功能**
- 样式映射（推荐）：自动识别标题层级并应用对应样式
- 全文复制：完全套用模板格式
- 局部应用：仅应用页面设置/正文/表格/图片样式

**3. 模板管理功能**
- 模板列表查询
- 根据报告类型智能推荐模板
- 模板有效性验证
- 预设管理

### 使用场景

**场景1：为已有文档排版**
```
用户：帮我排版这个已有的文档 F:/docs/旧报告.docx

Skill：扫描templates/目录...
       找到可用模板：
       1. geological-survey-template.docx（地质资料归档格式）
       2. generic-engineering-template.docx（通用工程报告）
       
       请选择模板（输入编号）：

用户：1

Skill：请选择排版方式：
       A. 样式映射（自动识别标题层级）⭐ 推荐
       B. 全文复制（完全套用模板）
       C. 局部应用

用户：A

Skill：排版完成！
       输出：旧报告-排版后.docx
       应用统计：
       - 章标题: 3 个
       - 节标题: 5 个
       - 正文段落: 12 段
       - 表格: 2 个
```

**场景2：无现成模板时生成并排版**
```
用户：帮我排版这个文档 report.docx

Skill：扫描templates/目录...
       未找到可用模板。
       
       请选择：
       A. 生成地质资料归档格式模板（快速）⭐ 推荐
       B. 生成通用工程技术报告模板
       C. 自定义生成模板
       D. 不使用模板

用户：C（选择自定义生成）

Skill：【进入交互式自定义流程】
       === 页面设置 ===
       纸张大小 [A4]：
       上页边距 (cm) [2.75]：2.5
       下页边距 (cm) [2.75]：2.5
       左页边距（内侧）(cm) [2.86]：3.0
       右页边距（外侧）(cm) [2.27]：2.5
       装订线 (cm) [1.0]：0.8
       
       === 字体设置 ===
       中文字体 [宋体]：微软雅黑
       章标题字体 [宋体]：黑体
       
       === 字号设置 ===
       章标题字号 (pt) [22]：24
       节标题字号 (pt) [16]：18
       正文字号 (pt) [10.5]：11
       
       === 预览并确认 ===
       [显示所有设置参数]
       
       确认以上参数？
       A. 确认并生成
       B. 修改某些参数
       C. 保存为预设（命名为：我的自定义格式）

用户：A

Skill：[生成中] 创建页面设置... ✓
       [生成中] 创建字体样式... ✓
       [生成中] 创建段落样式... ✓
       [完成] 模板已生成：templates/custom-my-20260203.docx
       
       是否立即应用此模板进行排版？
       A. 立即应用
       B. 保存模板，稍后手动排版

用户：A

Skill：正在分析文档结构...
       [识别] 找到 2 个章标题，4 个节标题，15 个正文段落，1 个表格
       
       应用自定义模板...
       [应用] 页面设置... ✓
       [应用] 标题样式... ✓
       [应用] 正文样式... ✓
       [应用] 表格样式... ✓
       
       ╔══════════════════════════════════════════╗
       ║           文档排版完成                    ║
       ╠══════════════════════════════════════════╣
       ║  源文件: report.docx                       ║
       ║  输出文件: report-排版后.docx              ║
       ║  使用模板: custom-my-20260203.docx          ║
       ║                                          ║
       ║  自定义参数:                              ║
       ║  ├── 字体: 微软雅黑                       ║
       ║  ├── 章标题: 黑体 24pt                    ║
       ║  ├── 页边距: 2.5cm（上/下/右），3.0cm（左） ║
       ║  └── 装订线: 0.8cm                        ║
       ║                                          ║
       ║  应用统计:                                ║
       ║  ├── 章标题: 2 个                         ║
       ║  ├── 节标题: 4 个                         ║
       ║  ├── 正文段落: 15 段                      ║
       ║  └── 表格: 1 个                           ║
       ╚══════════════════════════════════════════╝
       
       💡 提示：自定义模板已保存，下次可直接使用！
```

### 命令行使用

**generate_template.py - 模板生成**
```bash
# 生成预定义模板
python scripts/generate_template.py --type geological --output templates/geo.docx
python scripts/generate_template.py --type engineering --output templates/eng.docx

# 交互式自定义生成
python scripts/generate_template.py --type custom --interactive

# 命令行参数自定义生成
python scripts/generate_template.py --type custom \
  --page-margin "2.75,2.75,2.86,2.27" \
  --gutter 1.0 \
  --body-font "宋体" \
  --body-size 10.5 \
  --output templates/custom.docx

# 使用预设生成
python scripts/generate_template.py --preset "my-format"

# 列出所有预设
python scripts/generate_template.py --list-presets
```

**apply_template.py - 文档排版**
```bash
# 样式映射方式（推荐）- 自动识别标题层级
python scripts/apply_template.py \
  --input source.docx \
  --template templates/geological-template.docx \
  --output formatted.docx \
  --method mapping

# 全文复制方式 - 完全套用模板
python scripts/apply_template.py \
  --input source.docx \
  --template templates/geological-template.docx \
  --output formatted.docx \
  --method copy

# 局部应用方式 - 仅应用特定部分
python scripts/apply_template.py \
  --input source.docx \
  --template templates/geological-template.docx \
  --output formatted.docx \
  --method partial \
  --parts "pagesetup,body,table"
```

**template_manager.py - 模板管理**
```bash
# 列出所有模板
python scripts/template_manager.py --list

# 查看模板详情
python scripts/template_manager.py --info geological-template.docx

# 根据报告类型推荐模板
python scripts/template_manager.py --recommend "地质调查报告"

# 验证所有模板
python scripts/template_manager.py --validate

# 删除模板
python scripts/template_manager.py --delete old-template.docx

# 列出所有预设
python scripts/template_manager.py --list-presets

# 查看预设详情
python scripts/template_manager.py --preset-info "my-format"
```

### 排版方法说明

**样式映射（mapping）- 推荐**
- **原理**：自动分析源文档段落特征（字体大小、加粗、对齐方式），智能识别标题层级，映射到模板的对应样式
- **适用**：文档结构清晰，有明确的标题层级
- **优点**：保留原文档结构，智能识别，批量应用
- **识别规则**：
  - 大字体+加粗+居中 → 章标题
  - 中字体+加粗+左对齐 → 节标题
  - 正常字体+首行缩进 → 正文

**全文复制（copy）**
- **原理**：将源文档内容复制到新模板中，按模板重新排版
- **适用**：文档格式混乱，需要彻底重新排版
- **优点**：完全套用模板格式，确保一致性

**局部应用（partial）**
- **原理**：仅应用指定的部分样式
- **适用**：只需要修改部分格式
- **可选部分**：
  - `pagesetup`：页面设置（边距、装订线、页眉页脚）
  - `body`：正文样式（字体、字号、行距）
  - `table`：表格样式
  - `figure`：图片样式

### 自定义模板参数

**页面设置**
- 纸张大小：A4（默认）
- 页边距：上/下/左/右（单位：cm）
- 装订线：内侧装订线宽度（单位：cm）
- 页眉页脚距离（单位：cm）

**字体设置**
- 中文字体：宋体、黑体、楷体、仿宋、微软雅黑
- 英文字体：Times New Roman（默认）
- 专用字体：封面标题、章标题、节标题、正文

**字号设置**
- 章标题：22pt（二号，可调整）
- 节标题：16pt（三号，可调整）
- 段标题：14pt（四号，可调整）
- 正文：10.5pt（五号，可调整）
- 表文：9pt（小五号）
- 表注：7.5pt（六号）

**段落格式**
- 行距：1.0/1.25/1.5/2.0倍
- 首行缩进：2字符（默认）
- 段前段后间距

**特殊格式**
- 封面页：地质调查项目成果报告、题名、单位、日期
- 扉页：项目信息、人员信息
- 目录页：自动生成目录
- 页眉页脚：页码（罗马数字+阿拉伯数字）
- 表格样式：表头、表文、表注
- 图片样式：图号、图名
- 参考文献样式

### 注意事项

1. **备份源文件**：排版前建议备份原始文档
2. **字体兼容性**：确保系统已安装模板所需的中文字体
3. **复杂文档**：包含复杂宏或交叉引用的文档可能需要手动调整
4. **页码设置**：排版后会应用模板的页码格式，可能需要重新生成目录
5. **图片和表格**：排版后会应用新的格式样式，位置可能需要微调

### 常见问题

**Q: 排版会改变我的文档内容吗？**
A: 不会。排版只修改格式（字体、字号、间距等），不会改变文字内容。

**Q: 原有图片和表格会丢失吗？**
A: 不会。所有图片和表格都会保留，并应用新的格式样式。

**Q: 排版后格式混乱怎么办？**
A: 可以尝试：
- 使用"全文复制"方式重新排版
- 手动在Word中调整
- 检查源文档是否有复杂格式

**Q: 可以批量排版多个文档吗？**
A: 可以。使用命令行方式配合批处理脚本（bash/python）实现批量排版。

**Q: 如何保存自定义格式供将来使用？**
A: 在交互式自定义流程中，选择"保存为预设"，输入预设名称，下次可直接使用。

---

## FAQ

### Q1: skill支持哪些报告类型？

A: 本skill主要支持工程技术报告，包括：
- 技术方案报告
- 可行性研究报告
- 工程设计报告
- 施工组织设计
- 环境影响评价报告
- 立项申请报告

其他类型的报告（如学术报告、商业报告）也可以使用，但效果可能不如工程技术报告理想。

### Q2: 资料搜集的四个深度有什么区别？

A: 四个深度的区别如下：

| 深度级别 | 资料数量 | 时间预算 | 验证标准 | 适用场景 |
|---------|---------|---------|---------|---------|
| 快速搜索 | 1-2个 | 3-5分钟 | 来源可信赖、信息一致 | 通用概念、基础原理 |
| 标准搜索 | 3-5个 | 8-10分钟 | 至少2个来源一致、有时间标注 | 技术方案、数据分析 |
| 深度搜索 | 6-10个 | 15-20分钟 | 至少3个来源交叉验证、研究方法透明 | 核心技术、创新方案 |
| 广泛搜索 | 10-15个 | 30-40分钟 | 至少5个来源、多重验证、权威背书 | 前沿技术、学术级研究 |

### Q3: 可以跳过章节确认吗？

A: 不可以。严格确认模式是本skill的核心特性，每章必须用户确认后才能继续下一章。这是确保报告质量的关键机制。

### Q4: 如何修改已确认的章节？

A: 如果需要修改已确认的章节，请：
1. 明确说明需要修改的内容
2. skill会重新生成该章节
3. 您需要再次确认修改后的内容
4. 可以多次修改，直到满意为止

### Q5: 图表会自动插入到Word文档中吗？

A: 是的。skill会使用/docx skill生成Word文档，所有图表都会按照正确的格式和位置插入到文档中。

### Q6: skill支持哪些图表类型？

A: skill支持以下图表类型：
- 流程图（Mermaid）
- 柱状图（Python Matplotlib）
- 折线图（Python Matplotlib）
- 饼图（Python Matplotlib）
- 表格（Markdown）

### Q7: 可以在编写过程中添加或删除章节吗？

A: 可以。您可以在任何时候提出添加或删除章节的建议：
```
建议添加：第X章 [章节标题]
建议删除：第X章
原因：[说明原因]
```
skill会根据您的建议调整章节结构。

### Q8: skill会记住我的写作风格偏好吗？

A: 是的。skill具有自动迭代系统，会记录：
- 写作风格偏好（正式/简洁/详实/图文并茂）
- 术语使用偏好
- 图表偏好
- 资料搜集深度偏好

这些偏好会累积在 iteration/ 目录中，并在后续报告中自动应用。

### Q9: 报告完成后可以修改吗？

A: 报告完成后，skill会生成Word文档。您可以在Word中打开文档进行后续修改。如果需要skill重新生成整个报告或某些章节，可以重新启动skill并说明需求。

### Q10: skill支持多语言吗？

A: 当前版本主要支持中文报告生成。如果需要英文报告，可以在大纲中指定章节标题为英文，skill会尝试生成英文内容，但质量可能不如中文报告理想。

### Q11: 如何确保数据真实性？

A: skill采用多级验证机制：
1. **来源验证**：优先使用国家标准、行业标准、权威机构报告
2. **交叉引用**：至少2个来源的数据才会采用
3. **事实检查**：对关键数据进行多方验证
4. **不编造原则**：所有数据必须来源于可靠资料，绝不编造

### Q12: 可以指定引用格式吗？

A: 当前版本使用非正式引用格式，如：
- "根据《XXX报告》..."
- "YYY标准（2023版）要求..."

如果需要更正式的引用格式（如APA、GB/T 7714），可以在使用说明中指定，skill会尝试调整。

### Q13: skill会保存我的使用记录吗？

A: 是的。skill会自动记录：
- 使用日志（iteration/usage-log.md）：记录报告基本信息、章节明细、图表使用、个性化偏好
- 反馈日志（iteration/feedback-log.md）：记录章节反馈、整体反馈、改进建议

这些记录用于分析使用模式、识别用户偏好、生成改进建议。

### Q14: 如何清理skill生成的缓存？

A: skill生成的缓存保存在 iteration/cache/ 目录中。您可以：
1. 手动删除 iteration/cache/ 目录
2. 使用 cache_manager.py 脚本清理：
   ```bash
   python3 scripts/cache_manager.py --cleanup --days 30
   ```

### Q15: skill的迭代系统如何工作？

A: 迭代系统工作流程：
1. **收集反馈**：每次使用后记录用户反馈和使用记录
2. **分析模式**：定期分析反馈，识别用户偏好和常见问题
3. **生成建议**：基于分析结果生成改进建议
4. **用户确认**：所有更新建议需要用户批准后才应用
5. **共享资源**：优秀模式会提取到共享资源库，供其他用户使用

详细说明见 SKILL.md 中的"自动迭代系统"章节。

### Q16: skill的脚本如何使用？

A: skill提供了三个辅助脚本，使用方法如下：

**generate_chart.py - 图表生成**
```bash
python3 scripts/generate_chart.py --type bar --data data.csv --output chart.png
python3 scripts/generate_chart.py --type line --data data.csv --output trend.png
python3 scripts/generate_chart.py --type pie --data data.csv --output pie.png
python3 scripts/generate_chart.py --type flowchart --input flowchart.mmd --output flowchart.png
```

**cache_manager.py - 缓存管理**
```bash
python3 scripts/cache_manager.py --query "生态修复规范"
python3 scripts/cache_manager.py --add --name "GB/T 31084-2014" --file standard.txt --tags "风电,标准"
python3 scripts/cache_manager.py --list --category engineering-standards
python3 scripts/cache_manager.py --cleanup --days 30
```

**analyze_usage.py - 使用分析**
```bash
python3 scripts/analyze_usage.py --usage-log iteration/usage-log.md --report usage_report.txt
python3 scripts/analyze_usage.py --feedback-log iteration/feedback-log.md --report feedback_report.txt
```

详细使用说明见 scripts/README.md。

### Q17: skill对参考文档有什么要求？

A: 参考文档可以是以下格式：
- Word文档（.docx）
- PDF文档（.pdf）
- Markdown文档（.md）
- 纯文本文档（.txt）

参考文档应包含：
- 技术规范和标准
- 工程数据和参数
- 案例资料和实例
- 研究报告和论文
- 政策文件和导则

skill会自动读取和分析这些文档，提取关键信息。

### Q18: 大纲有什么格式要求？

A: 大纲可以是以下格式：
- Markdown文档（.md）
- Word文档（.docx）
- 纯文本输入

大纲应包含：
- 章节标题（一级标题，如：第1章 XXX）
- 节标题（二级标题，如：1.1 XXX）
- 可选的小节标题（三级标题，如：1.1.1 XXX）

skill会解析大纲结构，但**仅使用章节结构**，忽略格式样式。

### Q19: skill对输出文件路径有什么要求？

A: 输出文件路径可以是：
- 绝对路径（如：F:/output/报告.docx）
- 相对路径（如：output/报告.docx）

skill会：
1. 检查路径是否存在
2. 如果不存在，会询问是否创建
3. 自动生成文件名（如：[报告标题].docx）
4. 保存Word文档到指定路径

### Q20: skill生成的Word文档可以直接使用吗？

A: 是的。skill生成的Word文档：
- 使用标准样式（标题、正文、页眉页脚）
- 包含完整的文档结构
- 图表正确插入
- 格式规范、可直接打印或提交

如果需要进一步调整，可以在Word中打开文档进行编辑。

## 技术支持

如果您在使用过程中遇到问题，请：
1. 查阅本文档的FAQ部分
2. 查阅 SKILL.md 的详细说明
3. 查看 scripts/README.md 了解脚本使用
4. 查看 iteration/ 目录了解迭代系统

---

**更新日期**: 2026-01-30
**版本**: v1.0
