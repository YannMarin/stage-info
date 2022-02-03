import numpy as np
from sympy import binomial
import copy

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

def from_bases_to_points(B): #B ensemble de base (points), return les points couverts par ces bases.
    tab_points=[]
    for x in B:
        for y in x:
            if y not in tab_points:
                tab_points.append(y)

    return sorted(tab_points)


def create_combination_tab(N,d):
    tab_combinations = [binomial(n,d) for n in range(d,N+1)]
    return tab_combinations

def create_combination_reverse(N,d): #donne les combinaisons dans l'ordre : d'abord les k parmis k puis k parmi k+1...k parmi n, utiliser pour le critère de sous-modèle fixe.
    list_tab_combinations_reverse = combinations(range(N),d)
    tab_combinations_reverse = [[y for y in x] for x in list_tab_combinations_reverse]
    return [[N-y-1 for y in x[::-1]] for x in tab_combinations_reverse[::-1]]
'''
def from_lexical_order_to_grow_order(i): #passe l'indice d'une base dans l'ordre 123 124 125 dans l'ordre 123 124 134
    for j in range(len(tab_base_ordered)):
        if tab_base[i] == tab_base_ordered[j]:
            return j
        '''
def Si_base_indice_est_bien_dans_les_k_premiers_points(i,k): #prend un indice dans l'ordre 123 124 134 et test si cette base est bien contenue dans les k premiers points.
     return i<combination_tab[k-d]


def from_base_to_base_indice(b): #sur tab_base_m
    i=0
    while tab_base_m[i] != b:
        i+=1
    return i



print("Taille des modèles ?")
n=int(input("n: "))
print("Dimension ?:")
d=int(input("d: "))
print("Taille des premiers points à regarder ?")
m=int(input("m:"))

list_base = combinations(range(n),d)
tab_base = [[y for y in x] for x in list_base]
liste_base_m = combinations(range(m),d)
tab_base_m = [[y for y in x] for x in liste_base_m]

#tab_base_ordered = create_combination_reverse(n,d)
combination_tab = create_combination_tab(n,d)
nom_du_fichier =input("nom du fichier ?")
fichier = open(nom_du_fichier,"r")
bases_fixes_fichier = fichier.readlines()
fichier.close()
tab_bases_fixes_complete = [int(x) for x in bases_fixes_fichier]
tab_base_fixes = []
f = open('0P.txt', 'w')
for x in tab_bases_fixes_complete:
    count = 0
    for y in tab_base[x]:
        if y<m:
            count+=1
    if count == d:
        b=from_base_to_base_indice(tab_base[x])
        tab_base_fixes.append(b)
        f.write(str(b)+'\n')

print(len(tab_base_fixes))
print(len(tab_bases_fixes_complete))

f.close()