#!/bin/bash

source $HOME/run/jump/modules.sh
jump_args=()


__jump_search_print() {
    if [[ -d $2 && $2 != ".." ]]; then
        echo "$1 $2/"
    else
        echo "$1 $2"
    fi
}
__jump_search_display() {
    local -n arr=$1
    __jump_search_print ">" "${arr[0]:2}"
    for i in $(seq 1 ${#arr[@]}); do
        __jump_search_print " " "${arr[i]:2}"
    done
    for i in $(seq -1 ${#array[@]}); do
        tput cuu1
    done
}
__jump_search_clear() {
    for i in $(seq 0 $1); do
        tput el
        tput cud1
    done
    for i in $(seq 0 $1); do
        tput cuu1
    done
}
__jump_add_argument() {
    if [[ $(find . -maxdepth 1 -name "$1*" ! -name ".") != "" ]]; then
        jump_args+=("$1")
    fi
}


__jump_func() {
    local result=""

    if [ ! ${1} ]; then
        echo "${jump_args[*]}"
        read -a array <<< $(echo $(find . -maxdepth 1 -name "*" ! -name "." ! -path '*/.*'))
        __jump_search_display array

        while read -s -n 1 char; do
            num=`echo $char | tr -d "\n" | od -An -t dC`
            if [[ ! $char ]]; then
                break 
            elif [[ $num -eq 127 ]]; then
                if [[ ${#result} -gt 0 ]]; then
                    result="${result::-1}"
                fi
            elif [[ $num -eq 27 ]]; then
                __jump_search_clear ${#array[@]}
                return
            elif [[ $char == "/" ]]; then
                if [[ ${#jump_args} -gt 0 ]]; then unset jump_args[-1]; fi
                cd ..
            else
                result="$result$char"
            fi

            __jump_search_clear ${#array[@]}

            if [[ ${#jump_args} -gt 0 ]]; then echo -n "${jump_args[*]} "; fi
            echo "$result"

            if [[ ${result::1} != "." ]]; then
                read -a array <<< $(echo $(find . -maxdepth 1 -name "${result}*" ! -name "." ! -path '*/.*'))
            else
                read -a array <<< $(echo $(find . -maxdepth 1 -name "${result}*" ! -name "."))
            fi

            __jump_search_display array
        done

        __jump_search_clear ${#array[@]}
    else
        result=$1
        for i in "$@"; do
            if [[ $2 ]]; then
                __jump_add_argument $1
                cd $(find . -maxdepth 1 -name "$1*" ! -name ".")
                shift
            else
                if [[ $1 == "/" ]]; then
                    jump_args+=("/")
                    ls
                    return
                else
                    result=$1
                fi
            fi
        done
    fi

    local obj=$(find . -maxdepth 1 -name "${result}*" ! -name "." -print -quit)
    if [[ ${#result} -gt 0 && ${#obj} -gt 0 ]]; then
        __jump_add_argument $result
        local ending=$(cut -d "." -f3 <<< $obj)
        if [[ -d $obj ]]; then
            cd $obj
            __jump_func
        elif [[ $ending == "png" ]]; then
            feh $obj
        else
            nvim $obj
        fi
    else
        __jump_func
    fi
}


jump() {
    tput civis
    jump_args=()
    jump_args_select=0
    cd
    
    if [[ ${1} ]]; then
        in_arr="\<${1}\>"

        if [[ ${jumpShorts[$1]} != "" ]]; then
            __jump_func ${jumpShorts[$1]}; return 0
        fi

        if [[ ${jumpDjango[@]} =~ $in_arr ]]; then
            __jump_django $1; return 0
        fi

        if [[ ${jumpDaphne[@]} =~ $in_arr ]]; then
            __jump_daphne $1; return 0
        fi

        if [[ ${jumpScad[@]} =~ $in_arr ]]; then
            __jump_scad $1; return 0
        fi
    fi

    __jump_func $@
    echo "jump ${jump_args[*]}"
}
