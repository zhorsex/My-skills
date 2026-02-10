#!/usr/bin/env python3
"""
资料缓存管理脚本 (Cache Manager Script)

Usage:
    python3 cache_manager.py --help
    python3 cache_manager.py --query "生态修复规范" --search-path cache/
    python3 cache_manager.py --add --name "生态修复规范" --content "...content..." --cache-path cache/
    python3 cache_manager.py --list --cache-path cache/
    python3 cache_manager.py --update --id CACHE001 --content "...updated content..." --cache-path cache/
    python3 cache_manager.py --delete --id CACHE001 --cache-path cache/
    python3 cache_manager.py --cleanup --days 30 --cache-path cache/

Examples:
    cache_manager.py --query "GB/T 31084-2014"
    cache_manager.py --add --name "风电技术规范" --file standard.txt --tags "风电,标准"
    cache_manager.py --list --category engineering-standards
    cache_manager.py --cleanup --days 30

Features:
    - Query cached data by keyword
    - Add new cache entries
    - List cached entries
    - Update existing entries
    - Delete cache entries
    - Cleanup expired cache
"""

import sys
import argparse
import json
import os
from pathlib import Path
from datetime import datetime, timedelta


CACHE_FILE = 'cache_index.json'
DEFAULT_CACHE_PATH = 'iteration/cache/'


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Manage cached reference materials',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s --query "生态修复规范"
  %(prog)s --add --name "GB/T 31084-2014" --file standard.txt --tags "风电,标准"
  %(prog)s --list --category engineering-standards
  %(prog)s --cleanup --days 30
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query cache by keyword')
    query_parser.add_argument('keyword', help='Search keyword')
    query_parser.add_argument('--cache-path', default=DEFAULT_CACHE_PATH, help='Cache directory path')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add new cache entry')
    add_parser.add_argument('--name', required=True, help='Entry name')
    add_parser.add_argument('--content', help='Content text (or use --file)')
    add_parser.add_argument('--file', help='Content file path')
    add_parser.add_argument('--category', required=True, 
                          choices=['engineering-standards', 'technical-standards', 'industry-data', 'case-studies'],
                          help='Category (engineering-standards, technical-standards, industry-data, case-studies)')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    add_parser.add_argument('--cache-path', default=DEFAULT_CACHE_PATH, help='Cache directory path')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List cache entries')
    list_parser.add_argument('--category', 
                           choices=['engineering-standards', 'technical-standards', 'industry-data', 'case-studies'],
                           help='Filter by category')
    list_parser.add_argument('--tags', help='Filter by tags')
    list_parser.add_argument('--cache-path', default=DEFAULT_CACHE_PATH, help='Cache directory path')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update existing cache entry')
    update_parser.add_argument('--id', required=True, help='Entry ID (e.g., CACHE001)')
    update_parser.add_argument('--content', help='Updated content text (or use --file)')
    update_parser.add_argument('--file', help='Updated content file path')
    update_parser.add_argument('--cache-path', default=DEFAULT_CACHE_PATH, help='Cache directory path')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete cache entry')
    delete_parser.add_argument('--id', required=True, help='Entry ID to delete')
    delete_parser.add_argument('--cache-path', default=DEFAULT_CACHE_PATH, help='Cache directory path')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Cleanup expired cache entries')
    cleanup_parser.add_argument('--days', type=int, default=30, help='Expiration days (default: 30)')
    cleanup_parser.add_argument('--cache-path', default=DEFAULT_CACHE_PATH, help='Cache directory path')
    
    return parser.parse_args()


