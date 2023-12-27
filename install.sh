#! /bin/zsh

pip install --upgrade pip
brew install gh
gh auth login
pip install -r requirements.txt