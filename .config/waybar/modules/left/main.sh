#!/bin/bash

show="$HOME/.config/waybar/modules/show"

render() {
    margin="      "

    cpu="`LC_ALL=C top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}'`%"
    ram="`free -m | awk '/Mem:/ { printf("%3.1f%%", $3/$2*100) }'`"
    hdd="`df -h / | awk '/\// {print $(NF-1)}'`"

    echo "$cpu$margin$ram$margin$hdd"
}

render

while true; do
    sleep 1
    render
done
