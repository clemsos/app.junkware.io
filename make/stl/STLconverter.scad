include <supershape.scad>

create_supershape();

module create_supershape()
{
    scale([10,10,10])
    RenderSuperShape(
        shape1=supershape(m=5, n1=837, n2=155, n3=825, a=1, b=1),
        shape2=supershape(m=8, n1=132, n2=596.104995766, n3=466.045723963, a=1, b=1),
        phisteps = 8,
        thetasteps = 64,
        points=false,
        pointcolor=[1,1,1],
        wireframe=false,
        faces=true);

}
