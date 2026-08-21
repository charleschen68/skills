# HTML and JSX in Cocomoon MDX

Read this reference only when an article needs HTML/JSX or contains pasted HTML.

## Decision rule

Prefer Markdown for content. Add HTML/JSX only when it materially improves semantics, disclosure,
captioning, responsive layout, or visual hierarchy. Avoid wrapping ordinary paragraphs in `<div>`
elements or converting the entire article into JSX.

This project's `.mdx` files compile as MDX/JSX. HTML-looking markup must therefore follow JSX syntax:

- use `className`, `htmlFor`, `tabIndex`, and camel-cased SVG attributes;
- close every element and self-close void elements such as `<img />` and `<br />`;
- use a JavaScript object for `style`, although static Tailwind classes are preferred;
- keep Tailwind class names as complete static strings so the build can discover them;
- protect literal `{`, `}`, `<`, and `>` in prose with code formatting or entities when MDX could
  parse them as expressions or tags;
- leave blank lines around Markdown nested inside a JSX flow element.

The registered MDX components are `Image`, `TOCInline`, `BlogNewsletterForm`, custom links, code
blocks, and responsive tables. Reuse these when appropriate. Do not assume an unregistered custom
component exists.

## Safe patterns

Disclosure:

```mdx
<details className="my-6 rounded-lg border border-gray-200 p-4 dark:border-gray-700">
  <summary className="cursor-pointer font-semibold">Show the implementation details</summary>

Markdown, lists, and fenced code can appear here.

</details>
```

Figure with caption:

```mdx
<figure className="my-8">
  <Image
    src="/static/images/blog/example.png"
    alt="Describe the information conveyed by the image"
    width={1200}
    height={630}
  />
  <figcaption className="mt-2 text-center text-sm text-gray-500 dark:text-gray-400">
    A caption that adds context instead of repeating the alt text.
  </figcaption>
</figure>
```

Responsive comparison cards:

```mdx
<section aria-label="Comparison" className="my-8 grid gap-4 md:grid-cols-2">
  <article className="rounded-lg border border-gray-200 p-5 dark:border-gray-700">
    <h3 className="mt-0">Option A</h3>
    <p className="mb-0">Best when latency is the primary constraint.</p>
  </article>
  <article className="rounded-lg border border-gray-200 p-5 dark:border-gray-700">
    <h3 className="mt-0">Option B</h3>
    <p className="mb-0">Best when operational simplicity matters more.</p>
  </article>
</section>
```

Use native Markdown tables by default; the project already wraps them for horizontal scrolling.

## Pasted HTML

Convert pasted HTML rather than inserting it unchanged:

1. Remove document wrappers such as `doctype`, `<html>`, `<head>`, and `<body>`.
2. Remove scripts, inline event handlers, tracking pixels, hidden forms, and unknown embeds.
3. Convert attributes and styles to valid JSX and static Tailwind classes.
4. Preserve meaningful text, links, lists, tables, captions, code, and heading hierarchy.
5. Replace site-specific classes whose CSS is not present in this repository.
6. Move local images under `public/static/images/`. Review `next.config.js`, CSP, privacy, and
   reliability before using any new external host.

## Prohibited by default

Do not add `<script>`, `dangerouslySetInnerHTML`, event handlers such as `onClick`, remote executable
widgets, tracking markup, or raw third-party forms to an article. Do not add `<style>` blocks or rely
on external CSS that the repository does not load.

Use an `<iframe>` only when the user explicitly requests the embed and after checking the provider,
privacy impact, accessibility title, responsive sizing, loading behavior, and the site's CSP. A plain
link or static image is the default fallback.

If real client-side behavior is required, implement a reviewed React component rather than embedding
arbitrary code in MDX. That component change requires normal TypeScript, lint, build, accessibility,
and visual validation.

## Accessibility and rendering checks

- Prefer semantic elements (`section`, `article`, `figure`, `details`) over layout-only `div` trees.
- Keep heading levels ordered; a card grid does not justify skipping heading levels.
- Give images meaningful `alt` text, or `alt=""` only when truly decorative.
- Ensure disclosures and links work by keyboard and retain visible focus styles.
- Use `<th scope="col">` or `<th scope="row">` when hand-writing a table.
- Prevent wide code, tables, and grids from overflowing small screens.
- Include `dark:` styles whenever custom colors would otherwise break dark mode.
- Verify that minification and typography styles do not collapse required spacing or obscure content.

The production build is mandatory after introducing or changing HTML/JSX because MDX syntax errors,
missing components, and invalid expressions often surface only during compilation.
