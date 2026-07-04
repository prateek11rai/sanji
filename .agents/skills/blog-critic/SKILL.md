---
name: blog-critic
description: Adversarial pre-publication review for Sanji blog posts. Use before any post ships (or after major edits) to catch overclaimed causality, unevidenced claims, copy-paste-broken code, and readability failures. Runs three reader personas plus a claims-evidence audit and returns findings ranked by severity with proposed edits.
version: 1.0.0
license: MIT
---

# Blog Critic

Adversarial review harness for posts in `docs/blog/posts/`. Born from the rglob-race post review (July 2026), where three independent critics found publishable-quality prose sitting on top of an unproven causal story and copy-paste-broken fix code. This skill encodes what they caught so every future post gets the same treatment before it ships.

## When to use

- Before opening the PR for any new post.
- After any edit that changes a technical claim, a diagram, or a code block.
- NOT for drafting — this skill only critiques. Pair with `write-blog-post` and `avoid-ai-writing`.

## How to run

Read the full post, then execute the four audits below **in order** (evidence first — readability polish is worthless on top of a wrong claim). Where practical, run the three personas as parallel subagents against the rendered page rather than the source file: fresh eyes, real rendering, no author bias. Consolidate into the output format at the end.

## Audit 1 — Claims and evidence (the one that prevents embarrassment)

For every claim in the post, ask which of these it is, and enforce the matching rule:

| Claim type | Rule |
|---|---|
| Cited third-party fact (issue, quote, date, benchmark) | Must link a primary source. Verify quotes verbatim; verify the source actually shows what the sentence says it shows (scope check — a delete race is not a listing race). |
| Own observation | Must state what was actually measured, on what (versions, hardware, rates), or explicitly say it wasn't measured. "It reproduced" with no numbers is a finding, not evidence. |
| Causal claim about own incident | The hard one. Either show the mechanism (trace, error, repro) or explicitly hedge — "we never identified the mechanism" is publishable; implying certainty is not. Check the TITLE and DIAGRAMS against this too: a diagram that draws an unobserved step as a runtime fact is a claim, and the single likeliest target of the top corrective comment. |
| Spec/standard quote | Check the quote's *conditions* against the post's scenario. A clause about concurrent modification does not cover a sequential write-then-read. Misapplied spec quotes are catnip for expert commenters. |
| Folklore ("X is 2x faster", "everyone knows") | Source it, benchmark it, or cut it. |

Also check: does the post hold others to an evidentiary standard its own incident section doesn't meet? (The rglob post celebrated a CPython issue "accepted because it came with strace output" while showing no traces of its own.)

## Audit 2 — Code blocks

Every code block a reader might paste:

- **Runs as pasted.** All imports present, all names defined (no phantom exception classes or loggers), stdlib-compatible idioms (no structlog kwargs on a stdlib logger).
- **No magic numbers** without a comment or a `getattr`-style fallback that explains them.
- **Docstrings tell the truth** — if a check is a heuristic tripwire, say "tripwire, not proof"; if a step is a theory, say so in the comment.
- **Gate sentence before the fix**: tell the reader in one line whether they even need this code ("only if you list a directory in the same breath as writing into it").
- Off-by-one/dead-code sweep: retry loops vs backoff tables, unused entries, mislabeled variables.

## Audit 3 — The three personas

Run each persona against the post (parallel subagents reading the live/preview URL when possible):

1. **The impatient searcher** — googled the symptom, has the bug right now. Can they reach the fix in under 30 seconds? Is there a jump link near the top? Does the fix section open with the gate sentence?
2. **The junior dev (2 years, no systems background)** — where do they get lost? Every syscall/tool name (`strace`, `fd`, `st_ino`, IOPS) glossed at first mention? Are the "in plain English" boxes pitched at the *actual* gap — never below the audience floor (a box explaining `try/except` to Python readers teaches them to skip all boxes, including the load-bearing one)? Would they retain the thesis — ask for the two-sentence version they'd tell a coworker.
3. **The HN skeptic (staff systems engineer)** — write the top five corrective comments this post would receive, each rated: `would-embarrass` / `needs-caveat` / `nitpick`. This persona gets Audit 1's results as ammunition.

## Audit 4 — House style (Sanji-specific)

- `blog-rules.md` compliance: front matter, H2-only, language tags on every fence, footnotes at bottom (first = image attribution), intro + closing One Piece images, theme not forced.
- Mermaid: no `style` directives; diagrams must survive `scripts/syndicate.py` (mermaid.ink conversion) — and remember diagrams are claims (Audit 1).
- Collapsibles (`???`) and admonitions must survive the dev.to transform (`{% details %}` / blockquotes) — run the transform on the real file, don't assume.
- Length sanity: if the middle is history, is there an escape hatch for the symptom-driven reader? History is an asset only when it's skippable.

## Output format

```markdown
## Verdict
One paragraph: survives publication as-is / needs fixes first. Name the single likeliest top corrective comment.

## Findings
| # | Severity | Section | Finding | Proposed edit |
severity ∈ would-embarrass | needs-caveat | nitpick
Ordered by severity. Quote the exact sentence at fault.

## What's strong
Two or three genuinely defensible strengths — so edits don't sand them off.
```

## Standing lessons (extend as posts teach new ones)

- The absence of an error is not evidence an error didn't fire — when the API is silent, say "we can't know," don't pick the story that flatters the narrative.
- fsync is a durability primitive, not a visibility primitive. Any "we synced before reading" claim needs a theory label.
- An honest hedge in paragraph nine does not license a confident title, intro, or diagram — readers meet those first, and critics quote them.
- "Bring your own X" after a code block means the code block is broken.
