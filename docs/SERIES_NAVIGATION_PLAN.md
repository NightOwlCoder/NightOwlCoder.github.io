# Blog Series Navigation System

## Proposed Standard

### Front Matter Format
```yaml
---
series: "Series Name"
series_part: 1
series_total: 6  # Optional: total parts planned
---
```

### Detected Series

#### 1. AI Consent Security (3 parts)
- Part 1: 2025-12-05 - Local LLM Command Safety Classifier
- Part 2: 2025-12-08 - Trusted Commands Betrayal  
- Part 3: 2025-12-10 - Consent Bypass via Indirect Execution

#### 2. Building AI Memory Systems (1 published, 5 planned)
- Part 1: 2025-12-15 - Why Your AI Agent Forgets Everything
- Part 2-6: Planned (see quick-launch/docs/blog-series.md)

#### 3. QL Journey (2 parts, non-sequential)
- Part 1: 2025-10-27 - From 25 Aliases to One Command
- Part 6: 2025-12-03 - JetBrains Observation Masking

### Auto-Generated Navigation

Each post in a series should have:

**At top (after intro paragraph):**
```markdown
<div class="series-nav">
  <strong>📚 AI Consent Security Series</strong> (Part 3 of 3)
  <ul>
    <li>← Previous: <a href="/url">Part 2: Trusted Commands Betrayal</a></li>
    <li>→ Next: Coming soon!</li>
  </ul>
</div>
```

**At bottom (before closing):**
```markdown
---
### 📚 Complete Series
1. [Local LLM Command Safety](/2025/12/05/...) 
2. [Trusted Commands Betrayal](/2025/12/08/...)
3. **Consent Bypass via Indirect Execution** (this post)
```

### Series Index Pages

Create `/series/ai-consent-security.html` with:
- Series overview
- All posts listed in order
- Status (complete/ongoing)
- Subscribe/follow link

## Implementation Plan

### Phase 1: Standardize Front Matter
- Add `series:` and `series_part:` to all series posts
- Make naming consistent

### Phase 2: Generate Navigation
- Create Jekyll include: `_includes/series-nav.html`
- Reads front matter, generates prev/next links
- Add to post layout automatically

### Phase 3: Series Index Pages
- Create `_layouts/series.html` 
- Auto-generate index pages for each series
- Add to main navigation

## Questions

1. **Auto-detect series posts?** Or manually tag each?
2. **Show "coming soon" for planned parts?** Or hide until published?
3. **Series in main nav?** Or just in posts?

