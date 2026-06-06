# Terminal & Dev Setup — Complete Handoff

## Overview

This is a macOS-first terminal setup centered around WezTerm + Tmux + Starship, with the Dracula theme across everything. The entire config is managed via a dotfiles repo at `github.com/prateek11rai/dotfiles`.

---

## 1. WezTerm (Terminal Emulator)

**Config file:** `~/.config/wezterm/wezterm.lua`
**Modules:** `~/.config/wezterm/startup/init.lua`, `~/.config/wezterm/keybindings/init.lua`

### wezterm.lua Settings

| Setting | Value | Why |
|---------|-------|-----|
| `enable_tab_bar = false` | Off | Disables the built-in tab bar because Tmux handles tabs/sessions instead |
| `window_decorations = "RESIZE"` | Only resize handle | Hides title bar and close/minimize buttons for a clean, minimal look |
| `font = JetBrains Mono Bold` | JetBrains Mono at weight Bold | Clean developer-friendly monospace font |
| `font_size = 15` | 15px | Comfortable readability without being too large |
| `color_scheme = "Dracula (Official)"` | Dracula | Consistent purple/dark theme across all tools |
| `window_background_opacity = 0.99` | 99% opaque | Slight transparency (almost solid) for a modern look |
| `macos_window_background_blur = 20` | 20px blur | Blurs the background behind the terminal window on macOS |
| `window_close_confirmation = "NeverPrompt"` | No confirmation | Skips the "are you sure?" prompt on Cmd+Q for fast quitting |

### Modules

WezTerm config is split into modules loaded via `require()`:

**1. `startup/init.lua`** — Startup behavior

| Behavior | Why |
|----------|-----|
| Runs `tmux new-session -A` on launch | Attaches to the most recent tmux session if one exists, or creates a new session if none exist. This means WezTerm and Tmux start together. |
| Maximizes window on startup | Fills the entire screen automatically so there's no manual resizing |
| Uses full path `/opt/homebrew/bin/tmux` | WezTerm's spawn process doesn't inherit the user shell PATH, so an absolute path is required |

**2. `keybindings/init.lua`** — Custom keybindings

| Keybinding | Action | Why |
|------------|--------|-----|
| `Ctrl+Shift+F` | Fit window to active screen | Fixes the window when an external display is disconnected and the window ends up larger than the internal screen. Repositions and resizes to fill the new active display. |

---

## 2. Tmux (Terminal Multiplexer)

**Config file:** `~/.config/tmux/tmux.conf`
**Plugin manager:** TPM (Tmux Plugin Manager) at `~/.config/tmux/plugins/tpm`

### Settings

| Setting | Why |
|---------|-----|
| `prefix = C-a` | Changed from default `C-b` to `C-a` because it's easier to reach and more intuitive (similar to Screen) |
| `mouse on` | Enables click-to-select panes, scroll with mouse wheel, resize panes by dragging — essential for modern terminal usage |
| `bind r` to reload config | Quick reload without restarting tmux after editing `tmux.conf` |
| `bind i` to install plugins | Runs TPM's install script to pull plugins listed in the config |

### Why tmux instead of WezTerm's built-in tabs

WezTerm has its own tab/multiplexing system, but tmux is preferred because:
- Sessions persist even if the terminal window is closed (attach/detach)
- Works over SSH the same way it works locally
- Decades of community usage, plugins, and muscle memory
- Can share sessions with other users

### Plugins Installed

| Plugin | Why |
|--------|-----|
| `tmux-plugins/tpm` | Plugin manager itself — required to install and manage the other plugins |
| `tmux-plugins/tmux-sensible` | A set of sensible defaults for tmux (better escape time, UTF-8 support, improved window/pane behavior) |
| `tmux-plugins/tmux-yank` | Enables copying to system clipboard from tmux — critical for working with copy/paste |

---

## 3. Starship (Shell Prompt)

**Config file:** `~/.config/starship.toml`

Starship is a cross-shell prompt that shows contextual information:

