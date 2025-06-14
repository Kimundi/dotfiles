#!/bin/sh

set -e

sudo cp ~/.dotfiles/system_setup/fishlogin /usr/local/bin/fishlogin
echo /usr/local/bin/fishlogin | sudo tee -a /etc/shells
sudo usermod -s /usr/local/bin/fishlogin $USER

echo Installed fish as the default shell with .profile inhertance from bash
