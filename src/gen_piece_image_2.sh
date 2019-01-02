#!/usr/bin/env bash
inp_path="$1"  # path to image
out_path="$2"  # path to folder that store all 90 images

s=${inp_path##*/}
echo 'crop file: ' $s
convert $inp_path -crop 10%x11.11% +repage -rotate "0" $out_path/${s%.jpg}_%02d.jpg
