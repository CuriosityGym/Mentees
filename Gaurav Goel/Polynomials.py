"""This file contains machinery to deal with polynomials, represented as lists of coefficients."""
import random;
import math;

"""The Polynomial Value function returns the value of the given polynomial at the given x."""
def pvalue(x, lis=[]):
    sum_ = 0;
    for i in range(len(lis)):
        sum_ += lis[-i-1]*x**i;
    return sum_;
  
"""The Derivative function returns the polynomial which is the derivative of the input polynomial."""
def deriv(lis=[]):
    lis1 = [];
    n = len(lis)-1;
    for i in range(n):
        lis1.append((n-i)*lis[i]);
    return lis1;

"""The Polynomial Newton-Raphson function starts with a random seed in range [-5,5] and returns an approximate root close the seed with a precision of 4 decimal digits."""
def polynr(lis=[]):
    xi = (random.random()-.5)*10; temp = 0;
    while(math.fabs(pvalue(xi, lis))>0.000001):
        if(pvalue(xi, deriv(lis))==0): return 0;
        xi = xi - pvalue(xi, lis)/pvalue(xi, deriv(lis));
    xi = math.trunc(xi*10000)/10000;
    return xi;

"""The All Roots function returns a list containing all the roots of the given polynomial with repeated calling to the function polynr. Roots with difference <0.001 are not considered to be separate."""
def allroots(lis=[]):
    lisr = [];  temp = 0;
    for i in range(1000):
        flag = 1;
        temp = polynr(lis);
        for el in lisr:
            if math.fabs(temp-el)<0.001:
                flag = 0; break;
        if(flag): 
            lisr.append(temp);
    return lisr;

"""The Sum Lists function takes in two lists and returns the sum of the two polynomials, adjusting for size discrepancies."""
def sumlists(lis1=[], lis2=[]):
    m = len(lis1)-1;
    n = len(lis2)-1;
    sumlis = [];
    if(m==n):
        for i in range(m+1):
            sumlis.append(lis1[i]+lis2[i]);
    if(m>n):
        for i in range(m-n):
            lis2.insert(0,0);
        for i in range(m+1):
            sumlis.append(lis1[i]+lis2[i]);
    if(n>m):
        for i in range(n-m):
            lis1.insert(0,0);
        for i in range(n+1):
            sumlis.append(lis1[i]+lis2[i]);
    return sumlis;

"""The Trim function removes any zeroes at the start of the list."""
def trim(lis=[]):
    while(lis[0]==0):
        del lis[0]
    return lis;

"""The Product function is a function to implement polynomial multiplication."""
def product(lis1=[], lis2=[]):
    n = len(lis1)-1;
    m = len(lis2)-1;
    lisp = [];
    for i in range(m+n+1):
        sum1 = 0;
        for r in range(m+n+1-i):
            if(r>=0 and r<=n and r<=m+n-i and r>=n-i):
                sum1 += lis1[n-r]*lis2[i+r-n];
        lisp.append(sum1);
    return lisp;