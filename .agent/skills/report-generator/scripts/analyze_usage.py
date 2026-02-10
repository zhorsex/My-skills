#!/usr/bin/env python3
"""
使用分析脚本 (Usage Analysis Script)

Usage:
    python3 analyze_usage.py --help
    python3 analyze_usage.py --usage-log usage-log.md
    python3 analyze_usage.py --feedback-log feedback-log.md
    python3 analyze_usage.py --patterns-path iteration/patterns/
    python3 analyze_usage.py --all --iteration-path iteration/

Examples:
    analyze_usage.py --usage-log usage-log.md --report usage_report.txt
    analyze_usage.py --feedback-log feedback-log.md --report feedback_report.txt
    analyze_usage.py --all --iteration-path iteration/ --report comprehensive_report.txt

Features:
    - Analyze usage logs (time, chapters, charts, search depth)
    - Analyze feedback logs (satisfaction, modification types, issues)
    - Identify patterns and preferences
    - Generate analysis reports
    - Provide improvement suggestions
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Analyze usage and feedback logs to identify patterns and preferences',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --usage-log iteration/usage-log.md --report usage_report.txt
  %(prog)s --feedback-log iteration/feedback-log.md --report feedback_report.txt
  %(prog)s --all --iteration-path iteration/ --report comprehensive_report.txt
        '''
    )
    
    parser.add_argument('--usage-log', help='Path to usage-log.md')
    parser.add_argument('--feedback-log', help='Path to feedback-log.md')
    parser.add_argument('--iteration-path', default='iteration/', help='Path to iteration directory')
    parser.add_argument('--report', required=True, help='Output report file path')
    parser.add_argument('--all', action='store_true', help='Analyze all iteration data')
    
    return parser.parse_args()


def read_markdown_table(file_path, table_start="|"):
    """Simple parser to extract table data from markdown tables."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        return []
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []
    
    # Find table rows
    table_rows = []
    in_table = False
    
    for line in lines:
        if line.strip().startswith("|") or line.strip().startswith("+-"):
            in_table = True
            if line.strip().startswith("|") and not line.strip().startswith("|-"):
                table_rows.append(line.strip())
        else:
            if in_table:
                break
    
    return table_rows


def parse_usage_table(table_rows):
    """Parse usage table rows into structured data."""
    if len(table_rows) < 3:
        return []
    
    # Extract headers
    headers = [h.strip() for h in table_rows[1].split('|') if h.strip()]
    data = []
    
    # Extract data rows
    for row in table_rows[2:]:
        if row.strip():
            values = [v.strip() for v in row.split('|') if v.strip()]
            if len(values) == len(headers):
                entry = {headers[i]: values[i] for i in range(len(headers))}
                data.append(entry)
    
    return data


def analyze_usage_data(usage_data):
    """Analyze usage data and generate statistics."""
    if not usage_data:
        return None
    
    # Extract numeric data
    word_counts = []
    times = []
    
    for entry in usage_data:
        # Extract word count from "字数" column
        if '字数' in entry:
            word_count = entry['字数']
            if word_count.isdigit():
                word_counts.append(int(word_count))
        
        # Extract time from "耗时" column
        if '耗时' in entry:
            time_str = entry['耗时']
            if '分钟' in time_str:
                time_val = time_str.replace('分钟', '').strip()
                if time_val.isdigit():
                    times.append(int(time_val))
    
    # Calculate statistics
    stats = {
        'total_entries': len(usage_data),
        'avg_word_count': sum(word_counts) / len(word_counts) if word_counts else 0,
        'max_word_count': max(word_counts) if word_counts else 0,
        'min_word_count': min(word_counts) if word_counts else 0,
        'avg_time': sum(times) / len(times) if times else 0,
        'max_time': max(times) if times else 0,
        'min_time': min(times) if times else 0,
        'total_time': sum(times) if times else 0
    }
    
    return stats


def analyze_feedback_data(feedback_data):
    """Analyze feedback data and generate statistics."""
    if not feedback_data:
        return None
    
    # Extract satisfaction scores
    satisfaction_scores = []
    
    for entry in feedback_data:
        if '满意度' in entry or '评分' in entry:
            score_str = entry.get('满意度', entry.get('评分', ''))
            # Extract numeric score from star strings like "⭐⭐⭐⭐⭐ 5星"
            score_num = 0
            for c in score_str:
                if c.isdigit():
                    score_num = int(c)
                    break
            if score_num > 0:
                satisfaction_scores.append(score_num)
    
    # Calculate statistics
    stats = {
        'total_feedback': len(feedback_data),
        'avg_satisfaction': sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0,
        'max_satisfaction': max(satisfaction_scores) if satisfaction_scores else 0,
        'min_satisfaction': min(satisfaction_scores) if satisfaction_scores else 0,
        'satisfaction_distribution': {}
    }
    
    # Build distribution
    for score in satisfaction_scores:
        key = f"{score}星"
        stats['satisfaction_distribution'][key] = stats['satisfaction_distribution'].get(key, 0) + 1
    
    return stats


