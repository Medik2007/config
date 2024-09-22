#!/bin/bash

default_PS1() {
    export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w)\e[0m\n~> '
}

act() {
    if [[ $1 ]]; then
        source ~/prj/.venv/$1/bin/activate &&
        export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w) \e[0;35m($(basename $VIRTUAL_ENV))\e[0m\n~> '
    else
        source bin/activate &&
        export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w) \e[0;35m($(basename $VIRTUAL_ENV))\e[0m\n~> '
    fi
}

deact() {
    deactivate
    default_PS1
}
