#
# ~/.bashrc
#

[[ $- != *i* ]] && return

alias bashrc='source ~/.bashrc'
alias steam='echo NO'
alias minecraft='java -jar ~/stf/TLauncher.v10/TLauncher.jar'

alias reflect='sudo reflector --latest 5 --age 2 --fastest 5 --protocol https --sort rate --save /etc/pacman.d/mirrorlist'
alias kali='virtualboxvm --startvm Kali & exit'
alias windows='virtualboxvm --startvm Windows'

alias nv='nvim'
alias ju='jump'
alias ls='ls --color=auto'
alias l1='ls -1'
alias ll='ls -goh'
alias grep='grep --color=auto'

source ~/.local/share/blesh/ble.sh
source ~/run/utils/run.sh

shopt -s autocd

export VIRTUAL_ENV_DISABLE_PROMPT=1
default_PS1

[[ ! -d "$HOME/Downloads/" ]] || rmdir $HOME/Downloads/
[[ ! -d "$HOME/Documents/" ]] || rmdir $HOME/Documents/
[[ ! -d "$HOME/Desktop/" ]] || rmdir $HOME/Desktop/
