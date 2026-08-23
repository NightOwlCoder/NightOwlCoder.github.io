#!/usr/bin/env python3
"""Upload an image to X and print the media_id.

v2 /2/media/upload with multipart; falls back to the v1.1 upload host,
which still accepts OAuth1 multipart for images.
"""
import pathlib
import sys

import requests
from requests_oauthlib import OAuth1

SECRETS = pathlib.Path.home() / ".config" / "secrets"


def auth():
    read = lambda n: (SECRETS / n).read_text().strip()
    return OAuth1(
        read("twitter_api_key"),
        read("twitter_api_secret"),
        read("twitter_access_token"),
        read("twitter_access_token_secret"),
    )


def upload(path):
    a = auth()
    blob = pathlib.Path(path).read_bytes()
    for url, field in (
        ("https://api.x.com/2/media/upload", "media"),
        ("https://upload.twitter.com/1.1/media/upload.json", "media"),
    ):
        data = {"media_category": "tweet_image"} if "/2/media" in url else None
        r = requests.post(url, files={field: blob}, data=data, auth=a, timeout=90)
        if r.status_code in (200, 201):
            j = r.json()
            mid = j.get("data", {}).get("id") or j.get("media_id_string")
            if mid:
                print(f"{url} -> media_id {mid}")
                return mid
        print(f"{url} -> {r.status_code} {r.text[:160]}")
    return None


if __name__ == "__main__":
    mid = upload(sys.argv[1])
    sys.exit(0 if mid else 1)
