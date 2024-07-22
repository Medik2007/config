#!/bin/bash

if [[ $1 == "-" ]]; then
    brightnessctl set 1%-
else
    brightnessctl set +1%
fi

$HOME/.config/waybar/modules/right/trigger.sh

brightness=$(brightnessctl | grep "Current" | cut -f4- -d ' ')
brightness=${brightness:1:-2}

$HOME/.config/hypr/scripts/notifications/notif.sh low brightness "$brightness%"
