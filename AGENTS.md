# AI Agent Guide: Creating Blog Posts for NightOwlCoder

This guide explains how an AI assistant (LLM) can help create new blog posts for the NightOwlCoder blog.

## 🤖 Overview

This document provides a structured workflow for AI agents to assist in creating well-formatted Jekyll blog posts that integrate seamlessly with the existing site structure.

## 📋 Pre-Creation Checklist

Before creating a blog post, the AI agent should gather the following information:

### Required Information
- **Title**: The blog post title
- **Categories**: 1-3 relevant categories (e.g., java, kotlin, design-patterns, android)
- **Content**: The main body of the post in Markdown format

### Optional Information
- **Date/Time**: Specific publication date (defaults to current date/time)
- **Images**: Any images to include (will be saved to `assets/` folder)
- **Code Samples**: Programming language for syntax highlighting
- **External Links**: URLs to reference

## 🔧 Step-by-Step Workflow

### Step 1: Gather Information

**Example Prompts to Ask User:**
```
"What would you like to title your blog post?"
"What categories would you like to assign? (e.g., java, kotlin, design-patterns)"
"Do you have any images to include? If so, please provide them."
"What's the main content you'd like to write about?"
```

### Step 2: Generate Filename

Create filename using the pattern: `YYYY-MM-DD-slug.md`

**Rules:**
- Use current date or user-specified date
- Convert title to lowercase slug
- Replace spaces with hyphens
- Remove special characters (keep only a-z, 0-9, hyphens)
- Use `.md` or `.markdown` extension

**Example:**
```
Title: "Understanding Kotlin Coroutines"
Filename: 2024-01-15-understanding-kotlin-coroutines.md
```

**Code Logic:**
```python
from datetime import datetime
import re

def generate_filename(title, date=None):
    if date is None:
        date = datetime.now()
    
    # Create slug from title
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remove special chars
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
    slug = re.sub(r'-+', '-', slug)  # Remove multiple hyphens
    slug = slug.strip('-')  # Remove leading/trailing hyphens
    
    # Format: YYYY-MM-DD-slug.md
    return f"{date.strftime('%Y-%m-%d')}-{slug}.md"
```

### Step 3: Create Front Matter

Build the YAML front matter with proper formatting:

```yaml
---
layout: post
title: "Your Post Title Here"
date: YYYY-MM-DD HH:MM:SS -0800
categories: category1 category2 category3
---
```

**Rules:**
- `layout`: Always set to `post`
- `title`: Wrap in double quotes, escape any internal quotes
- `date`: Use ISO format with timezone (-0800 for PST/-0700 for PDT)
- `categories`: Space-separated list of categories (no commas)

**Date Format:**
```
Current timestamp in Pacific Time:
date: 2024-01-15 14:30:00 -0800
```

### Step 4: Format Content

Structure the content following these guidelines:

**Markdown Best Practices:**
```markdown
# Main Heading (H1)

## Section Heading (H2)

### Subsection Heading (H3)

Regular paragraph text here.

**Bold text** and *italic text*

- Bullet point 1
- Bullet point 2

1. Numbered item 1
2. Numbered item 2

`inline code`

```language
// Code block with syntax highlighting
public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

