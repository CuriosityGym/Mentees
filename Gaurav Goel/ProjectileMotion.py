mport math;
import matplotlib.pyplot as plt;
class Instant:
    #class attributes
    g=9.8;
    #instance attributes
    def __init__(self,x=0,y=0,vx=0,vy=0):
        self.x=x; self.y=y; self.vx=vx; self.vy=vy;
    #to print the data
    def display(self):
        print("The particle is at ({},{}) and its velocity is <{},{}>.".format(self.x,self.y,self.vx,self.vy));
        print("Acceleration due to gravity is {} m/s^2.".format(self.__class__.g));
def projectile(v, theta):
    lisx=[0]; lisy=[0];
    dt = 0.0001; g=9.8;
    maxh = 0;
    lis=[Instant(0,0,v*math.cos(theta),v*math.sin(theta))]
    i=0;
    while True:
        lis.append(Instant(lis[i].x+lis[i].vx*dt, lis[i].y+lis[i].vy*dt, lis[i].vx, lis[i].vy-g*dt));
        if lis[i+1].vy>=0: maxh = lis[i+1].y;
        if lis[i+1].y<=0: break;
        lisx.append(lis[i+1].x); lisy.append(lis[i+1].y);
        i+=1;
    plt.plot(lisx,lisy);
    rang = lis[-1].x;
    time = len(lis)*dt;
    print("The range of projectile is {}.\nThe time of flight is {}.\nThe maximum height is {}.".format(rang,time,maxh))

#implementing air drag now
def projectile_with_drag(v, theta):
    lisx=[0]; lisy=[0];
    dt = 0.0001; k = .00008; maxh = 0; g = 9.8
    lis=[Instant(0,0,v*math.cos(theta),v*math.sin(theta))];
    i=0;
    while True:
        lis.append(Instant(lis[i].x+lis[i].vx*dt,lis[i].y+lis[i].vy*dt,(lis[i].vx)*(1-k),(lis[i].vy)*(1-k)-g*dt));
        if lis[i+1].vy>=0: maxh = lis[i+1].y;
        if lis[i+1].y<=0: break;
        lisx.append(lis[i+1].x); lisy.append(lis[i+1].y);
        i+=1;
    plt.plot(lisx,lisy);
    rang = lis[-1].x;
    time = len(lis)*dt;
    print("The range of projectile is {}.\nThe time of flight is {}.\nThe maximum height is {}.".format(rang,time,maxh))

projectile(10,math.pi/3); projectile_with_drag(10,math.pi/3);
projectile(10,math.pi/4); projectile_with_drag(10,math.pi/4);
projectile(10,math.pi/6); projectile_with_drag(10,math.pi/6);

#implementing collisions now
def projectile_with_collisions(v, theta):
    lisx=[0]; lisy=[0];
    dt = 0.0001; e = 0.85; g = 9.8; xmax = 15;
    lis = [Instant(0,0,v*math.cos(theta),v*math.sin(theta))];
    i=0;
    while True:
        lis.append(Instant(lis[i].x+lis[i].vx*dt, lis[i].y+lis[i].vy*dt, lis[i].vx, lis[i].vy-g*dt));
        if lis[i+1].x<=xmax: 
            i+=1; lisx.append(lis[i].x); lisy.append(lis[i].y); 
        else: break;
        if lis[i].y<=0: 
            lis.append(Instant(lis[i].x+lis[i].vx*dt, lis[i].y, lis[i].vx, -e*(lis[i].vy)));
            i+=1; lisx.append(lis[i].x); lisy.append(lis[i].y); 
    plt.plot(lisx,lisy);   

projectile_with_collisions(6,math.pi/4);

#implementing collisions with air-drag now
def projectile_with_collisions_and_drag(v, theta):
    lisx=[0]; lisy=[0];
    dt = 0.0001; e = 0.85; g = 9.8; xmax = 10; k = 0.0001;
    lis = [Instant(0,0,v*math.cos(theta),v*math.sin(theta))];
    i=0;
    while True:
        lis.append(Instant(lis[i].x+lis[i].vx*dt, lis[i].y+lis[i].vy*dt, (lis[i].vx)*(1-k), (lis[i].vy)*(1-k)-g*dt));
        if lis[i+1].x<=xmax: 
            i+=1; lisx.append(lis[i].x); lisy.append(lis[i].y); 
        else: break;
        if lis[i].y<=0: 
            lis.append(Instant(lis[i].x+lis[i].vx*dt, lis[i].y, (lis[i].vx)*(1-k), -(lis[i].vy)*(1-k)*e));
            i+=1; lisx.append(lis[i].x); lisy.append(lis[i].y); 
    plt.plot(lisx,lisy);
    
projectile_with_collisions_and_drag(15,math.pi/4);