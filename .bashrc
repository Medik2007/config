#
# ~/.bashrc
#

[[ $- != *i* ]] && return

alias bashrc='source ~/.bashrc'
alias reflect='sudo reflector --latest 5 --age 2 --fastest 5 --protocol https --sort rate --save /etc/pacman.d/mirrorlist'
alias kali='virtualboxvm --startvm Kali & exit'
alias windows='virtualboxvm --startvm Windows'

alias nv='nvim'
alias ju='python ~/run/jump/jump.py'
alias ls='ls --color=auto'
alias l1='ls -1'
alias ll='ls -goh'
alias grep='grep --color=auto'
alias backoff='backup && poweroff'
alias back_pub='backup && printf "\n\n\n" && publish'
alias bottle='prime-run bottles -b bottle'
alias mods='cd ~/.local/share/bottles/bottles/fallout/drive_c/users/steamuser/Documents/Paradox\ Interactive/'

source ~/.local/share/blesh/ble.sh
source ~/run/utils/run.sh

shopt -s autocd

export VIRTUAL_ENV_DISABLE_PROMPT=1
default_PS1

[[ ! -d "$HOME/Downloads/" ]] || rmdir $HOME/Downloads/
[[ ! -d "$HOME/Documents/" ]] || rmdir $HOME/Documents/
[[ ! -d "$HOME/Desktop/" ]] || rmdir $HOME/Desktop/
