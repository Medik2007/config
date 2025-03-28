#!/bin/bash

change=5
if [ $2 ]; then
    change=$2
fi
 
wpctl set-volume -l 1.0 @DEFAULT_AUDIO_SINK@ $change%$1

$HOME/.config/waybar/modules/right/trigger.sh

volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@)
volume=$(echo ${volume:8}*100 | bc)
if [ $volume != 0 ]; then
    volume=${volume::-3}
fi

$HOME/.config/hypr/scripts/notifications/notif.sh low volume "$volume%"
