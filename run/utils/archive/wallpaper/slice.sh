#!/bin/bash

DIR="$HOME/run/wallpaper"
VIDEO_PATH="$DIR/videos/wallpaper-2.mp4"
OUTPUT_DIR="$DIR/images"
FPS=20

mkdir -p "$OUTPUT_DIR"

ffmpeg -i "$VIDEO_PATH" -r "$FPS" -vf scale=-1:-1 "$OUTPUT_DIR/image_%04d.png"

echo
echo "Wallpaper sliced"
