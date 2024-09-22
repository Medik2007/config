#!/bin/bash


__dir_backup() {
    if [ ! -d ".git" ]; then
        echo "\nNo git repo was found"
        git init -q
        touch .gitignore
        ln .gitignore $HOME/run/backup/gitignore/$1
        gh repo create $1 --private || echo "Github repo already exists"
        git remote add origin git@github.com:Medik2007/$1.git
        echo "Git repo created and remote added\n"
    fi
    echo "Looking for changes..."
    git add -A
    if [[ $(git diff --cached --name-only | wc -l) -gt 0 ]]; then
        echo "Uploading changes..."
        git commit -m "Backup"
        git push -f origin master
    else
        echo "There are no changes"
    fi
}

backup() {
    cd
    echo
    echo "===> System backup"
    echo
    __dir_backup config
    echo
    echo "===> Projects backup"
    mkdir -p prj
    cd ~/prj
    for dir in /$PWD/*/; do
        if [[ $a != .* ]]; then
            dir=${dir%*/}
            dir=${dir##*/}
            echo
            echo "=> ${dir}"
            cd ${dir}
            __dir_backup ${dir}
            cd ..
        fi
    done
    cd
}
