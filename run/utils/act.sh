#!/bin/bash

default_PS1() {
    export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w) \e[0;35m$(git_branch)\e[0m\n~> '

}

git_branch() {
  branch=$(git symbolic-ref --short HEAD 2>/dev/null)
  if [ -n "$branch" ]; then
    echo "($branch)"
  fi
}


act() {
    if [[ $1 ]]; then
        source ~/prj/.venv/$1/bin/activate &&
        export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w) \e[0;35m$(git_branch) \e[0;35m($(basename $VIRTUAL_ENV))\e[0m\n~> '
    else
        source bin/activate &&
        export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w) \e[0;35m$(git_branch) \e[0;35m($(basename $VIRTUAL_ENV))\e[0m\n~> '
    fi
}

deact() {
    deactivate
    default_PS1
}
