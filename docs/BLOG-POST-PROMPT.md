# Blog Post Creation Prompt

**Copy and paste this entire prompt to any LLM when you want to create a blog post:**

---

# Instructions for Creating a NightOwlCoder Blog Post

You are helping create a new blog post for the NightOwlCoder blog (nightowlcoder.github.io). Follow these instructions carefully.

## Context Files to Read First

1. **Read `AGENTS.md`** - Contains comprehensive guidelines for blog post creation
2. **Read `README.md`** - Understanding the blog structure

## Your Task

Create a complete blog post following this workflow:

### Step 1: Gather Requirements
Ask the user:
- What topic should the post cover?
- Any specific points or code examples to include?

### Step 2: Create the Blog Post

Generate a complete blog post with:

**Front Matter (Required):**
```yaml
---
layout: post
title: "The Post Title"
date: YYYY-MM-DD HH:MM:SS -0700
categories: category1 category2
excerpt: "Compelling 1-2 sentence hook under 150 characters"
image: /assets/YYYY-MM-DD-slug-image.png
---
```

**Content:**
- Well-structured Markdown
- Code blocks with language specified
- Clear headings (##, ###)
- Practical examples

### Step 3: Image Selection

Analyze the post and recommend ONE of these options:

**Option 1: Code Screenshot** (for technical "how-to" posts)
- Suggest the user take a screenshot or use carbon.now.sh
- Or: Offer to create formatted code they can screenshot

**Option 2: AI-Generated Image** (for concept/explanation posts)
- Provide a DALL-E/Midjourney prompt like:
  ```
  "minimalist technical illustration of [topic], clean lines, 
   professional, dark background, tech theme, 16:9 aspect ratio"
  ```

**Option 3: Default Logo** (for opinion/discussion posts)
- Change image field to: `/assets/NightOwlCoderLogo.jpg`
- No additional work needed

**Ask the user which option they prefer.**

### Step 4: Finalize

Once image decision is made:

1. **Create the post file**: `_posts/YYYY-MM-DD-slug.md`
2. **Save image** (if custom): `assets/YYYY-MM-DD-slug-image.png`
3. **Show the user** what you created
4. **Remind them**: "Run `git add . && git commit -m 'Add blog post' && git push`"

## Critical Rules

✅ **DO:**
- Use proper filename format: `YYYY-MM-DD-slug.md`
- Keep excerpt under 150 characters
- Specify code block languages
- Use relative image paths: `../assets/image.png`
- Keep it bite-sized and guide the user step by step

❌ **DON'T:**
- Skip the excerpt field
- Forget to include an image field
- Use commas in categories list
- Create overly long excerpts
- Overwhelm the user with too many questions at once

## After Creation

The user will push to GitHub, and:
- 🐦 Auto-tweet posts to @OwlCoder within 60 seconds
- 🌐 Blog goes live on GitHub Pages
- 🎨 Custom image appears in Twitter preview card

## Example Interaction

**User:** "Create a post about Docker multi-stage builds"

**You:**
1. Read AGENTS.md and README.md
2. Ask: "Should I include a specific example or use case?"
3. Create the blog post with proper formatting
4. Suggest: "For the image, I recommend:
   - A diagram showing the build stages (DALL-E prompt: ...)
   - A screenshot of your Dockerfile
   - Or use the default logo
   Which do you prefer?"
5. Finalize based on their choice
6. Save everything and remind them to push

---

**That's it! Now help the user create their blog post following these instructions.**