def generate_usage_report(usage_stats, output_path):
    """Generate usage analysis report."""
    report_lines = [
        "# 使用分析报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 总体概况",
        "",
        f"- 总记录数: {usage_stats['total_entries']}",
        f"- 平均字数: {usage_stats['avg_word_count']:.1f}",
        f"- 最大字数: {usage_stats['max_word_count']}",
        f"- 最小字数: {usage_stats['min_word_count']}",
        f"- 平均耗时: {usage_stats['avg_time']:.1f}分钟",
        f"- 最大耗时: {usage_stats['max_time']}分钟",
        f"- 最小耗时: {usage_stats['min_time']}分钟",
        f"- 总耗时: {usage_stats['total_time']}分钟",
        "",
        "## 分析结论",
        "",
        "### 效率分析",
        "- 平均每章字数符合预期范围（2000-3000字）" if 2000 <= usage_stats['avg_word_count'] <= 3000 else "- 平均字数超出预期范围",
        "- 平均每章耗时在合理范围内（30-90分钟）" if 30 <= usage_stats['avg_time'] <= 90 else "- 平均耗时较长，建议优化",
        "",
        "### 优化建议",
        "1. 针对耗时较长的章节，建议优化资料搜集策略",
        "2. 考虑增加常用资料的缓存",
        "3. 分析用户偏好，提供个性化模板",
        "",
        "---",
        "**报告生成时间**: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ]
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        print(f"✅ Usage report generated: {output_path}")
    except Exception as e:
        print(f"❌ Error writing report: {e}")


def generate_feedback_report(feedback_stats, output_path):
    """Generate feedback analysis report."""
    report_lines = [
        "# 反馈分析报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 总体概况",
        "",
        f"- 总反馈数: {feedback_stats['total_feedback']}",
        f"- 平均满意度: {feedback_stats['avg_satisfaction']:.1f}星",
        f"- 最高满意度: {feedback_stats['max_satisfaction']}星",
        f"- 最低满意度: {feedback_stats['min_satisfaction']}星",
        "",
        "## 满意度分布",
        "",
        "| 满意度 | 数量 | 占比 |",
        "|---------|------|------|"
    ]
    
    total = feedback_stats['total_feedback']
    for score, count in sorted(feedback_stats['satisfaction_distribution'].items()):
        percentage = (count / total * 100) if total > 0 else 0
        report_lines.append(f"| {score} | {count} | {percentage:.1f}% |")
    
    report_lines.extend([
        "",
        "## 分析结论",
        "",
        "### 质量评估",
        f"- 平均满意度{'较高' if feedback_stats['avg_satisfaction'] >= 4 else '一般' if feedback_stats['avg_satisfaction'] >= 3 else '较低'}",
        f"- 大部分用户{'满意' if feedback_stats['avg_satisfaction'] >= 4 else '基本满意' if feedback_stats['avg_satisfaction'] >= 3 else '需要改进'}",
        "",
        "### 改进建议",
        "1. 针对低满意度反馈，分析具体问题和原因",
        "2. 优化常见问题的处理流程",
        "3. 增强用户交互和确认机制",
        "",
        "---",
        "**报告生成时间**: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ])
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        print(f"✅ Feedback report generated: {output_path}")
    except Exception as e:
        print(f"❌ Error writing report: {e}")


def main():
    """Main function."""
    args = parse_arguments()
    
    # Analyze usage log if specified
    if args.usage_log:
        print(f"ℹ️  Analyzing usage log: {args.usage_log}")
        table_rows = read_markdown_table(args.usage_log)
        usage_data = parse_usage_table(table_rows)
        usage_stats = analyze_usage_data(usage_data)
        generate_usage_report(usage_stats, args.report)
    
    # Analyze feedback log if specified
    if args.feedback_log:
        print(f"ℹ️  Analyzing feedback log: {args.feedback_log}")
        table_rows = read_markdown_table(args.feedback_log)
        feedback_data = parse_usage_table(table_rows)
        feedback_stats = analyze_feedback_data(feedback_data)
        generate_feedback_report(feedback_stats, args.report)
    
    # Analyze all iteration data
    if args.all:
        print(f"ℹ️  Analyzing all iteration data from: {args.iteration_path}")
        iteration_path = Path(args.iteration_path)
        
        # Analyze usage log
        usage_log_path = iteration_path / 'usage-log.md'
        if usage_log_path.exists():
            table_rows = read_markdown_table(str(usage_log_path))
            usage_data = parse_usage_table(table_rows)
            usage_stats = analyze_usage_data(usage_data)
            generate_usage_report(usage_stats, args.report.replace('.txt', '_usage.txt'))
        
        # Analyze feedback log
        feedback_log_path = iteration_path / 'feedback-log.md'
        if feedback_log_path.exists():
            table_rows = read_markdown_table(str(feedback_log_path))
            feedback_data = parse_usage_table(table_rows)
            feedback_stats = analyze_feedback_data(feedback_data)
            generate_feedback_report(feedback_stats, args.report.replace('.txt', '_feedback.txt'))
    
    if not args.usage_log and not args.feedback_log and not args.all:
        print("❌ Error: No input specified. Use --help for usage.")
        sys.exit(1)


if __name__ == "__main__":
    main()
