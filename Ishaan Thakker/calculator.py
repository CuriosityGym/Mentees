addition=0
difference=0
product=0
quotient=0
raisedTo=0
print ("Please Enter the First Number: ")
first=int(input())
print("Please Enter the Second Number: ")
second=int(input())
addition=first+second
difference=first-second
product=first * second
raisedTo=first ** second

print("The sum of " + str(first)+  " and " + str(second) + " is " + str(addition))
print("The difference between " + str(first)+ " and "  +str(second) + " is " + str(difference))
print("The product of " + str(first)+ " and "  +str(second) + " is " + str(product))
print("The Raised To of " + str(first)+ " and "  +str(second) + " is " + str(raisedTo))

if second==0:
	print("Divide by zero error")
else:
        quotient=first/second
        print("The quotient of " + str(first)+ " and " + str(second) + " is " + str(quotient))
                       
                       
