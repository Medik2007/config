#
# ~/.bash_profile
#

if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
    export GTK_THEME=Adwaita-dark
    export QT_QPA_PLATFORM=wayland
    export QT_QPA_PLATFORMTHEME=qt5ct
    export QT_STYLE_OVERRIDE=kvantum
    export XCURSOR_THEME=Bibata-Modern-Ice
    Hyprland
fi

[[ -f ~/.bashrc ]] && . ~/.bashrc
