import numpy as np
from sympy import binomial
import copy

'''
Programme pour créer la liste des symétriques des points.


'''
def combinations(iterable, r): #piqué ici https://docs.python.org/3/library/itertools.html#itertools.combinations
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)




print("***Programme pour attribuer des symétries à des points.***")
print("Taille des modèles ?")
n=int(input("n: "))
print("Dimension ?:")
d=int(input("d: "))
list_base = combinations(range(n),d)
tab_base = [[y for y in x] for x in list_base]
print(tab_base)

nom_du_fichier =input("nom du fichier ?")
fichier = open(nom_du_fichier,"r")
bases_fixes_fichier = fichier.readlines()
fichier.close()
tab_bases_fixes = [int(x) for x in bases_fixes_fichier]

f = open('PointsSym16P.txt', 'w')

x=0
tab_sym  = []
while x<n:
    l=input("Symétrique de "+str(x)+" ?")
    f.write(l+"\n")
    tab_sym.append(int(l))
    x=x+1

print(tab_sym)
print("Calcul des symétriques des bases:")



tab_base_symetrique=[]
for x in tab_base:
    xx = [tab_sym[y] for y in x]
    xx.sort()
    tab_base_symetrique.append(tab_base.index(xx))

f = open('BasesSym16P.txt','w')
for x in tab_base_symetrique:
    f.write(str(x)+"\n")
print(tab_base_symetrique)
sym_tab_base = []

for x in tab_bases_fixes:
    if x in tab_bases_fixes and tab_base_symetrique[x] in tab_bases_fixes:
        sym_tab_base.append(x)

sym_tab_base.sort()
f= open('RestrictionSym16P.txt','w')
for x in sym_tab_base:
    f.write(str(x)+"\n")
print(sym_tab_base)
print(tab_bases_fixes)