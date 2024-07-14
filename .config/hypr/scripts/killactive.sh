#!/bin/bash

hyprctl dispatch killactive
sleep 1

active_workspace=$(hyprctl activeworkspace -j | jq '.id')
window_count=$(hyprctl activeworkspace -j | jq -r .windows)
if [[ $window_count == 0 ]]; then
    if [[ $active_workspace == 9 ]]; then
        firefox &
    elif [[ $active_workspace == 10 ]]; then
        kitty ~ &
    fi
fi
