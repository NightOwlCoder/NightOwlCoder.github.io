#!/usr/bin/env python3
"""
Local tweet script for when GitHub Actions is blocked by Cloudflare.
Run from: ~/fileZ/projZ/blog

Usage:
    python3 scripts/tweet-local.py                    # Posts pending thread
    python3 scripts/tweet-local.py --dry-run          # Preview without posting
    python3 scripts/tweet-local.py --thread <file>    # Post specific thread file
"""

import os
import sys
import argparse
import tweepy

# You'll need to set these environment variables or hardcode them
# export TWITTER_API_KEY="..."
# export TWITTER_API_SECRET="..."
# export TWITTER_ACCESS_TOKEN="..."
# export TWITTER_ACCESS_TOKEN_SECRET="..."

def get_client():
    """Get authenticated Twitter client."""
    api_key = os.environ.get('TWITTER_API_KEY')
    api_secret = os.environ.get('TWITTER_API_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("❌ Missing Twitter credentials!")
        print("Set these environment variables:")
        print("  export TWITTER_API_KEY='...'")
        print("  export TWITTER_API_SECRET='...'")
        print("  export TWITTER_ACCESS_TOKEN='...'")
        print("  export TWITTER_ACCESS_TOKEN_SECRET='...'")
        sys.exit(1)
    
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

def parse_thread(filepath):
    """Parse thread file into list of tweets."""
    with open(filepath, 'r') as f:
        content = f.read()
    tweets = [t.strip() for t in content.split('---TWEET---') if t.strip()]
    return tweets

def list_threads():
    """List available thread files."""
    threads_dir = '_threads'
    if not os.path.exists(threads_dir):
        print(f"❌ No {threads_dir}/ directory found")
        return []
    
    files = [f for f in os.listdir(threads_dir) if f.endswith('.txt')]
    return sorted(files)

def post_thread(client, tweets, dry_run=False):
    """Post a thread."""
    print(f"\n🧵 Thread has {len(tweets)} tweets\n")
    
    previous_tweet_id = None
    
    for i, tweet_text in enumerate(tweets):
        # Truncate if needed
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."
        
        print(f"--- Tweet {i+1}/{len(tweets)} ({len(tweet_text)} chars) ---")
        print(tweet_text)
        print()
        
        if not dry_run:
            try:
                if previous_tweet_id:
                    response = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=previous_tweet_id)
                else:
                    response = client.create_tweet(text=tweet_text)
                
                previous_tweet_id = response.data['id']
                print(f"✅ Posted! ID: {previous_tweet_id}\n")
            except Exception as e:
                print(f"❌ Failed: {e}")
                return False
    
    if dry_run:
        print("🔍 DRY RUN - nothing was posted")
    else:
        print(f"🎉 Thread posted successfully!")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Post Twitter threads locally')
    parser.add_argument('--dry-run', action='store_true', help='Preview without posting')
    parser.add_argument('--thread', type=str, help='Specific thread file to post')
    parser.add_argument('--list', action='store_true', help='List available threads')
    args = parser.parse_args()
    
    # Change to blog directory if needed
    if os.path.exists('_threads'):
        pass  # Already in blog dir
    elif os.path.exists(os.path.expanduser('~/fileZ/projZ/blog/_threads')):
        os.chdir(os.path.expanduser('~/fileZ/projZ/blog'))
    else:
        print("❌ Can't find _threads/ directory")
        print("Run from ~/fileZ/projZ/blog or specify --thread path")
        sys.exit(1)
    
    if args.list:
        threads = list_threads()
        if threads:
            print("📋 Available threads:")
            for t in threads:
                print(f"  • {t}")
        return
    
    # Get thread file
    if args.thread:
        thread_file = args.thread
    else:
        # Default to consent-bypass (the pending one)
        thread_file = '_threads/2025-12-10-consent-bypass-indirect-execution.txt'
    
    if not os.path.exists(thread_file):
        print(f"❌ Thread file not found: {thread_file}")
        print("\nAvailable threads:")
        for t in list_threads():
            print(f"  • _threads/{t}")
        sys.exit(1)
    
    print(f"📄 Thread file: {thread_file}")
    tweets = parse_thread(thread_file)
    
    if not args.dry_run:
        client = get_client()
        print("✅ Twitter client authenticated")
    else:
        client = None
    
    post_thread(client, tweets, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
