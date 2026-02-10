#!/usr/bin/env python3
"""
Material Image Management Module

素材配图管理模块，提供配图查询、智能匹配、推荐生成、引用嵌入、使用追踪等功能。

Usage:
    python3 manage_material_images.py --help
    python3 manage_material_images.py --query --material 生态修复技术导则
    python3 manage_material_images.py --match --chapter "技术方案概述"
    python3 manage_material_images.py --recommend --chapter "第2章" --persona "高级工程师"
    python3 manage_material_images.py --track --image IMG_001

Examples:
    manage_material_images.py --query --type 示意图
    manage_material_images.py --match --chapter "第3章 工程设计方案"
    manage_material_images.py --stats

Features:
    - 素材配图查询和检索
    - 智能匹配算法（基于标题、内容、类型）
    - 配图推荐生成
    - Markdown 引用语法生成
    - 使用统计和追踪
"""

import os
import sys
import argparse
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher

# 尝试导入 fuzzywuzzy 进行模糊匹配
try:
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False
    print("Warning: fuzzywuzzy not available. Using basic string matching.")

# 尝试导入 pandas 进行数据处理
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class MaterialImageManager:
    """素材配图管理器"""
    
    def __init__(self, index_file: str = None, verbose: bool = False):
        """
        初始化管理器
        
        Args:
            index_file: 素材配图索引文件路径
            verbose: 是否显示详细日志
        """
        self.verbose = verbose
        
        # 默认索引文件路径
        if index_file is None:
            self.index_file = Path('iteration/material-index.md')
        else:
            self.index_file = Path(index_file)
        
        # 配图目录
        self.images_dir = Path('assets/docx_images')
        
        # 加载索引
        self.index = self._load_index()
        
        # 使用记录
        self.usage_log = []
    
    def log(self, message: str, level: str = "INFO"):
        """打印日志"""
        if self.verbose or level in ["ERROR", "WARNING"]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")
    
    def _load_index(self) -> Dict:
        """加载素材配图索引"""
        index = {
            'materials': {},
            'total_images': 0,
            'image_types': {}
        }
        
        if not self.index_file.exists():
            self.log(f"索引文件不存在: {self.index_file}", "WARNING")
            return index
        
        try:
            # 解析 Markdown 格式的索引文件
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单的 Markdown 解析
            current_material = None
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # 识别素材章节
                if line.startswith('## 素材:'):
                    current_material = line.replace('## 素材:', '').strip()
                    index['materials'][current_material] = {
                        'name': current_material,
                        'images': [],
                        'total': 0
                    }
                
                # 识别配图明细表格
                elif current_material and line.startswith('| IMG_'):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 5:
                        img_info = {
                            'id': parts[1],
                            'filename': parts[2],
                            'type': parts[3],
                            'dimensions': parts[4],
                            'size': parts[5] if len(parts) > 5 else '0KB'
                        }
                        index['materials'][current_material]['images'].append(img_info)
                        index['materials'][current_material]['total'] += 1
                        index['total_images'] += 1
                        
                        # 统计类型
                        img_type = img_info['type']
                        index['image_types'][img_type] = index['image_types'].get(img_type, 0) + 1
                        
        except Exception as e:
            self.log(f"加载索引失败: {str(e)}", "ERROR")
        
        self.log(f"加载完成: {len(index['materials'])} 个素材, {index['total_images']} 张配图")
        return index
    
    def query_images(self, material: str = None, img_type: str = None, 
                    keyword: str = None) -> List[Dict]:
        """
        查询配图
        
        Args:
            material: 素材名称（可选）
            img_type: 配图类型（可选）
            keyword: 关键词（可选）
            
        Returns:
            配图信息列表
        """
        results = []
        
        # 遍历所有素材
        for mat_name, mat_data in self.index['materials'].items():
            # 过滤素材
            if material and material not in mat_name:
                continue
            
            # 遍历配图
            for img in mat_data['images']:
                # 过滤类型
                if img_type and img['type'] != img_type:
                    continue
                
                # 过滤关键词
                if keyword:
                    keyword_lower = keyword.lower()
                    if (keyword_lower not in img['id'].lower() and
                        keyword_lower not in img['filename'].lower() and
                        keyword_lower not in img['type'].lower()):
                        continue
                
                # 添加素材信息
                img_with_material = img.copy()
                img_with_material['material'] = mat_name
                results.append(img_with_material)
        
        self.log(f"查询结果: {len(results)} 张配图")
        return results
    
    def match_paragraph(self, chapter_title: str, chapter_content: str = None) -> List[Dict]:
        """
        智能匹配段落
        
        基于章节标题和内容，匹配素材中的相关段落
        
        Args:
            chapter_title: 章节标题
            chapter_content: 章节内容（可选）
            
        Returns:
            匹配的配图列表（带匹配分数）
        """
        matches = []
        
        # 遍历所有素材的配图
        for mat_name, mat_data in self.index['materials'].items():
            for img in mat_data['images']:
                # 计算匹配分数
                scores = self._calculate_match_score(
                    chapter_title, 
                    chapter_content,
                    img,
                    mat_name
                )
                
                total_score = scores['total']
                
                # 只返回有一定匹配度的结果
                if total_score > 30:  # 阈值 30%
                    match_info = img.copy()
                    match_info['material'] = mat_name
                    match_info['match_score'] = total_score
                    match_info['match_details'] = scores
                    matches.append(match_info)
        
        # 按匹配分数排序
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        self.log(f"匹配完成: {len(matches)} 个相关配图")
        return matches
    
    def _calculate_match_score(self, chapter_title: str, chapter_content: str,
                               img: Dict, material_name: str) -> Dict:
        """
        计算匹配分数
        
        多维度评分:
        - 标题匹配 (40%)
        - 内容匹配 (30%)
        - 类型匹配 (30%)
        """
        scores = {
            'title': 0,
            'content': 0,
            'type': 0,
            'total': 0
        }
        
        # 标题匹配 (40%)
        title_score = self._string_similarity(chapter_title, material_name)
        scores['title'] = title_score * 40
        
        # 内容匹配 (30%)
        if chapter_content:
            content_score = self._string_similarity(chapter_content, img['filename'])
            scores['content'] = content_score * 30
        else:
            scores['content'] = 15  # 默认中等分数
        
        # 类型匹配 (30%)
        # 根据章节标题关键词判断期望的图片类型
        expected_type = self._infer_image_type_from_title(chapter_title)
        if expected_type and img['type'] == expected_type:
            scores['type'] = 30
        elif expected_type and self._are_types_related(expected_type, img['type']):
            scores['type'] = 20
        else:
            scores['type'] = 10
        
        # 总分
        scores['total'] = scores['title'] + scores['content'] + scores['type']
        
        return scores
    
    def _string_similarity(self, str1: str, str2: str) -> float:
        """计算两个字符串的相似度 (0-1)"""
        if not str1 or not str2:
            return 0.0
        
        if FUZZY_AVAILABLE:
            # 使用 fuzzywuzzy
            return fuzz.ratio(str1.lower(), str2.lower()) / 100.0
        else:
            # 使用简单的 SequenceMatcher
            return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def _infer_image_type_from_title(self, title: str) -> str:
        """从章节标题推断期望的图片类型"""
        title_lower = title.lower()
        
        # 流程相关
        if any(kw in title_lower for kw in ['流程', '过程', '步骤', '工艺', 'flow', 'process']):
            return '流程图'
        
        # 数据相关
        if any(kw in title_lower for kw in ['数据', '统计', '对比', '分析', '参数', 'data']):
            return '数据图'
        
        # 设计/方案相关
        if any(kw in title_lower for kw in ['设计', '方案', '结构', '原理', 'design', 'scheme']):
            return '示意图'
        
        # 现场/实施相关
        if any(kw in title_lower for kw in ['现场', '实景', '照片', '施工', 'photo']):
            return '照片'
        
        return None
    
    def _are_types_related(self, type1: str, type2: str) -> bool:
        """判断两种图片类型是否相关"""
        related_groups = [
            {'流程图', '示意图'},  # 流程和示意相关
            {'数据图', '示意图'},  # 数据和示意相关
            {'照片', '实景图'},    # 照片相关
        ]
        
        for group in related_groups:
            if type1 in group and type2 in group:
                return True
        
        return False
    
    def recommend_images(self, chapter_title: str, chapter_content: str = None,
                        persona: str = None, top_k: int = 5) -> List[Dict]:
        """
        生成配图推荐
        
        Args:
            chapter_title: 章节标题
            chapter_content: 章节内容
            persona: 写作人设（可选）
            top_k: 返回推荐数量
            
        Returns:
            推荐的配图列表（带推荐标记）
        """
        # 获取匹配的配图
        matches = self.match_paragraph(chapter_title, chapter_content)
        
        if not matches:
            self.log("未找到匹配的配图")
            return []
        
        # 添加推荐标记
        for i, img in enumerate(matches):
            score = img['match_score']
            
            if i == 0 and score >= 80:
                img['recommendation'] = '⭐ 综合推荐'
                img['reason'] = '与当前章节高度匹配'
            elif score >= 60:
                img['recommendation'] = '🌟 相关推荐'
                img['reason'] = '与当前章节相关'
            elif score >= 40:
                img['recommendation'] = '可选'
                img['reason'] = '可能相关'
            else:
                img['recommendation'] = ''
                img['reason'] = ''
        
        # 只返回前 top_k 个
        recommendations = matches[:top_k]
        
        self.log(f"生成推荐: {len(recommendations)} 张配图")
        return recommendations
    
    def generate_markdown_reference(self, img: Dict, chapter_num: int = 1,
                                   img_seq: int = 1) -> str:
        """
        生成 Markdown 图片引用语法
        
        Args:
            img: 配图信息
            chapter_num: 章节编号
            img_seq: 图片序号
            
        Returns:
            Markdown 引用字符串
        """
        # 构建图片路径
        img_path = f"../assets/docx_images/{img['material']}/{img['filename']}"
        
        # 图片标题
        img_title = f"图{chapter_num}-{img_seq}：{img['type']}"
        
        # 来源标注
        source = f"（来源：{img['material']}）"
        
        # 生成 Markdown
        md = f"\n![{img['type']}]({img_path})\n\n"
        md += f"*{img_title}{source}*\n"
        
        return md
    
    def track_usage(self, img_id: str, chapter: str, action: str = 'referenced'):
        """
        记录配图使用
        
        Args:
            img_id: 配图ID
            chapter: 使用章节
            action: 操作类型 (referenced/ignored)
        """
        usage = {
            'timestamp': datetime.now().isoformat(),
            'image_id': img_id,
            'chapter': chapter,
            'action': action
        }
        
        self.usage_log.append(usage)
        self.log(f"记录使用: {img_id} -> {chapter}")
    
    def save_usage_log(self, output_file: str = None):
        """保存使用记录到日志文件"""
        if output_file is None:
            output_file = Path('iteration/usage-log.md')
        else:
            output_file = Path(output_file)
        
        if not self.usage_log:
            return
        
        try:
            # 追加到日志文件
            with open(output_file, 'a', encoding='utf-8') as f:
                f.write("\n## 素材配图使用记录\n\n")
                f.write(f"**记录时间**: {datetime.now().isoformat()}\n\n")
                f.write("| 时间 | 配图ID | 章节 | 操作 |\n")
                f.write("|------|--------|------|------|\n")
                
                for usage in self.usage_log:
                    f.write(f"| {usage['timestamp']} | {usage['image_id']} | "
                           f"{usage['chapter']} | {usage['action']} |\n")
                
                f.write("\n")
            
            self.log(f"使用记录已保存: {output_file}")
            
        except Exception as e:
            self.log(f"保存使用记录失败: {str(e)}", "ERROR")
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        stats = {
            'total_materials': len(self.index['materials']),
            'total_images': self.index['total_images'],
            'image_types': self.index['image_types'],
            'usage_count': len(self.usage_log)
        }
        
        return stats
    
    def print_statistics(self):
        """打印统计信息"""
        stats = self.get_statistics()
        
        print("\n" + "=" * 60)
        print("素材配图统计")
        print("=" * 60)
        print(f"素材文件总数: {stats['total_materials']}")
        print(f"配图总数: {stats['total_images']}")
        print(f"使用记录数: {stats['usage_count']}")
        
        if stats['image_types']:
            print("\n配图类型分布:")
            for img_type, count in sorted(stats['image_types'].items(), 
                                          key=lambda x: x[1], reverse=True):
                percentage = count / stats['total_images'] * 100
                print(f"  {img_type}: {count} ({percentage:.1f}%)")
        
        print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='素材配图管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --query --material "生态修复技术导则"
  %(prog)s --match --chapter "第2章 技术方案概述"
  %(prog)s --recommend --chapter "第3章 工程设计方案" --top-k 3
  %(prog)s --stats
        '''
    )
    
    # 子命令
    parser.add_argument('--query', action='store_true',
                      help='查询配图')
    parser.add_argument('--match', action='store_true',
                      help='匹配段落')
    parser.add_argument('--recommend', action='store_true',
                      help='生成推荐')
    parser.add_argument('--stats', action='store_true',
                      help='显示统计')
    
    # 参数
    parser.add_argument('--material', '-m',
                      help='素材名称')
    parser.add_argument('--type', '-t',
                      help='配图类型')
    parser.add_argument('--keyword', '-k',
                      help='关键词')
    parser.add_argument('--chapter', '-c',
                      help='章节标题')
    parser.add_argument('--content',
                      help='章节内容')
    parser.add_argument('--persona', '-p',
                      help='写作人设')
    parser.add_argument('--top-k', type=int, default=5,
                      help='推荐数量 (默认: 5)')
    parser.add_argument('--index', '-i',
                      default='iteration/material-index.md',
                      help='索引文件路径')
    parser.add_argument('--verbose', '-v',
                      action='store_true',
                      help='显示详细日志')
    
    args = parser.parse_args()
    
    # 创建管理器
    manager = MaterialImageManager(
        index_file=args.index,
        verbose=args.verbose
    )
    
    # 执行命令
    if args.stats:
        manager.print_statistics()
    
    elif args.query:
        results = manager.query_images(
            material=args.material,
            img_type=args.type,
            keyword=args.keyword
        )
        
        print(f"\n查询结果: {len(results)} 张配图\n")
        for img in results:
            print(f"  [{img['id']}] {img['filename']} ({img['type']})")
            print(f"    素材: {img['material']}")
            print(f"    尺寸: {img['dimensions']}, 大小: {img['size']}")
            print()
    
    elif args.match:
        if not args.chapter:
            print("Error: --chapter is required for matching")
            sys.exit(1)
        
        matches = manager.match_paragraph(args.chapter, args.content)
        
        print(f"\n匹配结果: {len(matches)} 张相关配图\n")
        for i, img in enumerate(matches[:10], 1):  # 只显示前10个
            score = img['match_score']
            print(f"{i}. [{img['id']}] 匹配度: {score:.1f}%")
            print(f"   文件: {img['filename']}")
            print(f"   类型: {img['type']}, 素材: {img['material']}")
            print()
    
    elif args.recommend:
        if not args.chapter:
            print("Error: --chapter is required for recommendation")
            sys.exit(1)
        
        recommendations = manager.recommend_images(
            chapter_title=args.chapter,
            chapter_content=args.content,
            persona=args.persona,
            top_k=args.top_k
        )
        
        if not recommendations:
            print("\n未找到匹配的配图")
            sys.exit(0)
        
        print(f"\n推荐配图 ({len(recommendations)} 张):\n")
        for i, img in enumerate(recommendations, 1):
            rec_mark = img.get('recommendation', '')
            reason = img.get('reason', '')
            
            print(f"{i}. {rec_mark}")
            print(f"   ID: {img['id']}")
            print(f"   文件: {img['filename']}")
            print(f"   类型: {img['type']}")
            print(f"   匹配度: {img['match_score']:.1f}%")
            if reason:
                print(f"   推荐理由: {reason}")
            
            # 生成 Markdown 引用示例
            md_ref = manager.generate_markdown_reference(img, 1, i)
            print(f"   Markdown引用:")
            print(f"   {md_ref[:100]}...")
            print()
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
