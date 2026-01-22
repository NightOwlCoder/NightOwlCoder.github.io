# Auto-Tweet Setup - Complete Guide

## 🎉 What's Been Set Up

I've created a fully automated system that will tweet every time you publish a new blog post. Here's what's in place:

### Files Created:

1. **`.github/workflows/auto-tweet-new-post.yml`**
   - GitHub Action that triggers on new posts
   - Runs automatically when you push to master branch

2. **`.github/scripts/tweet-new-post.py`**
   - Python script that posts the tweet
   - Extracts title and excerpt from your post
   - Formats the tweet nicely

3. **`docs/X-API-SETUP-GUIDE.md`**
   - Step-by-step guide to get Twitter API credentials

4. **`docs/GITHUB-SECRETS-SETUP.md`**
   - Instructions for adding credentials to GitHub

---

## 📝 How It Works

**Your normal workflow stays the same:**

1. Create blog post in `_posts/`
2. Write content in markdown
3. Commit and push to GitHub

**What happens automatically:**

4. GitHub Actions detects the new post
5. Extracts title and excerpt
6. Posts tweet: "📝 New post: [Title] [Excerpt] [URL]"
7. Done! ✨

---

## ✅ Next Steps (Your To-Do List)

### Step 1: Get Twitter API Credentials (5-10 minutes)
📄 Follow: `docs/X-API-SETUP-GUIDE.md`

You'll get 4 values:
- API Key
- API Key Secret  
- Access Token
- Access Token Secret

### Step 2: Add Secrets to GitHub (2 minutes)
📄 Follow: `docs/GITHUB-SECRETS-SETUP.md`

Add the 4 credentials to your GitHub repository secrets.

### Step 3: Test It! (optional)
Create a test blog post with an excerpt to see it work.

---

## 📋 Blog Post Format

**Add an `excerpt` field to your front matter:**

```yaml
---
layout: post
title: "Your Awesome Post Title"
date: 2025-10-25 19:50:00 -0700
categories: category1 category2
excerpt: "A short 1-2 sentence summary for the tweet"
---
```

**Example tweet that will be posted:**
```
📝 New post: Your Awesome Post Title

A short 1-2 sentence summary for the tweet

https://nightowlcoder.kovadj.dev/your-awesome-post-title
```

**If you don't add an excerpt:**
```
📝 New post: Your Awesome Post Title

https://nightowlcoder.kovadj.dev/your-awesome-post-title
```

---

## 🔍 How to Check if It Worked

After pushing a new post:

1. Go to: https://github.com/NightOwlCoder/NightOwlCoder.github.io/actions
2. Click on the latest workflow run
3. Watch it execute (takes ~30 seconds)
4. Check your Twitter (@OwlCoder) for the new tweet!

---

## 🐛 Troubleshooting

**Workflow doesn't run?**
- Make sure you pushed to the `master` branch
- Check that your post is in `_posts/` directory
- Verify GitHub Actions are enabled in your repo settings

**Tweet doesn't post?**
- Check the workflow logs in the Actions tab
- Verify all 4 secrets are correctly added
- Make sure your Twitter app has "Read and Write" permissions

**Tweet looks weird?**
- Check your excerpt length (keep it under 100-150 chars for best results)
- Make sure your post has valid front matter with title

---

## 🎯 Benefits

✅ **Never forget to promote** - Automatic on every push  
✅ **Consistent format** - Every tweet looks professional  
✅ **Zero extra work** - Part of your normal workflow  
✅ **Custom excerpts** - You control the message  
✅ **Full automation** - Set it and forget it  

---

## 📚 Quick Reference

| File | Purpose |
|------|---------|
| `.github/workflows/auto-tweet-new-post.yml` | GitHub Action workflow |
| `.github/scripts/tweet-new-post.py` | Tweet posting script |
| `docs/X-API-SETUP-GUIDE.md` | Get Twitter credentials |
| `docs/GITHUB-SECRETS-SETUP.md` | Add credentials to GitHub |

---

**Ready to get started? Follow Step 1 in the X-API-SETUP-GUIDE.md!**
