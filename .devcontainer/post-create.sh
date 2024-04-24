#!/bin/sh

# Setup gpg
# https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials#_sharing-gpg-keys
#export GPG_TTY=$(tty)
#echo 'export GPG_TTY=$(tty)' | tee -a /home/vscode/.bashrc
sudo apt-get update
sudo apt-get install gnupg2 -y

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/vscode/.local/bin:$PATH"
echo 'export PATH="/home/vscode/.local/bin:$PATH"' | tee -a /home/vscode/.bashrc

# Install dependencies
poetry install
