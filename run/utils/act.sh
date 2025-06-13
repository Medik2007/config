#!/bin/bash

venv_prompt() {
  [ -n "$VIRTUAL_ENV" ] && echo "($(basename "$VIRTUAL_ENV"))"
}
git_branch() {
  branch=$(git symbolic-ref --short HEAD 2>/dev/null)
  if [ -n "$branch" ]; then
    echo "($branch)"
  fi
}

export PS1='\n\e[0;35m[$(hostname)] \e[0;37m(\w) \e[0;35m$(git_branch) \e[0;35m$(venv_prompt)\e[0m\n~> '


act() {
    if [[ $1 ]]; then
        source ~/prj/.venv/$1/bin/activate
    else
        source bin/activate
    fi
}
deact() {
    deactivate
}
