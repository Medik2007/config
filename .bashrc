#
# ~/.bashrc
#

[[ $- != *i* ]] && return

alias nv='nvim'
alias ju='python ~/run/steve/jump.py'
alias runserver='python manage.py runserver'
alias bashrc='source ~/.bashrc'

alias ls='ls --color=auto'
alias l1='ls -1'
alias ll='ls -goh'
alias grep='grep --color=auto'

alias backoff='backup && poweroff'
alias back_pub='backup && printf "\n\n\n" && publish'
alias bottle='prime-run bottles -b bottle'

source ~/.local/share/blesh/ble.sh
source ~/run/utils/run.sh

shopt -s autocd

export VIRTUAL_ENV_DISABLE_PROMPT=1
default_PS1

[[ ! -d "$HOME/Downloads/" ]] || rmdir $HOME/Downloads/
[[ ! -d "$HOME/Documents/" ]] || rmdir $HOME/Documents/
[[ ! -d "$HOME/Desktop/" ]] || rmdir $HOME/Desktop/
