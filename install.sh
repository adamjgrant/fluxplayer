#! /bin/zsh

pip3 install --upgrade pip
brew install gh
gh auth login
pip3 install -r requirements.txt