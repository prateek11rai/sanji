# Sanji Blog — Agent Framework

This directory contains conventions and tooling for maintaining consistent blog posts on the Sanji site.

## Files

| File | Purpose |
|------|---------|
| `.agents/rules/blog-rules.md` | All writing conventions: front matter, tone, code blocks, images, secrets |
| `.agents/patterns/blog-patterns.md` | Post architecture templates (Technical Guide, Character Analysis, Extension) |
| `.agents/skills/write-blog-post.md` | Step-by-step workflow for generating a new post |
| `.agents/commands/new-blog.md` | Quick reference for creating and verifying posts |

## Critical Rules

- **Never use real-looking tokens or secrets in examples** — always `YOUR_BOT_TOKEN`, `YOUR_API_KEY`, etc.
- Always run `uv run poe build` before committing a new post
- Place images in `docs/assets/images/<slug>/` before referencing them
- Image paths are relative: `../../assets/images/<slug>/file.jpg`
- Author is always `prateek11rai` (configured in `docs/blog/.authors.yml`)
