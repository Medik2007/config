#!/bin/bash

$HOME/.config/hypr/scripts/notifications/notif.sh low time "$(date +"%R       -       %d  %b       -       $(cat /sys/class/power_supply/BAT1/capacity)%")"
