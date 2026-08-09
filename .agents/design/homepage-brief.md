# Homepage Redesign — Build Brief

Working brief for replacing the plain markdown landing page with a custom
template. Companion to the design-direction pitch (three directions: Log Pose /
Baratie / Statusline).

Everything here was verified against **mkdocs-material 9.7.6** as installed in
`.venv` — not against the published docs. Where a claim was checked by building
this repo, it says so.

## Ground truth about the stack

| Fact | Value |
|---|---|
| Installed Material version | **9.7.6** (`pyproject` floor says `>=9.6.14,<10` — it floats) |
| Edition | Free. 9.7.x ships `optimize`, `privacy`, `projects`, `typeset`, `group` — a lot of "Insiders-only" advice online is stale |
| Palette scheme names | `dracula-dark` / `dracula-light` — **not** `slate` / `default`. Every copy-pasted `[data-md-color-scheme="slate"]` selector is dead CSS here |
| Tab bar | `.md-tabs { display: none }` below **1220px**. Tabs are desktop-only; don't design mobile spacing around them |
| Upstream status | Maintenance mode since 2025-11-05, critical fixes for *at least* 12 months. Successor is Zensical, which promises unchanged generated HTML |

**Consequence of the last row:** keep the homepage to **one template file and one
stylesheet**. Do not fork partials. A migration should be a copy, not a rewrite.

## Current defects

Two are live on the site; three fire the moment `template: home.html` is
un-commented in `docs/index.md`.

- **Live** — `docs/extra/css/dracula.css:87` sets `--md-typeset-a-color: #00b3cc`,
  which is **2.37:1** on `#f8f8f2`. Every light-mode link fails AA, and fails the
  3:1 large-text floor too. Line 72's `--md-accent-fg-color: #c0448b` is 4.44:1 —
  just under. `.report-pill:hover` forces `#ffffff` on pink: 2.39:1.
- **Live** — `overrides/main.html` loads `Avenir Roman` from Google Fonts.
  Confirmed **HTTP 400** by curl. Avenir isn't a Google font; the stylesheet
  handle (`contentberg-gfonts-custom-css`) is a WordPress theme's. Dead request
  on every page.
- **Latent** — `overrides/home.html` overrides `{% block tabs %}` without
  `{{ super() }}`. That block *is* the tab bar; the override deletes Me /
  Projects / Blog.
- **Latent** — `home.css` references
  `docs/assets/images/metallic-metallic-3d-abstract-colorful-shape-1.png`, which
  does not exist. Hero renders as a bare overlay. Buttons are teal `#008080`
  (not in the palette) with `#ffffff !important` text that disappears in light
  mode. The primary CTA links to `about/`, which is not a page and not in nav.
- **Latent** — `{% block footer %}{% endblock %}` drops all nine configured
  social icons and the copyright line.

Also missing: `dracula.css` never defines `--md-shadow-z1/z2/z3`, so card shadows
keep their light-mode values in dark mode.

## The template skeleton

```jinja
{% extends "base.html" %}

{# extrahead renders AFTER the extra_css loop, so home.css wins cascade ties
   against dracula.css. {% block styles %} renders BEFORE it and loses them. #}
{% block extrahead %}
  {{ super() }}
  <link rel="stylesheet" href="{{ 'extra/css/home.css' | url }}">
{% endblock %}

{% block tabs %}
  {{ super() }}          {# ← without this the nav tabs vanish #}
  <section class="mdx-hero">
    <div class="md-grid md-typeset">   {# ← .md-button and .grid.cards are
                                           .md-typeset-scoped; without this
                                           ancestor they render unstyled #}
      ...hero...
    </div>
  </section>
{% endblock %}

{# Do NOT declare {% block footer %} — leaving it alone keeps the social row. #}
```

Notes:

- `{% block hero %}` also exists and is empty by default, but it renders **above**
  the tab bar — a tall hero there pushes the nav off-screen. `tabs` + `super()`
  is squidfunk's own choice and the right one.
- `{% block content %}{% endblock %}` still emits the `.md-content` wrapper and
  `<article class="md-content__inner md-typeset">`. You cannot remove it by
  emptying the block; hide it in CSS, or better, leave it and let `docs/index.md`
  render as the second fold.
- Prefer `hide: [navigation, toc]` in front matter over media queries to drop the
  sidebars. It doesn't break the mobile drawer.
- Pass paths to `| url` **without** a leading slash — `{{ '/x' | url }}` emits an
  absolute `/x` that 404s under the `/sanji/` subpath.
- Hero copy in the template is **not** search-indexed. The search plugin reads
  `page.content` from markdown only. Keep the real bio in `docs/index.md`.

## Live blog posts on the homepage — verified working

Confirmed by building this repo with a probe template. No hook, no extra plugin,
no Insiders.

```jinja
{% set bp = config.plugins.get('material/blog') %}
{% if bp %}
  {% for post in bp.blog.posts[:3] %}
    <a href="{{ post.url | url }}">{{ post.title }}</a>
    <span>{{ post.config.date.created.strftime('%Y-%m-%d') }}</span>
    <span>{{ post.config.categories | join(' · ') }}</span>
    <span>{{ post.config.readtime }} min</span>
  {% endfor %}
{% endif %}
```

