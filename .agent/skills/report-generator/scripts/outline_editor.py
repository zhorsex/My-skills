#!/usr/bin/env python3
"""
Outline Editor - 大纲文本编辑器

Provides text-based editing capabilities for outline files generated
by generate_outline.py. Supports add/remove/move/adjust level operations.

Usage:
    python outline_editor.py --help
    python outline_editor.py --input outline.md --output outline-edited.md
    python outline_editor.py --input outline.md --mode interactive
    python outline_editor.py --add-chapter "项目投资估算" --after 3 --input outline.md --output outline.md
"""

import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class OutlineEditor:
    """大纲文本编辑器"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.outline_pattern = r'### 第(\d+)章\s+([^\n]+)'
        self.section_pattern = r'#### ([\d\.?\d*?)\s+[^\n]+'
    
    def log(self, message: str, level: str = "INFO"):
        """打印日志信息"""
        if self.verbose or level in ["ERROR", "WARNING"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")
    
    def load_outline(self, file_path: str) -> str:
        """加载大纲文件"""
        try:
            path = Path(file_path)
            content = path.read_text(encoding='utf-8')
            self.log(f"大纲文件加载成功: {file_path}")
            return content
        except FileNotFoundError:
            self.log(f"文件不存在: {file_path}", "ERROR")
            raise
        except Exception as e:
            self.log(f"加载文件失败: {e}", "ERROR")
            raise
    
    def save_outline(self, content: str, file_path: str):
        """保存大纲文件"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            self.log(f"大纲文件保存成功: {file_path}")
        except Exception as e:
            self.log(f"保存文件失败: {e}", "ERROR")
            raise
    
    def parse_outline(self, content: str) -> Dict:
        """解析大纲内容为结构化数据"""
        chapters = []
        
        # 提取标题
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "未命名大纲"
        
        # 提取章节
        chapter_matches = list(re.finditer(self.outline_pattern, content))
        
        for i, match in enumerate(chapter_matches):
            chapter_num = match.group(1)
            chapter_title = match.group(2).strip()
            
            # 查找小节（在当前章到下一章之间）
            start_pos = match.end()
            end_pos = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(content)
            chapter_content = content[start_pos:end_pos]
            
            # 提取小节
            sections = []
            for section_match in re.finditer(self.section_pattern, chapter_content):
                section_num = section_match.group(1)
                section_title = section_match.group(2).strip()
                sections.append({
                    'num': section_num,
                    'title': section_title,
                    'line_start': section_match.start()
                })
            
            chapters.append({
                'num': chapter_num,
                'title': chapter_title,
                'sections': sections,
                'line_start': match.start(),
                'line_end': end_pos
            })
        
        # 提取元数据部分（如果存在）
        metadata_section = self._extract_metadata(content)
        
        return {
            'title': title,
            'chapters': chapters,
            'metadata': metadata_section
        }
    
    def _extract_metadata(self, content: str) -> Dict:
        """提取元数据部分"""
        # 查找元数据章节（通常在开头的 ## 元数据）
        metadata_match = re.search(r'## 元数据\s*\n(.*?)(?=###\s第|\Z)', content, re.DOTALL)
        if metadata_match:
            metadata_content = metadata_match.group(1)
            lines = metadata_content.split('\n')
            metadata = {}
            for line in lines:
                line = line.strip()
                if line.startswith('-'):
                    parts = line[1:].split('：')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        metadata[key] = value
            return metadata
        return {}
    
    def add_chapter(
        self,
        content: str,
        chapter_title: str,
        after_chapter: Optional[int] = None,
        before_chapter: Optional[int] = None
    ) -> str:
        """添加章节"""
        self.log(f"添加章节: {chapter_title}")
        
        # 查找插入位置
        insert_pos = self._find_insert_position(content, after_chapter, before_chapter)
        if insert_pos is None:
            # 没有找到插入位置，添加到最后
            insert_pos = len(content)
        
        # 生成新章节内容
        new_chapter = f"### 第{self._get_next_chapter_number(content)}章 {chapter_title}\n\n"
        
        # 插入新章节
        new_content = content[:insert_pos] + new_chapter + content[insert_pos:]
        
        self.log(f"章节添加成功")
        return new_content
    
    def _get_next_chapter_number(self, content: str) -> str:
        """获取下一个章节编号"""
        chapter_nums = re.findall(r'### 第(\d+)章', content)
        if not chapter_nums:
            return "1"
        max_num = max(int(num) for num in chapter_nums)
        return str(max_num + 1)
    
    def _find_insert_position(
        self,
        content: str,
        after_chapter: Optional[int],
        before_chapter: Optional[int]
    ) -> Optional[int]:
        """查找插入位置"""
        chapters = list(re.finditer(self.outline_pattern, content))
        
        if after_chapter is not None:
            # 在指定章节之后插入
            for match in chapters:
                if int(match.group(1)) == after_chapter:
                    return match.end()
        elif before_chapter is not None:
            # 在指定章节之前插入
            for match in chapters:
                if int(match.group(1)) == before_chapter:
                    return match.start()
        
        # 没有找到匹配的位置
        return None
    
    def remove_chapter(self, content: str, chapter_num: int) -> str:
        """删除章节"""
        self.log(f"删除章节: 第{chapter_num}章")
        
        # 查找章节
        pattern = rf'### 第{re.escape(str(chapter_num))}章\s+[^\n]+\n(?:\s*####[^\n]+\n)*'
        new_content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # 检查是否删除成功
        if '### 第{}章'.format(chapter_num) in new_content:
            self.log(f"删除章节失败: 未找到第{chapter_num}章", "WARNING")
        else:
            self.log(f"章节删除成功")
        
        return new_content
    
    def rename_chapter(self, content: str, chapter_num: int, new_title: str) -> str:
        """重命名章节"""
        self.log(f"重命名章节: 第{chapter_num}章 -> {new_title}")
        
        pattern = rf'(### 第{re.escape(str(chapter_num))}章)\s+[^\n]+'
        replacement = f'\\1 {new_title}'
        new_content = re.sub(pattern, replacement, content)
        
        if new_content == content:
            self.log(f"重命名章节失败: 未找到第{chapter_num}章", "WARNING")
        else:
            self.log(f"章节重命名成功")
        
        return new_content
    
    def move_chapter(
        self,
        content: str,
        chapter_num: int,
        after_chapter: Optional[int] = None,
        before_chapter: Optional[int] = None
    ) -> str:
        """移动章节"""
        self.log(f"移动章节: 第{chapter_num}章")
        
        # 先删除章节
        content_without_chapter = self.remove_chapter(content, chapter_num)
        
        # 获取被删除章节的内容（需要重新提取）
        original_match = re.search(
            rf'(### 第{re.escape(str(chapter_num))}章\s+[^\n]+\n(?:\s*####[^\n]+\n)*)',
            content
        )
        
        if not original_match:
            self.log(f"移动章节失败: 未找到第{chapter_num}章", "ERROR")
            return content
        
        chapter_content = original_match.group(1)
        
        # 重新插入
        new_content = self._insert_chapter_at_position(
            content_without_chapter,
            chapter_content,
            after_chapter,
            before_chapter
        )
        
        self.log(f"章节移动成功")
        return new_content
    
    def _insert_chapter_at_position(
        self,
        content: str,
        chapter_content: str,
        after_chapter: Optional[int],
        before_chapter: Optional[int]
    ) -> str:
        """在指定位置插入章节"""
        insert_pos = self._find_insert_position(content, after_chapter, before_chapter)
        if insert_pos is None:
            insert_pos = len(content)
        
        return content[:insert_pos] + chapter_content + "\n" + content[insert_pos:]
    
    def add_section(
        self,
        content: str,
        chapter_num: int,
        section_title: str
    ) -> str:
        """添加小节"""
        self.log(f"添加小节: {section_title} 到 第{chapter_num}章")
        
        # 查找章节位置
        pattern = rf'(### 第{re.escape(str(chapter_num))}章\s+[^\n]+\n)'
        match = re.search(pattern, content)
        
        if not match:
            self.log(f"添加小节失败: 未找到第{chapter_num}章", "ERROR")
            return content
        
        # 查找该章节中现有的小节编号
        chapter_start = match.start()
        # 查找该章节的结尾（下一个章节开始或文件结尾）
        next_chapter_match = re.search(r'### 第\d+章', content[chapter_start + 1:])
        chapter_end = next_chapter_match.start() + chapter_start + 1 if next_chapter_match else len(content)
        chapter_content = content[chapter_start:chapter_end]
        
        # 查找现有小节编号
        existing_sections = re.findall(r'#### ([\d\.?\d*?)\s+', chapter_content)
        if not existing_sections:
            new_section_num = f"{chapter_num}.1"
        else:
            last_num = existing_sections[-1]
            # 简单递增
            if '.' in last_num:
                prefix, suffix = last_num.rsplit('.', 1)
                new_suffix = int(suffix) + 1
                new_section_num = f"{prefix}.{new_suffix}"
            else:
                new_section_num = f"{last_num}.1"
        
        # 插入新小节（在章节标题后）
        insert_pos = match.end()
        new_section = f"#### {new_section_num} {section_title}\n"
        
        new_content = content[:insert_pos] + new_section + content[insert_pos:]
        
        self.log(f"小节添加成功")
        return new_content
    
    def remove_section(self, content: str, section_num: str) -> str:
        """删除小节"""
        self.log(f"删除小节: {section_num}")
        
        pattern = rf'#### {re.escape(section_num)}\s+[^\n]+\n'
        new_content = re.sub(pattern, '', content)
        
        if f'#### {section_num}' in new_content:
            self.log(f"删除小节失败: 未找到小节 {section_num}", "WARNING")
        else:
            self.log(f"小节删除成功")
        
        return new_content
    
    def renumber_chapters(self, content: str) -> str:
        """重新编号章节"""
        self.log("重新编号所有章节")
        
        lines = content.split('\n')
        chapter_counter = 1
        section_counters = {}
        
        new_lines = []
        for line in lines:
            # 匹配章节
            chapter_match = re.match(r'### 第(\d+)章\s+(.+)', line)
            if chapter_match:
                old_chapter = chapter_match.group(1)
                chapter_title = chapter_match.group(2).strip()
                new_lines.append(f'### 第{chapter_counter}章 {chapter_title}')
                section_counters[old_chapter] = chapter_counter
                chapter_counter += 1
            # 匹配小节
            elif line.strip().startswith('#### '):
                section_match = re.match(r'#### ([\d\.?\d*?)\s+(.+)', line)
                if section_match:
                    old_section_num = section_match.group(1)
                    section_title = section_match.group(2).strip()
                    # 提取章节编号
                    old_chapter = old_section_num.split('.')[0]
                    # 获取新章节编号
                    new_chapter = section_counters.get(old_chapter, 1)
                    # 提取小节编号并更新
                    if '.' in old_section_num:
                        old_subsection = old_section_num.split('.')[1]
                        new_subsection = int(old_subsection) + 1
                        new_section_num = f"{new_chapter}.{new_subsection}"
                    else:
                        new_section_num = f"{new_chapter}.1"
                    new_lines.append(f'#### {new_section_num} {section_title}')
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        self.log("重新编号完成")
        return new_content
    
    def adjust_chapter_level(
        self,
        content: str,
        chapter_num: int,
        target_level: str  # 'up' or 'down' or specific level like '1.1'
    ) -> str:
        """调整章节层级"""
        if target_level == 'up':
            # 将章升级为主标题
            pattern = rf'(### 第{re.escape(str(chapter_num))}章)\s+([^\n]+)'
            new_content = re.sub(pattern, r'## \1', content)
        elif target_level == 'down':
            # 将章降级为小节（简化实现）
            self.log("降级功能：章无法降级为小节", "WARNING")
            return content
        else:
            # 移动到指定层级（简化实现）
            self.log(f"调整层级到: {target_level}（功能简化）", "WARNING")
            return content
        
        self.log(f"章节层级调整完成")
        return new_content


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='大纲文本编辑器 - 添加/删除/重命名/移动章节',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
    Examples:
      # 交互模式
      outline_editor.py --input outline.md --mode interactive
      
      # 命令模式 - 添加章节
      outline_editor.py --add-chapter "项目投资估算" --after 3 --input outline.md --output outline-edited.md
      
      # 命令模式 - 删除章节
      outline_editor.py --remove-chapter 4 --input outline.md --output outline-edited.md
      
      # 命令模式 - 重命名章节
      outline_editor.py --rename-chapter 2 "技术方案" -> "设计方案" --input outline.md --output outline-edited.md
      
      # 命令模式 - 移动章节
      outline_editor.py --move-chapter 5 --after 3 --input outline.md --output outline-edited.md
    ''')
    
    # 必需参数
    parser.add_argument('-i', '--input', required=True,
                        help='输入大纲文件路径')
    parser.add_argument('-o', '--output',
                        help='输出大纲文件路径（默认覆盖输入文件）')
    
    # 操作参数
    parser.add_argument('--mode', choices=['interactive', 'command'],
                        default='interactive',
                        help='操作模式：interactive（交互式）或 command（命令式）')
    
    # 命令式操作参数
    parser.add_argument('--add-chapter', metavar='TITLE',
                        help='添加章节（标题）')
    parser.add_argument('--add-section', nargs=2, metavar=('CHAPTER_NUM', 'TITLE'),
                        help='添加小节（章节编号 标题）')
    parser.add_argument('--remove-chapter', type=int, metavar='NUM',
                        help='删除章节（章节编号）')
    parser.add_argument('--remove-section', metavar='SECTION_NUM',
                        help='删除小节（小节编号）')
    parser.add_argument('--rename-chapter', nargs=2, metavar=('NUM', 'TITLE'),
                        help='重命名章节（章节编号 新标题）')
    parser.add_argument('--move-chapter', type=int, metavar='NUM',
                        help='移动章节（章节编号）')
    parser.add_argument('--after-chapter', type=int, metavar='NUM',
                        help='在该章节之后插入/移动')
    parser.add_argument('--before-chapter', type=int, metavar='NUM',
                        help='在该章节之前插入/移动')
    parser.add_argument('--renumber', action='store_true',
                        help='重新编号所有章节')
    parser.add_argument('--adjust-level', nargs=2, metavar=('NUM', 'LEVEL'),
                        help='调整章节层级（章节编号 up/down/具体层级）')
    
    parser.add_argument('--verbose', action='store_true',
                        help='显示详细输出')
    
    return parser.parse_args()


def interactive_mode(editor: OutlineEditor, input_path: str, output_path: str):
    """交互式编辑模式"""
    print("\n" + "="*60)
    print("        大纲编辑器 - 交互式模式")
    print("="*60)
    
    content = editor.load_outline(input_path)
    parsed = editor.parse_outline(content)
    
    while True:
        print(f"\n当前大纲: {parsed['title']}")
        print(f"章节数量: {len(parsed['chapters'])}")
        print("\n可用命令:")
        print("  1. 添加章节")
        print("  2. 添加小节")
        print("  3. 删除章节")
        print("  4. 删除小节")
        print("  5. 重命名章节")
        print("  6. 移动章节")
        print("  7. 重新编号")
        print("  8. 查看大纲")
        print("  9. 保存并退出")
        print("  0. 退出不保存")
        
        choice = input("\n请选择命令 (0-9): ").strip()
        
        if choice == '1':
            title = input("  请输入章节标题: ").strip()
            if title:
                after = input("  在第X章之后添加？(留空为末尾): ").strip()
                after_num = int(after) if after.isdigit() else None
                content = editor.add_chapter(content, title, after_chapter=after_num)
                parsed = editor.parse_outline(content)
        
        elif choice == '2':
            chap_num = input("  请输入章节编号: ").strip()
            sec_title = input("  请输入小节标题: ").strip()
            if chap_num.isdigit() and sec_title:
                content = editor.add_section(content, int(chap_num), sec_title)
                parsed = editor.parse_outline(content)
        
        elif choice == '3':
            chap_num = input("  请输入要删除的章节编号: ").strip()
            if chap_num.isdigit():
                confirm = input(f"  确认删除第{chap_num}章？(y/n): ").strip().lower()
                if confirm == 'y':
                    content = editor.remove_chapter(content, int(chap_num))
                    parsed = editor.parse_outline(content)
        
        elif choice == '4':
            sec_num = input("  请输入要删除的小节编号: ").strip()
            if sec_num:
                confirm = input(f"  确认删除小节 {sec_num}？(y/n): ").strip().lower()
                if confirm == 'y':
                    content = editor.remove_section(content, sec_num)
        
        elif choice == '5':
            chap_num = input("  请输入章节编号: ").strip()
            new_title = input("  请输入新标题: ").strip()
            if chap_num.isdigit() and new_title:
                content = editor.rename_chapter(content, int(chap_num), new_title)
                parsed = editor.parse_outline(content)
        
        elif choice == '6':
            chap_num = input("  请输入要移动的章节编号: ").strip()
            position = input("  移动到第X章之后？(留空为末尾): ").strip()
            after_num = int(position) if position.isdigit() else None
            if chap_num.isdigit():
                content = editor.move_chapter(content, int(chap_num), after_chapter=after_num)
                parsed = editor.parse_outline(content)
        
        elif choice == '7':
            confirm = input("  确认重新编号所有章节？(y/n): ").strip().lower()
            if confirm == 'y':
                content = editor.renumber_chapters(content)
                parsed = editor.parse_outline(content)
        
        elif choice == '8':
            print(f"\n大纲结构:\n")
            for i, chapter in enumerate(parsed['chapters'], 1):
                print(f"  第{i}. {chapter['title']}")
                for section in chapter['sections']:
                    print(f"      {section['num']} {section['title']}")
        
        elif choice == '9':
            editor.save_outline(content, output_path)
            print(f"\n✅ 大纲已保存到: {output_path}")
            break
        
        elif choice == '0':
            print("\n⚠️  退出不保存")
            break
        
        else:
            print("\n❌ 无效选择")


def command_mode(editor: OutlineEditor, args):
    """命令式编辑模式"""
    content = editor.load_outline(args.input)
    original_content = content
    
    # 执行命令
    if args.add_chapter:
        content = editor.add_chapter(
            content,
            args.add_chapter,
            after_chapter=args.after_chapter,
            before_chapter=args.before_chapter
        )
    
    if args.add_section:
        chap_num, sec_title = args.add_section
        if chap_num.isdigit():
            content = editor.add_section(content, int(chap_num), sec_title)
    
    if args.remove_chapter is not None:
        content = editor.remove_chapter(content, args.remove_chapter)
    
    if args.remove_section:
        content = editor.remove_section(content, args.remove_section)
    
    if args.rename_chapter:
        chap_num, new_title = args.rename_chapter
        if chap_num.isdigit():
            content = editor.rename_chapter(content, int(chap_num), new_title)
    
    if args.move_chapter is not None:
        content = editor.move_chapter(
            content,
            args.move_chapter,
            after_chapter=args.after_chapter,
            before_chapter=args.before_chapter
        )
    
    if args.renumber:
        content = editor.renumber_chapters(content)
    
    if args.adjust_level:
        chap_num, level = args.adjust_level
        if chap_num.isdigit():
            content = editor.adjust_chapter_level(content, int(chap_num), level)
    
    # 保存结果
    output_path = args.output if args.output else args.input
    if content != original_content:
        editor.save_outline(content, output_path)
        print(f"\n✅ 编辑完成！")
        print(f"📄 输出文件: {output_path}")
    else:
        print("\n⚠️  没有进行任何更改")


def main():
    """主函数"""
    args = parse_arguments()
    
    # 初始化编辑器
    editor = OutlineEditor(verbose=args.verbose)
    
    try:
        if args.mode == 'interactive':
            output_path = args.output if args.output else args.input
            interactive_mode(editor, args.input, output_path)
        else:
            command_mode(editor, args)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断，程序退出")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
