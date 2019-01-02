#!/usr/bin/env bash
inp_path="$1"  # path to board image
out_path="$2"  # path to folder that store all 90 images

# start cropping
for file in $inp_path/*; do
    s=${file##*/}
    echo 'crop file: ' $s
    convert $file -crop 10%x11.11% +repage -rotate "0" $out_path/${s%.jpg}_%02d.jpg
done
