#!/usr/bin/env python3
"""
Outline Manager - 大纲管理工具

Provides listing, viewing, deletion, and history management for outline files.

Usage:
    python outline_manager.py --help
    python outline_manager.py --list
    python outline_manager.py --show outline-generated.md
    python outline_manager.py --delete outline-old.md
    python outline_manager.py --history outline-generated.md
"""

import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class OutlineManager:
    """大纲管理器"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.history_dir = Path("iteration/outline-history")
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.outline_pattern = r'### 第(\d+)章\s+([^\n]+)'
        self.section_pattern = r'#### ([\d\.?\d*?)\s+[^\n]+'
    
    def log(self, message: str, level: str = "INFO"):
        """打印日志信息"""
        if self.verbose or level in ["ERROR", "WARNING"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")
    
    def list_outlines(self, path: Optional[str] = None) -> List[Dict]:
        """列出所有大纲文件"""
        self.log("正在列出大纲文件...")
        
        # 如果指定了路径，只列出该路径下的文件
        if path:
            search_path = Path(path)
            if search_path.is_file():
                return [{'path': str(search_path.absolute()), 'name': search_path.name}]
            outline_files = list(search_path.glob("*.md"))
        else:
            # 搜索当前目录和 history 目录
            current_files = list(Path(".").glob("outline-*.md"))
            history_files = list(self.history_dir.glob("outline_*.md"))
            outline_files = current_files + history_files
        
        outlines = []
        for file_path in outline_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # 提取标题
                title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else file_path.stem
                
                # 提取章节数量
                chapters = re.findall(self.outline_pattern, content)
                sections = re.findall(self.section_pattern, content)
                
                # 提取生成时间
                gen_time = "Unknown"
                time_match = re.search(r'- 生成时间：([^\n]+)', content)
                if time_match:
                    gen_time = time_match.group(1).strip()
                
                # 获取文件大小
                file_size = file_path.stat().st_size
                file_size_kb = file_size / 1024
                
                outlines.append({
                    'path': str(file_path.absolute()),
                    'name': file_path.name,
                    'title': title,
                    'chapters_count': len(chapters),
                    'sections_count': len(sections),
                    'generated_at': gen_time,
                    'size_kb': round(file_size_kb, 2)
                })
            except Exception as e:
                self.log(f"读取文件 {file_path.name} 失败: {e}", "WARNING")
        
        # 按文件修改时间排序
        outlines.sort(key=lambda x: Path(x['path']).stat().st_mtime, reverse=True)
        
        self.log(f"找到 {len(outlines)} 个大纲文件")
        return outlines
    
    def show_outline(self, file_path: str) -> Dict:
        """显示大纲详情"""
        self.log(f"显示大纲: {file_path}")
        
        try:
            path = Path(file_path)
            content = path.read_text(encoding='utf-8')
            
            # 提取元数据
            metadata = self._extract_outline_metadata(content)
            
            # 提取章节结构
            chapters = self._extract_outline_structure(content)
            
            outline_info = {
                'path': str(path.absolute()),
                'name': path.name,
                'metadata': metadata,
                'chapters': chapters,
                'file_stats': {
                    'size': path.stat().st_size,
                    'size_kb': round(path.stat().st_size / 1024, 2),
                    'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat()
                }
            }
            
            return outline_info
        except FileNotFoundError:
            self.log(f"文件不存在: {file_path}", "ERROR")
            raise
        except Exception as e:
            self.log(f"读取文件失败: {e}", "ERROR")
            raise
    
    def _extract_outline_metadata(self, content: str) -> Dict:
        """提取大纲元数据"""
        metadata = {
            'title': 'Unknown',
            'generated_at': 'Unknown',
            'generation_mode': 'Unknown',
            'template_used': 'Unknown'
        }
        
        # 提取标题
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # 提取元数据部分
        metadata_match = re.search(r'## 元数据\s*\n(.*?)(?=###\s第|\Z)', content, re.DOTALL)
        if metadata_match:
            metadata_content = metadata_match.group(1)
            lines = metadata_content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-'):
                    parts = line[1:].split('：')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        if key == '生成时间':
                            metadata['generated_at'] = value
                        elif key == '生成模式':
                            metadata['generation_mode'] = value
                        elif key == '使用模板':
                            metadata['template_used'] = value
        
        return metadata
    
    def _extract_outline_structure(self, content: str) -> List[Dict]:
        """提取大纲章节结构"""
        chapters = []
        
        chapter_matches = list(re.finditer(self.outline_pattern, content))
        
        for i, match in enumerate(chapter_matches):
            chapter_num = match.group(1)
            chapter_title = match.group(2).strip()
            
            # 查找小节
            start_pos = match.end()
            end_pos = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(content)
            chapter_content = content[start_pos:end_pos]
            
            sections = []
            for section_match in re.finditer(self.section_pattern, chapter_content):
                section_num = section_match.group(1)
                section_title = section_match.group(2).strip()
                sections.append({
                    'num': section_num,
                    'title': section_title
                })
            
            chapters.append({
                'num': chapter_num,
                'title': chapter_title,
                'sections_count': len(sections),
                'sections': sections
            })
        
        return chapters
    
    def delete_outline(self, file_path: str) -> bool:
        """删除大纲文件"""
        self.log(f"删除大纲: {file_path}")
        
        try:
            path = Path(file_path)
            if not path.exists():
                self.log(f"文件不存在: {file_path}", "WARNING")
                return False
            
            # 检查是否在 history 目录
            is_in_history = str(self.history_dir) in str(path.absolute())
            
            path.unlink()
            self.log(f"文件删除成功: {file_path}")
            return True
        except Exception as e:
            self.log(f"删除文件失败: {e}", "ERROR")
            return False
    
    def show_history(self, file_path: str) -> List[Dict]:
        """显示大纲历史版本"""
        self.log(f"显示大纲历史: {file_path}")
        
        try:
            base_name = Path(file_path).stem
            
            # 查找历史记录
            history_files = []
            for history_file in self.history_dir.glob("outline_*.json"):
                if base_name in history_file.stem:
                    try:
                        with open(history_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            history_files.append({
                                'file': str(history_file.name),
                                'path': str(history_file.absolute()),
                                'generated_at': data.get('metadata', {}).get('generated_at', 'Unknown'),
                                'generation_mode': data.get('metadata', {}).get('generation_mode', 'Unknown'),
                                'template_used': data.get('metadata', {}).get('template_used', 'Unknown'),
                                'chapters_count': len(data.get('chapters', []))
                            })
                    except Exception as e:
                        self.log(f"读取历史文件 {history_file.name} 失败: {e}", "WARNING")
            
            # 按生成时间排序
            history_files.sort(key=lambda x: x['generated_at'], reverse=True)
            
            self.log(f"找到 {len(history_files)} 个历史版本")
            return history_files
        except Exception as e:
            self.log(f"查询历史失败: {e}", "ERROR")
            raise
    
    def search_outlines(self, keyword: str, path: Optional[str] = None) -> List[Dict]:
        """搜索大纲文件"""
        self.log(f"搜索大纲关键词: {keyword}")
        
        outlines = self.list_outlines(path)
        results = []
        
        keyword_lower = keyword.lower()
        
        for outline in outlines:
            try:
                content = Path(outline['path']).read_text(encoding='utf-8')
                
                # 在标题、章节、小节中搜索
                matches = 0
                matches += keyword_lower in content.lower().count(keyword_lower)
                
                # 搜索章节标题
                chapter_matches = re.findall(
                    rf'第\d+章\s+([^{keyword}]*{keyword}[^{keyword}]*?)',
                    content,
                    re.IGNORECASE
                )
                matches += len(chapter_matches)
                
                if matches > 0:
                    outline['matches'] = matches
                    results.append(outline)
            except Exception as e:
                self.log(f"搜索文件 {outline['name']} 失败: {e}", "WARNING")
        
        self.log(f"找到 {len(results)} 个匹配结果")
        return results


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='大纲管理工具 - 列表/查看/删除/历史',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
    Examples:
      # 列出所有大纲
      outline_manager.py --list
      
      # 显示大纲详情
      outline_manager.py --show outline-generated.md
      
      # 删除大纲
      outline_manager.py --delete outline-old.md
      
      # 显示历史版本
      outline_manager.py --history outline-generated.md
      
      # 搜索大纲
      outline_manager.py --search "地质调查" --path iteration/
    ''')
    
    # 动作参数
    parser.add_argument('--list', action='store_true',
                        help='列出所有大纲文件')
    parser.add_argument('--show', metavar='FILE',
                        help='显示大纲详细信息')
    parser.add_argument('--delete', metavar='FILE',
                        help='删除大纲文件')
    parser.add_argument('--history', metavar='FILE',
                        help='显示大纲历史版本')
    parser.add_argument('--search', metavar='KEYWORD',
                        help='搜索大纲关键词')
    
    # 可选参数
    parser.add_argument('--path', metavar='PATH',
                        help='指定搜索路径（默认：当前目录和 history 目录）')
    parser.add_argument('--verbose', action='store_true',
                        help='显示详细输出')
    
    return parser.parse_args()


def print_outline_list(outlines: List[Dict]):
    """打印大纲列表"""
    print("\n" + "="*80)
    print("                        大纲文件列表")
    print("="*80)
    
    if not outlines:
        print("\n  未找到大纲文件")
        return
    
    # 表头
    print(f"\n{'序号':<6} {'文件名':<30} {'标题':<25} {'章节':<8} {'大小(KB)':<12}")
    print("-" * 85)
    
    for i, outline in enumerate(outlines, 1):
        title = outline['title'][:22] + '...' if len(outline['title']) > 25 else outline['title']
        print(f"{i:<6} {outline['name']:<30} {title:<25} {outline['chapters_count']:<8} {outline['size_kb']:<12.2f}")
    
    print("\n" + "="*80)
    print(f"总计: {len(outlines)} 个大纲文件")
    print("="*80 + "\n")


def print_outline_details(outline: Dict):
    """打印大纲详情"""
    print("\n" + "="*80)
    print("                        大纲详细信息")
    print("="*80)
    
    # 基本信息
    print(f"\n📄 文件信息")
    print(f"   路径: {outline['path']}")
    print(f"   名称: {outline['name']}")
    print(f"   大小: {outline['file_stats']['size_kb']} KB")
    print(f"   修改时间: {outline['file_stats']['modified']}")
    
    # 元数据
    metadata = outline['metadata']
    print(f"\n📋 元数据")
    print(f"   标题: {metadata['title']}")
    print(f"   生成时间: {metadata['generated_at']}")
    print(f"   生成模式: {metadata['generation_mode']}")
    print(f"   使用模板: {metadata['template_used']}")
    
    # 章节结构
    chapters = outline['chapters']
    print(f"\n📖 章节结构 ({len(chapters)} 章)")
    
    for i, chapter in enumerate(chapters, 1):
        print(f"\n   {i}. 第{chapter['num']}章 {chapter['title']}")
        print(f"      小节数量: {chapter['sections_count']}")
        
        if chapter['sections']:
            for j, section in enumerate(chapter['sections'][:3], 1):  # 只显示前3个小节
                print(f"      {j}. {section['num']} {section['title']}")
            if len(chapter['sections']) > 3:
                print(f"      ... 还有 {len(chapter['sections']) - 3} 个小节")
    
    print("\n" + "="*80)


def print_history(history: List[Dict]):
    """打印历史版本"""
    print("\n" + "="*80)
    print("                    大纲历史版本")
    print("="*80)
    
    if not history:
        print("\n  未找到历史版本")
        return
    
    print(f"\n共找到 {len(history)} 个历史版本:\n")
    
    for i, version in enumerate(history, 1):
        print(f"{i}. {version['file']}")
        print(f"   生成时间: {version['generated_at']}")
        print(f"   生成模式: {version['generation_mode']}")
        print(f"   使用模板: {version['template_used']}")
        print(f"   章节数量: {version['chapters_count']}")
        print()
    
    print("="*80)


def print_search_results(results: List[Dict], keyword: str):
    """打印搜索结果"""
    print("\n" + "="*80)
    print(f"                    搜索结果: '{keyword}'")
    print("="*80)
    
    if not results:
        print("\n  未找到匹配结果")
        return
    
    print(f"\n找到 {len(results)} 个匹配:\n")
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['name']}")
        print(f"   匹配数: {result['matches']}")
        print(f"   标题: {result['title']}")
        print(f"   章节数: {result['chapters_count']}")
        print(f"   路径: {result['path']}")
        print()
    
    print("="*80)


def main():
    """主函数"""
    args = parse_arguments()
    
    # 初始化管理器
    manager = OutlineManager(verbose=args.verbose)
    
    try:
        if args.list:
            outlines = manager.list_outlines(args.path)
            print_outline_list(outlines)
        
        elif args.show:
            outline = manager.show_outline(args.show)
            print_outline_details(outline)
        
        elif args.delete:
            success = manager.delete_outline(args.delete)
            if success:
                print(f"\n✅ 文件已删除: {args.delete}")
            else:
                print(f"\n⚠️  删除失败: {args.delete}")
        
        elif args.history:
            history = manager.show_history(args.history)
            print_history(history)
        
        elif args.search:
            results = manager.search_outlines(args.search, args.path)
            print_search_results(results, args.search)
        
        else:
            # 没有指定动作，默认显示列表
            print("\n⚠️  未指定动作，默认显示大纲列表\n")
            outlines = manager.list_outlines(args.path)
            print_outline_list(outlines)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断，程序退出")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
