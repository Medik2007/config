#!/bin/bash


neofetch
yay
echo

echo Updating system configs
cd $HOME
git pull origin master
echo

echo Updating projects
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
        else
            echo
            echo Updating "$prj" project
            echo
            cd $prj
            git pull origin master
            cd ..
        fi
    done
fi
echo
echo Full system update complete
