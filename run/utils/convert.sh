#!/bin/bash

convert() {
    ffmpeg -i ${1} -c copy ${2}
}
