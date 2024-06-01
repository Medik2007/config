#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias reflect='sudo reflector --latest 5 --age 2 --fastest 5 --protocol https --sort rate --save /etc/pacman.d/mirrorlist'
alias nv='nvim'
alias fish='asciiquarium'
alias act='source bin/activate'
alias deact='deactivate'
alias bashrc='source ~/.bashrc'
alias ju='jump'

alias ls='ls --color=auto'
alias grep='grep --color=auto'

PS1='\W> '
source ~/.local/share/blesh/ble.sh
source ~/run/run.sh

[[ ! -d "$HOME/Downloads/" ]] || rmdir $HOME/Downloads/
