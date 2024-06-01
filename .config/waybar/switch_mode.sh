#!/bin/bash

path="$HOME/.config/waybar"
source $path/switch_power.sh
mode="$path/switch_mode"
config_max="$path/config_max"
config_min="$path/config_min"
config="$path/config"

if [[ $(cat $mode) -eq "0" ]]; then
    echo 1 > $mode
    waybaroff
    echo $(cat $config_max) > $config
    waybar
else
    echo 0 > $mode
    waybaroff
    echo $(cat $config_min) > $config
    waybar
fi
