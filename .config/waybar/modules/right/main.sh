#!/bin/bash

trigger="$HOME/.config/waybar/modules/right/trigger.tmp"

render() {
    margin="      "

    date=$(date +"%R")

    volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@)
    volume=$(echo ${volume:8}*100 | bc)
    if [ $volume != 0 ]; then
        volume=${volume::-3}
    fi

    brightness=$(brightnessctl | grep "Current" | cut -f4- -d ' ')
    brightness=${brightness:1:-2}

    battery=$(cat /sys/class/power_supply/BAT1/capacity)
    
    language=$(hyprctl devices -j | jq -r '.keyboards[] | select(.name == "at-translated-set-2-keyboard") | .active_keymap' | cut -c 1-2 | tr 'a-z' 'A-Z')

    echo "${language}${margin}${date}${margin}${volume}%${margin}${brightness}%${margin}${battery}%"
}

render

while true; do
    inotifywait -t 30 $trigger > /dev/null
    render
done
