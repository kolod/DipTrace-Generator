#!/bin/bash

# Sharing Git credentials with your container
# https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials#_sharing-gpg-keys

# Setup gpg
sudo apt-get update
sudo apt-get install gnupg2 -y

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/home/vscode/.local/bin:$PATH"
echo 'export PATH="/home/vscode/.local/bin:$PATH"' | tee -a /home/vscode/.bashrc

# Install dependencies
poetry install
