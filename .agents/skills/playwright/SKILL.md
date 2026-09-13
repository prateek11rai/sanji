---
name: playwright
description: Preview the Sanji site in a real browser. Use whenever a change needs to be seen rather than described — layout, palette, contrast, spacing, responsive behaviour — or when the user says "check", "look at it", or "screenshot it". Covers the agent's own preview server on a dedicated port, reading the page, and tearing both down once the check is reported.
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

`.mcp.json` at the repo root pins `@playwright/mcp` and points at
`.agents/playwright-mcp.json`, which starts Chrome maximised with
`viewport: null` — the page fills the window instead of rendering into a
fixed box with grey around it — and passes `--test-type` to drop Chrome's
"unsupported command-line flag" banner. Editing either takes a Claude Code
restart to apply.

**Don't leave the viewport resized.** `browser_resize` overrides the
window-filling viewport for the rest of the session, which is what puts a grey
band around the page. After a narrow check, resize back or reopen the browser.

Playwright MCP keeps **one** browser per session — currently Chrome.
Navigating replaces the page rather than opening another window, so within a
round of checking just navigate; reopening between two screenshots of the same
change is waste. Once the round is reported, close it — see teardown below.

## Seeing vs reading

Two tools, and the cheap one is usually right.

**`browser_snapshot`** returns the accessibility tree — every heading, link,
href and paragraph as text, inline. Use it to check *what* is on the page:
copy, heading levels, link targets, table-of-contents structure. It is exact,
greppable, and costs no image.

**`browser_take_screenshot`** shows *how* it looks: spacing, colour, contrast,
alignment, wrapping. Use it only when appearance is the question.

**Omit `filename` and the image comes back inline** — one call, and the agent
sees it immediately. Passing a filename saves a file you then have to `Read`
back, which is two calls for the same information. Name it only when the file
itself matters: keeping a before/after pair, or handing the user a path.

```text
browser_take_screenshot                       # inline, preferred
browser_take_screenshot(filename: ".playwright-mcp/before.png")
```

Either way a PNG lands in `.playwright-mcp/`, so the cleanup below still
applies. Paths outside the repo are refused with `outside allowed roots`.

`fullPage: true` for the whole page; omit for above-the-fold framing.

## Reading what you see

- **Confirm before calling something broken.** The snapshot omits accessible
  names for links that wrap an icon plus text — the résumé contact row shows
  as bare `link` with only a `/url`, though `textContent` is correct and so is
  the real accessible name. Check with `browser_evaluate` before filing an
  accessibility bug that isn't there.
- **Hover states lie.** The pointer stays where it last clicked, so an element
  may render in its hover colour. Confirm a resting state with
  `browser_evaluate` and `getComputedStyle` rather than trusting the pixels.
- **`mkdocs serve` rewrites `site_url`** to the dev address. Anything that
  builds absolute URLs — `llms.txt`, `sitemap.xml`, canonical tags — shows
  `127.0.0.1` locally and the real domain in a `mkdocs build`. Not a bug.
- **Check both themes** when touching colour. The palette is dark-only today,
  but link and contrast rules are written against tokens that could change.
- **Check ~400px wide** for anything involving layout — `browser_resize`, then
  snapshot or screenshot. The tab bar is hidden below 1220px, so desktop
  spacing tells you nothing about the phone. **Undo it afterwards** — the
  window stays where it was left and the user is looking at it.
- **`browser_console_messages`** catches JS errors a screenshot renders past.
  The GitHub releases 404 on every page is known and harmless.

## Tear down after every check

Not "at the end of the session" — **as soon as the verification round is
done and reported.** Leave them running and the window sits there showing a
stale page while a server holds a port in the background, which is how an
orphaned `mkdocs serve` once survived an entire session.

```bash
pkill -f 'mkdocs serve -a 127.0.0.1:8777'   # never the user's :8000
rm -rf .playwright-mcp                       # screenshots and console logs
pgrep -fl 'mkdocs serve' || echo "(none)"    # confirm
```

Then `browser_close`.

Starting again costs ~15s, which is cheaper than the confusion of a window
showing something that is no longer true. The one exception is when the user
asks to keep it up to look at — then leave it, and say so.

Kill the server by port, explicitly. A bare `pkill -f 'mkdocs serve'` would
take the user's :8000 down with it.

## Don't

- Don't run `mkdocs build` to "check" something — it writes `site/` and tells
  you nothing a browser wouldn't. Build only when verifying the build itself.
- Don't commit `.playwright-mcp/` (it's ignored — keep it that way).
- Don't report a visual change as verified without having looked at it.
- Don't screenshot what a snapshot answers — "is the heading right" is text.