[Link text](https://example.com)

![Image alt text](../assets/image-name.png)
```

**Code Blocks:**
- Always specify the language for syntax highlighting
- Common languages: `java`, `kotlin`, `python`, `javascript`, `bash`, `yaml`
- Use triple backticks with language identifier

**Images:**
- Reference images using relative path: `../assets/image-name.png`
- Optionally add size: `![Alt text](../assets/image.png){:width="350px"}`
- Always include meaningful alt text

**External Links:**
- For external links that open in new tab:
  ```markdown
  [Link text<sup style="font-size: 20px;">⇗</sup>](https://example.com){:target="_blank"}
  ```

### Step 5: Handle Images

If the user provides images:

1. Save images to `NightOwlCoder.github.io/assets/` directory
2. Use descriptive filenames (e.g., `kotlin-coroutines-diagram.png`)
3. Common formats: PNG, JPG, GIF
4. Reference in post using: `![Description](../assets/filename.png)`

### Step 6: Create the Blog Post File

Write the complete file with:
1. Front matter (YAML)
2. Blank line
3. Content (Markdown)

**Complete File Example:**
```markdown
---
layout: post
title: "Understanding Kotlin Coroutines"
date: 2024-01-15 14:30:00 -0800
categories: kotlin android coroutines
---

# Understanding Kotlin Coroutines

Kotlin coroutines provide a way to write asynchronous code that looks synchronous...

## What are Coroutines?

Coroutines are lightweight threads...

### Example Code

```kotlin
import kotlinx.coroutines.*

fun main() = runBlocking {
    launch {
        delay(1000L)
        println("World!")
    }
    println("Hello,")
}
```

## Conclusion

Coroutines make async programming much easier...
```

### Step 7: Validation

Before finalizing, verify:

- [ ] Filename follows `YYYY-MM-DD-slug.md` pattern
- [ ] Front matter has all required fields
- [ ] Front matter uses proper YAML syntax (check indentation)
- [ ] Title is wrapped in double quotes
- [ ] Date includes timezone
- [ ] Categories are space-separated (no commas)
- [ ] Content is valid Markdown
- [ ] Code blocks specify language
- [ ] Image paths use relative notation (`../assets/`)
- [ ] All images exist in assets folder
- [ ] External links are properly formatted

### Step 8: Inform User

After creating the post, provide:
1. Confirmation message with filename
2. Path to the created file
3. Brief summary of the post
4. Next steps for publishing (git commit/push)

## 📝 Complete Example Workflow

### User Request
```
"Create a blog post about Java Streams API with some code examples"
```

### AI Agent Response Flow

**1. Gather Information:**
```
AI: "I'll create a blog post about Java Streams API. Let me gather some details:
- Title: 'Mastering Java Streams API'
- Categories: java, programming, streams
- Would you like me to include any specific topics or examples?"

User: "Yes, include map, filter, and reduce operations"
```

**2. Create Filename:**
```
Filename: 2024-01-15-mastering-java-streams-api.md
```

**3. Generate Content Structure:**
```markdown
---
layout: post
title: "Mastering Java Streams API"
date: 2024-01-15 16:45:00 -0800
categories: java programming streams
---

# Mastering Java Streams API

## Introduction
The Java Streams API, introduced in Java 8, revolutionized how we process collections...

## Key Operations

### Map Operation
The `map` operation transforms each element...

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> squared = numbers.stream()
    .map(n -> n * n)
    .collect(Collectors.toList());
```

### Filter Operation
The `filter` operation selects elements based on a predicate...

```java
List<Integer> evenNumbers = numbers.stream()
    .filter(n -> n % 2 == 0)
    .collect(Collectors.toList());
```

### Reduce Operation
The `reduce` operation combines elements...

```java
int sum = numbers.stream()
    .reduce(0, Integer::sum);
```

## Conclusion
Java Streams provide a powerful, declarative way to process data...
```

**4. Create the File:**
```
AI: "I've created your blog post at:
NightOwlCoder.github.io/_posts/2024-01-15-mastering-java-streams-api.md

The post covers:
- Introduction to Java Streams API
- Map, Filter, and Reduce operations with examples
- Conclusion and best practices

To publish:
1. Review the content
2. Run `git add .`
3. Run `git commit -m 'Add Java Streams API blog post'`
4. Run `git push origin master`
5. Wait 2-5 minutes for GitHub Pages to rebuild

Would you like me to make any changes to the post?"
```

## ⚠️ Common Pitfalls to Avoid

### 1. Incorrect Filename Format
❌ Wrong: `my-blog-post.md`, `2024-1-5-post.md`, `jan-15-post.md`
✅ Correct: `2024-01-15-my-blog-post.md`

### 2. Malformed Front Matter
❌ Wrong:
```yaml
---
layout: post
title: My Post (no quotes for title with special chars)
date: 2024-01-15 (missing time and timezone)
categories: java, kotlin, android (commas not allowed)
---
```

✅ Correct:
```yaml
---
layout: post
title: "My Post: A Guide"
date: 2024-01-15 14:30:00 -0800
categories: java kotlin android
---
```

### 3. Broken Image Paths
❌ Wrong: `/assets/image.png`, `assets/image.png`, `./assets/image.png`
✅ Correct: `../assets/image.png`

### 4. Missing Language in Code Blocks
❌ Wrong:
```
public class Example { }
```

✅ Correct:
```java
public class Example { }
```

### 5. Incorrect Date Format
❌ Wrong: `2024-01-15` (missing time), `01/15/2024 2:30pm` (wrong format)
✅ Correct: `2024-01-15 14:30:00 -0800`

## 🧪 Testing Recommendations

After creating a post, suggest the user:

1. **Test Locally** (if they have Jekyll installed):
   ```bash
   cd NightOwlCoder.github.io
   bundle exec jekyll serve
   ```
   Then check `http://localhost:4000`

2. **Validate Markdown**:
   - Check that headings render correctly
   - Verify code blocks have syntax highlighting
   - Ensure images display properly
   - Test all links

3. **Check Front Matter**:
   - Run `jekyll build` to catch YAML errors
   - Verify date is in correct timezone

## 🎯 Best Practices for AI Agents

1. **Always confirm details with user before creating**
2. **Provide examples when asking for input**
3. **Validate all paths and filenames**
4. **Use existing posts as reference for style/format**
5. **Offer to preview content before finalizing**
6. **Explain next steps clearly (git commands)**
7. **Be prepared to make edits based on feedback**
8. **Check existing categories to maintain consistency**

## 📚 Quick Reference

### Categories Used in Existing Posts
- `java`
- `kotlin`
- `android`
- `design-patterns`
- `dagger`
- `flutter`
- `learning`
- `mdlive`
- `xaml`

### Timezone
- Use `-0800` (PST) or `-0700` (PDT) depending on season

### File Location
- All posts go in: `NightOwlCoder.github.io/_posts/`
- All images go in: `NightOwlCoder.github.io/assets/`
- Static pages go in: `NightOwlCoder.github.io/_pages/` (e.g., about, archive, custom pages)

### Deployment
- Push to `master` branch
- GitHub Pages auto-deploys in 2-5 minutes
- No manual build needed

---

## 🐦 Auto-Tweet Feature

### Overview

This blog automatically posts to Twitter ([@OwlCoder](https://twitter.com/OwlCoder)) when new posts are pushed to GitHub.

### Required Fields for Auto-Tweet

```yaml
---
layout: post
title: "Your Post Title"
date: 2025-10-25 21:00:00 -0700
categories: category1 category2
excerpt: "A compelling 1-2 sentence summary for the tweet"
image: /assets/post-specific-image.png  # Optional but recommended
---
```

### Writing Good Excerpts

The `excerpt` field is crucial for auto-tweets. Best practices:

1. **Length**: Keep under 150 characters for best results
2. **Hook**: Start with a problem, question, or intriguing statement
3. **Clarity**: Be specific about what the post covers
4. **Action**: Use active voice and strong verbs
5. **Avoid**: Don't repeat the title word-for-word

**Good Examples:**
```yaml
excerpt: "AI coding assistants get stuck waiting for terminal commands in VSCode? Here's a simple one-line alias that fixes it instantly."

excerpt: "Stop fighting with async code. This Kotlin coroutines pattern makes concurrent operations 10x easier."

excerpt: "Spent 3 hours debugging a production issue. Here's the subtle bug that caused it and how to prevent it."
```

**Poor Examples:**
```yaml
excerpt: "This post is about terminal detection in VSCode."  # Too vague
excerpt: "In this comprehensive guide, I will show you..."   # Too wordy
excerpt: "Check out my latest blog post about coding!"       # No value proposition
```

## 🎨 Image Selection and Generation

### Why Images Matter

- **Higher engagement**: Tweets with images get 150% more retweets
- **Professional appearance**: Preview cards look polished
- **Visual interest**: Stands out in feed
- **Context**: Reinforces the post's topic

### Image Strategy

**For AI Agents Creating Blog Posts:**

When creating a blog post, you should:

1. **Assess the topic** - Determine what visual would best represent it
2. **Choose an approach** - Select from options below
3. **Generate/find image** - Create or locate appropriate image
4. **Add to post** - Include in front matter and save to assets

### Image Options

#### Option 1: No Custom Image (Default)
If no `image:` field is provided, tweets use the NightOwlCoder logo.
- **Use when**: Post is text-focused or conceptual
- **Pros**: Zero effort, consistent branding
- **Cons**: Less visually engaging

#### Option 2: Code Screenshots
For technical posts, create syntax-highlighted code screenshots.
- **Use when**: Post features specific code solutions
- **Tools**: Carbon.now.sh, ray.so, or VS Code screenshots
- **Best for**: "How-to" posts, bug fixes, code patterns

**Example Front Matter:**
```yaml
image: /assets/2025-10-25-terminal-fix-code.png
```

#### Option 3: Conceptual Graphics
Simple, clean graphics that represent the concept.
- **Use when**: Explaining concepts, architectures, workflows
- **Style**: Minimalist, high contrast, clear typography
- **Tools**: Figma, Canva, Excalidraw
- **Best for**: Architecture posts, design patterns, explainers

#### Option 4: AI-Generated Images
Generate relevant imagery using AI tools.
- **Use when**: Need quick, topical illustrations
- **Tools**: DALL-E, Midjourney, Stable Diffusion
- **Prompts**: "minimalist technical illustration of [topic], clean, professional, code theme, dark background"
- **Best for**: Abstract concepts, general tech topics

#### Option 5: Screenshots/Diagrams
Actual screenshots or diagrams from the post content.
- **Use when**: Post includes visual demonstrations
- **Process**: Take key screenshot from post, add to assets
- **Best for**: UI/UX posts, tool comparisons, bug reports

### Image Specifications

**Technical Requirements:**
- **Format**: PNG or JPG
- **Size**: 1200x630px recommended (Twitter Large Card)
- **Min size**: 600x314px
- **Max size**: 5MB
- **Aspect ratio**: ~1.91:1 (wider is better)

**Design Guidelines:**
- **Text**: If adding text, use large, readable fonts (60pt+)
- **Contrast**: Ensure good contrast for readability
- **Branding**: Consider adding small NightOwl logo in corner
- **Colors**: Match blog theme (dark background, green accents)
- **Simplicity**: Less is more - focus on one key visual

### AI Agent Image Workflow

When an AI agent creates a blog post:

**Step 1: Analyze the Post**
```
Post type: [Technical tutorial / Concept explanation / Problem-solution / etc]
Key visual: [Code snippet / Diagram / Concept / etc]
Image needed: [Yes/No]
```

**Step 2: Determine Best Approach**
```
IF post has critical code solution:
  → Use code screenshot (Option 2)
ELSE IF post explains architecture/concept:
  → Use conceptual graphic (Option 3)
ELSE IF post is opinion/discussion:
  → Use default logo (Option 1)
ELSE:
  → Suggest custom image to user
```

**Step 3: Implementation**
```yaml
# If using custom image:
---
image: /assets/YYYY-MM-DD-post-slug-image.png
---

# Note: Agent should inform user:
# "I recommend adding a custom image. I can help you:
#  1. Generate one with AI (describe what you'd like)
#  2. Create a code screenshot (I'll format the key code)
#  3. Use the default NightOwlCoder logo"
```

**Step 4: Image File Naming**
```
Format: YYYY-MM-DD-post-slug-description.png
Example: 2025-10-25-terminal-fix-code-screenshot.png
Location: NightOwlCoder.github.io/assets/
```

### Example Complete Post with Image

```markdown
---
layout: post
title: "Fixing AI Terminal Detection in VSCode"
date: 2025-10-25 21:00:00 -0700
categories: ai-tools vscode terminal
excerpt: "AI coding assistants get stuck waiting for terminal commands? Here's a simple one-line alias that fixes it instantly."
image: /assets/2025-10-25-terminal-fix-preview.png
---

# Content starts here...
```

### Image Generation Prompts

**For AI-Generated Images:**

```
Technical Post:
"minimalist technical illustration of [topic], clean lines, professional, technology theme, dark blue background, subtle code elements, modern, 16:9 aspect ratio"

Code/Programming:
"abstract representation of [concept], coding symbols, terminal window, syntax highlighting colors, dark theme, professional developer aesthetic, wide format"

Problem-Solving:
"before and after concept, [problem] being solved, clean minimal design, tech illustration style, green accent color, dark background"

Tutorial/Guide:
"step-by-step visual metaphor for [topic], clear progression, modern tech aesthetic, instructional design, professional"
```

## 🚀 Quick Start Template for AI Agents

When asked to create a blog post, use this template:

```markdown
---
layout: post
title: "[TITLE]"
date: [YYYY-MM-DD HH:MM:SS -0700]
categories: [category1 category2]
excerpt: "[Compelling 1-2 sentence hook that sells the post]"
image: /assets/[YYYY-MM-DD-slug-image.png]  # Optional but recommended
---

# [Title]

[Introduction paragraph]

## [Section 1]

[Content]

```[language]
[Code example]
```

## [Section 2]

[Content]

## Conclusion

[Closing thoughts]
```

Save to: `NightOwlCoder.github.io/_posts/[YYYY-MM-DD]-[slug].md`

### Post-Creation Checklist

After creating a blog post:

- [ ] Filename follows `YYYY-MM-DD-slug.md` format
- [ ] Front matter includes all required fields
- [ ] `excerpt` field is present and under 150 characters
- [ ] `image` field included (or consciously omitted)
- [ ] If custom image: file saved to `assets/` directory
- [ ] If custom image: filename follows `YYYY-MM-DD-slug-description.png`
- [ ] Content is well-structured with headers
- [ ] Code blocks specify language
- [ ] All links work correctly
- [ ] Post ready to commit and push

**Note:** Upon pushing to GitHub:
1. GitHub Actions will automatically trigger
2. Auto-tweet posts to @OwlCoder within 30-60 seconds
3. Preview card will include image (custom or default logo)
4. GitHub Pages will rebuild and deploy the site

---

*This guide is maintained as part of the NightOwlCoder blog infrastructure.*
