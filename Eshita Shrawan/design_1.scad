$fn = 100;

union()
{
    difference()
    {
        cylinder(r = 24/2, h = 20, center=true);
       
        union()
        {
            
        cylinder(r = 6.2/2, h = 20,center=true);
        }
    }

      
}

 translate([0,3-0.5,0])
            {
                
                        cube([4.4,1.2, 20],center=true);
                        
                        //r = 10.81,h = 1.8);
                       
            }