def load_cache_index(cache_path):
    """Load cache index from JSON file."""
    cache_index_path = Path(cache_path) / CACHE_FILE
    if not cache_index_path.exists():
        return {}
    
    try:
        with open(cache_index_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading cache index: {e}")
        return {}


def save_cache_index(cache_path, cache_index):
    """Save cache index to JSON file."""
    cache_index_path = Path(cache_path) / CACHE_FILE
    try:
        with open(cache_index_path, 'w', encoding='utf-8') as f:
            json.dump(cache_index, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"❌ Error saving cache index: {e}")
        return False


def query_cache(args):
    """Query cache by keyword."""
    cache_index = load_cache_index(args.cache_path)
    
    keyword = args.keyword.lower()
    results = []
    
    for entry_id, entry_data in cache_index.items():
        if keyword in entry_data.get('name', '').lower() or \
           keyword in entry_data.get('content', '').lower() or \
           any(keyword in tag.lower() for tag in entry_data.get('tags', [])):
            results.append((entry_id, entry_data))
    
    if results:
        print(f"✅ Found {len(results)} matching entries:\n")
        for entry_id, entry_data in results:
            print(f"  ID: {entry_id}")
            print(f"  Name: {entry_data.get('name', '')}")
            print(f"  Category: {entry_data.get('category', '')}")
            print(f"  Cached: {entry_data.get('cached_date', '')}")
            print(f"  Expires: {entry_data.get('expiry_date', '')}")
            print(f"  Hits: {entry_data.get('hits', 0)}")
            print(f"  Score: {entry_data.get('score', 0)}")
            print()
    else:
        print(f"ℹ️  No entries found matching: {args.keyword}")


def add_cache_entry(args):
    """Add new cache entry."""
    cache_index = load_cache_index(args.cache_path)
    
    # Generate new ID
    if cache_index:
        max_id = max(int(k.replace('CACHE', '')) for k in cache_index.keys() if k.startswith('CACHE'))
        new_id = f"CACHE{max_id + 1:03d}"
    else:
        new_id = "CACHE001"
    
    # Read content from file or use provided content
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
    else:
        content = args.content if args.content else ""
    
    # Parse tags
    tags = [tag.strip() for tag in args.tags.split(',')] if args.tags else []
    
    # Calculate expiry date (default 30 days)
    expiry_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Create entry
    entry = {
        'name': args.name,
        'content': content,
        'category': args.category,
        'tags': tags,
        'cached_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'expiry_date': expiry_date,
        'hits': 0,
        'score': 0
    }
    
    # Add to index
    cache_index[new_id] = entry
    
    # Save index
    if save_cache_index(args.cache_path, cache_index):
        print(f"✅ Cache entry added: {new_id}")
        print(f"  Name: {entry['name']}")
        print(f"  Category: {entry['category']}")
        print(f"  Expiry: {entry['expiry_date']}")


def list_cache_entries(args):
    """List cache entries."""
    cache_index = load_cache_index(args.cache_path)
    
    # Filter by category and tags if specified
    results = []
    for entry_id, entry_data in cache_index.items():
        if args.category and entry_data.get('category') != args.category:
            continue
        if args.tags:
            filter_tags = [tag.strip().lower() for tag in args.tags.split(',')]
            entry_tags = [tag.lower() for tag in entry_data.get('tags', [])]
            if not any(tag in entry_tags for tag in filter_tags):
                continue
        results.append((entry_id, entry_data))
    
    if results:
        print(f"✅ Found {len(results)} entries:\n")
        for entry_id, entry_data in sorted(results, key=lambda x: x[1].get('cached_date', ''), reverse=True):
            print(f"  ID: {entry_id}")
            print(f"  Name: {entry_data.get('name', '')}")
            print(f"  Category: {entry_data.get('category', '')}")
            print(f"  Tags: {', '.join(entry_data.get('tags', []))}")
            print(f"  Cached: {entry_data.get('cached_date', '')}")
            print(f"  Expires: {entry_data.get('expiry_date', '')}")
            print(f"  Hits: {entry_data.get('hits', 0)}")
            print(f"  Score: {entry_data.get('score', 0)}")
            print()
    else:
        print("ℹ️  No cache entries found matching criteria")


def update_cache_entry(args):
    """Update existing cache entry."""
    cache_index = load_cache_index(args.cache_path)
    
    if args.id not in cache_index:
        print(f"❌ Error: Entry ID not found: {args.id}")
        return
    
    # Read content from file or use provided content
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
    else:
        content = args.content if args.content else cache_index[args.id].get('content', '')
    
    # Update entry
    cache_index[args.id]['content'] = content
    cache_index[args.id]['updated_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save index
    if save_cache_index(args.cache_path, cache_index):
        print(f"✅ Cache entry updated: {args.id}")


def delete_cache_entry(args):
    """Delete cache entry."""
    cache_index = load_cache_index(args.cache_path)
    
    if args.id not in cache_index:
        print(f"❌ Error: Entry ID not found: {args.id}")
        return
    
    # Delete entry
    entry_name = cache_index[args.id].get('name', '')
    del cache_index[args.id]
    
    # Save index
    if save_cache_index(args.cache_path, cache_index):
        print(f"✅ Cache entry deleted: {args.id} ({entry_name})")


def cleanup_expired_cache(args):
    """Cleanup expired cache entries."""
    cache_index = load_cache_index(args.cache_path)
    
    # Find expired entries
    expired_ids = []
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    for entry_id, entry_data in cache_index.items():
        expiry_date = entry_data.get('expiry_date', '')
        if expiry_date < current_date:
            expired_ids.append(entry_id)
    
    if expired_ids:
        for entry_id in expired_ids:
            del cache_index[entry_id]
        
        if save_cache_index(args.cache_path, cache_index):
            print(f"✅ Cleaned up {len(expired_ids)} expired entries")
            print(f"   Expiration threshold: {args.days} days")
            print(f"   Cleanup date: {current_date}")
    else:
        print(f"ℹ️  No expired entries (threshold: {args.days} days)")


def main():
    """Main function."""
    args = parse_arguments()
    
    # Ensure cache directory exists
    cache_dir = Path(args.cache_path)
    if not cache_dir.exists():
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created cache directory: {cache_dir}")
        except Exception as e:
            print(f"❌ Error creating cache directory: {e}")
            sys.exit(1)
    
    # Execute command
    if args.command == 'query':
        query_cache(args)
    elif args.command == 'add':
        add_cache_entry(args)
    elif args.command == 'list':
        list_cache_entries(args)
    elif args.command == 'update':
        update_cache_entry(args)
    elif args.command == 'delete':
        delete_cache_entry(args)
    elif args.command == 'cleanup':
        cleanup_expired_cache(args)
    else:
        print("❌ Error: No command specified. Use --help for usage.")


if __name__ == "__main__":
    main()
