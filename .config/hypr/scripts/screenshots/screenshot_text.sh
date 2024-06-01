#!/bin/bash

path="$HOME/stf/img/screenshots/part/$(date +"%S-%M-%H-%d-%m-%Y.png")"
txt="$HOME/.config/hypr/scripts/screenshot_text"
grim -g "$(slurp)" $path
tesseract $path $txt -l eng
wl-copy "$(cat "${txt}.txt")"
