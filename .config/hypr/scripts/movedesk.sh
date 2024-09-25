#!/bin/bash


ws_all=$(hyprctl workspaces -j)
ws_count=$(echo $ws_all | jq length)
ws_active=$(hyprctl activeworkspace -j | jq -r '.id')
passed=0

echo $ws_all | jq -r

for i in $(seq 0 $((ws_count-1))); do
    id=$(echo $ws_all | jq -r ".[$i]" | jq -r ".id")
    if [ $1 -eq 0 ]; then
        if [ $id -eq $ws_active ]; then
            echo $ws_all | jq -r ".[$((i-1))]"
        fi
    else
        if [ $passed -eq 1 ]; then
            echo $ws_all | jq -r ".[$((i))]" | jq -r ".id"
        fi
        if [ $id -eq $ws_active ]; then
            passed=1
        fi
    fi
done

#hyprctl dispatch workspace $result

