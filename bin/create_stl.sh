#!/bin/bash

# create STL shapes from DB
python ./make/create_stl_files.py

# create thumb images
cd ./make/stl2png
node stl2png

# invert color (black background)
for i in `ls ./data/png/*.png`; 
    do 
        echo ${i}
        mv ${i%.*}.png ${i%.*}-original.png
        convert -negate ${i%.*}-original.png ${i%.*}.png; 
done
