#!/bin/bash

language=$(hyprctl devices -j | jq -r '.keyboards[] | select(.name == "at-translated-set-2-keyboard") | .active_keymap' | cut -c 1-2 | tr 'A-Z' 'a-z')
notif=$HOME/.config/hypr/scripts/language/notif.tmp
if [[ $(cat $notif) -eq ""  ]]; then
    echo "0" > $notif
fi

if [[ $language == "en" ]]; then
    hyprctl keyword input:kb_layout ru
    echo $(notify-send -p -u low -r $(cat $notif) "Switched to Russian") > $notif
else
    hyprctl keyword input:kb_layout us
    echo $(notify-send -p -u low -r $(cat $notif) "Switched to English") > $notif
fi

$HOME/.config/waybar/modules/right/trigger.sh
