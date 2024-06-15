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
        git checkout $(hostname)
        git commit -m "Backup"
        git push origin $(hostname)
    else
        echo "There are no changes"
    fi
}



__projects_check() {
    echo Checking that all projects are installed
    cd ~/prj

    repo_exclude=('config' 'archive')
    gh_prj=$(($(gh repo list | wc -l) - ${#repo_exclude[@]}))
    local_prj=$(find . -maxdepth 1 -type d ! -name "." | wc -l)

    repo_exclude_jq=$(printf '%s\n' "${repo_exclude[@]}" | jq -R . | jq -s .)
    projects=($(gh repo list --json name |
               jq -r --argjson names "$repo_exclude_jq" '.[] | select(.name as $name | $names | index($name) | not)' |
               jq -r '.name'))

    if [[ $local_prj -lt $gh_prj ]]; then
        for prj in ${projects[@]}; do
            if [[ ! -d $prj ]]; then
                echo
                echo Installing "$prj" project
                echo
                gh repo clone $prj
            fi
        done
    fi
    echo
    echo All projects are installed
}


backup() {
    cd
    echo "===> System backup"
    echo
    __dir_backup config
    echo
    echo "===> Projects backup"
    mkdir -p prj
    cd ~/prj
    for dir in /$PWD/*/; do
        dir=${dir%*/}
        dir=${dir##*/}
        echo
        echo "=>${dir}"
        cd ${dir}
        __dir_backup ${dir}
        cd ..
    done
    cd
}


clear_backups() {
    echo -n "Are you sure you want to delete all backups? (y/N) "
    read char
    if [[ false ]]; then
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
