# Blog Writing Rules

These rules encode the writing conventions used across all Sanji blog posts.

## Front Matter

Every post MUST start with YAML front matter in this exact format:

```yaml
---
authors:
    - prateek11rai
categories:
  - CategoryName
date: YYYY-MM-DD
draft: false
---
```

- Only one author: `prateek11rai`
- Categories: 1-2 max, PascalCase (e.g. `Self-Hosting`, `Homelab`, `Anime`, `AI`)
- Date: use the actual publication date
- Never leave `draft: true` for published posts

## Voice & Tone

- First-person narrative (I, my, we)
- Technical but conversational — explain concepts like you're talking to a friend
- Avoid generic blog filler ("In today's post", "Let's dive in", "Stay tuned")
- Short paragraphs (2-4 sentences max)
- This is a personal blog — opinions and personality are encouraged
- When referencing the server, use its nickname (Ohara) after introducing it
- Reference One Piece theming when relevant but don't force it

## Post Structure (Body)

1. `# Title` — H1, descriptive but not clickbait (no colons if avoidable)
2. Intro paragraph(s) — set the scene, hook the reader
3. `![alt text](path){ loading=lazy }` — an image right before the break
4. `<!-- more -->` — the excerpt cut
5. Sections with `## Subheading` (H2 only, never H3)
6. A closing section that summarizes or reflects

## Image Rules

- Every post needs an intro image (before `<!-- more -->`)
- Add a closing or thematic image near the end
- Place images within relevant sections, not just at section boundaries
- Images use relative paths: `../../assets/images/<post-slug>/<filename>.{jpg,png}`
- Every image gets `{ loading=lazy }`
- Alt text describes what the image shows
- Use footnotes for image attribution if sourcing from the web

## Footnotes

- Use `[^1]`, `[^2]` for attribution or minor clarifications
- Place footnote definitions at the **very bottom** of the file
- First footnote should be image attribution with contact email

## Code Blocks

- Language tag required on every fenced code block
- Prefer `bash` for shell commands, `yaml` for compose files, `powershell` for Windows
- Code blocks must be directly useful — copy-paste should work
- Include comments (`# ...`) for brevity but keep commands runnable
- For multi-service Docker Compose, show the service block, not the full file

## Secrets & Placeholders

- **Never use real-looking tokens, API keys, or secrets** in code blocks or examples
- Replace tokens with clear placeholders: `YOUR_BOT_TOKEN`, `YOUR_API_KEY`, `sk-or-...` (with the `...` visible)
- If a token format has a recognizable prefix (e.g. `sk-or-` for OpenRouter), keep the prefix for realism but make the rest clearly fake
- Use double quotes for `echo` with variable placeholders to avoid shell expansion confusion: `echo "TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN"`
- Review every code block before publication — if a value looks like it could be mistaken for a real secret, replace it

## Diagrams (Mermaid)

- Use `graph TB` or `graph LR` for architecture diagrams
- Use `sequenceDiagram` for step-by-step workflows
- **Never use hardcoded `style` directives** with `fill:` colors — they break on the site's dark/light theme toggle
- Let Mermaid use its default theme colors — they automatically adapt to both backgrounds
- Keep mermaid blocks concise — if it spans >60 lines, split the diagram

## Admonitions & Cards

- Use `!!! note`, `!!! warning`, `!!! tip` for callouts sparingly
- Use `<div class="grid cards" markdown>` for feature comparison or spec lists
- Only use inline styles when grid cards need custom icon coloring
- For two images side by side, use a `<div class="grid" markdown>` with two `![...](...)` items

## MkDocs Features Allowed

- `attr_list` — for `{ loading=lazy }`
- `md_in_html`
- `pymdownx.blocks.caption`
- `footnotes`
- `admonition` / `pymdownx.details`
- `pymdownx.superfences` (for mermaid)
- `pymdownx.emoji` — inline icons like :material-check-circle:
