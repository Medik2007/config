#!/bin/bash

language=$(hyprctl devices -j | jq -r '.keyboards[0].layout')

if [[ $language == "us" ]]; then
    hyprctl keyword input:kb_layout ru
    $HOME/.config/hypr/scripts/notifications/notif.sh low language "Switched to Russian"
else
    hyprctl keyword input:kb_layout us
    $HOME/.config/hypr/scripts/notifications/notif.sh low language "Switched to English"
fi

$HOME/.config/waybar/modules/right/trigger.sh
