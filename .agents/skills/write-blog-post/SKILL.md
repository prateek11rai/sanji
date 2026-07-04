---
name: write-blog-post
description: Write a blog post for Sanji — Prateek Rai's personal One Piece-themed technical blog (prateek11rai.github.io/sanji). Every post must follow .agents/rules/blog-rules.md (front matter, voice, H2-only structure, code-block and secrets rules) and carry the One Piece visual identity — a themed intro image and closing image are mandatory, an in-text lore angle is optional and never forced. Composes with the avoid-ai-writing skill (mid-draft editing pass) and the blog-critic skill (pre-PR adversarial review).
version: 2.0.0
license: CC0-1.0
---

# Skill: Write a Blog Post

## When to use

When asked to write a new blog post for the Sanji site. This is the drafting skill; it delegates editing to `avoid-ai-writing` and review to `blog-critic` at fixed points in the workflow (see the hooks below — they are steps, not suggestions).

## Phase 0 — Load context (parallel, before writing anything)

Read ALL of these before drafting — they are independent, so read them in parallel (single batch of reads or parallel subagents), not one by one:

- `.agents/rules/blog-rules.md` — the house rules: front matter format, voice, image rules, One Piece theming strategy, code-block and secrets rules. Non-negotiable.
- `.agents/patterns/blog-patterns.md` — pick the pattern that fits the post type.
- `.agents/handoffs/<slug>.md` (if it exists) — key decisions, screenshots, OP angle, trivia from the project work.
- The 2 most recent posts in `docs/blog/posts/` — current voice calibration.

Do not start drafting until all four are loaded. A draft written before the rules are in context gets rewritten; that is wasted work.

## Phase 1 — Plan

1. **Identify the pattern** from blog-patterns.md.
2. **Determine the One Piece angle** — character/theme parallel (Pattern 4 matrix helps). Intro + closing OP images are mandatory; an in-text metaphor is optional. When in doubt, leave the metaphor out — the images carry the identity.
3. **Decide the reader's escape hatch** — if the post is long or history-heavy, plan a jump-to-the-fix link near the top for symptom-driven searchers.

## Phase 2 — Draft

4. **Source images** — OP intro + closing images into `docs/assets/images/blog/<slug>/`, plus handoff screenshots. The One Piece wiki's MediaWiki API works when page scraping is blocked; images arrive as WebP regardless of extension — convert (`sips -s format jpeg`) before committing.
5. **Draft the post** at `docs/blog/posts/<slug>.md`.
6. **Evidence discipline while drafting** (cheaper now than at review): every third-party claim gets a primary-source link; every claim about your own incident either shows its evidence or says plainly it's unproven; code blocks must run as pasted (imports, definitions, stdlib-compatible idioms) and open with a "do you need this?" gate when they're fixes.

## Phase 3 — Edit (MID HOOK: avoid-ai-writing)

7. **Run the `avoid-ai-writing` skill on the draft** — edit-in-place mode, technical voice profile. It strips AI-isms while the blog rules keep the personal voice. Apply its edits before any human review; do not skip because the draft "reads fine."

## Phase 4 — Verify

8. **Run `uv run poe build`** (never raw `mkdocs build`) — fix every warning.
9. **Test the syndication transform** against the real file — `scripts/syndicate.py`'s `transform_body` must cleanly convert admonitions, `???` collapsibles, and mermaid blocks (fetch the generated mermaid.ink URLs and confirm they return images).

## Phase 5 — Review (POST HOOK: blog-critic)

10. **Run the `blog-critic` skill on the built post** — the four audits, three personas, severity-ranked findings.
11. **Fix every `would-embarrass` and `needs-caveat` finding** before opening the PR. Nitpicks are judgment calls.
12. Only then: commit on a branch, PR to `main`. Merge triggers Pages deploy + dev.to syndication automatically.

## Conventions

- Slug: lowercase, hyphenated, matches the post filename.
- Date: today's date as YYYY-MM-DD. `draft: false` only for ready posts.
- Image paths: `../../assets/images/blog/<slug>/<filename>` with `{ loading=lazy }`.
- Every post gets an OP intro image and OP closing image (mandatory). Thematic references in text are optional.
- Trivia and hot takes are encouraged but not required — only include them if they add value.
- First footnote is always the image attribution with the contact email.
