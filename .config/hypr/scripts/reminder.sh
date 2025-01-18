#!/bin/bash

big_break=0
while true; do
    sleep 1200
    bash $HOME/.config/hypr/scripts/notifications/notif.sh critical reminder "Eyes off monitor for 20 seconds"
    ((big_break++))
    if [ "$big_break" -eq 3 ]; then
        bash $HOME/.config/hypr/scripts/notifications/notif.sh critical reminder "Big break for 10 minutes"
        sleep 600
        big_break=0
    fi
done
