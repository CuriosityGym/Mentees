import math;
import matplotlib.pyplot as plt;
"""Solving a boundary value problem. y'' = - w^2*y; y(0) = 0; y(1) = 0"""

x = 0; dx = 0.01;
lisx = [];
while x<=1:
    lisx.append(x);
    x+=dx;

y = 0;
lisy = [];
y1 = 0;
lisy1 = [];

#This function takes w as input and gives y(1) as output
def solving(w):
    x  = 0;
    y = 0;
    y1 = 2;
    while (x<=1):
        y1 -= (w**2)*y*dx;
        y += y1*dx;
        x += dx;
    return y;

#solves for w that give y(1)=0
def doeswork():
    lisw =[];
    w = 0;
    dw = 0.001;
    while(w<=16):
        if math.fabs(solving(w))<0.001:
            lisw.append(math.trunc(w*1000)/1000);
        w+=dw;
    return lisw;
    
def printing(lis=[]):
    for w in lis:
        lisy = [];
        x = 0;
        y = 0;
        y1 = 1;
        while(x<=1):
            y1 -= (w**2)*y*dx;
            y += y1*dx;
            x += dx;
            lisy.append(y);
        plt.plot(lisx,lisy);