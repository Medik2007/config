#!/bin/bash

if [[ $1 == "-" ]]; then
    brightnessctl set 5%-
else
    brightnessctl set +5%
fi

$HOME/.config/waybar/modules/right/trigger.sh

brightness=$(brightnessctl | grep "Current" | cut -f4- -d ' ')
brightness=${brightness:1:-2}

notif=$HOME/.config/hypr/scripts/brightness/notif
echo $(notify-send -p -u low -r $(cat $notif) "Brightnesss: $brightness%") > $notif
