---
name: blog-publish
description: >
  Write, revise, format, or publish a Cocomoon blog article from notes, drafts, discussions, or research.
  Use for requests to create, 整理, 写成文章, or publish a blog post in this repository. Produces MDX and
  supports intentional semantic HTML/JSX when it improves the article. Do not use for unrelated site
  components, git-only operations, or generic code changes.
---

# Blog Publish

Create a production-ready article under `data/blog/` while preserving the user's content, repository
state, and publication authority.

## Choose the operation

- **Write or edit:** create or update the article and validate it. Do not commit, push, copy to Jarvis,
  or refresh QMD unless the user also asks to publish or index it.
- **Publish:** perform the write/edit work, validation, knowledge-base mirror, exact-file commit, and
  push. Treat words such as “发布”, “publish”, “push”, or an explicit request for the live blog as
  publication authority.
- If the request is ambiguous, stop after writing and validation. Report the resulting file and what
  remains unpublished.

## Workflow

1. Read the applicable repository instructions and inspect `git status --short` before editing. Treat
   all pre-existing changes as user-owned.
2. Gather the actual source material. Distinguish supplied facts from newly researched facts; do not
   invent citations, measurements, or examples. If the user asks for formatting with minimal content
   change, preserve the wording and technical claims and limit edits to structure and presentation.
3. Choose an article shape that fits the material. Do not force every post into a fixed number of
   sections. Establish prerequisites before relying on them, use descriptive headings, and include a
   conclusion only when it adds value.
4. Use Markdown for normal prose, headings, lists, tables, links, images, and code. Use semantic
   HTML/JSX selectively when it provides behavior or layout Markdown cannot express cleanly—for
   example `<details>`, `<figure>`, responsive cards, or a comparison grid. Before doing so, read
   [references/mdx-html.md](references/mdx-html.md) and follow its compatibility and safety rules.
5. Write the article as `data/blog/<slug>.mdx`. Format the exact file with Prettier, then validate it.
6. Only in publish mode, create the Jarvis Markdown mirror, refresh its QMD index, commit the exact
   article file, and push.

## Article file

Use valid frontmatter matching `contentlayer.config.ts`:

```yaml
---
title: "Concise English Title"
date: "YYYY-MM-DD"
tags: ["tag1", "tag2", "tag3"]
draft: false
summary: "One-line article summary"
images: ["static/images/avatar_bak.png"]
---
```

- Use an English, descriptive, kebab-case filename, normally no more than six words. Shorten long
  words only when the abbreviation remains clear. Do not add a `demo-` prefix.
- The body may follow the source language. The title may follow an explicit user preference even
  though the default is English.
- Reuse tags and author identifiers already established in the repository when applicable.
- Never silently overwrite an existing article. Inspect it first. Update it only when the request
  clearly targets that article; otherwise choose a distinct slug or ask when the intended identity
  cannot be inferred safely.
- Keep reusable interactive or complex UI in `components/`. Adding a component is a separate code
  change and must be within the user's requested scope.

## Validation

Run from the repository root:

```bash
npx prettier --write data/blog/<article-file>.mdx
npm run lint
npm run build
git diff --check -- data/blog/<article-file>.mdx
```

- A successful formatter or linter does not prove the MDX compiles; the production build is the
  compilation gate.
- For visual HTML/JSX changes, also inspect the rendered article at mobile and desktop widths, in
  light and dark themes when relevant. Check keyboard access, heading order, overflow, links, image
  alternatives, and table readability.
- Build steps may update generated tag or search artifacts. Never stage them manually. If they were
  clean before validation, restore only the exact generated artifacts dirtied by validation; never
  overwrite a pre-existing user change.
- Report validation failures precisely. Do not publish a build that failed.

## Jarvis mirror and QMD

Do this only in publish/index mode. Write the mirror to
`~/Documents/Jarvis/blog/<article-file-with-.md-extension>`.

- For Markdown-only articles, an extension-changing copy is acceptable.
- If the MDX contains HTML/JSX, imports, or expressions, create a Markdown-equivalent mirror instead
  of blindly copying it. Preserve headings, prose, code, links, table data, captions, and disclosure
  content; replace layout-only wrappers with ordinary Markdown. The mirror is for retrieval, not for
  reproducing visual presentation.
- Do not claim indexing succeeded until the commands exit successfully and the `jarvis-blog`
  collection can retrieve the article.

```bash
qmd update
qmd embed
```

## Publication

Do not use `npm run pub`; it reformats broad repository scope. After validation:

1. Recheck `git status --short` and the article diff.
2. Stage only `data/blog/<article-file>.mdx` and any explicitly authorized, article-specific assets or
   components. Never use `git add -A` or include unrelated/generated changes.
3. Commit with a short imperative message describing the article.
4. Push the current branch and verify both the commit and remote update.

If push is rejected, inspect the branch, upstream, worktree, and divergence first. Do not automatically
rebase, overwrite files, force-push, or broaden the commit. Ask for direction when integrating remote
changes would materially change the user's work.

## Completion report

State separately:

- article path and whether it was created or updated;
- whether HTML/JSX was used and why;
- formatter, lint, build, and visual-check results;
- Jarvis/QMD status, if requested;
- commit and push status, if publication was requested;
- any generated or unrelated files deliberately left out.
