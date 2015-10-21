# app.junkware.io

Online showcase app for the Junkware project

## Install

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt


## Develop 

    (venv)$ python app.py

You need compass to compile the stylesheets

    gem install compass


### Deploy

To deploy, use [those Fabric scripts](https://github.com/clemsos/flask-fabric-deploy).

## Load JSON data into mongo

    mongoimport -d junks -c junks db.json 
    # 2015-01-31T17:15:39.281+0100 imported 41 objects

## Generate STL 3D models

    sudo apt-get install openscad 
    python make/create_stl_files.py

## Generate thumbnails

    sudo apt-get install povray
    cd make/stl2png
    npm install
    node stl2png.js
