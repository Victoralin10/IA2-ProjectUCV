#!/bin/bash

audio_dir=$1
if [ "$audio_dir" == "" ]; then
    audio_dir="data-original"
fi

for f in $audio_dir/*
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