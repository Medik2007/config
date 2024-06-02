#!/bin/bash
 
wpctl set-volume -l 1.0 @DEFAULT_AUDIO_SINK@ 5%$1

$HOME/.config/waybar/modules/right/trigger.sh

volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@)
volume=$(echo ${volume:8}*100 | bc)
if [ $volume != 0 ]; then
    volume=${volume::-3}
fi

$HOME/run/notif/notif.sh low volume "Volume: $volume%"
