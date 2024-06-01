#!/bin/bash

path="$HOME/stf/img/screenshots/part/$(date +"%S-%M-%H-%d-%m-%Y.png")"
grim -g "$(slurp)" $path
wl-copy < $path
