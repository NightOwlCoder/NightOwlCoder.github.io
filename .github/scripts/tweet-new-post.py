#!/usr/bin/env python3
"""
Script to automatically tweet new blog posts.
Supports both single tweets and threads (from _threads/ files).
"""

import os
import re
import subprocess
import sys
import yaml
import tweepy

def get_new_or_modified_posts():
    """Get list of new or modified posts in the last commit."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True, text=True, check=True
        )
        files = result.stdout.strip().split('\n')
        posts = [f for f in files if f.startswith('_posts/') and f.endswith('.md')]
        return posts
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []

def parse_post(filepath):
    """Parse blog post to extract front matter."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
        
        front_matter = yaml.safe_load(match.group(1))
        categories = front_matter.get('categories', [])
        if isinstance(categories, str):
            categories = categories.split()
        
        hashtags = front_matter.get('hashtags', [])
        if isinstance(hashtags, str):
            hashtags = hashtags.split()
        
        return {
            'title': front_matter.get('title', 'Untitled'),
            'excerpt': front_matter.get('excerpt', ''),
            'categories': categories,
            'hashtags': hashtags,
            'filepath': filepath
        }
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None

def get_post_url(filepath):
    """Generate the full URL for a blog post.
    
    Uses permalink: /:title format (no date in URL).
    """
    filename = os.path.basename(filepath)
    # Extract slug from filename: YYYY-MM-DD-title-slug.md -> title-slug
    match = re.match(r'^\d{4}-\d{2}-\d{2}-(.*?)\.md$', filename)
    if match:
        title_slug = match.group(1)
        return f"https://nightowlcoder.github.io/{title_slug}"
    # Fallback - strip .md
    slug = filename.replace('.md', '').replace('.markdown', '')
    return f"https://nightowlcoder.github.io/{slug}"

