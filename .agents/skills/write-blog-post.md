# Skill: Write a Blog Post

## When to use
When asked to write a new blog post for the Sanji site.

## Steps

1. **Read reference posts** — read the 2 most recent posts in `docs/blog/posts/` to understand current style
2. **Identify the pattern** — match the new post to one of the patterns in `.agents/patterns/blog-patterns.md`
3. **Read the rules** — review `.agents/rules/blog-rules.md`
4. **Draft the post** — place in `docs/blog/posts/<slug>.md`
5. **Create image directory** — `docs/assets/images/<slug>/`
6. **Run build** — `uv run poe build` to verify no errors
7. **Clean up** — fix any warnings or errors

## Conventions

- Slug: lowercase, hyphenated, matches the post filename
- Date: use today's date as YYYY-MM-DD
- Draft: set `draft: false` for ready posts, `true` for WIP
- Image paths: `../../assets/images/<slug>/<filename>`
- Always use `uv run poe build` (not raw `mkdocs build`)
