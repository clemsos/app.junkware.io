include <supershape.scad>

create_supershape();

module create_supershape()
{
    scale([10,10,10])
    RenderSuperShape(
        shape1=supershape(m=8, n1=2, n2=9, n3=40, a=1, b=1),
        shape2=supershape(m=18, n1=0, n2=39, n3=3, a=1, b=1),
        phisteps = 8,
        thetasteps = 64,
        points=false,
        pointcolor=[1,1,1],
        wireframe=false,
        faces=true);

}
