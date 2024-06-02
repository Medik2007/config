#!/bin/bash

while true; do
    battery=$(cat /sys/class/power_supply/BAT1/capacity)
    if [[ $battery -lt 20 ]]; then
        $HOME/run/notif/notif.sh critical battery "Battery charge is low: $battery%"
    fi
    sleep 300
done
