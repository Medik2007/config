#!/bin/bash

pacman -Syu $(cat packages.txt)

pacman -S --needed git base-devel
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si

gh auth login --with-token < token.txt
gh repo clone config
gh repo clone run

cp config/.bash_profile ~/ 
cp config/.bashrc ~/ 
cp config/.config ~/ 
