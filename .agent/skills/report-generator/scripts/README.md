# Scripts Directory

本目录包含 `report-generator` skill 的辅助工具脚本。

## 脚本列表

### generate_chart.py

**功能**：图表生成脚本

**支持的图表类型**：
- 柱状图（Bar Chart）- 使用 Python Matplotlib
- 折线图（Line Chart）- 使用 Python Matplotlib
- 饼图（Pie Chart）- 使用 Python Matplotlib
- 流程图（Flowchart）- 使用 Mermaid

**依赖**：
- Python 3.6+
- matplotlib（可选，用于柱状图、折线图、饼图）
- pandas（可选，用于读取CSV数据）

**使用示例**：
```bash
# 生成柱状图
python3 scripts/generate_chart.py --type bar --data data.csv --output chart.png --title "对比" --xlabel "类型" --ylabel "数值"

# 生成折线图
python3 scripts/generate_chart.py --type line --data data.csv --output trend.png --title "趋势" --xlabel "时间" --ylabel "数值"

# 生成饼图
python3 scripts/generate_chart.py --type pie --data data.csv --output pie.png --title "构成"

# 生成流程图
python3 scripts/generate_chart.py --type flowchart --input flowchart.mmd --output flowchart.png
```

**输出**：
- PNG格式图片（DPI=300）
- Mermaid文件（.mmd格式，用于流程图）

---

### cache_manager.py

**功能**：资料缓存管理脚本

**支持的操作**：
- 查询缓存（query）- 按关键词搜索缓存
- 添加缓存（add）- 添加新的缓存条目
- 列表显示（list）- 列出缓存条目
- 更新缓存（update）- 更新现有缓存
- 删除缓存（delete）- 删除指定缓存
- 清理过期（cleanup）- 清理过期缓存

**依赖**：
- Python 3.6+
- 无外部依赖（仅使用标准库）

**使用示例**：
```bash
# 查询缓存
python3 scripts/cache_manager.py --query "生态修复规范"

# 添加缓存
python3 scripts/cache_manager.py --add --name "GB/T 31084-2014" --content "..." --category engineering-standards --tags "风电,标准"

# 列出所有缓存
python3 scripts/cache_manager.py --list

# 列出指定类别的缓存
python3 scripts/cache_manager.py --list --category engineering-standards

# 清理30天前的过期缓存
python3 scripts/cache_manager.py --cleanup --days 30
```

**缓存结构**：
- `cache_index.json` - 缓存索引文件
- 分类存储：engineering-standards/, technical-standards/, industry-data/, case-studies/

---

### analyze_usage.py

**功能**：使用分析脚本

**支持的分析类型**：
- 使用日志分析（usage-log）- 分析报告生成情况
- 反馈日志分析（feedback-log）- 分析用户反馈
- 全面分析（all）- 分析所有迭代数据

**依赖**：
- Python 3.6+
- 无外部依赖（仅使用标准库）

**使用示例**：
```bash
# 分析使用日志
python3 scripts/analyze_usage.py --usage-log iteration/usage-log.md --report usage_report.txt

# 分析反馈日志
python3 scripts/analyze_usage.py --feedback-log iteration/feedback-log.md --report feedback_report.txt

# 全面分析
python3 scripts/analyze_usage.py --all --iteration-path iteration/ --report comprehensive_report.txt
```

**输出**：
- Markdown格式分析报告
- 包含统计数据、分析结论、改进建议

## 使用说明

### 依赖安装

如果需要使用 Matplotlib 图表生成功能，请先安装依赖：
```bash
pip install matplotlib pandas
```

### 运行脚本

所有脚本都支持 `--help` 参数查看详细使用说明：
```bash
python3 scripts/generate_chart.py --help
python3 scripts/cache_manager.py --help
python3 scripts/analyze_usage.py --help
```

### 路径说明

- 脚本应从 `report-generator/` 目录运行
- 使用相对路径访问 iteration/ 子目录
- 输出文件可指定绝对路径或相对路径

## 注意事项

1. **数据格式**：CSV文件应使用逗号分隔，第一列为标签/类别
2. **Mermaid语法**：确保Mermaid代码语法正确
3. **缓存管理**：定期清理过期缓存，避免占用过多空间
4. **Python环境**：确保使用Python 3.6或更高版本

## 故障排除

### 常见问题

**问题**：`ModuleNotFoundError: No module named 'matplotlib'`
**解决**：`pip install matplotlib pandas`

**问题**：`FileNotFoundError: data.csv not found`
**解决**：检查文件路径是否正确，文件是否存在

**问题**：`Error parsing CSV file`
**解决**：检查CSV文件格式，确保使用UTF-8编码

## 贡献指南

如需添加新功能或修复bug：
1. 保持脚本向后兼容
2. 添加清晰的错误处理
3. 更新本README文档
4. 遵循PEP 8编码规范
5. 添加必要的注释和文档字符串

## 许可证

本脚本随 `report-generator` skill 一起分发，遵循 skill 的许可证协议。

更新日期：2026-01-30
