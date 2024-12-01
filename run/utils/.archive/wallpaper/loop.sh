#!/bin/bash

DIR="$HOME/run/wallpaper"
OUTPUT_DIR="$DIR/images1"
STATE="$DIR/state.txt"
image_count=$(ls "$OUTPUT_DIR" | wc -l)

set_wallpaper() {
  feh --bg-scale "$1"
}
check_bspc() {
    echo $(($(bspc query -N -n .window -d focused | wc -l)-$(bspc query -N -n .floating.window -d focused | wc -l)))
}
reverse_i() {
    echo $(($image_count-$1))
}

for j in $(seq 0 2); do
    if [[ $(check_bspc) -eq 0 ]]; then
        read state < $STATE || echo "1" > $STATE
        while true; do
            for i in $(seq $state $image_count); do
                set_wallpaper "$OUTPUT_DIR/image_$(printf "%04d" $i).png"
                sleep 0.03
                if [[ $(check_bspc) -ne 0 ]]; then
                    echo $i > $STATE
                    exit
                fi
            done
            state=1
            for i in $(seq $state $image_count); do
                set_wallpaper "$OUTPUT_DIR/image_$(printf "%04d" $(reverse_i $i)).png"
                sleep 0.03
                if [[ $(check_bspc) -ne 0 ]]; then
                    echo $(reverse_i $i) > $STATE
                    exit
                fi
            done
        done
    fi
    sleep 0.05
done
