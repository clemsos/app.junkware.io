import os
import json
import random
from flask import render_template, jsonify, send_from_directory, request, make_response
from resources import app, api, mongo
from Junk import Junk, JunkList

# routes
@app.route('/')
def home():
    junks= [x for x in mongo.db.junks.find()]
    return render_template('home.html', junks=junks)

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

# junks

@app.route('/junks')
def junk_index():
    junks= [x for x in mongo.db.junks.find()]
    return render_template('index.html', junks=junks)

@app.route('/junk/<ObjectId:objectId>')
def junwkare(objectId):
    junk=mongo.db.junks.find_one_or_404({"_id": objectId})
    del junk["_id"]
    return render_template('junk/view.html', objectId=objectId, junk=junk)

@app.route('/junk/partials/<path:path>')
def partials(path):
    print path
    return render_template(os.path.join('partials',path+".html"))


@app.route('/junk/<ObjectId:objectId>/<path:path>')
def single_junk(objectId, path):
    junk=mongo.db.junks.find_one_or_404({"_id": objectId})
    del junk["_id"]
    return render_template(os.path.join('partials',path+".html"), objectId=objectId, junk=junk)

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

'''
@app.route('/data/toStl/<ObjectId:objectId>', methods = ['POST']) 
def convertToSTL(objectId):

    shapeData = json.loads(request.form["shape"])

    print str(shapeData["m1"])+"ha"

    shape1="shape1=supershape(" + "m=" + str(shapeData["m1"]) + ", n1=" + str(shapeData["n11"]) + ", n2=" + str(shapeData["n12"]) + ", n3=" + str(shapeData["n13"]) + ", a=1, b=1),"
    
    shape2="shape2=supershape(" + "m=" + str(shapeData["m2"]) + ", n1=" + str(shapeData["n21"]) + ", n2=" + str(shapeData["n22"]) + ", n3=" + str(shapeData["n23"]) + ", a=1, b=1),"
    
    print shape1, shape2

    scad = template_scad.replace("#SHAPE1#", shape1).replace("#SHAPE2#", shape2)
    print scad
    print 'creating STL shape...'
 
    make_path = os.path.join(os.getcwd(),"make")
    scad_file = os.path.join(make_path,"STLconverter.scad")
    stl_file = os.path.join(make_path,str(objectId)+".stl")

    with open(scad_file, "w") as f:
        f.write(scad)

    cmd = "/usr/bin/openscad -o " + " " + stl_file + " " +scad_file

    # no block, it start a sub process.
    p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # and you can block util the cmd execute finish
    p.wait()

    print "STL file saved at %s"%stl_file

    with open(stl_file, "r") as f :
        stl= f.read()

    response = make_response(stl)
    response.headers["Content-Disposition"] = "attachment; filename=" + str(objectId)+ ".stl"
    return response
    # return jsonify({'fileUrl' : "/data/stlFile/"+str(objectId)+"/download" })

@app.route('/data/getStlFile/<ObjectId:objectId>') 
def getSTL(objectId):
    print objectId
    make_path = os.path.join(os.getcwd(),"make")
    stl_file = os.path.join(make_path,str(objectId)+".stl")

    with open(stl_file, "r") as f :
        stl= f.read()
    response = make_response(stl)
    response.headers["Content-Disposition"] = "attachment; filename=" + str(objectId)+ ".stl"
    return response


template_scad = """
include <supershape.scad>

create_supershape();

module create_supershape()
{
    scale([10,10,10])
    RenderSuperShape(
        #SHAPE1#
        #SHAPE2#
        phisteps = 8,
        thetasteps = 64,
        points=false,
        pointcolor=[1,1,1],
        wireframe=false,
        faces=true);

}
"""
'''
