#!/bin/bash


if [[ $1 == "f" ]]; then
    dir="$HOME/stf/img/screenshots/"
elif [[ $1 == "p" ]]; then
    dir="$HOME/stf/img/screenshots/part/"
elif [[ $1 == "t" ]]; then
    dir="$HOME/stf/img/screenshots/text/"
fi

echo $dir

mkdir -p $dir
path="$dir$(date +"%d-%m-%Y")-"
i=0
while [ -f "$path$i.png" ]; do
    i=$((i+1))
done
path="$path$i.png"


if [[ $1 == "f" ]]; then
    grim $path
    wl-copy < $path
    
elif [[ $1 == "p" ]]; then
    grim -g "$(slurp)" $path
    wl-copy < $path

elif [[ $1 == "t" ]]; then
    txt="${path::-4}"
    grim -g "$(slurp)" $path
    tesseract $path $txt -l eng
    wl-copy "$(cat "${txt}.txt")"
fi


