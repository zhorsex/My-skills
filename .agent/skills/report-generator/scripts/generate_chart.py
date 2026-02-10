#!/usr/bin/env python3
"""
图表生成脚本 (Generate Chart Script)

Usage:
    python3 generate_chart.py --help
    python3 generate_chart.py --type bar --data data.csv --output chart.png
    python3 generate_chart.py --type line --data data.csv --output line_chart.png
    python3 generate_chart.py --type pie --data data.csv --output pie_chart.png
    python3 generate_chart.py --type flowchart --input flowchart.mmd --output flowchart.png

Examples:
    generate_chart.py --type bar --data turbines.csv --output comparison.png
    generate_chart.py --type line --data generation.csv --output trend.png
    generate_chart.py --type pie --data investment.csv --output structure.png
    generate_chart.py --type flowchart --input process.mmd --output flowchart.png

Supports:
    - Bar charts (Python Matplotlib)
    - Line charts (Python Matplotlib)
    - Pie charts (Python Matplotlib)
    - Flowcharts (Mermaid)
"""

import sys
import argparse
import os
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate charts for engineering reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --type bar --data data.csv --output chart.png
  %(prog)s --type line --data data.csv --output trend.png
  %(prog)s --type pie --data data.csv --output structure.png
  %(prog)s --type flowchart --input flowchart.mmd --output flowchart.png
        '''
    )
    
    parser.add_argument('--type', required=True,
                      choices=['bar', 'line', 'pie', 'flowchart'],
                      help='Chart type to generate')
    parser.add_argument('--data', help='CSV data file (for bar/line/pie charts)')
    parser.add_argument('--input', help='Mermaid input file (for flowcharts)')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--title', help='Chart title')
    parser.add_argument('--xlabel', help='X-axis label (for bar/line charts)')
    parser.add_argument('--ylabel', help='Y-axis label (for bar/line charts)')
    parser.add_argument('--colors', help='Comma-separated colors (e.g., steelblue,coral)')
    parser.add_argument('--dpi', type=int, default=300, help='Output DPI (default: 300)')
    
    return parser.parse_args()


def read_csv_data(data_file):
    """Read data from CSV file."""
    try:
        return pd.read_csv(data_file)
    except FileNotFoundError:
        print(f"❌ Error: Data file not found: {data_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        sys.exit(1)


def generate_bar_chart(args, df):
    """Generate bar chart using Matplotlib."""
    if not MATPLOTLIB_AVAILABLE:
        print("❌ Error: matplotlib not installed. Install with: pip install matplotlib pandas")
        sys.exit(1)
    
    # Parse colors
    colors = args.colors.split(',') if args.colors else ['steelblue']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Generate bar chart
    for i, col in enumerate(df.columns[1:]):
        ax.bar(df.iloc[:, 0], df.iloc[:, i+1], color=colors[i % len(colors)], alpha=0.8, label=col)
    
    # Set labels and title
    if args.title:
        ax.set_title(args.title, fontsize=16, fontweight='bold')
    if args.xlabel:
        ax.set_xlabel(args.xlabel, fontsize=12)
    if args.ylabel:
        ax.set_ylabel(args.ylabel, fontsize=12)
    
    ax.legend(fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Save figure
    plt.tight_layout()
    plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Bar chart generated: {args.output}")


def generate_line_chart(args, df):
    """Generate line chart using Matplotlib."""
    if not MATPLOTLIB_AVAILABLE:
        print("❌ Error: matplotlib not installed. Install with: pip install matplotlib pandas")
        sys.exit(1)
    
    # Parse colors
    colors = args.colors.split(',') if args.colors else ['steelblue']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Generate line chart
    for i, col in enumerate(df.columns[1:]):
        ax.plot(df.iloc[:, 0], df.iloc[:, i+1], marker='o', linewidth=2, markersize=6, 
                label=col, color=colors[i % len(colors)])
    
    # Set labels and title
    if args.title:
        ax.set_title(args.title, fontsize=16, fontweight='bold')
    if args.xlabel:
        ax.set_xlabel(args.xlabel, fontsize=12)
    if args.ylabel:
        ax.set_ylabel(args.ylabel, fontsize=12)
    
    ax.legend(fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Save figure
    plt.tight_layout()
    plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Line chart generated: {args.output}")


def generate_pie_chart(args, df):
    """Generate pie chart using Matplotlib."""
    if not MATPLOTLIB_AVAILABLE:
        print("❌ Error: matplotlib not installed. Install with: pip install matplotlib pandas")
        sys.exit(1)
    
    # Parse colors and explode
    colors = args.colors.split(',') if args.colors else ['steelblue', 'coral', 'mediumseagreen', 'royalblue']
    explode = [0.05] + [0] * (len(df.columns[1:]) - 1)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Generate pie chart
    values = df.iloc[:, 1].values
    labels = df.iloc[:, 0].values
    
    ax.pie(values, labels=labels, colors=colors[:len(values)], autopct='%1.1f%%',
            startangle=90, explode=explode[:len(values)],
            textprops={'fontsize': 12})
    
    # Set title
    if args.title:
        ax.set_title(args.title, fontsize=16, fontweight='bold', pad=20)
    
    ax.axis('equal')
    ax.legend(loc='upper right', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
    
    # Save figure
    plt.tight_layout()
    plt.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Pie chart generated: {args.output}")


def generate_flowchart(args):
    """Generate flowchart from Mermaid input."""
    # Read Mermaid input
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            mermaid_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Mermaid input file not found: {args.input}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading Mermaid file: {e}")
        sys.exit(1)
    
    # Write output file with Mermaid content
    try:
        output_path = Path(args.output)
        # Change extension to .mmd if it's not already
        if output_path.suffix != '.mmd':
            print(f"ℹ️  Note: Flowchart output will be saved as .mmd file (Mermaid format)")
            mmd_path = output_path.with_suffix('.mmd')
        else:
            mmd_path = output_path
        
        with open(mmd_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_content)
        
        print(f"✅ Flowchart generated: {mmd_path}")
        print(f"ℹ️  To render as image, use Mermaid CLI or online tool:")
        print(f"ℹ️  https://mermaid.live")
        
    except Exception as e:
        print(f"❌ Error writing output file: {e}")
        sys.exit(1)


def main():
    """Main function."""
    args = parse_arguments()
    
    # Check if output directory exists
    output_dir = Path(args.output).parent
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created output directory: {output_dir}")
        except Exception as e:
            print(f"❌ Error creating output directory: {e}")
            sys.exit(1)
    
    # Generate chart based on type
    if args.type == 'flowchart':
        generate_flowchart(args)
    else:
        # Read data from CSV
        if not args.data:
            print("❌ Error: --data required for bar/line/pie charts")
            sys.exit(1)
        
        df = read_csv_data(args.data)
        
        if args.type == 'bar':
            generate_bar_chart(args, df)
        elif args.type == 'line':
            generate_line_chart(args, df)
        elif args.type == 'pie':
            generate_pie_chart(args, df)


if __name__ == "__main__":
    main()
