#!/bin/bash


lil() { 
    ssh ${2} medik@192.168.1.${1}
}

lils() {
    lil 101 || lil 102 || lil 103 || lil 104 || lil 105 || {
        echo
        echo "No route to Lil Stevie was found"
    }
}