- **Git branch & status** — shows current branch, dirty/clean state, ahead/behind status
- **Language version** — auto-detects and shows versions for Python, Node.js, Rust, Go, Java, and 50+ other languages
- **Command duration** — shows how long the last command took to run
- **Exit code** — shows a red indicator if the previous command failed
- **Username, hostname, directory** — standard prompt info

The config file at `~/.config/starship.toml` contains format strings for every supported module. Each module is configured individually with its own format and styling.

Starship is initialized in `.zshrc` via `eval "$(starship init zsh)"`.

---

## 4. Zsh (Shell)

**Config file:** `~/.zshrc`

### What's in .zshrc

| Line | Why |
|------|-----|
| `eval "$(starship init zsh)"` | Initializes the Starship prompt |
| `pyenv` setup | Manages multiple Python versions. Sets `PYENV_ROOT` and adds pyenv to PATH. Required for Python development. |
| `EDITOR="code --wait"` | Sets VS Code as the default editor. The `--wait` flag makes terminal wait until the file is closed in VS Code — needed for git commits and other tools that open an editor. |
| `source zsh-autosuggestions` | Suggests commands based on history as you type. Shows a faint suggestion that you can accept with the right arrow key. |
| `JAVA_HOME` | Sets Java home to JDK 22 at `/Library/Java/JavaVirtualMachines/jdk-22.jdk/Contents/Home` |
| `uv` init | Source the uv (Python package manager) env if it exists |
| Netskope SSL certs | On corporate machines, sets `AWS_CA_BUNDLE`, `CURL_CA_BUNDLE`, `SSL_CERT_FILE`, `GIT_SSL_CAPATH`, `REQUESTS_CA_BUNDLE`, `NODE_EXTRA_CA_CERTS` to the Netskope cert bundle. Only activates if the cert file exists. |
| `alias vc` | `vcluster platform connect vcluster` — Kubernetes vcluster connection command |
| `alias ap` | `argopm install . -n default -f -c .` — ArgoCD plugin manager install command |

### Why zsh over bash

- Better autocompletion (context-aware, fuzzy matching)
- Framework support (oh-my-zsh, zinit, etc.)
- Richer theming and prompt capabilities
- macOS default shell since Catalina

---

## 5. Neofetch (System Info)

**Config file:** `~/.config/neofetch/config.conf`
**ASCII art:** `~/.config/neofetch/custom-ascii.txt`

Neofetch displays system information when the terminal starts (or when run manually):

- **OS** — macOS version
- **Host** — Mac model identifier
- **Kernel** — Darwin kernel version
- **Uptime** — how long since last boot
- **Packages** — number of Homebrew packages installed
- **Shell** — zsh
- **Resolution** — display resolution(s)
- **DE** — desktop environment
- **WM** — window manager
- **Theme & Icons** — system theme settings
- **Terminal** — WezTerm
- **Terminal Font** — JetBrains Mono

The custom ASCII art replaces the default neofetch logo.

**Note:** Neofetch is archived/unmaintained. The bootstrap script tries `brew install` first, and falls back to downloading the raw script from GitHub. Consider migrating to `fastfetch` as a maintained alternative.

---

## 6. Theme: Dracula

