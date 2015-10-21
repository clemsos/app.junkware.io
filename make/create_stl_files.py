import os
import subprocess
from  slugify import slugify
from pymongo import MongoClient
client = MongoClient()


make_path = os.path.join(os.path.join(os.getcwd(), "make"), "stl")
scad_file = os.path.join(make_path,"STLconverter.scad")
template_path = os.path.join(make_path,'template.scad')
output_path = os.path.join(os.path.join(os.getcwd(), "data"),"stl")

template_scad = ""
with open(template_path) as f:
    template_scad = f.read()

# load shape
db = client.junks
junks = db.junks

for junk in junks.find() :
    objectId = slugify(junk["title"])

    shapeData = junk["shape"]
    shape1="shape1=supershape(" + "m=" + str(shapeData["m1"]) + ", n1=" + str(shapeData["n11"]) + ", n2=" + str(shapeData["n12"]) + ", n3=" + str(shapeData["n13"]) + ", a=1, b=1),"

    shape2="shape2=supershape(" + "m=" + str(shapeData["m2"]) + ", n1=" + str(shapeData["n21"]) + ", n2=" + str(shapeData["n22"]) + ", n3=" + str(shapeData["n23"]) + ", a=1, b=1),"

    # print shape1, shape2

    # parse SCAD file
    scad = template_scad.replace("#SHAPE1#", shape1).replace("#SHAPE2#", shape2)
    print scad
    print 'creating STL shape...'

    with open(scad_file, "w") as f:
        f.write(scad)

    #create stl file
    stl_file = os.path.join(output_path,str(objectId)+".stl")

    # write command line for STL file
    cmd = "/usr/bin/openscad -o " + " " + stl_file + " " +scad_file

    # no block, it start a sub process.
    p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # block until the cmd execute finish
    p.wait()

    print "STL file saved at %s"%stl_file


    with open(stl_file, "r") as f :
        stl= f.read()
