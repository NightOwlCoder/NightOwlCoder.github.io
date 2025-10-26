# NightOwlCoder Blog

My personal [blog](https://nightowlcoder.github.io) site lives here, kindly hosted by [GitHub Pages](https://pages.github.com/).

Follow [@OwlCoder](https://twitter.com/OwlCoder) for new posts.

My life in code language:
```
void LifeLoop()
{
    Code();
    Family();
    Fun();
}
```

`.NightOwlCoder`

---

## 🚀 Technology Stack

- **Static Site Generator**: Jekyll 3.x
- **Theme**: [jekyll-theme-hacker](https://github.com/pages-themes/hacker)
- **Hosting**: GitHub Pages
- **Comments**: Disqus
- **Analytics**: Google Analytics
- **Plugins**:
  - jekyll-feed (RSS)
  - jekyll-seo-tag (SEO optimization)
  - jekyll-paginate (Pagination)
  - jekyll-sitemap (Sitemap generation)

## 📁 Project Structure

```
NightOwlCoder.github.io/
├── _config.yml           # Site configuration
├── _posts/               # Blog posts (Markdown files)
├── _pages/               # Static pages
│   ├── 404.md           # Error page
│   ├── about.md         # About page
│   └── archive.md       # Posts archive
├── _layouts/             # Page templates
│   ├── default.html      # Base layout
│   ├── page.html         # Static pages
│   └── post.html         # Blog posts
├── _includes/            # Reusable components
│   ├── header.html
│   ├── footer.html
│   ├── head.html
│   ├── analytics.html
│   └── disqus_comments.html
├── _sass/                # Custom styles (SCSS)
├── assets/               # Images and media files
├── css/                  # Main stylesheet
├── index.html            # Homepage
├── Gemfile               # Ruby dependencies
├── README.md             # This file
└── AGENT.md              # AI agent instructions
```

## 🛠️ Local Development Setup

### Prerequisites
- Ruby 2.5+ installed
- Bundler gem installed (`gem install bundler`)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/NightOwlCoder/NightOwlCoder.github.io.git
cd NightOwlCoder.github.io
```

2. Install dependencies:
```bash
bundle install
```

3. Run the development server:
```bash
bundle exec jekyll serve
```

4. Open your browser to `http://localhost:4000`

The site will auto-regenerate when you make changes to files.

## ✍️ Creating a New Blog Post

### Manual Method

1. Create a new file in the `_posts/` directory with the naming convention:
   ```
   YYYY-MM-DD-title-slug.md
   ```
   Example: `2024-01-15-my-awesome-post.md`

2. Add front matter at the top of the file:
   ```yaml
   ---
   layout: post
   title: "Your Post Title"
   date: 2024-01-15 20:00:00 -0800
   categories: category1 category2 category3
   ---
   ```

3. Write your content in Markdown below the front matter

4. Add images to the `assets/` folder and reference them:
   ```markdown
   ![Alt text](../assets/image-name.png)
   ```

5. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Add new blog post: Your Post Title"
   git push origin master
   ```

GitHub Pages will automatically build and deploy your changes within a few minutes.

### Using an AI Agent

See [AGENT.md](AGENT.md) for detailed instructions on how to use an AI assistant to create blog posts.

## 🖼️ Adding Images

1. Place image files in the `assets/` directory
2. Reference images in your posts using relative paths:
   ```markdown
   ![Description](../assets/your-image.png)
   ```
3. Optionally resize images:
   ```markdown
   ![Description](../assets/your-image.png){:width="350px"}
   ```

## 🎨 Customization

### Site Configuration
Edit `_config.yml` to customize:
- Site title and description
- Social media links
- Google Analytics ID
- Disqus shortname
- Pagination settings

### Styling
- Modify SCSS files in `_sass/` directory
- Edit `css/main.scss` to import custom styles

### Layouts and Components
- Edit HTML templates in `_layouts/`
- Modify reusable components in `_includes/`

## 📝 Blog Post Front Matter Options

```yaml
---
layout: post              # Required: Always 'post'
title: "Your Title"       # Required: Post title
date: YYYY-MM-DD HH:MM:SS -0800  # Required: Publication date
categories: cat1 cat2     # Optional: Post categories
excerpt: "Short summary"  # Recommended: Used for auto-tweet and previews
image: /assets/post-image.png  # Optional: Custom social media preview image
comments: true            # Optional: Enable/disable Disqus comments
---
```

### Auto-Tweet Feature

**🐦 Automatic Twitter Posting**

When you push a new blog post to GitHub, it automatically posts to [@OwlCoder](https://twitter.com/OwlCoder) with:
- Post title
- Custom excerpt (if provided)
- Link to the full post
- Preview card with image

**Setup Requirements:**
- Twitter API credentials configured in GitHub Secrets
- See `docs/X-API-SETUP-GUIDE.md` for setup instructions
- See `docs/AUTO-TWEET-SUMMARY.md` for complete documentation

**Best Practices:**
- Always include an `excerpt:` field for better tweet text
- Add an `image:` field for custom preview images (optional)
- Without custom image, defaults to NightOwlCoder logo
- Keep excerpts under 150 characters for best results

## 🔧 Configuration Files

### _config.yml
Main site configuration including:
- Site metadata (title, description, URLs)
- Jekyll settings (theme, plugins)
- Pagination configuration
- Social media links
- Analytics and comments configuration

### Gemfile
Ruby gem dependencies for Jekyll and plugins

## 🚢 Deployment

This site automatically deploys via GitHub Pages when you push to the `master` branch.

No manual deployment steps required!

## 📊 Features

- ✅ Responsive design
- ✅ Syntax highlighting for code blocks
- ✅ Pagination (4 posts per page)
- ✅ RSS feed at `/atom.xml`
- ✅ SEO optimized
- ✅ Google Analytics integration
- ✅ Disqus comments
- ✅ Twitter integration
- ✅ Sitemap generation

## 🐛 Troubleshooting

### Bundle Install Fails
```bash
bundle update
bundle install
```

### Jekyll Serve Fails
Clear the cache:
```bash
bundle exec jekyll clean
bundle exec jekyll serve
```

### Changes Not Showing on GitHub Pages
- Wait 2-5 minutes for GitHub Pages to rebuild
- Check the Actions tab in your GitHub repository for build status
- Ensure `_config.yml` is valid YAML

## 📚 Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Markdown Guide](https://www.markdownguide.org/)
- [Jekyll Hacker Theme](https://github.com/pages-themes/hacker)

## 📄 License

Content is copyrighted. Code structure follows Jekyll's standard MIT license.

---

*Built with ❤️ using [Jekyll](https://jekyllrb.com/) and hosted on [GitHub Pages](https://pages.github.com/)*
