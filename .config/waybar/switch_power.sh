#!/bin/bash

waybaroff() {
    killall waybar
    while pgrep -x waybar >/dev/null; do sleep 1; done
}

if [[ $(pgrep waybar) ]]; then
    waybaroff
else
    waybar
fi
