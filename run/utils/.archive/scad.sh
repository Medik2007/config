#!/bin/bash

scad() {
    path="${PWD}/${1}"
    openscad $path &
    nv $path
}
