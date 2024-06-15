#!/bin/bash

djrun() {
    path=$PWD
    cd ..
    source bin/activate
    cd $path
    python manage.py runserver
}
