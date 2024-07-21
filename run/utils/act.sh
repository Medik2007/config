#!/bin/bash

default_PS1() {
    export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w)\e[0m\n~> '
}

act() {
    source bin/activate &&
    export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w) \e[0;35m($(basename $VIRTUAL_ENV))\e[0m\n~> '
}

deact() {
    deactivate
    default_PS1
}
