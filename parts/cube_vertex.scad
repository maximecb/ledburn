// Radius of the pipe hole
r=22/2;

module edge()
{
    translate([0, 0, -13])
    
    difference()
    {
        translate([-13, -13, 0])
        cube([26, 26, 50]);
        
        translate([0, 0, -1])
        cylinder(r=r, h=52, $fn=100);
        
        translate([0, 50, 37])
        rotate([90, 0, 0])
        cylinder(r=2, h=100, $fn=100);
    }
}

module vertex()
{
    rotate([90, 0, 0]) edge();
    rotate([0, 90, 0]) edge();
    edge();
    
    // Make sure the inside of the corner is filled
    cube([24, 24, 24], center=true);
}

difference()
{
    vertex();
    
    rotate([90, 0, 0]) cylinder(r=9, h=40, $fn=100, center=true);
    rotate([0, 90, 0]) cylinder(r=9, h=40, $fn=100, center=true);
    cylinder(r=9, h=40, $fn=100, center=true);
}