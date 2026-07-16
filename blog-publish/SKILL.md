---
name: blog-publish
description: >
  Transform any content (notes, articles, discussions, research) into a polished MDX learning article and publish.
  Trigger whenever the user says "将 xx 总结成一篇文章", "summarize into an article", "write a blog post",
  "convert to article", "写成文章", "整理成文", or any phrase meaning turn content into a blog article.
  Also trigger when the user pastes content and says "article", "blog", "post", "文章".
  Do NOT trigger for simple git commits, code writing, or file operations alone.
---

## Blog Publish Skill

Convert raw content into a structured MDX learning article and publish to the cocomoon blog.

### Workflow

1. **Read the content** — Gather source material (pasted text, files, links, or conversation context).

2. **Structure the article** — Organize into a clear learning article:
   - Title, core concepts, principles, practical advice
   - Numbered sections (1., 2., 3., ...) with subsections (2.1, 2.2, ...)
   - Code blocks and tables where appropriate
   - Summary/conclusion section

3. **Write the MDX file** — Output to `~/app/cocomoon/data/blog/`:

```yaml
---
title: 'English Title'
date: 'YYYY-MM-DD'
tags: ['tag1', 'tag2', 'tag3']
draft: false
summary: 'One-line article summary'
images: ['static/images/avatar_bak.png']
---

Article body in Markdown...
```

4. **File naming**:
   - **English title** — filename uses English words
   - **Max 6 words** — keep title concise
   - **Abbreviate long words** — words >10 letters → abbreviation (e.g., Infrastructure → Infra, Authentication → Auth)
   - **Kebab-case** — e.g., `ai-builders-digest-2026-07-14.mdx`
   - **No `demo-` prefix** — descriptive name only
   - Tags in frontmatter: `['tag1', 'tag2', 'tag3']` array format

5. **Copy to knowledge base** — Save a copy of the article to the Jarvis knowledge base so it is searchable there:
   ```bash
   cp ~/app/cocomoon/data/blog/<article-file>.mdx ~/Documents/Jarvis/blog/<article-file>.md
   ```
   Note the extension changes from `.mdx` to `.md` (the knowledge base indexes markdown). Create `~/Documents/Jarvis/blog/` if it does not exist.

6. **Publish** — Commit and push with git (do NOT use `npm run pub`; it reformats the whole repo and bypasses hooks). Run in `~/app/cocomoon/`:
   ```bash
   cd ~/app/cocomoon
   git add data/blog/<article-file>.mdx
   git commit -m "Add Article Title"
   git push
   ```
   Vercel auto-builds and deploys after the push.

### Content Guidelines

- Title and filename in English
- Article body can be in the language of the source content
- Self-contained and educational — teaches the reader something
- Use real data and examples when available
- Include practical recommendations or takeaways

### Article Structure Template

```
## 1. Introduction — Why [Topic] Matters
## 2. Core Concepts — The Key Ideas
## 3. How It Works — Principles and Mechanisms
## 4. Practical Application — Real-World Examples
## 5. Best Practices / Recommendations
## 6. Summary / Conclusion
```

### Error Handling

- If `git push` is rejected, run `git pull --rebase` then push again; check the current branch matches the remote default branch
- If file already exists, overwrite it
- Always verify the publish succeeded (`git log -1` shows the commit, push exits 0)
