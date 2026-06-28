# Sanji

A personal blog built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

| Section | Contents |
|---------|----------|
| Me | Personal information |
| Projects | Catalogue of projects |
| Blog | Rants |

**Hosted at:** <https://prateek11rai.github.io/sanji/>

![Sanji](docs/assets/images/blog/sanji/sanji-intro.jpg)

---

## Quick Start

```bash
git clone https://github.com/prateek11rai/sanji.git
cd sanji
brew install uv
uv sync --all-groups --all-extras --upgrade
uv run poe serve
```

Open <http://127.0.0.1:8000/sanji/>, then `^C` to stop.

---

## Prerequisites

### Xcode Command Line Tools

```bash
xcode-select --install
```

### Homebrew

```bash
curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash

# Add to ~/.zshrc:
export PATH=/usr/local/bin:$PATH

source ~/.zshrc
```

### Python (via pyenv)

```bash
brew install pyenv
```

Add to `~/.zshrc`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

```bash
source ~/.zshrc
pyenv install 3.12.2
pyenv global 3.12.2
```

## Setup

### System Dependencies

Social card generation requires the `cairo` graphics library:

```bash
brew install cairo
```

### Python Dependencies

```bash
brew install uv
uv sync --all-groups --all-extras --upgrade
```

## Development

| Command | What it does |
|---------|-------------|
| `uv run poe serve` | Start dev server with live reload |
| `uv run poe build` | Build static site to `site/` |

Stop the server with `^C`.
