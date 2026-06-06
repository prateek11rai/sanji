# Blog Post Patterns

## Pattern 1: Technical Guide (Homelab / Self-Hosting)

Used in: `ohara.md`

```
Title: Descriptive, benefit-driven ("Breathing Life Into an Old PC: ...")
```

Structure:
1. **Opening Hook** — personal anecdote about the problem
2. **Image** — OP-themed intro image before the break
3. `<!-- more -->`
4. **Hardware/Context** — what you're working with (grid cards for specs)
5. **Decision Points** — why you chose X over Y (table or comparison)
6. **Step-by-step Setup** — actionable commands, one concept per section
7. **Diagrams** — architecture mermaid for each component
8. **Client Setup** — how each device connects
9. **Complete Architecture** — full mermaid diagram showing everything
10. **Closing** — thematic reflection + checklist of what you'll have, tied to OP theme

Image placement:
- Intro image (before break): OP-themed or hardware photo
- Section images: optional, avoid forcing it
- Closing image: OP character parallel to the reflection

Code density: high. Every section has a runnable code block.

---

## Pattern 2: Character Analysis / Opinion

Used in: `sanji.md`

```
Title: Single-word or short name
```

Structure:
1. **Opening** — why this topic matters to you
2. **Image** — before the break
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
2. **Image** — before the break
3. `<!-- more -->`
4. **Context** — what you're adding and why
5. **Setup** — focused on just the new thing (assumes existing infra from previous post)
6. **Integration** — how it fits with existing services
7. **Troubleshooting** — issues encountered and fixes
8. **Architecture** — updated mermaid showing the new component
9. **Closing** — what's next

Image placement:
- Intro image: OP-themed or the new hardware
- Troubleshooting section: screenshots if relevant
- Architecture diagram: always

---

## Pattern 4: Rant + One Piece (Tooling, Workflow, Dotfiles)

Used in: (intended for `wezterm-tmux-setup` and similar)

```
Title: "Crafting Your Terminal Like a Chef Sharpens His Knives" — poetic, craft-focused
```

The idea: this pattern blends a technical walkthrough with the personality of a rant and the visual identity of One Piece. Every section carries a parallel to Sanji's philosophy — tools as craft, setup as ritual, config as personal expression.

Structure:
1. **Opening Hook** — personal rant about defaults being bad, why you care about this tool
2. **OP Intro Image** — character or scene that fits the craft theme (Sanji in the kitchen, Franky building, Zoro sharpening swords)
3. **Why This Tool** — hot take about why the mainstream alternative is overrated (e.g. "iTerm2 is fine if you like bloat"). Compare in a table.
4. **The Core Setup** — step-by-step config walkthrough. Each subsection ties back to the OP metaphor.
5. **Trivia Break** — an admonition or footnote with an obscure fact about the tool or its history
6. **The Dotfiles** — show the actual config files (or key excerpts). Explain why each setting matters.
7. **Visual Proof** — screenshot of the working setup + OP-themed image that matches the aesthetic
8. **Rant Section** — dedicated space for a strong opinion. What almost made you quit. What you'd change. Use `!!! quote "Hot Take"`.
9. **Architecture / Flow** — mermaid diagram showing how the pieces fit (e.g. WezTerm → tmux → zsh → starship)
10. **Closing** — tie back to the OP character. "Sanji doesn't use a dull knife. Why should you use a default terminal?"

Image placement:
- Intro: OP character in a craft/creation scene
- Each major section: optional but encouraged — mix of screenshots and OP art
- Closing: OP character reflecting on mastery

Code density: medium-high. Config file excerpts, not full files.

One Piece Angle Matrix (for reference):

| Tool/Concept | OP Parallel | Why |
|---|---|---|
| Terminal | Sanji's kitchen | Your space, your rules, your tools |
| tmux | Franky's workshop | Multiplexing = multiple projects at once |
| WezTerm | Zoro's swords | Configurable, sharp, cuts through lag |
| Dotfiles | Nami's maps | Navigation through your system |
| Starship prompt | Chopper's medicine chest | Diagnostic at a glance |
| Zsh plugins | Robin's bookshelf | Knowledge ready when you need it |
| Neovim | Sanji's knives | Craftsmanship, precision, personal |

Trivia / Rant Ideas:
- WezTerm history: why the author built it (GPU-accelerated terminals were all incomplete)
- tmux vs screen: the ancient war
- Lua vs TOML configs: opinionated take
- Your actual hot take about font rendering on macOS
