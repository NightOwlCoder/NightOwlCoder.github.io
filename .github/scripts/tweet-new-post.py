#!/usr/bin/env python3
"""
Script to automatically tweet new blog posts.
Detects new posts in _posts/ directory and tweets them with excerpt.
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
        # Get files changed in the last commit
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        
        files = result.stdout.strip().split('\n')
        # Filter for new posts in _posts directory
        posts = [f for f in files if f.startswith('_posts/') and f.endswith('.md')]
        
        return posts
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []

def parse_post(filepath):
    """Parse blog post to extract front matter and content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract front matter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            print(f"No front matter found in {filepath}")
            return None
        
        front_matter = yaml.safe_load(match.group(1))
        
        return {
            'title': front_matter.get('title', 'Untitled'),
            'excerpt': front_matter.get('excerpt', ''),
            'date': front_matter.get('date', ''),
            'filepath': filepath
        }
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None

def get_post_url(filepath):
    """Generate the full URL for a blog post from its filepath."""
    # Extract filename from path: _posts/2025-10-25-title.md -> 2025-10-25-title.md
    filename = os.path.basename(filepath)
    
    # Remove .md extension and convert to URL slug
    slug = filename.replace('.md', '').replace('.markdown', '')
    
    # The permalink in _config.yml is /:title which uses the slug without date
    # But let's extract just the title part (everything after YYYY-MM-DD-)
    match = re.match(r'^\d{4}-\d{2}-\d{2}-(.*)', slug)
    if match:
        slug = match.group(1)
    
    base_url = "https://nightowlcoder.github.io"
    return f"{base_url}/{slug}"

def create_tweet_text(post_data, post_url):
    """Create tweet text from post data."""
    title = post_data['title']
    excerpt = post_data['excerpt']
    
    # Start with title
    tweet = f"📝 New post: {title}\n\n"
    
    # Add excerpt if available
    if excerpt:
        # Trim excerpt if needed to fit in tweet (280 char limit)
        # Reserve space for title, URL, and formatting
        max_excerpt_length = 280 - len(tweet) - len(post_url) - 10  # 10 chars buffer
        
        if len(excerpt) > max_excerpt_length:
            excerpt = excerpt[:max_excerpt_length-3] + "..."
        
        tweet += f"{excerpt}\n\n"
    
    # Add URL
    tweet += post_url
    
    # Ensure total length doesn't exceed 280
    if len(tweet) > 280:
        # If still too long, trim the excerpt more aggressively
        excess = len(tweet) - 280
        if excerpt:
            trimmed_excerpt = excerpt[:len(excerpt)-excess-3] + "..."
            tweet = f"📝 New post: {title}\n\n{trimmed_excerpt}\n\n{post_url}"
    
    return tweet

def post_tweet(tweet_text):
    """Post tweet using Twitter API v2."""
    try:
        # Get credentials from environment
        api_key = os.environ.get('TWITTER_API_KEY')
        api_secret = os.environ.get('TWITTER_API_SECRET')
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        
        if not all([api_key, api_secret, access_token, access_token_secret]):
            print("Error: Missing Twitter API credentials")
            return False
        
        # Authenticate with Twitter API v2
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # Post tweet
        response = client.create_tweet(text=tweet_text)
        print(f"✓ Tweet posted successfully!")
        print(f"Tweet ID: {response.data['id']}")
        print(f"Tweet text: {tweet_text}")
        return True
        
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return False

def main():
    """Main function to detect new posts and tweet them."""
    print("Checking for new blog posts...")
    
    # Get new or modified posts
    posts = get_new_or_modified_posts()
    
    if not posts:
        print("No new posts detected.")
        return 0
    
    print(f"Found {len(posts)} new/modified post(s):")
    for post in posts:
        print(f"  - {post}")
    
    # Process each new post
    success_count = 0
    for post_file in posts:
        print(f"\nProcessing {post_file}...")
        
        # Parse post
        post_data = parse_post(post_file)
        if not post_data:
            print(f"Skipping {post_file} (couldn't parse)")
            continue
        
        # Generate URL
        post_url = get_post_url(post_file)
        
        # Create tweet text
        tweet_text = create_tweet_text(post_data, post_url)
        
        # Post tweet
        if post_tweet(tweet_text):
            success_count += 1
        else:
            print(f"Failed to tweet for {post_file}")
    
    print(f"\n{'='*50}")
    print(f"✓ Successfully tweeted {success_count}/{len(posts)} post(s)")
    return 0 if success_count > 0 else 1

if __name__ == '__main__':
    sys.exit(main())
