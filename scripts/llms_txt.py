"""Emit llms.txt and llms-full.txt (llmstxt.org) alongside the built site.

llms.txt is the index; llms-full.txt is every page's markdown concatenated,
for agents that would rather read once than crawl. Generated, not written:
a static index goes stale the next time a post is published.
"""

from __future__ import annotations

import html
import mimetypes
from urllib.parse import urljoin

# Generated navigation surfaces, not content — the posts are listed anyway.
_GENERATED = ("/blog/archive/", "/blog/category/")

_pages: list[dict] = []


def on_config(config):
    """`mkdocs serve` reuses the module across rebuilds; start each one empty."""
    _pages.clear()
    # The dev server sends bare `text/plain`, so browsers guess latin-1 and
    # mangle every accent. GitHub Pages appends the charset itself.
    mimetypes.add_type("text/plain; charset=utf-8", ".txt")
    return config


def on_page_context(context, page, config, nav):
    """Collect each rendered page."""
    url = page.abs_url or page.url
    if any(part in url for part in _GENERATED):
        return context

    _pages.append(
        {
            # Titles arrive HTML-escaped; this file is plain text.
            "title": html.unescape(page.title or ""),
            "url": url,
            # The blog plugin sets this; ordinary pages have none.
            "date": getattr(page, "meta", {}).get("date"),
            "description": (page.meta or {}).get("description"),
            "is_post": "/blog/20" in url,
            "markdown": page.markdown or "",
        }
    )
    return context


def on_post_build(config):
    from pathlib import Path

    site = config["site_url"] or ""

    def absolute(url: str) -> str:
        """Anything fetching this file is off-site; relative paths are no use."""
        return urljoin(site, url) if site else url

    lines = [
        f"# {config['site_name']}",
        "",
        f"> {config['site_description']}",
        "",
        f"Site: {site}",
        f"Full text of every page: {absolute('llms-full.txt')}",
        "",
    ]

    pages = [p for p in _pages if not p["is_post"]]
    posts = [p for p in _pages if p["is_post"]]
    social = config["extra"].get("social") or []

    if pages:
        lines += ["## Pages", ""]
        for p in pages:
            desc = f": {p['description']}" if p["description"] else ""
            lines.append(f"- [{p['title']}]({absolute(p['url'])}){desc}")
        lines.append("")

    if posts:
        # Newest first; undated posts sort last rather than crashing the build.
        posts.sort(key=lambda p: (p["date"] is not None, p["date"]), reverse=True)
        lines += ["## Blog", ""]
        for p in posts:
            date = f" ({p['date']:%Y-%m-%d})" if p["date"] else ""
            lines.append(f"- [{p['title']}]({absolute(p['url'])}){date}")
        lines.append("")

    # `## Optional` is reserved by the spec: agents skip it when context is
    # short. Off-site profiles are exactly that.
    if social:
        lines += ["## Optional", ""]
        for item in social:
            lines.append(f"- [{item.get('name') or item['link']}]({item['link']})")
        lines.append("")

    site_dir = Path(config["site_dir"])
    out = site_dir / "llms.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    full = [f"# {config['site_name']}", "", f"> {config['site_description']}", ""]
    for p in pages + posts:
        full += [
            "---",
            "",
            f"# {p['title']}",
            "",
            f"Source: {absolute(p['url'])}",
            "",
            p["markdown"].strip(),
            "",
        ]
    full_out = site_dir / "llms-full.txt"
    full_out.write_text("\n".join(full), encoding="utf-8")

    print(
        f"INFO    -  Wrote llms.txt ({len(pages)} pages, {len(posts)} posts) "
        f"and llms-full.txt ({full_out.stat().st_size // 1024} KB)"
    )

