#!/bin/bash

set -x

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade pip
pip install --upgrade pip
pip install -r requirements.txt

pyinstaller --onefile acctop.py

# Check if the directory exists before creating it
if [ ! -d "$HOME/bin/" ]; then
    mkdir "$HOME/bin/"
fi

mv dist/acctop "$HOME/bin/acctop"

# Add bin directory to PATH in shell configuration files (bashrc and zshrc for common ones)
for shell_config in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$shell_config" ]; then
        echo 'export PATH="$PATH:$HOME/bin"' >> "$shell_config"
    fi
done

# Add bin directory to PATH in shell configuration files (bashrc and zshrc for common ones)
for shell_config in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$shell_config" ]; then
        source "$shell_config"
    fi
done