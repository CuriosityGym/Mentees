$fn = 100;

union()
{
    translate([0,40.7/2-2.5,0])
{
cube([26,2.5,10]);
}

translate([0,-40.7/2-0.5,0])
{
cube([26,2.5,10]);
}

translate([0,-40.7/2-0.5,10])
{
    cube([26, 40.7+0.5,4]);
}
}

difference()
{
    translate([0,-40.7,0])
{
cube([26,20,2]);

}
translate([10,-30,0])
{
cylinder(r = 2.5,h = 5);
}
}



difference(){
    translate([0,40.7/2,0])
{
cube([26,20,2]);
}
translate([10,30,0])
{
cylinder(r = 2.5,h = 5);
}
}
