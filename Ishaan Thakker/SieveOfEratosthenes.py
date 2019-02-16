primeList=[2]
print ("Enter a Number: ") 
a=int(input())
for i in range (3,a):
    isPrime=True
    #print(primeList)
    for prime in primeList:
        if i%prime==0:
            isPrime=False
            #print(str(i) + " is divisible by " +str(prime))
            break
    if isPrime==True:
        primeList.append(i)
print("Numbers which are prime till " +str(a) +" are")
print(primeList)        
        
        
        

