#
# ~/.bashrc
#

[[ $- != *i* ]] && return

alias nv='nvim'
alias ls='ls --color=auto'
alias l1='ls -1'
alias ll='ls -goh'
alias du='du -hd 1'
alias rmr='rm -i'
alias rm='trash'
alias grep='grep --color=auto'
alias feh='feh --keep-zoom-vp --draw-filename'
alias wifi='nmcli dev wifi'

alias ju='python ~/run/jump.py'
alias backup='python ~/run/backup.py'
alias kb='python ~/run/knowledge.py'

alias runserver='python manage.py runserver'
alias runpython='python -m http.server 8000'
alias bashrc='source ~/.bashrc'
alias bottle='prime-run bottles -b games'
alias enterdocker='docker exec -it joomla /bin/bash'
alias vcb='/home/medik/stf/games/VCB/vcb.x86_64'

alias rest='sudo cp -r ~/prj/wp_rest /srv/http/wordpress/wp-content/themes/'
alias tanya='prj/college/website && act college'

alias django_files='cd ~/prj/.venv/college/lib/python3.13/site-packages/django/contrib'

alias steam='echo nah'

alias tanya='cd ~/prj/college/website && act college'

source ~/.local/share/blesh/ble.sh
source ~/run/utils/run.sh

shopt -s autocd
shopt -s extglob

export VIRTUAL_ENV_DISABLE_PROMPT=1
default_PS1

[[ ! -d "$HOME/Downloads/" ]] || rmdir $HOME/Downloads/
[[ ! -d "$HOME/Documents/" ]] || rmdir $HOME/Documents/
[[ ! -d "$HOME/Desktop/" ]] || rmdir $HOME/Desktop/
