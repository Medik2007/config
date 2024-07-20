#!/bin/bash

act() {
    source bin/activate
    export PS1='\n($(basename $VIRTUAL_ENV))-(\w)\n~> '
}

deact() {
    deactivate
    export PS1='\n(\w)\n~> '
}
