#!/bin/bash

for f in data-original/*
do
    if [[ "$f" =~ .*wav$ ]]; then
        echo $f
    else
        fname=$(basename -- "$f")
        ext="${fname##*.}"
        fout="${f/\.$ext/\.wav}"
        if [ ! -f "$fout" ]; then
            ffmpeg -i "$f" "$fout"
        fi
    fi
done