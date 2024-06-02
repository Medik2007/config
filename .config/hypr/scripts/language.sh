#!/bin/bash

language=$(hyprctl devices -j | jq -r '.keyboards[] | select(.name == "at-translated-set-2-keyboard") | .active_keymap' | cut -c 1-2 | tr 'A-Z' 'a-z')

if [[ $language == "en" ]]; then
    hyprctl keyword input:kb_layout ru
    $HOME/run/notif/notif.sh low language "Switched to Russian"
else
    hyprctl keyword input:kb_layout us
    $HOME/run/notif/notif.sh low language "Switched to English"
fi

$HOME/.config/waybar/modules/right/trigger.sh
