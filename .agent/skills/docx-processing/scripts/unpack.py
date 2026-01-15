#!/usr/bin/env python3
"""
解压 .docx 文件为 XML 结构

用法:
    python unpack.py document.docx output_dir/
"""

import sys
import zipfile
import os
from pathlib import Path


def unpack_docx(docx_file, output_dir):
    """解压 .docx 文件到指定目录"""
    
    # 检查文件是否存在
    if not os.path.exists(docx_file):
        print(f"错误: 文件不存在: {docx_file}")
        sys.exit(1)
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 解压
    try:
        with zipfile.ZipFile(docx_file, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        print(f"✓ 已解压到: {output_dir}")
    except zipfile.BadZipFile:
        print(f"错误: {docx_file} 不是有效的 ZIP 文件")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    # 建议 RSID
    suggest_rsid(output_dir)


def suggest_rsid(output_dir):
    """分析文档并建议一个 RSID"""
    import xml.etree.ElementTree as ET
    
    doc_xml = os.path.join(output_dir, 'word', 'document.xml')
    if not os.path.exists(doc_xml):
        return
    
    try:
        tree = ET.parse(doc_xml)
        root = tree.getroot()
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        # 查找现有的 RSID
        rsids = set()
        for elem in root.findall('.//*[@w:rsidR]', ns):
            rsid = elem.get('{%s}rsidR' % ns['w'])
            if rsid:
                rsids.add(rsid)
        
        if rsids:
            # 使用最常见的 RSID
            from collections import Counter
            rsid_counts = Counter()
            for elem in root.findall('.//*[@w:rsidR]', ns):
                rsid = elem.get('{%s}rsidR' % ns['w'])
                if rsid:
                    rsid_counts[rsid] += 1
            
            most_common = rsid_counts.most_common(1)[0][0]
            print(f"\n💡 建议使用 RSID: {most_common}")
            print(f"   (在文档中出现 {rsid_counts[most_common]} 次)")
        else:
            # 生成一个随机 RSID
            import random
            rsid = f"{random.randint(0, 0xFFFFFF):08X}"
            print(f"\n💡 建议使用 RSID: {rsid}")
            print(f"   (随机生成)")
    
    except Exception:
        pass  # 静默失败


def main():
    if len(sys.argv) < 3:
        print("用法: python unpack.py <docx_file> <output_dir>")
        print("\n示例:")
        print("  python unpack.py document.docx unpacked/")
        sys.exit(1)
    
    docx_file = sys.argv[1]
    output_dir = sys.argv[2]
    
    unpack_docx(docx_file, output_dir)


if __name__ == '__main__':
    main()
