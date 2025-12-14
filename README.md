# Sanji

A Personal blog site built using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
The site has three sections:
- About Me : Personal Information
- Projects : Catalogue of projects
- Blog : Rants

## Setup

Guide will contain Mac commands.

### Install Python

Recommend using pyenv to control different python versions.

#### Install xcode

```bash
xcode-select --install
```

#### Install and Setup Homebrew

Download the installer

```bash
curl -fsSL -o install.sh https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
```

Execute the installer

```bash
/bin/bash install.sh
```

Edit PATH

```bash
nano ~/.zshrc
```

```bash
# Add Homebrew's executable directory to the front of the PATH
export PATH=/usr/local/bin:$PATH
```

```bash
source ~/.zshrc
```

Check that homebrew is installed

```bash
brew doctor
```

#### Install pyenv

Install pyenv using brew

```bash
brew install pyenv
```

Edit Path

```bash
nano ~/.zshrc
```

```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

```bash
source ~/.zshrc
```

#### Install python 3.12.2

```bash
pyenv install 3.12.2
```

```bash
pyenv global 3.12.2
```

### Install Dependencies

#### Install uv

```bash
brew install uv
```

#### Sync libraries

Enter the root of the directory and install all libraries

```bash
uv sync
```

### Test

#### Run the Server

```bash
uv run mkdocs serve
```

#### Stop the Server

```bash
^ + C
```