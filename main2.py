import numpy as np
from sympy import binomial
import time
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





def from_base_indice_to_base(b):
    return tab_base[b]

def from_base_to_base_indice(b):
    i=0
    while tab_base[i] != b:
        i+=1
    return i

def from_bases_indices_to_bases(B): #B ensemble d'indice de base, return les bases correspondantes en d points.
    return [from_base_indice_to_base(b) for b in B]

'''Prend en entrée un tableau de bases triées
lexicographiquement et renvoit l'ensemble des points couverts '''
def from_bases_to_points(B): #B ensemble de base (points), return les points couverts par ces bases.
    tab_points=[]
    for x in B:
        for y in x:
            if y not in tab_points:
                tab_points.append(y)

    return sorted(tab_points)

'''Créer le tableau des points à partir du tableau des indices des bases'''
def from_bases_indices_to_point(B): #B ensemble de base (indices) return l'ensemble de points couvert par ces bases
    tab_bases = [from_base_indice_to_base(b) for b in B]
    return from_bases_to_points(tab_bases)

''' Créer le tableau des différentes valeurs de (d parmi n) pour 1<=n<=N'''
#TODO est-ce que ça marche avec des grands N ? (biblio sympy)
def create_combination_tab(N,d):
    tab_combinations = [binomial(n,d) for n in range(d,N+1)]
    return tab_combinations


def from_points_to_base(P,d): #P ensemble de point, d dimension, return l'ensemble des bases sur ces points.
    list_bases = combinations(range(len(P)),d) #TODO A OPTIMISER
    tab_bases = [[y for y in x] for x in list_bases]
    return [[P[y] for y in x] for x in tab_bases]

def from_points_to_basev2(P,d): #P ensemble de point, d dimension, return l'ensemble des bases sur ces points.
    tab_bases = [[y for y in x] for x in tab_base_ordered[0:combination_tab[len(P)-d]]]
    return [[P[y] for y in x] for x in tab_bases]

def from_bases_to_bases_indices(B): #B ensemble de bases (points), return l'ensemble des bases (indices)
    tab_indices = [from_base_to_base_indice(x) for x in B]
    return tab_indices



def test_sous_modèles_fixesv2(PBr,tab,recursions,L):
    nB = PBr[0]
    B = PBr[1]
    r = PBr[2]
    taillenB = len(nB)
    tailleB = len(B)
    combination = combination_tab[taillenB - d]
    if tailleB == combination: #On ne vérifie pas si le sous modèle est déjà dans la liste, c'est plus long que de l'ajouter et de trier la liste à la fin !
        tab.append(nB)

    else: #C'est ici l'important
        if taillenB - 1 >= d:
            for i in range(0, r): #TODO il faut que je re réfléchisse à ça
                nBi = copy.copy(nB)
                p=nBi[i]
                del nBi[i]
                Bi = [x for x in B if  p not in from_base_indice_to_base(x)]
                L.append((nBi,Bi,i))

def trouver_sous_modèles_fixesv3(B,tab,nB,recursions):

    L=[(nB,B,len(nB))] #list FIFO pour le parcourt en largeur.
    while len(L) !=0:
        test_sous_modèles_fixesv2(L[0],tab,recursions,L)
        del L[0]
        recursions[0] += 1
        if recursions[0] % 100 == 0:
            print("\r", recursions[0], end="")


def tester_si_sous_modele_fixe(B,nB,tab):
    taillenB = len(nB)
    tailleB = len(B)
    Bi = [x for x in B if  p not in from_base_indice_to_base(x)]
    tailleBi = len(Bi)
    combination = combination_tab[taillenB - d]
    if tailleBi == combination:
        tab.append(nB)
'''
def retirer_k_points_d_un_sous_ensemble(k)

def trouver_sous_modèles_fixesv4(B,tab,nB,recursions):
    for k in range(1,len(B)-d+1):



'''
def supprimer_les_bases_d_une_liste_de_point(P,d): #P liste de point, d dimension, retourne la même liste sans les éléments de taille d.
    return [x for x in P if len(x) > d]

def from_string_to_tab(string): #transforme un string de la forme 1,23,4 en un tableau [1,23,4]
    tab = []
    y = ''
    for x in string:
        if x != ',':
            y+=x

        else:
            tab.append(int(y))
            y=''
    tab.append(int(y))
    return tab



print("Taille des modèles ?")
n=int(input("n: "))
pE = 2**n
print("On va devoir tester au maximum 2^n = ",pE," sous ensemble. Espérons moins !")
print("Dimension ?:")
d=int(input("d: "))

list_base = combinations(range(n),d)
tab_base = [[y for y in x] for x in list_base]



combination_tab = create_combination_tab(n,d)




lecture_bases_fixes =input("bases-fixes en fichier text, npy ou en liste ?(f,npy,l)")
if lecture_bases_fixes == 'l':
    print("bases fixes ? (1,3,12...):")
    bases_fixes = input("bases_fixes: ")
    tab_bases_fixes = from_string_to_tab(bases_fixes)
elif lecture_bases_fixes == 'f':
    nom_du_fichier =input("nom du fichier ?")
    fichier = open(nom_du_fichier,"r")
    bases_fixes_fichier = fichier.readlines()
    fichier.close()
    tab_bases_fixes = [int(x) for x in bases_fixes_fichier]

tab_sous_modeles_fixe=[]
rec = [0]
start = time.time()
print("On cherche les sous-modèles constants")
trouver_sous_modèles_fixesv3(tab_bases_fixes,tab_sous_modeles_fixe,from_bases_indices_to_point(tab_bases_fixes),rec)
end = time.time()

elapsed = end-start
print(f'Le calcul à prit {elapsed:.2}ms')
print(f'et a fait {rec[0]} recursions')

tab_sous_modeles_fixe_sans_doublon = []
tab_sous_modeles_fixe_sans_doublon = [x for x in tab_sous_modeles_fixe if x not in tab_sous_modeles_fixe_sans_doublon]
tab_sous_modeles_fixe = tab_sous_modeles_fixe_sans_doublon

tab_sous_modeles_fixes_max = []

for x in range(len(tab_sous_modeles_fixe)):
    count = 0
    for y in range(len(tab_sous_modeles_fixe)):
        if not set(tab_sous_modeles_fixe[x]) < set(tab_sous_modeles_fixe[y]):
            count += 1
    if count == len(tab_sous_modeles_fixe) :
        tab_sous_modeles_fixes_max.append(tab_sous_modeles_fixe[x])


tab_sous_modeles_fixe = tab_sous_modeles_fixes_max

tab_sous_modeles_fixe_sans_bases = supprimer_les_bases_d_une_liste_de_point(tab_sous_modeles_fixe,d)
print("Il y en a :",len(tab_sous_modeles_fixe))

tab_sous_modeles_fixe_sans_bases = sorted(tab_sous_modeles_fixe_sans_bases)

print(tab_sous_modeles_fixe_sans_bases)
print("Il y en a :",len(tab_sous_modeles_fixe_sans_bases))

tab_base_des_sous_modeles = [from_points_to_base(x,d) for x in tab_sous_modeles_fixe_sans_bases]
print(tab_base_des_sous_modeles)

tab_indice_base_des_sous_modeles = [from_bases_to_bases_indices(x) for x in tab_base_des_sous_modeles]


np.save('sous_modeles_maximum.npy',tab_sous_modeles_fixes_max)