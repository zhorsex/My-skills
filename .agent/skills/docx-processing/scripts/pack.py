#!/usr/bin/env python3
"""
将 XML 结构打包为 .docx 文件

用法:
    python pack.py input_dir/ output.docx
"""

import sys
import zipfile
import os
from pathlib import Path


def pack_docx(input_dir, output_file):
    """将目录打包为 .docx 文件"""
    
    # 检查目录是否存在
    if not os.path.exists(input_dir):
        print(f"错误: 目录不存在: {input_dir}")
        sys.exit(1)
    
    # 检查必需文件
    required_files = [
        '[Content_Types].xml',
        '_rels/.rels',
        'word/document.xml'
    ]
    
    for req_file in required_files:
        full_path = os.path.join(input_dir, req_file)
        if not os.path.exists(full_path):
            print(f"警告: 缺少必需文件: {req_file}")
    
    # 创建 ZIP 文件
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历所有文件
            for root, dirs, files in os.walk(input_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 计算相对路径
                    arcname = os.path.relpath(file_path, input_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✓ 已打包为: {output_file}")
        
        # 验证文件
        verify_docx(output_file)
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


def verify_docx(docx_file):
    """验证生成的 .docx 文件"""
    try:
        with zipfile.ZipFile(docx_file, 'r') as zipf:
            # 检查文件列表
            file_list = zipf.namelist()
            
            # 检查必需文件
            required = ['[Content_Types].xml', 'word/document.xml']
            missing = [f for f in required if f not in file_list]
            
            if missing:
                print(f"⚠️  警告: 缺少文件: {', '.join(missing)}")
            else:
                print(f"✓ 验证通过: 包含 {len(file_list)} 个文件")
            
            # 测试 ZIP 完整性
            bad_file = zipf.testzip()
            if bad_file:
                print(f"⚠️  警告: 文件损坏: {bad_file}")
    
    except zipfile.BadZipFile:
        print("⚠️  警告: 生成的文件可能不是有效的 ZIP")
    except Exception as e:
        print(f"⚠️  验证失败: {e}")


def main():
    if len(sys.argv) < 3:
        print("用法: python pack.py <input_dir> <output_file>")
        print("\n示例:")
        print("  python pack.py unpacked/ output.docx")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    # 确保输出文件有 .docx 扩展名
    if not output_file.endswith('.docx'):
        output_file += '.docx'
    
    pack_docx(input_dir, output_file)


if __name__ == '__main__':
    main()
