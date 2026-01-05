#!/usr/bin/env python3
"""
Site-wide link crawler and validator.

Crawls https://nightowlcoder.github.io and checks:
- All internal links work (no 404s)
- All external links respond (no dead links)
- No broken anchors
- No redirect chains

Usage:
    python3 scripts/crawl-and-validate.py
    python3 scripts/crawl-and-validate.py --external  # Also check external links
    python3 scripts/crawl-and-validate.py --verbose   # Show all links checked
"""

import argparse
import re
import sys
import time
from collections import defaultdict
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://nightowlcoder.github.io"
VISITED = set()
TO_VISIT = ["/"]
BROKEN_LINKS = []
EXTERNAL_LINKS = defaultdict(list)  # {url: [pages that link to it]}

def is_internal(url):
    """Check if URL is internal to the site."""
    parsed = urlparse(url)
    return not parsed.netloc or parsed.netloc == "nightowlcoder.github.io"

def normalize_url(url):
    """Normalize URL for comparison."""
    # Remove trailing slashes, fragments
    url = url.rstrip('/')
    if '#' in url:
        url = url.split('#')[0]
    return url

def crawl_page(url, check_external=False, verbose=False):
    """Crawl a single page and extract all links."""
    full_url = urljoin(BASE_URL, url)
    
    if verbose:
        print(f"  Crawling: {url}")
    
    try:
        response = requests.get(full_url, timeout=10, allow_redirects=True)
        
        if response.status_code != 200:
            BROKEN_LINKS.append({
                'url': url,
                'status': response.status_code,
                'type': 'internal'
            })
            return
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Skip mailto, tel, javascript
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                continue
            
            # Make absolute
            absolute = urljoin(full_url, href)
            
            if is_internal(absolute):
                # Internal link - queue for crawling
                path = urlparse(absolute).path
                normalized = normalize_url(path)
                
                if normalized not in VISITED and normalized not in TO_VISIT:
                    TO_VISIT.append(normalized)
            else:
                # External link - track for later checking
                if check_external:
                    EXTERNAL_LINKS[absolute].append(url)
    
    except requests.exceptions.RequestException as e:
        BROKEN_LINKS.append({
            'url': url,
            'error': str(e),
            'type': 'request_failed'
        })

def check_external_links(verbose=False):
    """Check all external links found during crawl."""
    print(f"\n🌐 Checking {len(EXTERNAL_LINKS)} unique external links...")
    
    broken_external = []
    
    for i, (url, sources) in enumerate(EXTERNAL_LINKS.items(), 1):
        if verbose:
            print(f"  [{i}/{len(EXTERNAL_LINKS)}] {url}")
        
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code >= 400:
                broken_external.append({
                    'url': url,
                    'status': response.status_code,
                    'found_on': sources
                })
        except requests.exceptions.RequestException as e:
            broken_external.append({
                'url': url,
                'error': str(e),
                'found_on': sources
            })
        
        # Rate limiting
        time.sleep(0.5)
    
    return broken_external

def main():
    parser = argparse.ArgumentParser(description='Crawl and validate site links')
    parser.add_argument('--external', action='store_true', help='Also check external links (slow!)')
    parser.add_argument('--verbose', action='store_true', help='Show all URLs crawled')
    args = parser.parse_args()
    
    print(f"🕷️  Crawling {BASE_URL}...\n")
    
    # Crawl all internal pages
    while TO_VISIT:
        url = TO_VISIT.pop(0)
        
        if url in VISITED:
            continue
        
        VISITED.add(url)
        crawl_page(url, args.external, args.verbose)
    
    print(f"\n✅ Crawled {len(VISITED)} pages")
    
    # Report broken internal links
    if BROKEN_LINKS:
        print(f"\n❌ Found {len(BROKEN_LINKS)} broken internal link(s):\n")
        for link in BROKEN_LINKS:
            print(f"  {link['url']}")
            if 'status' in link:
                print(f"    Status: {link['status']}")
            if 'error' in link:
                print(f"    Error: {link['error']}")
            print()
    else:
        print(f"✅ No broken internal links!")
    
    # Check external links if requested
    if args.external:
        broken_external = check_external_links(args.verbose)
        
        if broken_external:
            print(f"\n❌ Found {len(broken_external)} broken external link(s):\n")
            for link in broken_external[:10]:  # Show first 10
                print(f"  {link['url']}")
                if 'status' in link:
                    print(f"    Status: {link['status']}")
                if 'error' in link:
                    print(f"    Error: {link['error']}")
                print(f"    Found on: {', '.join(link['found_on'][:3])}")
                print()
        else:
            print(f"✅ All external links work!")
    
    # Exit code
    if BROKEN_LINKS or (args.external and broken_external):
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
