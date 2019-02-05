"""This is a program to use Euler's method to numerically solve IVPs with second order ode's."""
import math;
import matplotlib.pyplot as plt;
dx = 0.01;

#Example 1: solving y'' = y' - y^2 sin(xy).
#Converting into 2 single order ode's: v' = v - y^2 sin(xy) and y' = v
#The parameters are values of y and y' at 0 respectively.
def ode1(y0, y1):
    x = 0;
    lisx = [0];
    y0n = y0;
    lisy0 = [y0];
    y1n = y1;
    lisy1 = [y1];
    while x <= 3:
        x += dx;
        lisx.append(x);
        y0n += y1n*dx;
        lisy0.append(y0n);
        y1n += (y1n - (y0n**2)*math.sin(x*y0n))*dx;
        lisy1.append(y1n);
    plt.plot(lisx, lisy0);
    plt.plot(lisy0, lisy1);

#Example 2: solving the standard y'' = - y
#converting into 2 single order ode's: v' = -y, y' = v
#Same parameters
def ode2(y0, y1):
    x = 0;
    lisx = [0];
    y0n = y0;
    lisy0 = [y0];
    y1n = y1;
    lisy1 = [y1];
    while x <= 10:
        x += dx;
        lisx.append(x);
        y0n += y1n*dx;
        lisy0.append(y0n);
        y1n += -y0n*dx;
        lisy1.append(y1n);
    plt.plot(lisx, lisy0);
    plt.plot(lisy0, lisy1);
    
#Example 3: solving y'' = y^3e^(-y')+e^(y)sin(y);
#Converting into 2 single order ode's: v' = e^(-v)+e^y; y' = v;
#Same parameters
def ode3(y0,y1):
    x = 0;
    lisx = [0];
    y0n = y0;
    lisy0 = [y0];
    y1n = y1;
    lisy1 = [y1];
    while x <= 5:
        x += dx;
        lisx.append(x);
        y0n += y1n*dx;
        lisy0.append(y0n);
        y1n += y0n**3*math.exp(-y1n)+math.exp(-y0n)*math.sin(y0n);
        lisy1.append(y1n);
    plt.plot(lisx, lisy0);
    plt.plot(lisy0, lisy1);

#Schrodinger equation infinite well
def schrinf(l, no):
    x = 0;
    lisx = [];
    dx = l/no;
    while x<l:
        lisx.append(x);
        x+=dx;
    
    E = 0;
    dE = 0.01;
    Emax = 5;
    
    j = 0;
    lisj = [];
    lisE = [];
    lisslop = [];
    
    y = 0; y1 = 0;
    slope = 0;
    lisy = [];
    lisy1 = [];
    
    while E<=Emax:
        slope = 0;
        while slope <= 10:
            lisy.append([]);
            lisy1.append([]);
            x = 0;
            y = 0;
            y1 = slope;
            while x < l:
                x+=dx;
                y += y1*dx;
                y1 += -E*y*dx;
                lisy[j].append(y);
                lisy1[j].append(y1);
            if(math.fabs(lisy[j][-1])<0.01):
                lisj.append(j);
                lisE.append(math.floor(E*1000)/1000);
                lisslop.append(slope);
            j+=1;
            slope+=0.01;
        E+=dE;
    
    print(lisE);
    print(lisj);
    print(lisslop);
    print(len(lisx));
    print(len(lisj));
    for j in lisj:
        plt.plot(lisx, lisy[j]);
        