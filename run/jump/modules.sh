#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

declare -A jumpShorts
jumpShorts=(
    ["hypr"]=".config hypr hyprland.conf"
    ["waybar"]=".config waybar config"
    ["mako"]=".config mako config"
    ["kitty"]=".config kitty kitty.conf"
    ["nvim"]=".config nvim init.lua"
    ["jump"]="run jump jump.sh"
    ["college"]="run jump images college.png"
    ["backup"]="run backup backup.sh"
    ["notif"]="run notif notif.sh"
    ["img"]="stf img /"
)
jumpDjango=(
    "yp"
    "grace"
    "sim"
)
jumpScad=(
    "rpi"
)

__jump_scad() {
    openscad $HOME/prj/$1/scad/main.scad &
    cd prj/$1/scad
    git pull origin master
    nv main.scad
}

__jump_django() {
    cd ~/prj/$1
    git pull origin master
    kitty @ launch --type tab --cwd current sh -c "source bin/activate && cd $1 && nvim; exec $SHELL" &&
    (
        kitty @ set-tab-title "$1 server"
        source bin/activate
        cd $1
        ./manage.py runserver 
    )
}
