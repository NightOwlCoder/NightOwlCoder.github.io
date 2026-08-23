#!/usr/bin/env python3
"""Post a thread file to X via the v2 endpoint.

tweepy's Client.create_tweet returns 401 against this app while a direct
OAuth1 POST to /2/tweets succeeds, so this talks to the endpoint directly.
Thread files are ---TWEET--- separated, same format as tweet-local.py.
"""
import argparse
import pathlib
import sys
import time

import requests
from requests_oauthlib import OAuth1

SECRETS = pathlib.Path.home() / ".config" / "secrets"
API = "https://api.x.com/2/tweets"
LIMIT = 280


def auth():
    read = lambda n: (SECRETS / n).read_text().strip()
    return OAuth1(
        read("twitter_api_key"),
        read("twitter_api_secret"),
        read("twitter_access_token"),
        read("twitter_access_token_secret"),
    )


def parse(path):
    parts = pathlib.Path(path).read_text().split("---TWEET---")
    return [p.strip() for p in parts if p.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--thread", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--image", help="image attached to the first tweet")
    args = ap.parse_args()

    tweets = parse(args.thread)
    over = [(i, len(t)) for i, t in enumerate(tweets, 1) if len(t) > LIMIT]
    if over:
        for i, n in over:
            print(f"tweet {i} is {n} chars, over {LIMIT}")
        sys.exit(1)

    print(f"{len(tweets)} tweets, all within {LIMIT}")
    if args.dry_run:
        for i, t in enumerate(tweets, 1):
            print(f"\n--- {i}/{len(tweets)} ({len(t)}) ---\n{t}")
        print("\ndry run, nothing posted")
        return

    a = auth()
    media_id = None
    if args.image:
        blob = pathlib.Path(args.image).read_bytes()
        up = requests.post(
            "https://api.x.com/2/media/upload",
            files={"media": blob},
            data={"media_category": "tweet_image"},
            auth=a,
            timeout=90,
        )
        if up.status_code not in (200, 201):
            print(f"media upload FAILED {up.status_code}: {up.text[:200]}")
            sys.exit(1)
        media_id = up.json()["data"]["id"]
        print(f"uploaded {args.image} -> {media_id}")

    reply_to = None
    posted = []
    for i, text in enumerate(tweets, 1):
        payload = {"text": text}
        if media_id and i == 1:
            payload["media"] = {"media_ids": [media_id]}
        if reply_to:
            payload["reply"] = {"in_reply_to_tweet_id": reply_to}
        r = requests.post(API, json=payload, auth=a, timeout=30)
        if r.status_code != 201:
            print(f"tweet {i} FAILED {r.status_code}: {r.text[:200]}")
            if posted:
                print("already posted:", ", ".join(posted))
            sys.exit(1)
        reply_to = r.json()["data"]["id"]
        posted.append(reply_to)
        print(f"{i}/{len(tweets)} posted {reply_to}")
        if i < len(tweets):
            time.sleep(2)

    print(f"\nthread live: https://x.com/OwlCoder/status/{posted[0]}")


if __name__ == "__main__":
    main()
