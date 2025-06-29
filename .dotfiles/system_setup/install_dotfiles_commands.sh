#!/bin/bash

set -e

function setup {
    if ! compgen -G "$HOME/.ssh/*.pub" > /dev/null; then
      echo "Set up a ssh key first, and register it with github!"
      exit 1
    fi

    echo "Setting up dotfiles"
    echo

    mkdir -p $HOME/.dotfiles
    git init --bare $HOME/.dotfiles/git_dir -b master
    dotfiles="git --git-dir=$HOME/.dotfiles/git_dir --work-tree=$HOME"
    $dotfiles remote add origin git@github.com:Kimundi/dotfiles.git
    $dotfiles fetch
    $dotfiles reset origin/master
    $dotfiles branch --set-upstream-to=origin/master
    $dotfiles restore $HOME/bin/dotfiles

    echo "✔ Done"
    echo
    echo "Current status:"
    $dotfiles status
    echo
    echo "Manage your dotfiles via ~/bin/dotfiles"
}

setup
