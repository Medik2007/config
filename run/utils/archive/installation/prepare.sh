#!/bin/bash

echo $(pacman -Qqe) > packages.txt
firefox https://github.com/settings/tokens
