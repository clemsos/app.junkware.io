var glob = require("glob")
var mkdirp = require('mkdirp');
var stljs = require('stljs');
var exec = require('child_process').exec,
    child;

// source path for STL files 
var STLPath = __dirname + "/../../data/stl";
console.log(STLPath);

// dest path to stoire PNG thumbs
var PNGPath = __dirname + "/../../data/png";

// create path if doesn't exist
mkdirp(PNGPath, function(err) {
    if (err) throw err;
    console.log("created", PNGPath);
});

// list all STL files
var STLfiles = [];
glob(STLPath + "/*.stl", function(er, files) {
    for (var i = 0; i < files.length; i++) {
        STLfiles.push(files[i])
    }
    convertSTLtoPNG(0); // start conversion
    console.log('test');
})

// convert STL file to PNG
var i=0;
var reg = /.+?\:\/\/.+?(\/.+?)(?:#|\?|$)/;
function convertSTLtoPNG(i) {

    console.log(i);
    var PNGFilename = PNGPath+"/"+STLfiles[i].replace(/^.*[\\\/]/, '').slice(0, -4) + ".png"

    STLfiles[i];
    stl2png(STLfiles[i], PNGFilename, function(){
        i++;
        convertSTLtoPNG(i);
    })
    // if(i < STLfiles.length-1) 
}

var stl2png = function(stlFile, pngFile, callback) {

    stljs.imageify(stlFile, {
        width: 400,
        height: 300,
        dst: pngFile
    }, function(err, povOutput, name) {
        if(err) throw err;
        // done with converting the image
        callback();
    }, function(err, povPolygon, name) {
        // poly 
    });
}

// stl2png( "/home/clemsos/Dev/junkware/app.junkware.io/data/stl/steering-column-paper-supply-cassette-and-paper-method.stl", __dirname+"/test.png")

// GIF !

// var step = 8;

// var next = function (stlFile, gifFile, i ) {

//   s = (i<10) ? '0'+i : i
//   phi = Math.PI * i / step

//   stl2image.imageify(stlFile, { width: 400, height: 300, phi: phi, dst: 'img/test'+ s +'.png' }
//     , function (err, povOutput, name ) {
//       process.stdout.write('.')
//       if ( i < step*2 ) {
//         next(i + 1);
//       } else {
//         process.stdout.write("\ngifin...\n")
//         gify(gifFile)
//         process.stdout.write("bye!\n")
//       }
//     }
//     , function (err, povPolygon, name) {
//       // poly 
//     }
//   );
// }

// var gify = function ( path, gifFile ) {
//   child = exec('convert -delay 20 -loop 0 ' + path + '/*.png ' + gifFile,
//     function (error, stdout, stderr) {
//       console.log('stdout: ' + stdout);
//       console.log('stderr: ' + stderr);
//       if (error !== null) {
//         console.log('exec error: ' + error);
//       }
//     });
// }

// var STLtoGif = function(STLFile, GifFile) {
//     var i = 0;
//     next(i);
// }


