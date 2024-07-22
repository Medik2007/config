#!/bin/bash

cat /sys/class/power_supply/BAT1/capacity &&
while true; do
    battery=$(cat /sys/class/power_supply/BAT1/capacity)
    if [[ $battery -lt 20 ]]; then
        $HOME/.config/hypr/scripts/notifications/notif.sh critical battery "Low battery: $battery%"
    fi
    sleep 300
done
