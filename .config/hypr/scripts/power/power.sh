#!/bin/bash

notif=$HOME/.config/hypr/scripts/power/notif
while true; do
    battery=$(cat /sys/class/power_supply/BAT1/capacity)
    if [[ $battery -lt 20 ]]; then
        echo $(notify-send -p -u critical -r $(cat $notif) "Battery charge is low: $battery%") > $notif
    fi
    sleep 300
done
