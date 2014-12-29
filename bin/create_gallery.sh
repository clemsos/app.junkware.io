#!/bin/bash

dest_folder=${PWD}/../gallery
thumbnail_size=200

echo "Creating gallery in $dest_folder"
mkdir -p $dest_folder
mkdir -p $dest_folder/thumb

find . -maxdepth 1 -type f  \( -name "*.JPG" -o -name "*.jpg" \)| while read f
do
    echo "processing image $f..."
    safename="$(echo $f | sed 's/ /_-_/g')"
    echo $safename

    convert "$f" -scale 20% -size 24% -quality 80 $dest_folder/$safename
    echo "   image resized and saved as $safename" 
    
    convert -define jpeg:size=200x200  "$f" -thumbnail ${thumbnail_size}x${thumbnail_size}^ -gravity center -extent ${thumbnail_size}x${thumbnail_size} "$dest_folder/thumb/$safename" 
    echo "   thumbnail created"
done
