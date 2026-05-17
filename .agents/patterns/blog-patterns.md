# Blog Post Patterns

## Pattern 1: Technical Guide (Homelab / Self-Hosting)

Used in: `ohara.md`

```
Title: Descriptive, benefit-driven ("Breathing Life Into an Old PC: ...")
```

Structure:
1. **Opening Hook** — personal anecdote about the problem
2. **Image** before the break
3. `<!-- more -->`
4. **Hardware/Context** — what you're working with (grid cards for specs)
5. **Decision Points** — why you chose X over Y (table or comparison)
6. **Step-by-step Setup** — actionable commands, one concept per section
7. **Diagrams** — architecture mermaid for each component
8. **Client Setup** — how each device connects
9. **Complete Architecture** — full mermaid diagram showing everything
10. **Closing** — thematic reflection + checklist of what you'll have

Image placement:
- Intro image (before break): hardware or setup photo
- Section images: optional, avoid forcing it
- Closing image: thematic / reflective

Code density: high. Every section has a runnable code block.

---

## Pattern 2: Character Analysis / Opinion

Used in: `sanji.md`

```
Title: Single-word or short name
```

Structure:
1. **Opening** — why this topic matters to you
2. **Image** before the break
3. `<!-- more -->`
4. **Thematic sections** — each explores a different angle of the topic
5. **Closing** — personal takeaway

Image placement:
- One image per major section (high density)
- Images illustrate the emotional/thematic point
- Closing image: optional

Code density: none. No code blocks.

---

## Pattern 3: Extension Post (follow-up to an existing guide)

Intended for: posts that build on a previous one (e.g. "Adding X to Ohara")

Structure:
1. **Opening** — reference the previous post, state what changed
2. **Image** before the break
3. `<!-- more -->`
4. **Context** — what you're adding and why
5. **Setup** — focused on just the new thing (assumes existing infra from previous post)
6. **Integration** — how it fits with existing services
7. **Troubleshooting** — issues encountered and fixes
8. **Architecture** — updated mermaid showing the new component
9. **Closing** — what's next

Image placement:
- Intro image: the new hardware or a thematic photo
- Troubleshooting section: screenshots if relevant
- Architecture diagram: always
