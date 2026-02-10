#!/usr/bin/env python3
"""
AI Outline Generator for Report Generator

Generates report outlines using AI with interactive modes, template matching,
and intelligent recommendations. Supports multiple generation modes and fallback mechanisms.

Usage:
    python generate_outline.py --help
    python generate_outline.py --input "风电场地质调查报告" --mode quick --output outline.md
    python generate_outline.py --input "风电项目" --mode chapter --template geological --output outline.md
    python generate_outline.py --input "风电项目" --mode keypoints --reference reference.md --output outline.md
"""

import sys
import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class OutlineGenerator:
    """AI驱动的报告大纲生成器"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.templates_dir = Path("iteration/outline-templates")
        self.outline_templates_file = self.templates_dir / "standard-outline-templates.md"
        self.industry_templates_dir = self.templates_dir / "industry-outlines"
        self.template_index_file = self.templates_dir / "index.md"
        self.history_dir = Path("iteration/outline-history")
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
        self.templates = {}
        self.industry_templates = {}
        self.template_index = {}
        
        # 加载模板
        self._load_templates()
        self._load_template_index()
    
    def log(self, message: str, level: str = "INFO"):
        """打印日志信息"""
        if self.verbose or level in ["ERROR", "WARNING"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")
    
    def _load_templates(self):
        """加载所有大纲模板"""
        self.log("正在加载大纲模板...")
        
        # 加载标准模板
        if self.outline_templates_file.exists():
            self._parse_standard_templates()
        else:
            self.log(f"标准模板文件不存在: {self.outline_templates_file}", "WARNING")
        
        # 加载行业模板
        if self.industry_templates_dir.exists():
            self._load_industry_templates()
        else:
            self.log(f"行业模板目录不存在: {self.industry_templates_dir}", "WARNING")
        
        self.log(f"加载完成：标准模板 {len(self.templates)} 个，行业模板 {len(self.industry_templates)} 个")
    
    def _parse_standard_templates(self):
        """解析标准大纲模板"""
        try:
            content = self.outline_templates_file.read_text(encoding='utf-8')
            self._extract_templates_from_content(content, "standard")
        except Exception as e:
            self.log(f"解析标准模板失败: {e}", "ERROR")
    
    def _load_industry_templates(self):
        """加载行业模板"""
        for template_file in self.industry_templates_dir.glob("*.md"):
            try:
                content = template_file.read_text(encoding='utf-8')
                self._extract_templates_from_template_file(template_file, content)
            except Exception as e:
                self.log(f"加载模板 {template_file.name} 失败: {e}", "ERROR")
    
    def _extract_templates_from_content(self, content: str, category: str):
        """从内容中提取模板"""
        # 提取模板ID和名称
        template_pattern = r'### 模板(\d+?)：([^\n]+)'
        for match in re.finditer(template_pattern, content):
            template_id = match.group(1)
            template_name = match.group(2).strip()
            
            # 提取模板结构
            start_pos = match.start()
            next_match = re.search(template_pattern, content[start_pos + 10:])
            end_pos = next_match.start() if next_match else len(content)
            
            structure_content = content[start_pos:end_pos]
            
            self.templates[template_id] = {
                'id': template_id,
                'name': template_name,
                'category': category,
                'content': structure_content
            }
    
    def _extract_templates_from_template_file(self, template_file: Path, content: str):
        """从模板文件中提取模板"""
        template_id_match = re.search(r'- 模板ID:\s*(OT\d{3})', content)
        if not template_id_match:
            self.log(f"无法提取模板ID: {template_file.name}", "WARNING")
            return
        
        template_id = template_id_match.group(1)
        
        # 提取模板名称（从标题行）
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        template_name = title_match.group(1).strip() if title_match else template_file.stem
        
        # 提取适用场景
        scenario_match = re.search(r'适用场景[:：]\s*(.+?)(\n|$)', content)
        scenario = scenario_match.group(1).strip() if scenario_match else ""
        
        # 提取章节结构
        chapter_pattern = r'### 第(\d+)章\s+([^\n]+)'
        chapters = []
        for match in re.finditer(chapter_pattern, content):
            chapter_num = match.group(1)
            chapter_title = match.group(2).strip()
            
            # 提取小节
            section_pattern = r'###?\s+([\d+\.?\d*?)\s+([^\n]+)'
            start_pos = match.end()
            
            sections = []
            for section_match in re.finditer(section_pattern, content[start_pos:]):
                section_num = section_match.group(1)
                section_title = section_match.group(2).strip()
                sections.append({
                    'num': section_num,
                    'title': section_title
                })
            
            chapters.append({
                'num': chapter_num,
                'title': chapter_title,
                'sections': sections
            })
        
        self.industry_templates[template_id] = {
            'id': template_id,
            'name': template_name,
            'scenario': scenario,
            'chapters': chapters
        }
        
        self.log(f"加载行业模板: {template_id} - {template_name} ({len(chapters)} 章)")
    
    def _load_template_index(self):
        """加载模板索引"""
        if not self.template_index_file.exists():
            self.log("模板索引文件不存在，跳过", "WARNING")
            return
        
        try:
            content = self.template_index_file.read_text(encoding='utf-8')
            # 简单解析，提取模板ID和链接
            self.log("模板索引加载成功")
        except Exception as e:
            self.log(f"加载模板索引失败: {e}", "ERROR")
    
    def generate_outline(
        self, 
        project_input: str,
        mode: str = "quick",
        template_id: Optional[str] = None,
        reference_docs: List[str] = None
    ) -> Dict:
        """
        生成报告大纲
        
        Args:
            project_input: 项目主题/关键词
            mode: 交互模式（quick/chapter/keypoints）
            template_id: 指定模板ID（可选）
            reference_docs: 参考文档路径列表（可选）
        
        Returns:
            大纲结构字典
        """
        self.log(f"开始生成大纲: {project_input}")
        self.log(f"交互模式: {mode}")
        self.log(f"指定模板: {template_id if template_id else '自动选择'}")
        
        outline = {
            'title': self._extract_title(project_input),
            'chapters': [],
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'generation_mode': mode,
                'template_used': template_id or 'auto',
                'reference_docs': reference_docs or []
            }
        }
        
        # 根据模式选择生成策略
        if mode == "quick":
            outline = self._generate_quick_outline(project_input, template_id, outline)
        elif mode == "chapter":
            outline = self._generate_chapter_by_chapter_outline(project_input, template_id, outline)
        elif mode == "keypoints":
            outline = self._generate_keypoints_outline(project_input, template_id, outline)
        else:
            self.log(f"不支持的交互模式: {mode}", "ERROR")
            raise ValueError(f"不支持的交互模式: {mode}")
        
        self.log(f"大纲生成完成，共 {len(outline['chapters'])} 个章节")
        return outline
    
    def _extract_title(self, project_input: str) -> str:
        """从输入中提取报告标题"""
        # 移除多余字符，保留关键词
        keywords = project_input.replace('报告', '').replace('方案', '').strip()
        return f"{keywords}报告"
    
    def _generate_quick_outline(
        self,
        project_input: str,
        template_id: Optional[str],
        outline: Dict
    ) -> Dict:
        """快速生成模式：直接生成完整大纲"""
        self.log("执行快速生成模式")
        
        # 智能选择模板
        if not template_id:
            template_id = self._recommend_template(project_input)
            self.log(f"自动选择模板: {template_id}")
        
        # 加载模板结构
        template = self._get_template(template_id)
        if not template:
            self.log(f"未找到模板: {template_id}，使用默认模板", "WARNING")
            template_id = "OT002"  # 默认使用标准版
            template = self._get_template(template_id)
        
        # 根据模板生成章节
        chapters = self._adapt_template_to_project(template, project_input)
        outline['chapters'] = chapters
        
        # 生成增强建议
        outline['recommendations'] = self._generate_recommendations(project_input, template_id, outline)
        
        return outline
    
    def _generate_chapter_by_chapter_outline(
        self,
        project_input: str,
        template_id: Optional[str],
        outline: Dict
    ) -> Dict:
        """逐章引导模式：逐步生成每个章节"""
        self.log("执行逐章引导模式")
        
        # 暂时简化实现：使用快速生成模式
        # 实际应用中应该有交互式引导
        return self._generate_quick_outline(project_input, template_id, outline)
    
    def _generate_keypoints_outline(
        self,
        project_input: str,
        template_id: Optional[str],
        outline: Dict
    ) -> Dict:
        """要点扩展模式：基于关键词扩展大纲"""
        self.log("执行要点扩展模式")
        
        # 暂时简化实现：使用快速生成模式
        return self._generate_quick_outline(project_input, template_id, outline)
    
    def _recommend_template(self, project_input: str) -> str:
        """智能推荐模板"""
        self.log(f"分析项目输入: {project_input}")
        
        keywords = project_input.lower()
        scores = {}
        
        # 基于关键词评分
        if "地质" in keywords:
            scores["OT101"] = scores.get("OT101", 0) + 10
            scores["OT002"] = scores.get("OT002", 0) + 5
            scores["OT003"] = scores.get("OT003", 0) + 7
        if "设计" in keywords or "方案" in keywords:
            scores["OT002"] = scores.get("OT002", 0) + 10
            scores["OT004"] = scores.get("OT004", 0) + 8
            scores["OT005"] = scores.get("OT005", 0) + 9
        if "环境" in keywords or "评估" in keywords:
            scores["OT103"] = scores.get("OT103", 0) + 10
            scores["OT002"] = scores.get("OT002", 0) + 6
            scores["OT004"] = scores.get("OT004", 0) + 7
        if "快速" in keywords or "简" in keywords:
            scores["OT001"] = scores.get("OT001", 0) + 10
        
        # 如果没有匹配，返回默认模板
        if not scores:
            self.log("无关键词匹配，使用默认模板 OT002", "WARNING")
            return "OT002"
        
        # 选择得分最高的模板
        recommended = max(scores.items(), key=lambda x: x[1])[0]
        self.log(f"推荐模板: {recommended} (得分: {scores[recommended]})")
        
        return recommended
    
    def _get_template(self, template_id: str) -> Optional[Dict]:
        """获取指定模板"""
        # 先在标准模板中查找
        if template_id in self.templates:
            return self.templates[template_id]
        
        # 在行业模板中查找
        if template_id in self.industry_templates:
            return self.industry_templates[template_id]
        
        return None
    
    def _adapt_template_to_project(
        self,
        template: Dict,
        project_input: str
    ) -> List[Dict]:
        """根据项目特点调整模板"""
        self.log(f"调整模板以匹配项目: {project_input}")
        
        # 如果是行业模板，返回其章节
        if template['category'] == 'industry':
            chapters = []
            for chapter in template['chapters']:
                chapters.append({
                    'num': chapter['num'],
                    'title': chapter['title'],
                    'sections': [
                        {'num': f"{chapter['num']}.{i+1}",
                         'title': section['title']}
                        for i, section in enumerate(chapter['sections'])
                    ]
                })
            return chapters
        
        # 如果是标准模板，需要调整章节标题
        # 简化实现：直接返回模板章节的简化版本
        return self._simplify_template_structure(template['content'])
    
    def _simplify_template_structure(self, template_content: str) -> List[Dict]:
        """简化模板结构为章节列表"""
        chapters = []
        chapter_pattern = r'### 第(\d+)章\s+([^\n]+)'
        
        for match in re.finditer(chapter_pattern, template_content):
            chapter_num = match.group(1)
            chapter_title = match.group(2).strip()
            
            # 提取小节
            start_pos = match.end()
            next_chapter = re.search(r'### 第\d+章', template_content[start_pos:])
            end_pos = next_chapter.start() if next_chapter else len(template_content)
            chapter_content = template_content[start_pos:end_pos]
            
            sections = []
            section_pattern = r'###?\s+([\d+\.?\d*?)\s+([^\n]+)'
            for section_match in re.finditer(section_pattern, chapter_content):
                section_title = section_match.group(2).strip()
                sections.append({
                    'num': section_match.group(1),
                    'title': section_title
                })
            
            chapters.append({
                'num': chapter_num,
                'title': chapter_title,
                'sections': sections
            })
        
        return chapters
    
    def _generate_recommendations(
        self,
        project_input: str,
        template_id: str,
        outline: Dict
    ) -> Dict:
        """生成增强建议"""
        recommendations = {
            'chapter_count': self._recommend_chapter_count(project_input),
            'chapter_order': self._recommend_chapter_order(template_id),
            'chart_suggestions': self._recommend_charts(template_id),
            'writing_direction': self._recommend_writing_direction(project_input)
        }
        
        self.log("生成增强建议完成")
        return recommendations
    
    def _recommend_chapter_count(self, project_input: str) -> str:
        """推荐章节数量"""
        keywords = project_input.lower()
        
        if "快速" in keywords or "简" in keywords:
            return "3-4章（精简版）"
        elif "详细" in keywords or "深度" in keywords:
            return "7-9章（详细版）"
        else:
            return "5-6章（标准版）"
    
    def _recommend_chapter_order(self, template_id: str) -> List[str]:
        """推荐章节顺序"""
        # 简化实现：返回通用建议
        return [
            "1. 从背景介绍开始",
            "2. 然后是技术方案",
            "3. 接着是实施细节",
            "4. 最后是结论与建议"
        ]
    
    def _recommend_charts(self, template_id: str) -> Dict:
        """推荐配图"""
        # 根据模板类型推荐
        chart_recommendations = []
        
        if template_id == "OT101":  # 地质调查报告
            chart_recommendations = [
                "第2章 地质概况 → 地层柱状图、剖面图",
                "第3章 工程地质条件 → 工程地质分区图",
                "第5章 勘查方法与技术 → 调查技术流程图"
            ]
        elif template_id in ["OT002", "OT004", "OT005"]:  # 技术方案/设计/实施
            chart_recommendations = [
                "第2章 技术方案 → 技术路线图、架构图",
                "第3章 设计方案 → 平面布置图、效果图",
                "第4章 实施组织 → 进度甘特图、施工流程图"
            ]
        
        return {'recommendations': chart_recommendations}
    
    def _recommend_writing_direction(self, project_input: str) -> Dict:
        """推荐写作方向"""
        keywords = project_input.lower()
        
        writing_direction = {
            'content_focus': '技术方案',
            'technical_depth': '综合分析',
            'narrative_style': '客观描述',
            'reader_perspective': '技术人员视角',
            'recommendation_reason': '基于项目关键词分析'
        }
        
        if "可行性" in keywords or "评估" in keywords:
            writing_direction['content_focus'] = '对比分析'
            writing_direction['technical_depth'] = '简明概述'
            writing_direction['narrative_style'] = '客观描述'
            writing_direction['reader_perspective'] = '决策者视角'
        elif "技术" in keywords or "方案" in keywords:
            writing_direction['content_focus'] = '技术方案'
            writing_direction['technical_depth'] = '原理讲解'
            writing_direction['narrative_style'] = '数据支撑'
            writing_direction['reader_perspective'] = '技术人员视角'
        elif "实施" in keywords or "组织" in keywords:
            writing_direction['content_focus'] = '实施细节'
            writing_direction['technical_depth'] = '实践指导'
            writing_direction['narrative_style'] = '流程导向'
            writing_direction['reader_perspective'] = '管理者视角'
        
        return writing_direction
    
    def format_as_markdown(self, outline: Dict) -> str:
        """将大纲格式化为 Markdown"""
        self.log("格式化大纲为 Markdown...")
        
        lines = []
        lines.append(f"# {outline['title']}\n")
        
        # 添加元数据
        lines.append("## 元数据\n")
        lines.append(f"- 生成时间：{outline['metadata']['generated_at']}")
        lines.append(f"- 生成模式：{outline['metadata']['generation_mode']}")
        lines.append(f"- 使用模板：{outline['metadata']['template_used']}")
        lines.append(f"\n")
        
        # 添加章节
        for chapter in outline['chapters']:
            lines.append(f"### 第{chapter['num']}章 {chapter['title']}\n")
            
            for section in chapter['sections']:
                lines.append(f"#### {section['num']} {section['title']}\n")
        
        # 添加推荐建议
        if 'recommendations' in outline:
            lines.append("\n## 增强建议\n")
            recs = outline['recommendations']
            
            lines.append(f"### 章节数量建议\n")
            lines.append(f"{recs['chapter_count']}\n")
            
            lines.append(f"### 章节顺序建议\n")
            for order in recs['chapter_order']:
                lines.append(f"- {order}\n")
            
            lines.append(f"### 配图建议\n")
            for chart in recs['chart_suggestions']['recommendations']:
                lines.append(f"- {chart}\n")
            
            lines.append(f"### 写作方向推荐\n")
            wd = recs['writing_direction']
            lines.append(f"- **内容侧重**：{wd['content_focus']}")
            lines.append(f"- **技术深度**：{wd['technical_depth']}")
            lines.append(f"- **叙述风格**：{wd['narrative_style']}")
            lines.append(f"- **读者视角**：{wd['reader_perspective']}")
            lines.append(f"- **推荐理由**：{wd['recommendation_reason']}\n")
        
        return '\n'.join(lines)
    
    def save_to_history(self, outline: Dict, output_path: str):
        """保存大纲到历史记录"""
        try:
            # 生成唯一文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            history_filename = f"outline_{timestamp}.json"
            history_path = self.history_dir / history_filename
            
            # 保存为 JSON
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(outline, f, ensure_ascii=False, indent=2)
            
            self.log(f"大纲已保存到历史记录: {history_path}")
            
        except Exception as e:
            self.log(f"保存历史记录失败: {e}", "ERROR")


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='AI驱动的交互式大纲生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=''
    )
    
    parser.add_argument('-i', '--input', required=True,
                        help='项目主题描述或项目名称（必需）')
    parser.add_argument('-m', '--mode', default='quick',
                        choices=['quick', 'chapter', 'keypoints'],
                        help='交互模式：quick（快速生成）、chapter（逐章引导）、keypoints（要点扩展）')
    parser.add_argument('-o', '--output', default='outline-generated.md',
                        help='输出文件路径（默认：outline-generated.md）')
    parser.add_argument('-t', '--template',
                        help='指定模板ID（如 OT002、OT101 等），留空则自动选择')
    parser.add_argument('-r', '--reference', nargs='+', default=[],
                        help='参考文档路径（可多个）')
    parser.add_argument('--verbose', action='store_true',
                        help='显示详细输出')
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()
    
    # 初始化生成器
    generator = OutlineGenerator(verbose=args.verbose)
    
    # 生成大纲
    try:
        outline = generator.generate_outline(
            project_input=args.input,
            mode=args.mode,
            template_id=args.template,
            reference_docs=args.reference
        )
        
        # 格式化为 Markdown
        markdown_content = generator.format_as_markdown(outline)
        
        # 保存到输出文件
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"\n✅ 大纲已成功生成！")
        print(f"\n📄 输出文件：{output_path.absolute()}")
        
        # 保存到历史记录
        generator.save_to_history(outline, str(output_path))
        
        # 显示统计信息
        print(f"\n📊 统计信息：")
        print(f"   - 章节数量：{len(outline['chapters'])}")
        print(f"   - 总小节数：{sum(len(c['sections']) for c in outline['chapters'])}")
        print(f"   - 使用模板：{outline['metadata']['template_used']}")
        print(f"   - 生成模式：{outline['metadata']['generation_mode']}")
        
        # 显示增强建议
        if 'recommendations' in outline:
            print(f"\n💡 增强建议：")
            recs = outline['recommendations']
            print(f"   • 建议章节数量：{recs['chapter_count']}")
            if recs['chart_suggestions']['recommendations']:
                print(f"   • 建议配图：{len(recs['chart_suggestions']['recommendations'])} 处")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断，程序退出")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 生成失败：{e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
