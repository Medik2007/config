#
# ~/.bash_profile
#

if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
    Hyprland
fi

[[ -f ~/.bashrc ]] && . ~/.bashrc
