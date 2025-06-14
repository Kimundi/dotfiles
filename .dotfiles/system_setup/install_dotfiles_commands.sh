#!/bin/bash

set -e

function setup {
    mkdir -p $HOME/.dotfiles
    git init --bare $HOME/.dotfiles/git_dir
    dotfiles="git --git-dir=$HOME/.dotfiles/git_dir --work-tree=$HOME"
    $dotfiles remote add origin git@github.com:Kimundi/dotfiles.git
    $dotfiles fetch
    $dotfiles reset origin/master
    $dotfiles branch --set-upstream-to=origin/master
    $dotfiles restore $HOME/bin/dotfiles

    echo "Done"
    echo "Manage your dotfiles via $HOME/bin/dotfiles"
}

setup
