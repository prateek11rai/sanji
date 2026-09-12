"""Inject schema.org JSON-LD into the pages that are about a person.

Unlike llms.txt, search engines actually consume this. Facts come from
`extra.person` in mkdocs.yml and `sameAs` from `extra.social`, so nothing is
restated here.
"""

from __future__ import annotations

import json

# Pages that are about Prateek rather than about something he made.
_PROFILE_PAGES = ("index.md", "resume.md")


def _person(config) -> dict:
    person = config["extra"].get("person") or {}
    data = {
        "@type": "Person",
        "name": person.get("name") or config["site_author"],
        "sameAs": [s["link"] for s in config["extra"].get("social") or []
                   if not s["link"].startswith("mailto:")],
    }
    for key in ("jobTitle", "email", "description"):
        if person.get(key):
            data[key] = person[key]
    for key, cls in (("worksFor", "Organization"), ("alumniOf", "CollegeOrUniversity")):
        item = person.get(key)
        if item:
            data[key] = {"@type": cls, **item}
    return data


def on_post_page(output, page, config):
    if page.file.src_uri not in _PROFILE_PAGES:
        return output

    block = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "url": page.canonical_url,
        "mainEntity": _person(config),
    }
    tag = (
        '<script type="application/ld+json">'
        + json.dumps(block, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )
    return output.replace("</head>", f"{tag}</head>", 1)
