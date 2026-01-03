#!/usr/bin/env python3
"""
Validate posted tweets - read back what was actually tweeted.

Usage:
    python3 scripts/validate-tweets.py                 # Show last 5 tweets
    python3 scripts/validate-tweets.py --count 10      # Show last 10 tweets
    python3 scripts/validate-tweets.py --check-links   # Validate all URLs work
"""

import os
import sys
import argparse
import tweepy
import re
from datetime import datetime

def get_twitter_client():
    """Get authenticated Twitter client."""
    api_key = os.environ.get('TWITTER_API_KEY')
    api_secret = os.environ.get('TWITTER_API_SECRET')
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("❌ Missing Twitter credentials!")
        sys.exit(1)
    
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

def get_my_tweets(client, count=5):
    """Get my recent tweets."""
    try:
        # Get authenticated user's ID
        me = client.get_me()
        user_id = me.data.id
        
        # Get recent tweets
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=count,
            tweet_fields=['created_at', 'conversation_id']
        )
        
        return tweets.data if tweets.data else []
    except Exception as e:
        print(f"❌ Error fetching tweets: {e}")
        return []

def check_for_placeholders(tweet_text):
    """Check for common placeholders that shouldn't be in tweets."""
    issues = []
    
    if '[LINK]' in tweet_text:
        issues.append("Contains [LINK] placeholder")
    
    if '[URL]' in tweet_text:
        issues.append("Contains [URL] placeholder")
    
    if '[IMAGE]' in tweet_text:
        issues.append("Contains [IMAGE] placeholder")
    
    # Check for broken URLs
    if 'nightowlcoder.github.io' in tweet_text:
        urls = re.findall(r'https://nightowlcoder\.github\.io/[^\s\)]+', tweet_text)
        for url in urls:
            if url.endswith('/'):
                issues.append(f"URL has trailing slash: {url}")
    
    return issues

def validate_tweet(tweet, index, check_links=False):
    """Validate a single tweet."""
    print(f"\n{'='*60}")
    print(f"Tweet #{index + 1}")
    print(f"ID: {tweet.id}")
    print(f"Posted: {tweet.created_at}")
    print(f"{'='*60}")
    print(f"\n{tweet.text}\n")
    
    # Check for issues
    issues = check_for_placeholders(tweet.text)
    
    if issues:
        print("⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ No issues detected")
        return True

def main():
    parser = argparse.ArgumentParser(description='Validate posted tweets')
    parser.add_argument('--count', type=int, default=5, help='Number of tweets to check')
    parser.add_argument('--check-links', action='store_true', help='Test if URLs actually work')
    args = parser.parse_args()
    
    client = get_twitter_client()
    tweets = get_my_tweets(client, args.count)
    
    if not tweets:
        print("No tweets found")
        return
    
    print(f"📊 Validating last {len(tweets)} tweets from @OwlCoder...\n")
    
    valid_count = 0
    for i, tweet in enumerate(tweets):
        if validate_tweet(tweet, i, args.check_links):
            valid_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ {valid_count}/{len(tweets)} tweets passed validation")
    
    if valid_count < len(tweets):
        print(f"⚠️  {len(tweets) - valid_count} tweets have issues!")
        sys.exit(1)

if __name__ == '__main__':
    main()
