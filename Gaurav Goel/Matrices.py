"""This file contains machinery to deal with matrices and linear algebra."""
import Polynomials

"""The following class contains the details of an mxn matrix (m rows and n columns)."""
class Matrix:
    #constructor accepting size of matrix, and creeating an empty two-dimensional array of the specified size containing None
    def __init__(self, rows, cols):
        self.m = rows;
        self.n = cols;
        self.entries = [];
        for i in range(self.m):
            self.entries.append([]);
            for j in range(self.n): 
                self.entries[i].append(None);
    
    #sets the value of element (i,j) of the matrix to the given value
    def setvalue(self, i, j, val):
        if(1<=i and i<=self.m and 1<=j and j<=self.n): 
            self.entries[i-1][j-1] = val;
        else:
            print("Error: i or j not acceptable.")
    
    #returns the value of element (i,j)
    def getvalue(self, i, j):
        if(1<=i and i<=self.m and 1<=j and j<=self.n): 
            return self.entries[i-1][j-1];
        else:
            print("Error: i or j not acceptable.")
            return(-1);
    
    #displays the matrix in a tabular format where each element has field width 10
    def display(self):
        for i in range(self.m):
            for j in range(self.n):
                print(f"{self.getvalue((i+1),(j+1)):10}", end=" ");
            print();
    
    #checks for compatibility and adds two matrices
    def __add__(self, other):
        if(self.m!=other.m or self.n!=other.n):
            print("Error: incompatible.")
            return(Matrix(0,0));
        sum1 = Matrix(self.m, self.n);
        for i in range(self.m):
            for j in range(self.n):
                sum1.setvalue(i+1,j+1,self.getvalue(i+1,j+1) + other.getvalue(i+1,j+1));
        return sum1;
    
    #checks for compatibility and multiplies two matrices
    def __mul__(self,other):
        if(self.n!=other.m):
            print("Error: incompatible.")
            return(Matrix(0,0));
        prod = Matrix(self.m,other.n);
        for i in range(self.m):
            for j in range(other.n):
                val = 0;
                for r in range(self.n):
                    val += self.getvalue(i+1,r+1)*other.getvalue(r+1,j+1);
                prod.setvalue(i+1,j+1,val);
        return prod;
    
"""The following class contains the details of a square matrix, as a derived class of Matrix. This implements inheritance."""
class Square(Matrix):
    #constructor taking order and intializing both rows and columns to same size
    def __init__(self, order):
        Matrix.__init__(self,order,order);
     
    #given (i,j) returns the square matrix formed by deleting the ith row and jth column from the given matrix
    def minormatrix(self, i, j):
        if(1<=i and i<=self.m and 1<=j and j<=self.m):
            minmat = Square(self.m-1);
            mini = 1;
            minj = 1;
            for loopi in range(self.m): 
                if i==loopi+1: continue;
                for loopj in range(self.m):
                    if j==loopj+1: continue;
                    temp = self.getvalue(loopi+1,loopj+1);
                    minmat.setvalue(mini, minj, temp);
                    #updating and reaching the next element of minmat, traversing it row by row
                    if(mini<=self.m-1 and minj<self.m-1): minj += 1;
                    elif (mini<self.m-1 and minj==self.m-1): minj = 1; mini += 1;
            return minmat;
        else:
            print("Out of bounds.");
            return(Square(0));
        
    #Expanding along row 1, recursively
    def det(self):
        det = 0;
        if self.m == 1: #if the order is 1, the determinant is just the value
            return self.getvalue(1,1);
        else:  #if the order is greater than 1, evaluates by recursively finding the cofactors along row 1
            for i in range (self.m):
                m = self.minormatrix(i+1,1);
                cofactor = ((-1)**i)*m.det();
                det += self.getvalue(i+1,1)*cofactor;
        return det;
    
    #returns the size of the square matrix   
    def getsize(self):
        return self.m;
    
"""The following class contains the details of a square matrix, all of whose elements are polynomials. This is what can actually be used to find the eigenvalues of a given matrix."""
class PolySq(Square):
    #initialization with optional base. The base, if given here, is the square matrix whose eigenvalues are to be found.
    def __init__(self, order, base=None):
        Square.__init__(self, order);
        if base is not None:
            if base.getsize()!=order:
                print("Error: base and order do not match.");
            else: #initializing elements to lists corresponding to (base - (lambda)I)
                for i in range (order):
                    for j in range(order):
                        l = [];
                        if i==j:
                            l.append(-1);
                        l.append(base.getvalue(i+1,j+1));
                        self.setvalue(i+1,j+1,l);

    #overriding display style to incorporate usage of lists
    #can be improved
    def display(self):
        for i in range(self.m):
            for j in range(self.n):
                print(self.getvalue(i+1,j+1),sep=',',end=" ");
            print();
    
    #Expanding along row 1 - but incorporating polynomial multiplication to get the characteristic equation this time
    def det(self):
        det = [];
        if self.m == 1:
            return self.getvalue(1,1);
        else: 
            for i in range (self.m):
                m = self.minormatrix(i+1,1);
                cofactor = Polynomials.product([(-1)**i],m.det());
                det = Polynomials.sumlists(det,Polynomials.product(self.getvalue(i+1,1), cofactor));
        return det;
    
    #returns a list containing all the roots of the characteristic equation, i.e. all the eigenvalues
    def geteigenvalues(self):
        return Polynomials.allroots(self.det());
    
    #machinery to calculate eigenvectors still needs to be developed