# New Blog Post Workflow

Run these steps in order when creating a new blog post:

## 1. Create the post file

```
touch docs/blog/posts/<slug>.md
```

## 2. Create image directory

```
mkdir docs/assets/images/<slug>/
```

## 3. Write the post with front matter:

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

## 4. Verify

```
uv run poe build
```

## Quick Reference

| Task | Command |
|------|---------|
| Serve locally | `uv run poe serve` |
| Build | `uv run poe build` |
| Create post | `touch docs/blog/posts/<slug>.md` |
| Create image dir | `mkdir docs/assets/images/<slug>/` |
