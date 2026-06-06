# New Blog Post Workflow

Run this when asked to write a new blog post. Follow the steps in order.

## Usage

```bash
# Without handoff doc (agent knows the topic)
new-blog <topic-slug>

# With handoff doc from another agent
new-blog <topic-slug> <path-to-handoff-doc>
```

## Step-by-Step

### Step 1: Accept Inputs

- `slug` — lowercase, hyphenated, matches the filename (e.g. `wezterm-tmux-setup`)
- `handoff_doc` — optional path to a `.md` file produced by another agent who did the project work

### Step 2: Read Handoff Doc (if provided)

If a handoff doc exists at `.agents/handoffs/<slug>.md` or a custom path, read it. Expect this format:

```markdown
# Handoff: <Topic>

## What Was Built
<summary of the project, setup, or workflow>

## Key Decisions
- <decision 1> — why
- <decision 2> — why

## Screenshots Available
- <path/to/screenshot> — what it shows

## One Piece Angle Suggestion
<which character, island, or theme maps to this>

## Trivia / Hot Takes
- <interesting detail worth calling out>
- <strong opinion or rant>

## Config Files / Dotfiles (if relevant)
- <path/to/file> — what it configures
```

If no handoff doc exists, gather the same information by asking the user or researching.

### Step 3: Identify the Pattern

Read `.agents/patterns/blog-patterns.md` and pick the best match:

| Post type | Pattern |
|---|---|
| First-time setup, hardware, new service | **1: Technical Guide** |
| Character analysis, opinion piece | **2: Character Analysis** |
| Follow-up to an existing post | **3: Extension Post** |
| Tooling, workflow, dotfiles, personal setup | **4: Rant + One Piece** |

For WezTerm/tmux/dotfiles posts, Pattern 4 is the best fit.

### Step 4: Determine the One Piece Angle

Every post needs at least **one** One Piece thread. Spend 2-3 minutes deciding:

- **Metaphor**: What OP character or concept parallels the tech? (e.g. Ohara = knowledge preservation, Sanji = chef/craft, Franky = shipwright/builder, Chopper = medicine/health, Nami = navigation/mapping)
- **Intro image**: Must be OP-themed. Sources: official art from wiki, fanart from Pinterest, manga panels from Reddit.
- **Closing image**: OP character that ties the reflection together.
- **Section tie-ins**: Can a section header or aside reference an OP scene or quote?

### Step 5: Gather Trivia / Hot Takes

Inject 2-3 pieces of personality per post:

- **Trivia**: obscure fact about the tool, a historical footnote, a comparison nobody asked for
- **Hot take**: strong opinion about why something is overrated/underrated, a setup choice you'd defend in a fight
- **Rant**: something that annoyed you during the process — permission issues, bad docs, missing features

Place these in admonitions (`!!! tip "Trivia"` or `!!! quote "Hot Take"`) or weave them into section text.

### Step 6: Source Images

- OP intro image: look in `docs/assets/images/` for reuse, else find from web (save to `docs/assets/images/<slug>/`)
- Closing image: OP character that matches the post's theme
- Screenshots: provided by user or handoff doc
- All images get `{ loading=lazy }` and descriptive alt text

### Step 7: Create Files

```bash
mkdir -p docs/assets/images/<slug>/
touch docs/blog/posts/<slug>.md
```

### Step 8: Draft the Post

Write the post following:
- `.agents/rules/blog-rules.md` — front matter, tone, code blocks, images, secrets
- The chosen pattern from `.agents/patterns/blog-patterns.md`
- One Piece theming and trivia from steps 4-5

Front matter template:

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

### Step 9: Verify

```bash
uv run poe build
```

Fix any warnings or errors.

## Handoff Doc Convention

Handoff docs live in `.agents/handoffs/<slug>.md`. When Agent A finishes project work, they write a handoff doc there. Agent B (blog writer) reads it via `new-blog <slug> .agents/handoffs/<slug>.md`.

This keeps the project work and the writing decoupled — you can hand off to a different agent or resume days later.

## Quick Reference

| Task | Command |
|------|---------|
| Serve locally | `uv run poe serve` |
| Build | `uv run poe build` |
| Create post | `touch docs/blog/posts/<slug>.md` |
| Create image dir | `mkdir -p docs/assets/images/<slug>/` |
| Handoff dir | `.agents/handoffs/` |