Gotchas, all verified:

- The key is **`material/blog`**, not `blog`. MkDocs namespaces theme-provided
  plugins; `config.plugins.get('blog')` returns `None`.
- `post.url` is site-relative — pipe it through `| url` or it breaks on `/sanji/`.
- `post.excerpt.content` is **empty** at homepage render time. Excerpts are
  populated lazily when a blog view renders them. Use your own teaser field.
- `bp.blog.posts` is pre-sorted pinned-first, then date-descending — so
  `pin: true` on one post gives a free "featured" slot. Currently **zero** posts
  use it.
- `post.config.slug` is `None` unless explicitly set. Use `post.url`.
- The blog plugin runs with `draft: true` + `draft_on_serve: true`, so post
  counts differ between `mkdocs serve` and CI. Verify against `mkdocs build`.

## Phase 0 — do this regardless of direction

1. `--md-typeset-a-color` in `dracula-light`: `#00b3cc` → **`#036A96`** (5.62:1).
2. `--md-accent-fg-color` in `dracula-light`: `#c0448b` → **`#A3144D`** (7.13:1).
3. Delete the `{% block fonts %}` override in `overrides/main.html`.
4. `.report-pill:hover` — never white on a Dracula accent. Use `#282a36` as the
   text colour on a filled accent.
5. Define `--md-shadow-z1/z2/z3` per scheme.

### Contrast reference (computed, not estimated)

On `#282a36`: `#f8f8f2` 13.36 · `#f1fa8c` 12.85 · `#50fa7b` 10.49 · `#8be9fd`
10.30 · `#ffb86c` 8.36 · `#ff79c6` 5.97 · `#bd93f9` 5.91 · `#ff5555` 4.53
(passes by 0.03) · **`#6272a4` 3.03 — fails AA for text.**

Rules that follow:

- `#6272a4` is for dot grids and hairlines only. Never labels, metadata or
  section numerals. Use `#f8f8f2` at reduced opacity.
- Never put white text on any Dracula accent — they're all high-lightness.
  Filled chips and buttons need **dark** text (`#282a36`).
- Cards go on `#343746`, not `#44475a`. `#44475a` is only 1.56:1 from the page;
  keep it for borders and selection.
- Use `#8be9fd` for `:focus-visible` — it's the only accent above 6.6:1 on every
  Dracula surface including `#44475a`. Light-mode equivalent: `#036A96`.
- Keep link underlines. Cyan link vs body text is 1.30:1 in dark mode — colour
  alone can't distinguish them.

## Motion rules

- Author every animated element in its **final visible state**, then animate
  inside `@supports (animation-timeline: view())`. Firefox has not shipped
  scroll-driven animations in stable (Aug 2026) and fails *loudly* — unsupported
  browsers run the keyframes once on load. `opacity: 0` in the base rule means
  Firefox users get a blank page.
- Opt **in** with `@media (prefers-reduced-motion: no-preference)`. Never a
  blanket `* { animation: none !important }` — that kills focus rings too.
- Safe unguarded: `@property` (Baseline Jul 2024, Firefox 128+), `@starting-style`,
  `transition-behavior: allow-discrete`, `:has()`, `text-wrap: balance`
  (headings only), same-document View Transitions.
- Keep `navigation.instant` **off**. It's mutually exclusive with cross-document
  view transitions, and any inline `<script>` in a custom template stops
  re-executing after client-side swaps unless it subscribes to `document$`.
- No CDN scripts. If a shader hero is ever non-negotiable, OGL is ~14 KB gzip —
  but pause it on `visibilitychange` and skip it under reduced-motion. three.js
  (84 KB), Rive (2 MB wasm), Lottie (1.2 MB wasm), Vanta (unmaintained since
  2022) and tsParticles (42 KB + per-frame physics) are all disqualifying.

## Deferred, with prerequisites

- **`optimize` plugin** — free in 9.7.6, would take images from ~17 MB to ~4 MB.
  Blocked on two things: it needs the `pngquant` binary (missing → the build
  **aborts**, it does not skip), and three JPEGs in `docs/` are RGBA-mode which
  raises `cannot write mode RGBA as JPEG`. Fix both, add an apt step to
  `deploy.yml`, then it's a one-line win.
- **Self-hosted JetBrains Mono** — ~40 KB latin woff2 kills two third-party
  origins. `theme.font: false` also removes `--md-text-font` / `--md-code-font`;
  redefine both or the site silently falls back to Helvetica. Material currently
  loads only weights 300/400/700, so any type scale must live within those.
- **Lighthouse CI on PRs** — serve the built artifact under a `/sanji/`
  subdirectory or every relative asset 404s and the score tanks for the wrong
  reason.
- **Live-data widgets** — Goodreads RSS works (18 items on the `read` shelf) but
  sends no CORS headers; Strava is OAuth2-only. Everything must be fetched in the
  Action and committed as JSON, never fetched from the browser. Third-party
  iframes would also load trackers before the existing cookie-consent banner is
  answered.
