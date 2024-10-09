#!/bin/bash

ws_all=$(hyprctl workspaces -j)
ws_count=$(echo $ws_all | jq length)
ws_active=$(hyprctl activeworkspace -j | jq -r '.id')
current=$ws_active
success=1

while [[ $current != 0 && $current != 11 ]]; do
    if [ $1 == 0 ]; then
        current=$((current - 1))
    else
        current=$((current + 1))
    fi

    for i in $(seq 0 $((ws_count-1))); do
        id=$(echo $ws_all | jq -r ".[$i]" | jq -r ".id")
        if [ $current == $id ]; then
            success=0
            break
        fi
    done

    if [ $success == 0 ]; then
        break
    fi
done

if [ $success != 0 ]; then
    if [ $1 == 0 ]; then
        current=$((ws_active - 1))
    else
        current=$((ws_active + 1))
    fi
fi

hyprctl dispatch workspace $current
$HOME/.config/waybar/modules/center/trigger.sh $current
