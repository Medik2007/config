#!/bin/bash


__dir_backup() {
    echo "Moving to $1"
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
        git push origin master
    else
        echo "There are no changes"
    fi
}


backup() {
    path="$HOME/run/backup"

    cd
    __dir_backup config

    echo

    cd ~/prj
    for dir in /$PWD/*/; do
        dir=${dir%*/}
        dir=${dir##*/}
        echo
        echo ${dir}
        cd ${dir}
        __dir_backup ${dir}
        cd ..
    done

    cd
}


clear_backups() {
    echo -n "Are you sure you want to delete all backups? (y/N) "
    read char
    if [[ char == 'y' ]]; then
        cd ~/run
        gh repo delete --yes
        rm -rf .git/
        
        cd
        gh repo delete --yes
        rm -rf .git/

        cd ~/stf/archive
        gh repo delete --yes
        rm -rf .git/

        cd ~/prj
        for dir in /$PWD/*/; do
            dir=${dir%*/}
            dir=${dir##*/}
            echo
            echo ${dir}
            cd ${dir}
            gh repo delete --yes
            rm -rf .git/
            cd ..
        done
    fi
}
