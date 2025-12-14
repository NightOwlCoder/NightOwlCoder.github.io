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
    """Generate the full URL for a blog post."""
    filename = os.path.basename(filepath)
    slug = filename.replace('.md', '').replace('.markdown', '')
    match = re.match(r'^\d{4}-\d{2}-\d{2}-(.*)', slug)
    if match:
        title_slug = match.group(1)
        return f"https://nightowlcoder.github.io/{title_slug}/"
    return f"https://nightowlcoder.github.io/{slug}/"

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
    
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

def post_thread(client, tweets, post_url):
    """Post a thread (multiple tweets as replies)."""
    try:
        previous_tweet_id = None
        
        for i, tweet_text in enumerate(tweets):
            # Replace [LINK] placeholder with actual URL
            tweet_text = tweet_text.replace('[LINK]', post_url)
            
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
        
    except Exception as e:
        print(f"Error posting thread: {e}")
        return False

def post_single_tweet(client, post_data, post_url):
    """Post a single tweet for the post."""
    try:
        tweet = f"📝 New post: {post_data['title']}\n\n{post_url}"
        
        if post_data['hashtags']:
            hashtag_str = ' '.join(f"#{tag.lstrip('#')}" for tag in post_data['hashtags'][:4])
            if len(tweet) + len(hashtag_str) + 2 <= 280:
                tweet += f"\n\n{hashtag_str}"
        
        response = client.create_tweet(text=tweet)
        print(f"✓ Tweet posted successfully! (ID: {response.data['id']})")
        return True
        
    except Exception as e:
        print(f"Error posting tweet: {e}")
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
        
        post_url = get_post_url(post_file)
        
        # Check for thread file
        thread_file = get_thread_file(post_file)
        
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