The Dracula theme (https://draculatheme.com/) is used everywhere:

| App | Where it's applied | How to set up |
|-----|-------------------|---------------|
| WezTerm | Config file (built-in scheme) | Already set via `color_scheme = "Dracula (Official)"` |
| VS Code | Extension | Install "Dracula Official" from extensions marketplace |
| Firefox | Theme from Firefox Add-ons | Visit addons.mozilla.org and search for Dracula |
| YouTube | Browser-level | No automation — requires manual theme extension |
| Tmux | Inherited from terminal | Tmux uses the terminal's color scheme, so Dracula in WezTerm covers it |
| Starship | Styling via config | Starship inherits terminal colors; the prompt colors are configured in `starship.toml` |

Anything not covered here needs to be set up manually at `draculatheme.com`.

---

## 7. Wallpaper

**Location in repo:** `wallpapers/macos.png`

The Dracula-themed macOS wallpaper stored in the dotfiles repo for use on any machine.

---

## 8. Dotfiles Repository

**Remote:** `https://github.com/prateek11rai/dotfiles`
**Local clone:** `~/github/prateek11rai/dotfiles/`

### Structure

```
dotfiles/
├── .zshrc                        # Zsh configuration
├── .config/
│   ├── starship.toml             # Starship prompt config
│   ├── tmux/
│   │   └── tmux.conf             # Tmux config
│   ├── neofetch/
│   │   ├── config.conf           # Neofetch display config
│   │   └── custom-ascii.txt      # Custom ASCII art
│   └── wezterm/
│       ├── wezterm.lua           # WezTerm main config
│       ├── startup/
│       │   └── init.lua          # Startup behavior (tmux attach + maximize)
│       └── keybindings/
│           └── init.lua          # Custom keybindings (Ctrl+Shift+F to fit screen)
├── wallpapers/
│   └── macos.png                 # Dracula wallpaper
├── scripts/
│   └── mac-bootstrap.sh          # Full macOS setup script
└── README.md
```

---

## 9. Bootstrap Script

**File:** `scripts/mac-bootstrap.sh`

### What it does (in order)

1. **Install Homebrew** — if not already installed
2. **Install packages via brew:**
   - `tmux` — terminal multiplexer
   - `starship` — prompt
   - `gh` — GitHub CLI
   - `zsh-autosuggestions` — shell autocomplete suggestions
   - `pyenv` — Python version manager
   - `wezterm` (cask) — terminal emulator
   - `font-jetbrains-mono` (cask) — developer font
   - `neofetch` — tries brew first, falls back to direct download from GitHub
3. **Back up existing configs** — if a target file exists and is NOT already a symlink, it's renamed to `<target>.backup.<YYYYMMDD-HHMMSS>` before symlinking. Existing symlinks are replaced silently.
4. **Symlink all config files** — links each file from the repo into the correct `~` or `~/.config/` location. WezTerm modules (`startup/`, `keybindings/`) each get their own directory.
5. **Install tpm and tmux plugins** — clones TPM and runs `install_plugins` to pull tmux-sensible and tmux-yank

### Running on a fresh Mac

```sh
git clone https://github.com/prateek11rai/dotfiles.git ~/github/prateek11rai/dotfiles
~/github/prateek11rai/dotfiles/scripts/mac-bootstrap.sh
```

After this, restart the shell or open WezTerm. Manual steps remaining:
- Install Dracula theme in VS Code, Firefox, etc.
- Set the wallpaper from `wallpapers/macos.png`

---

## 10. VS Code

- **Editor:** VS Code
- **Default terminal inside VS Code:** WezTerm (set via system default)
- **Theme:** Dracula Official (install from VS Code extensions)
- **Git editor:** VS Code with `--wait` flag (configured in `.zshrc`)
- **Shell integration:** Uses the system zsh, which inherits all the dotfiles config

---

## 11. Firefox

- **Theme:** Dracula (manual install from Firefox Add-ons store)
- **No automation possible** — Firefox themes are installed through the browser's addon marketplace

---

## Philosophy Behind the Setup

1. **Tmux-first** — Tmux manages sessions, not the terminal. WezTerm is just a display layer.
2. **One config repo** — All dotfiles live in one place, one bootstrap script sets everything up.
3. **Minimal dependencies** — Only Homebrew and git are needed to bootstrap from scratch.
4. **Consistent theme** — Dracula everywhere reduces visual distraction.
5. **macOS-focused** — This setup is designed for macOS (Apple Silicon). Some paths assume `/opt/homebrew`.
6. **Safe bootstrap** — The script backs up existing files before overwriting, so running it on an already-configured machine won't lose anything.

---

## Potential Future Improvements

- Migrate from neofetch to `fastfetch` (maintained fork)
- Add VS Code settings sync (Settings Sync extension or `~/.config/Code/`)
- Add `.gitconfig` with common aliases
- Create a Linux bootstrap variant
