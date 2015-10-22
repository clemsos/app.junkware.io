import os
import json
import random
from flask import render_template, jsonify, send_from_directory, request, make_response
from resources import app, api, mongo
from slugify import slugify
from Junk import Junk, JunkList

GALLERY_PATH=os.path.join("uploads","gallery")

def get_random_junks():
    return [x for x in mongo.db.junks.find().limit(8).skip( random.randint(0, mongo.db.junks.count()) )]
# routes
@app.route('/')
def home():
    gallery_path = os.path.join(os.getcwd(), GALLERY_PATH)
    gallery_files = [pic for pic in os.listdir(gallery_path) if not os.path.isdir(pic)]
    gallery_files.remove("thumb")
    for f in gallery_files : print f
    junks= get_random_junks()
    if len(junks) is not 8 : get_random_junks()
    return render_template('home/index.html', junks=junks, gallery=gallery_files)

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

# STATIC
@app.route('/js/<path:path>')
def js_static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))

@app.route('/css/<path:path>')
def css_static_proxy(path):
    print os.path.join('css', path)
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))

@app.route('/lib/<path:path>')
def lib_static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('lib', path))

@app.route('/libs/<path:path>')
def libs_static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('libs', path))

@app.route('/img/<path:path>')
def img_static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('img', path))

@app.route('/data/<path:path>')
def data_static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('data', path))

@app.route('/uploads/<path:path>')
def uploads_static(path):
    uploads_dir=os.path.join(os.getcwd(), os.path.join('uploads'))
    # print uploads_dir
    # return app.send_file(os.path.join(uploads_dir, path))
    return send_from_directory(uploads_dir, path)

# junks

@app.route('/junks')
def junk_index():
    junks= [x for x in mongo.db.junks.find()]
    return render_template('junks/index.html', junks=junks)

@app.route('/junk/<ObjectId:objectId>')
def junwkare(objectId):
    junk=mongo.db.junks.find_one_or_404({"_id": objectId})
    del junk["_id"]
    return render_template('junk/single.html', objectId=objectId, junk=junk)

@app.route('/junk/partials/<path:path>')
def partials(path):
    print path
    return render_template(os.path.join("junk", os.path.join('partials',path+".html")))

@app.route('/junk/<ObjectId:objectId>/<path:path>')
def single_junk(objectId, path):
    junk=mongo.db.junks.find_one_or_404({"_id": objectId})
    del junk["_id"]
    return render_template(os.path.join("junk",os.path.join('partials',path+".html")), objectId=objectId, junk=junk)

# API
api.add_resource(JunkList, '/api/junks')
api.add_resource(Junk, '/api/junk/<ObjectId:junk_id>')

@app.route('/api/junk/<ObjectId:objectId>/dna')
def get_junk_dna(objectId):
    junk=mongo.db.junks.find_one_or_404({"_id": objectId})
    return jsonify({"dna":junk["dna"]})

@app.route('/api/junk/<ObjectId:objectId>/molecule')
def get_junk_molecule(objectId):
    junk=mongo.db.junks.find_one_or_404({"_id": objectId})
    return jsonify({"molecule":junk["molecule"]})

# data
@app.route('/data/molecules/<path:path>')
def get_molecule_file(path):
    print path
    app_path = os.getcwd()
    data_path= os.path.join(app_path, 'data')
    molecule_path=os.path.join(data_path, "molecules")
    print molecule_path
    return send_from_directory(molecule_path, path)

# STL files (3D print)
@app.route('/data/stl/<ObjectId:objectId>') 
def getSTL(objectId):
    junk=mongo.db.junks.find_one_or_404({"_id": objectId})
    slug = slugify(junk["title"])
    stl_path = os.path.join(os.path.join(os.getcwd(),"data"), "stl")
    stl_file = os.path.join(stl_path,str(slug)+".stl")

    with open(stl_file, "r") as f :
        stl= f.read()

    response = make_response(stl)
    response.headers["Content-Disposition"] = "attachment; filename=" + str(objectId)+ ".stl"
    return response

# 3D print
@app.route('/data/img3D/<ObjectId:objectId>') 
def getPNG(objectId):

    junk=mongo.db.junks.find_one_or_404({"_id": objectId})
    slug = slugify(junk["title"])

    png_path = os.path.join(os.path.join(os.getcwd(),"data"), "png")
    png_file = os.path.join(png_path,str(slug)+".png")
    print png_file 

    with open(png_file, "r") as f :
        png= f.read()

    response = make_response(png)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'attachment; filename=' + str(slug)+ '.png'
    return response
