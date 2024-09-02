#!/bin/bash


#echo "● ○ ○"
#inotifywait $HOME/.config/waybar/modules/center/trigger.tmp > /dev/null

while true; do
    workspaces=(0 0 0 0 0 0 0 0 0 0)
    ws_all=$(hyprctl workspaces -j)
    ws_count=$(echo $ws_all | jq length)
    ws_active=$(hyprctl activeworkspace -j | jq -r '.id')
    result=""

    for i in $(seq 0 $((ws_count-1))); do
        id=$(echo $ws_all | jq -r ".[$i]" | jq -r ".id")
        if [ $id -eq $ws_active ]; then
            workspaces[$((id-1))]=2
        else
            workspaces[$((id-1))]=1
        fi
    done

    for i in $(seq 0 9); do
        case ${workspaces[i]} in
            1) result+=" ○" ;;
            2) result+=" ●" ;;
        esac
    done

    echo $result

    inotifywait $HOME/.config/waybar/modules/center/trigger.tmp > /dev/null
done
