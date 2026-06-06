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
- Categories: 1-2 max, PascalCase (e.g. `Self-Hosting`, `Homelab`, `Anime`, `AI`, `Tooling`)
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
- **Rant voice is allowed** — if something annoyed you, say it. If you have a hot take, say it. This is a blog, not a documentation project.

## Post Structure (Body)

1. `# Title` — H1, descriptive but not clickbait (no colons if avoidable)
2. **Intro text** — 1-3 very short paragraphs, 2-4 sentences total. Hook the reader fast. State the problem or the promise. No rambling, no scene-setting essays.
3. `![alt text](path){ loading=lazy }` — an image right before the break
4. `<!-- more -->` — the excerpt cut
5. Sections with `## Subheading` (H2 only, never H3)
6. A closing section that summarizes or reflects

## Image Rules

- Every post needs an intro image (before `<!-- more -->`)
- Add a closing or thematic image near the end
- **Intro and closing images should be One Piece themed where possible**
- Place images within relevant sections, not just at section boundaries
- Images use relative paths: `../../assets/images/<post-slug>/<filename>.{jpg,png}`
- Every image gets `{ loading=lazy }`
- Alt text describes what the image shows
- Use footnotes for image attribution if sourcing from the web

### One Piece Image Sourcing

- **Intro images**: Find OP art that parallels the topic. Use official art from the One Piece wiki, manga panels (official translation), or high-quality fanart from Pinterest.
- **Closing images**: A character or scene that reflects the post's theme. Vegapunk for future/ambition, Luffy for freedom/breaking limits, Sanji for craft/mastery, Franky for building, Robin for knowledge.
- **Section images**: Optional but encouraged. Screenshots of the actual setup work better here than OP art.
- **Avoid overusing the same character** — rotate through the crew.
- **Alt-text convention**: Describe the scene AND state the character name: "Sanji lighting a cigarette in the Baratie kitchen, reflecting on craft"

## Footnotes

- Use `[^1]`, `[^2]` for attribution or minor clarifications
- Place footnote definitions at the **very bottom** of the file
- First footnote should be image attribution with contact email

## One Piece Theming Strategy

Every post on this site should feel like part of a series, not an isolated technical article. The OP thread unifies them.

**One Piece visual identity — mandatory:**

1. **Intro image** — OP themed (before `<!-- more -->`)
2. **Closing image** — OP themed (near the end)

These two images are what make the site feel cohesive. The intro sets the mood, the closing leaves a reflection.

**Thematic reference in text — optional:**

If the tech has a natural parallel to an OP character, event, or island, draw it. If it doesn't, don't force it. Purely technical posts with no anime reference in the body are fine — the images carry the identity.

**How to find the angle (when it fits):**
- Does the tool "build" something? → Franky
- Does it "serve" or "preserve"? → Sanji or Ohara
- Does it explore or navigate? → Nami or Robin
- Does it fight or overcome limitations? → Luffy or Zoro
- Does it heal or monitor? → Chopper

**When in doubt, leave it out.** A forced metaphor is worse than none.

## Trivia & Rants

### Trivia Placement
- Use `!!! tip "Trivia"` or `!!! info "Did You Know?"` admonitions for fun facts
- Keep them short — one paragraph, directly relevant to the section
- Examples: historical origin of the tool, naming backstory, a comparison with a dead project
- **Not required** — only include if you have something genuinely interesting to say

### Rants / Hot Takes
- Use `!!! quote "Hot Take"` admonitions or weave into section prose
- Rants are encouraged but **not required**. Only write one if you actually have a strong opinion.
- Examples: "X terminal emulator is overrated because...", "The default config is bad and here's why", "This package manager war is stupid but I choose Y"
- Signpost it clearly — don't sound accidentally angry. Make it intentional.
- A purely informative, straightforward post is fine. Not everything needs a hot take.

## Handoff Docs

When an agent produces a project and hands it off for blog writing, the handoff doc goes in `.agents/handoffs/<slug>.md`. Format:

```markdown
# Handoff: <Topic>

## What Was Built
<summary>

## Key Decisions
- <decision> — <why>

## Screenshots Available
- <path> — <what it shows>

## One Piece Angle Suggestion
<character/theme>

## Trivia / Hot Takes
- <trivia fact>
- <hot take>

## Config Files / Dotfiles
- <path> — <purpose>
```

The blog-writing agent reads this before drafting. Handoff docs keep project work and writing decoupled.

## Code Blocks

- **Language tag REQUIRED on every fenced code block** — never leave `` ``` `` bare. Use ` ```bash `, ` ```yaml `, ` ```text `, etc.
- Use `text` for non-code content: directory trees (`/srv/...`), UI navigation paths (`Settings → ...`), file listings, URLs — anything that's not executable
- Prefer `bash` for shell commands, `yaml` for compose files, `powershell` for Windows, `ini` or `env` for config files
- **Every block must have a language tag** — no exceptions. A bare `` ``` `` opening fence means no syntax highlighting.
- Code blocks must be copy-paste ready — commands should work as written
- Include comments (`# ...`) for brevity but keep commands runnable
- For multi-service Docker Compose, show the service block, not the full file
- For config file excerpts, show only the relevant section with a comment showing the file path

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
- For trivia: `!!! tip "Trivia"` — one paragraph, directly relevant
- For hot takes: `!!! quote "Hot Take"` — intentional, opinionated, signed with personality

## MkDocs Features Allowed

- `attr_list` — for `{ loading=lazy }`
- `md_in_html`
- `pymdownx.blocks.caption`
- `footnotes`
- `admonition` / `pymdownx.details`
- `pymdownx.superfences` (for mermaid)
- `pymdownx.emoji` — inline icons like :material-check-circle:
