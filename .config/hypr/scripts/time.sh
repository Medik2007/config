#!/bin/bash

$HOME/.config/hypr/scripts/notifications/notif.sh low time "$(date +"%d  %b       -       %R       -       $(cat /sys/class/power_supply/BAT1/capacity)%")"
