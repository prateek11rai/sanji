---
name: playwright
description: Preview the Sanji site in a real browser. Use whenever a change needs to be seen rather than described — layout, palette, contrast, spacing, responsive behaviour — or when the user says "check", "look at it", or "screenshot it". Covers the agent's own preview server, the long-lived browser window, and the cleanup that stops orphaned servers piling up.
version: 1.0.0
license: CC0-1.0
---

# Previewing the site

CSS and template work cannot be verified by reading the diff. Render it, look
at it, and only then say it works.

## Port ownership

The agent and the user each get a port, and neither touches the other's.

| Port | Owner | Started by |
|------|-------|-----------|
| `8000` | the user | `uv run poe serve` |
| `8777` | the agent | the command below |

**The agent starts and stops its own server.** Don't ask the user to run one,
and don't attach to theirs — they restart it, change branches and kill it
whenever they like, and a preview that dies mid-session is worse than no
preview. Two servers on one port means whoever started last wins silently.

```bash
# Start. Backgrounded so it survives across tool calls.
(DYLD_LIBRARY_PATH=/opt/homebrew/lib nohup uv run mkdocs serve -a 127.0.0.1:8777 \
  > /tmp/sanji-preview.log 2>&1 &)

# It takes 10-15s to boot — the social-cards plugin renders every card at
# startup. Requests before that fail; wait rather than concluding it's broken.
sleep 15 && curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8777/sanji/
```

`DYLD_LIBRARY_PATH` is required on macOS for the `imaging` extra (cairo). The
build fails without it.

Live reload is on, so edits appear without restarting. Restart only after
changing `mkdocs.yml`, a hook in `scripts/`, or anything under `overrides/`.

## The browser window

Playwright MCP keeps **one** browser across the whole session — currently
Chrome. Navigating replaces the page in that window; it does not open a new
one. So leave it open: the user can then say "check the résumé" at any point
and it is one `browser_navigate` away.

**Do not call `browser_close` until the session is genuinely finished.**
Closing it discards the window, and the next check pays the startup cost again.

Screenshots must be written **inside the repo** — anywhere else is refused
with `outside allowed roots`. Use `.playwright-mcp/`, which is gitignored:

```text
.playwright-mcp/<name>.png
```

Read the PNG back with the Read tool to actually look at it. Taking a
screenshot and not reading it verifies nothing.

`fullPage: true` for a whole page; omit it for above-the-fold framing.

## Reading what you see

- **Hover states lie.** The pointer stays where it last clicked, so an element
  may render in its hover colour. Confirm a resting state with
  `browser_evaluate` and `getComputedStyle` rather than trusting the pixels.
- **`mkdocs serve` rewrites `site_url`** to the dev address. Anything that
  builds absolute URLs — `llms.txt`, `sitemap.xml`, canonical tags — shows
  `127.0.0.1` locally and the real domain in a `mkdocs build`. Not a bug.
- **Check both themes** when touching colour. The palette is dark-only today,
  but link and contrast rules are written against tokens that could change.
- **Check ~400px wide** for anything involving layout.

## Before finishing

```bash
pkill -f 'mkdocs serve -a 127.0.0.1:8777'   # never the user's :8000
rm -rf .playwright-mcp                       # screenshots and console logs
pgrep -fl 'mkdocs serve' || echo "(none)"    # confirm
```

An orphaned server holds the port and silently serves a stale branch to the
next session. Kill it by port, explicitly — `pkill -f 'mkdocs serve'` alone
would take the user's down with it.

## Don't

- Don't run `mkdocs build` to "check" something — it writes `site/` and tells
  you nothing a browser wouldn't. Build only when verifying the build itself.
- Don't commit `.playwright-mcp/` (it's ignored — keep it that way).
- Don't report a visual change as verified without a screenshot you read.
