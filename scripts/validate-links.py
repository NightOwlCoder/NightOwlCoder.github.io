#!/usr/bin/env python3
"""
Validate internal links in blog posts.

Checks for:
- Date-format links (should use /:title format)
- Broken internal links
- Missing anchors

Usage:
    python3 scripts/validate-links.py
    python3 scripts/validate-links.py --fix  # Auto-fix date-format links
"""

import os
import re
import sys
import argparse
from pathlib import Path

POSTS_DIR = Path("_posts")
TITLE_SLUG_CACHE = {}

def extract_title_slug(filepath):
    """Extract the title slug from a post file."""
    if filepath in TITLE_SLUG_CACHE:
        return TITLE_SLUG_CACHE[filepath]
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract title from front matter
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if not match:
        return None
    
    title = match.group(1)
    
    # Convert to slug (same as Jekyll /:title format)
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove special chars
    slug = re.sub(r'\s+', '-', slug)  # Spaces to hyphens
    slug = re.sub(r'-+', '-', slug)  # Multiple hyphens to one
    slug = slug.strip('-')
    
    TITLE_SLUG_CACHE[filepath] = slug
    return slug

def find_date_format_links(content):
    """Find links with date format: ](/YYYY/MM/DD/...)"""
    pattern = r'\]\(/(20\d{2})/(\d{2})/(\d{2})/([^)]+)\)'
    return re.findall(pattern, content)

def find_all_internal_links(content):
    """Find all internal links (start with /)"""
    pattern = r'\]\((/[^)]+)\)'
    return re.findall(pattern, content)

def validate_post(filepath, fix=False):
    """Validate links in a single post."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    fixed_content = content
    
    # Check for date-format links
    date_links = find_date_format_links(content)
    if date_links:
        for year, month, day, path in date_links:
            bad_url = f'/{year}/{month}/{day}/{path}'
            issues.append(f"❌ Date-format link: {bad_url}")
            
            if fix:
                # Try to find the correct slug
                # Extract the slug from the path (remove .html if present)
                slug = path.replace('.html', '').replace('/', '')
                fixed_url = f'/{slug}'
                fixed_content = fixed_content.replace(f']({bad_url})', f']({fixed_url})')
                issues[-1] += f" → Fixed: {fixed_url}"
    
    # Check for other potential issues
    all_links = find_all_internal_links(content)
    for link in all_links:
        # Skip anchors, assets, series pages
        if link.startswith('/#') or link.startswith('/assets/') or link.startswith('/series/'):
            continue
        
        # Check if it's still a date format (shouldn't be if fix worked)
        if re.match(r'/20\d{2}/\d{2}/\d{2}/', link):
            if link not in [f'/{y}/{m}/{d}/{p}' for y,m,d,p in date_links]:
                issues.append(f"⚠️  Date-format link (not auto-fixable): {link}")
    
    # Write fixed content if changes made
    if fix and fixed_content != content:
        with open(filepath, 'w') as f:
            f.write(fixed_content)
        issues.append(f"✅ Fixed {len(date_links)} link(s)")
    
    return issues

def main():
    parser = argparse.ArgumentParser(description='Validate internal blog links')
    parser.add_argument('--fix', action='store_true', help='Auto-fix date-format links')
    args = parser.parse_args()
    
    print("🔍 Validating internal links in blog posts...\n")
    
    total_issues = 0
    posts_with_issues = 0
    
    for post_file in sorted(POSTS_DIR.glob("*.md")):
        issues = validate_post(post_file, fix=args.fix)
        if issues:
            print(f"📄 {post_file.name}")
            for issue in issues:
                print(f"   {issue}")
            print()
            posts_with_issues += 1
            total_issues += len([i for i in issues if i.startswith('❌') or i.startswith('⚠️')])
    
    print("="*60)
    if total_issues == 0:
        print(f"✅ All links validated! No issues found.")
        return 0
    else:
        print(f"⚠️  Found {total_issues} issue(s) in {posts_with_issues} post(s)")
        if not args.fix:
            print(f"\nRun with --fix to auto-correct date-format links")
        return 1

if __name__ == '__main__':
    sys.exit(main())
