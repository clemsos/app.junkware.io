define(function() {
  var WIDTH = 250;
  var HEIGHT = 120;

  return {
    width: WIDTH,
    height: HEIGHT,
    aspect: WIDTH / HEIGHT,
    viewAngle: 45,
    near: .1,
    far: 1000,
    phiSteps: 200,
    thetaSteps:200
  };
});
