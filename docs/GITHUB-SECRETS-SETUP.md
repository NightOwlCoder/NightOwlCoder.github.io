# Setting Up GitHub Secrets for Auto-Tweet

Once you have your 4 X (Twitter) API credentials from the previous guide, follow these steps to add them to GitHub.

## Step 1: Go to Your Repository Settings

1. Open your browser and go to: **https://github.com/NightOwlCoder/NightOwlCoder.github.io**
2. Click the **"Settings"** tab (far right)
3. In the left sidebar, click **"Secrets and variables"** → **"Actions"**

## Step 2: Add Each Secret

You need to add 4 secrets. For each one:

1. Click **"New repository secret"** button
2. Enter the **Name** (exactly as shown below)
3. Paste the corresponding **Value** from your X API credentials
4. Click **"Add secret"**

### Secret 1: TWITTER_API_KEY
- **Name**: `TWITTER_API_KEY`
- **Value**: Your API Key (also called Consumer Key)

### Secret 2: TWITTER_API_SECRET
- **Name**: `TWITTER_API_SECRET`
- **Value**: Your API Key Secret (also called Consumer Secret)

### Secret 3: TWITTER_ACCESS_TOKEN
- **Name**: `TWITTER_ACCESS_TOKEN`
- **Value**: Your Access Token

### Secret 4: TWITTER_ACCESS_TOKEN_SECRET
- **Name**: `TWITTER_ACCESS_TOKEN_SECRET`
- **Value**: Your Access Token Secret

## Step 3: Verify All Secrets Are Added

After adding all 4 secrets, you should see them listed:
- ✓ TWITTER_API_KEY
- ✓ TWITTER_API_SECRET
- ✓ TWITTER_ACCESS_TOKEN
- ✓ TWITTER_ACCESS_TOKEN_SECRET

**Note**: You won't be able to see the secret values after saving them (for security), but that's normal!

## ✅ You're Done!

The automation is now set up. Here's what happens next:

1. You create a new blog post in `_posts/`
2. Add an `excerpt:` field to your front matter (optional but recommended)
3. Commit and push to GitHub
4. GitHub Actions automatically tweets your new post! 🎉

---

## How to Add an Excerpt to Your Posts

When creating a blog post, add an `excerpt:` field to the front matter like this:

```yaml
---
layout: post
title: "Your Post Title"
date: 2025-10-25 19:50:00 -0700
categories: category1 category2
excerpt: "A short 1-2 sentence summary that will appear in the tweet"
---
```

**Without excerpt**: Tweet will just have title + link  
**With excerpt**: Tweet will have title + your custom summary + link

---

## Testing the Automation

Want to test it? Here's how:

1. Create a simple test post in `_posts/`
2. Add an excerpt
3. Commit and push
4. Go to your repo → **Actions** tab
5. Watch the workflow run
6. Check your Twitter feed! (@OwlCoder)

If something goes wrong, check the Actions logs for error messages.