def extract_url_from_thread(thread_path):
    """Extract URL from thread file if it contains one."""
    try:
        with open(thread_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Look for https://nightowlcoder.github.io URL in the content
        match = re.search(r'https://nightowlcoder.github.io/[^\s\)]+', content)
        if match:
            return match.group(0)
    except Exception:
        pass
    return None

def get_thread_file(post_filepath):
    """Check if a thread file exists for this post."""
    filename = os.path.basename(post_filepath).replace('.md', '.txt')
    thread_path = f"_threads/{filename}"
    if os.path.exists(thread_path):
        return thread_path
    return None

def parse_thread_file(thread_path):
    """Parse thread file into list of tweets."""
    with open(thread_path, 'r', encoding='utf-8') as f:
        content = f.read()
    tweets = [t.strip() for t in content.split('---TWEET---') if t.strip()]
    return tweets

def get_twitter_client():
    """Get authenticated Twitter client."""
    api_key = os.environ.get('TWITTER_API_KEY')
    api_secret = os.environ.get('TWITTER_API_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("Error: Missing Twitter API credentials")
        return None
    
    # Print partial keys for debugging (first 4 chars only)
    print(f"   API Key: {api_key[:4]}...")
    print(f"   Access Token: {access_token[:4]}...")
    
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

def post_thread(client, tweets, post_url):
    """Post a thread (multiple tweets as replies)."""
    try:
        # CRITICAL: Validate no [LINK] placeholders remain
        for i, tweet_text in enumerate(tweets):
            if '[LINK]' in tweet_text:
                print(f"❌ VALIDATION FAILED!")
                print(f"   Tweet {i+1} contains [LINK] placeholder!")
                print(f"   Text: {tweet_text[:100]}...")
                print(f"\n   This means the thread file has [LINK] but no actual URL.")
                print(f"   Fix the thread file to include the real URL!")
                return False
        
        previous_tweet_id = None
        
        for i, tweet_text in enumerate(tweets):
            
            # Truncate if too long (280 char limit)
            if len(tweet_text) > 280:
                tweet_text = tweet_text[:277] + "..."
            
            if previous_tweet_id:
                response = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=previous_tweet_id)
            else:
                response = client.create_tweet(text=tweet_text)
            
            previous_tweet_id = response.data['id']
            print(f"✓ Tweet {i+1}/{len(tweets)} posted (ID: {previous_tweet_id})")
        
        print(f"🧵 Thread posted successfully! ({len(tweets)} tweets)")
        return True
        
    except tweepy.errors.Forbidden as e:
        print(f"❌ 403 Forbidden Error!")
        print(f"   Error message: {e}")
        if hasattr(e, 'api_messages'):
            print(f"   API messages: {e.api_messages}")
        if hasattr(e, 'api_codes'):
            print(f"   API codes: {e.api_codes}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response text: {e.response.text}")
        return False
    except tweepy.errors.Unauthorized as e:
        print(f"❌ 401 Unauthorized Error!")
        print(f"   Error message: {e}")
        print("   → Check that API keys and tokens are correct")
        print("   → Verify app is attached to a Project in Developer Portal")
        return False
    except Exception as e:
        print(f"❌ Error posting thread: {type(e).__name__}: {e}")
        return False

def post_single_tweet(client, post_data, post_url):
    """Post a single tweet for the post."""
    try:
        # CRITICAL: Validate no [LINK] placeholders
        if '[LINK]' in post_url:
            print(f"❌ VALIDATION FAILED!")
            print(f"   URL contains [LINK] placeholder: {post_url}")
            return False
        
        tweet = f"📝 New post: {post_data['title']}\n\n{post_url}"
        
        if post_data['hashtags']:
            hashtag_str = ' '.join(f"#{tag.lstrip('#')}" for tag in post_data['hashtags'][:4])
            if len(tweet) + len(hashtag_str) + 2 <= 280:
                tweet += f"\n\n{hashtag_str}"
        
        response = client.create_tweet(text=tweet)
        print(f"✓ Tweet posted successfully! (ID: {response.data['id']})")
        return True
        
    except tweepy.errors.Forbidden as e:
        print(f"❌ 403 Forbidden Error!")
        print(f"   Error message: {e}")
        if hasattr(e, 'api_messages'):
            print(f"   API messages: {e.api_messages}")
        if hasattr(e, 'api_codes'):
            print(f"   API codes: {e.api_codes}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response text: {e.response.text}")
        return False
    except tweepy.errors.Unauthorized as e:
        print(f"❌ 401 Unauthorized Error!")
        print(f"   Error message: {e}")
        return False
    except Exception as e:
        print(f"❌ Error posting tweet: {type(e).__name__}: {e}")
        return False

def main():
    """Main function to detect new posts and tweet them."""
    print("Checking for new blog posts...")
    
    posts = get_new_or_modified_posts()
    
    if not posts:
        print("No new posts detected.")
        return 0
    
    print(f"Found {len(posts)} new/modified post(s)")
    
    client = get_twitter_client()
    if not client:
        return 1
    
    success_count = 0
    for post_file in posts:
        print(f"\nProcessing {post_file}...")
        
        post_data = parse_post(post_file)
        if not post_data:
            continue
        
        # Check for thread file
        thread_file = get_thread_file(post_file)
        
        # Try to get URL from thread file first, fall back to generated URL
        post_url = None
        if thread_file:
            post_url = extract_url_from_thread(thread_file)
            if post_url:
                print(f"   Using URL from thread file: {post_url}")
        
        if not post_url:
            post_url = get_post_url(post_file)
            print(f"   Generated URL: {post_url}")
        
        if thread_file:
            print(f"🧵 Thread file found: {thread_file}")
            tweets = parse_thread_file(thread_file)
            print(f"   {len(tweets)} tweets in thread")
            if post_thread(client, tweets, post_url):
                success_count += 1
        else:
            print("📝 No thread file, posting single tweet")
            if post_single_tweet(client, post_data, post_url):
                success_count += 1
    
    print(f"\n{'='*50}")
    print(f"✓ Successfully tweeted {success_count}/{len(posts)} post(s)")
    return 0 if success_count > 0 else 1

if __name__ == '__main__':
    sys.exit(main())
