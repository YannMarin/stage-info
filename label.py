import numpy as np
from sympy import binomial
import copy

'''
Programme pour attribuer des labels g,c,d à des points.


'''
print("***Programme pour attribuer des labels g,c,d à des points.***")
print("Taille des modèles ?")
n=int(input("n: "))
f = open('Label16P.txt', 'w')

x=0
while x<n:
    l=input("Label de "+str(x)+" ? ('g','c','d')")
    if l=='g' or l=='c' or l=='d':
        f.write(l)
        f.write("\n")
        x=x+1

