#!/usr/bin/env python3
"""Syndicate a Sanji blog post to dev.to.

Usage:
    # Draft (default) — creates as unpublished, safe to inspect on dev.to
    python scripts/syndicate.py docs/blog/posts/hermes.md

    # Publish immediately
    python scripts/syndicate.py docs/blog/posts/hermes.md --publish

    # Update an existing article (pass its dev.to ID)
    python scripts/syndicate.py docs/blog/posts/hermes.md --update 12345

    # Preview the payload without sending
    python scripts/syndicate.py docs/blog/posts/hermes.md --dry-run

Environment (in order of precedence):
    DEVTO_API_KEY  (or .env file in project root)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import zlib
from pathlib import Path

try:
    import requests
except ImportError:
    print("error: `requests` is required — run: uv add requests", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # optional


RAW_BASE = "https://raw.githubusercontent.com/prateek11rai/sanji/main"
SITE_BASE = "https://prateek11rai.github.io/sanji"
DEVTO_API = "https://dev.to/api/articles"
MAX_TAGS = 4


def parse_front_matter(content: str) -> tuple[dict, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}, content

    raw = match.group(1)
    body = content[match.end() :]
    fm: dict = {}

    cats = re.search(r"^categories:\s*\n((?:\s+- .+\n?)+)", raw, re.MULTILINE)
    if cats:
        fm["categories"] = re.findall(r"\s+- (.+)", cats.group(1))

    dt = re.search(r"^date:\s*(.+)", raw, re.MULTILINE)
    if dt:
        fm["date"] = dt.group(1).strip()

    draft = re.search(r"^draft:\s*(.+)", raw, re.MULTILINE)
    fm["draft"] = draft and draft.group(1).strip().lower() == "true"

    return fm, body


def extract_title(body: str) -> str | None:
    m = re.search(r"^# (.+)", body, re.MULTILINE)
    return m.group(1).strip() if m else None


def extract_description(body: str, max_chars: int = 200) -> str | None:
    text = re.sub(r"^# .+\n*", "", body, count=1).strip()
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("![") or line.startswith("<!--") or line.startswith("<"):
            continue
        if line.startswith("[^") and line.endswith("]:"):
            continue
        clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", clean)
        clean = re.sub(r"\*([^*]+)\*", r"\1", clean)
        clean = re.sub(r"`([^`]+)`", r"\1", clean)
        clean = re.sub(r"\[\^\d+\]", "", clean).rstrip(".").strip()
        if len(clean) > max_chars:
            clean = clean[: max_chars - 3] + "..."
        return clean or None
    return None


def extract_first_image(body: str) -> str | None:
    m = re.search(r"!\[.*?\]\((.+?)\)", body)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------------------
# Transformers — applied in order
# ---------------------------------------------------------------------------

def _replace_image_urls(body: str) -> str:
    def _repl(m: re.Match) -> str:
        alt, url = m.group(1), m.group(2)
        if url.startswith("../../"):
            url = f"{RAW_BASE}/docs/{url[6:]}"
        elif url.startswith("../"):
            url = f"{RAW_BASE}/docs/{url[3:]}"
        return f"![{alt}]({url})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _repl, body)


def _strip_loading_lazy(body: str) -> str:
    return re.sub(r"\{\s*loading\s*=\s*lazy\s*\}", "", body)


def _strip_more_tag(body: str) -> str:
    return re.sub(r"<!-- more -->\s*\n*", "", body)


def _strip_footnote_refs(body: str) -> str:
    return re.sub(r"\[\^\d+\]", "", body)


def _unwrap_footnote_defs(body: str) -> str:
    lines = body.split("\n")
    kept: list[str] = []
    footnotes: list[str] = []
    for line in lines:
        if re.match(r"^\[\^\d+\]:\s*", line):
            footnotes.append(re.sub(r"^\[\^\d+\]:\s*", "", line))
        else:
            kept.append(line)
    if footnotes:
        kept.append("")
        kept.append("---")
        kept.append("")
        kept.extend(footnotes)
    return "\n".join(kept)


def _strip_html_styles(body: str) -> str:
    return re.sub(r"<style>.*?</style>", "", body, flags=re.DOTALL)


def _render_mermaid(body: str) -> str:
    def _repl(m: re.Match) -> str:
        code = m.group(1).strip()
        payload = json.dumps({
            "code": code,
            "mermaid": json.dumps({"theme": "neutral"}),
            "updateEditor": False,
            "autoSync": False,
            "updateDiagram": True,
        }, separators=(",", ":"))
        compressed = zlib.compress(payload.encode(), level=9)
        encoded = base64.urlsafe_b64encode(compressed).decode().rstrip("=")
        url = f"https://mermaid.ink/img/pako:{encoded}"
        return f"![Architecture diagram]({url})\n"
    return re.sub(
        r"```mermaid\n(.*?)```\s*\n*",
        _repl,
        body,
        flags=re.DOTALL,
    )


def _strip_grid_divs(body: str) -> str:
    body = re.sub(r'<div[^>]*>', "", body)
    body = re.sub(r"</div>", "", body)
    return body


def _strip_mkdocs_attrs(body: str) -> str:
    return re.sub(r"\{\s*\.[a-zA-Z0-9_-]+[\s,.]*[a-zA-Z0-9_-]*\s*\}", "", body)


def _convert_admonitions(body: str) -> str:
    def _repl(m: re.Match) -> str:
        t = m.group(1).strip()
        title_raw = m.group(2)
        content = m.group(3)
        heading = title_raw.strip("\" ") if title_raw else t.title()
        lines = [f"> **{heading}**"]
        for cl in content.split("\n"):
            stripped = cl.strip()
            if stripped:
                lines.append(f"> {stripped}")
            else:
                lines.append(">")
        return "\n".join(lines)

    return re.sub(
        r"!!!\s+(\w+)\s*(\"[^\"]*\")?\s*\n((?:\s{4}[^\n]*\n?)*)",
        _repl,
        body,
    )


def _replace_icons(body: str) -> str:
    body = re.sub(r":material-check-circle:", "✅", body)
    body = re.sub(r":material-cigar:", "🚬", body)
    body = re.sub(r":material-desktop-tower:", "🖥️", body)
    body = re.sub(r":material-checkbox-marked-circle:", "✅", body)
    body = re.sub(r":material-[a-z_-]+:", "", body)
    body = re.sub(r":simple-[a-z_-]+:", "", body)
    return body


def _strip_h1(body: str) -> str:
    return re.sub(r"^# .+\n*", "", body, count=1).strip() + "\n"


def transform_body(body: str) -> str:
    body = _strip_more_tag(body)
    body = _strip_html_styles(body)
    body = _strip_grid_divs(body)
    body = _render_mermaid(body)
    body = _strip_loading_lazy(body)
    body = _strip_mkdocs_attrs(body)
    body = _replace_icons(body)
    body = _convert_admonitions(body)
    body = _replace_image_urls(body)
    body = _unwrap_footnote_defs(body)
    body = _strip_footnote_refs(body)
    body = _strip_h1(body)
    return body.strip() + "\n"


# ---------------------------------------------------------------------------
# Payload builder
# ---------------------------------------------------------------------------

def make_slug(title: str) -> str:
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            from pymdownx.slugs import uslugify
            return uslugify(title, "-")
    except ImportError:
        return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def build_payload(post_file: Path, slug: str | None = None, publish: bool = False) -> dict:
    content = post_file.read_text(encoding="utf-8")
    fm, body = parse_front_matter(content)

    title = extract_title(body) or slug or post_file.stem.replace("-", " ").title()
    description = extract_description(body)
    raw_image = extract_first_image(body)
    slug = slug or make_slug(title)

    tags = [t.lower() for t in fm.get("categories", [])][:MAX_TAGS]
    if not tags:
        tags = ["meta"]

    date_str = fm.get("date", "")
    date_parts = date_str.split("-")
    if len(date_parts) == 3:
        canonical_url = f"{SITE_BASE}/blog/{date_parts[0]}/{date_parts[1]}/{date_parts[2]}/{slug}/"
    else:
        canonical_url = f"{SITE_BASE}/blog/{slug}/"

    main_image_url = None
    if raw_image:
        if raw_image.startswith("../../"):
            main_image_url = f"{RAW_BASE}/docs/{raw_image[6:]}"
        elif raw_image.startswith("../"):
            main_image_url = f"{RAW_BASE}/docs/{raw_image[3:]}"
        else:
            main_image_url = raw_image

    should_publish = publish and not fm.get("draft", False)

    body_markdown = transform_body(body)

    return {
        "article": {
            "title": title,
            "body_markdown": body_markdown,
            "published": should_publish,
            "canonical_url": canonical_url,
            "description": description or "",
            "tags": ", ".join(tags),
            "main_image": main_image_url,
        }
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def find_existing(api_key: str, canonical_url: str) -> int | None:
    """Return dev.to article ID if one with this canonical_url already exists."""
    headers = {"api-key": api_key}
    for url in [
        f"{DEVTO_API}/me/all?per_page=100",
        f"{DEVTO_API}/me/published?per_page=100",
    ]:
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            continue
        for article in resp.json():
            if article.get("canonical_url") == canonical_url:
                return article["id"]
    return None


def fetch_article(api_key: str, article_id: int) -> dict | None:
    """Fetch article metadata from dev.to (works for drafts too)."""
    resp = requests.get(
        f"{DEVTO_API}/me/all?per_page=100",
        headers={"api-key": api_key},
    )
    if resp.status_code != 200:
        return None
    for article in resp.json():
        if article["id"] == article_id:
            return article
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Syndicate a Sanji blog post to dev.to",
    )
    parser.add_argument("post_file", type=Path, help="Path to the markdown blog post")
    parser.add_argument("--publish", action="store_true", help="Publish immediately (default: draft)")
    parser.add_argument("--dry-run", action="store_true", help="Print payload and exit")
    parser.add_argument("--update", type=int, metavar="ID", default=None,
                        help="Update article by dev.to ID (auto-detected if omitted)")
    parser.add_argument("--slug", help="Override the URL slug (default: filename stem)")
    parser.add_argument(
        "--force-new", action="store_true",
        help="Skip duplicate check and create a new article",
    )
    args = parser.parse_args()

    if load_dotenv:
        load_dotenv()

    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        print("error: DEVTO_API_KEY not set — add to .env or export it", file=sys.stderr)
        sys.exit(1)

    if not args.post_file.exists():
        print(f"error: file not found — {args.post_file}", file=sys.stderr)
        sys.exit(1)

    payload = build_payload(args.post_file, slug=args.slug, publish=args.publish)

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return

    headers = {"api-key": api_key, "Content-Type": "application/json"}

    existing_id = args.update
    if existing_id is None and not args.force_new:
        canonical_url = payload["article"]["canonical_url"]
        existing_id = find_existing(api_key, canonical_url)
        if existing_id:
            print(f"ℹ existing article found (ID {existing_id}) — updating")

    if existing_id:
        existing = fetch_article(api_key, existing_id)
        if existing is not None and not args.publish:
            payload["article"]["published"] = existing.get("published", False)
        url = f"{DEVTO_API}/{existing_id}"
        resp = requests.put(url, headers=headers, json=payload)
    else:
        resp = requests.post(DEVTO_API, headers=headers, json=payload)

    if resp.status_code in (200, 201):
        result = resp.json()
        print(f"✅ {result.get('url', result.get('title', 'published'))}")
    else:
        print(f"❌ {resp.status_code} — {resp.text}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
