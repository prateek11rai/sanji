# Skill: Write a Blog Post

## When to use
When asked to write a new blog post for the Sanji site.

## Steps

1. **Read handoff doc (if available)** — check `.agents/handoffs/` for a matching slug. If found, read it — it contains key decisions, screenshots, OP angle, and trivia from the project work.
2. **Read reference posts** — read the 2 most recent posts in `docs/blog/posts/` to understand current style
3. **Identify the pattern** — match the new post to one of the patterns in `.agents/patterns/blog-patterns.md`
4. **Read the rules** — review `.agents/rules/blog-rules.md`, especially the One Piece theming and trivia sections
5. **Determine the OP angle** — pick a character/theme parallel (use the matrix in Pattern 4 if applicable)
6. **Source images** — find OP intro + closing images, add any screenshots from the handoff doc
7. **Draft the post** — place in `docs/blog/posts/<slug>.md`
8. **Create image directory** — `docs/assets/images/<slug>/`
9. **Run build** — `uv run poe build` to verify no errors
10. **Clean up** — fix any warnings or errors

## Conventions

- Slug: lowercase, hyphenated, matches the post filename
- Date: use today's date as YYYY-MM-DD
- Draft: set `draft: false` for ready posts, `true` for WIP
- Image paths: `../../assets/images/<slug>/<filename>`
- Always use `uv run poe build` (not raw `mkdocs build`)
- Every post gets an OP intro image and OP closing image (mandatory). Thematic references in text are optional.
- Trivia and hot takes are encouraged but not required — only include them if they add value
