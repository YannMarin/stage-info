import numpy as np
from sympy import binomial
import time
import copy

'''
Le programme va demander une taille n qui correspond à la taille d'un modèle (ex n=8)
puis il demandera la dimension (ex d=4)
Il affichera ensuite l'ensemble des bases possibles et leurs indice
ainsi que la table des (d parmi i) pour i de d à n.
Ensuite il demandera si l'on veut une liste de base pour être sur d'avoir un sous-modèles fixe. Il faut répondre o ou n
dans le cas o, il demandera la liste des points (ex 0,1,2,3,5)
il montre alors les bases associés à ces points et leurs indices.
Il demande ensuite les bases fixes (ex:0,2,4,6,8,16,36,38)
Il donne ensuite les sous modèles fixes maximaux avec et sans les bases ainsi que leurs nombre et leurs indices.

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
        for y in x:   #TODO a optimiser ? C'est la fonction qu'on appelle le plus
            if y not in tab_points:
                tab_points.append(y)

    return tab_points #TODO est-ce que l'on a vraiment besoin de trier les points ? (non ?)

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
    list_bases = combinations(range(len(P)),d)
    tab_bases = [[y for y in x] for x in list_bases]
    return [[P[y] for y in x] for x in tab_bases]


def from_bases_to_bases_indices(B): #B ensemble de bases (points), return l'ensemble des bases (indices)
    tab_indices = [from_base_to_base_indice(x) for x in B]
    return tab_indices

def from_number_to_letter(x): #x un nombre, return la lettre correspondante en commençant par 0=a
    return chr(ord('`')+x+1)

def from_letter_to_number(L): #L une lettre, return le nombre correspondant en commençant par a=0.
    return int(ord(L)-ord('`')-1)

def print_alphabet(x): #affiche l'alphabet pour ceux qui ne le connaissent pas.
    for x, y in ((x, chr(ord('a') + x)) for x in range(x)):
        print(x,"=",y,end=", ")
    print("")

''' trouve les sous_modèles fixes maximaux
    à partir d'un ensemble d'indice de bases fixes
    détails ici: https://docs.google.com/presentation/d/1YnGofHivYb_Xr2KnetLFWNmz9Z_GS-d_--weLX5VNyw/edit#slide=id.g10c4f279e95_0_10

    variables: B tableau d'indices de base
                nB tableau de points couvert par B
                combination_tab: tableaux des combinaisons précalculé
                combination: le nombre (d parmi nB)
                r sert à réduire le nombre de récursion en ne supprimant que les bases à la rème position ou plus dans l'étape 3.
'''


def trouver_sous_modèles_fixesv1(B, r, tab): #B un ensemble d'indice, nB l'ensemble des points couvert par B,r indice de récursion, tab tableau du résultat
    tailleB = len(B)
    nB = from_bases_indices_to_point(B)
    taillenB = len(nB)
    combination = combination_tab[taillenB-d]
    if tailleB == combination : #on termine la récursion
        tab.append(nB)
    elif tailleB > combination : #Normalement on entre jamais dans cette boucle.
        print("Qu'est-ce qu'il se passe ????")
    else: #cas tailleB < combination #TODO si on peut améliorer l'algorithme c'est ici
        #print("Cas 3!")
        for i in range(r,tailleB):
            Bi = copy.copy(B)
            del Bi[i]
            trouver_sous_modèles_fixesv1(Bi, i, tab)
            '''On test tous les sous-ensemble de B (sauf ceux correspondants à des sous-modèles non maximaux) mais est-ce bien nécessaire ?
                -Si on ne prend que les sous ensemble de degré inférieur ?
                 A tester, je crois que ça revient au même en fait, on ferait moins de récursion mais autant de test
                 Mais est-ce qu'il ne faut pas diminuer au maximum le nombre de récursion ?
                 '''


            #v2 cherche à diminuer le nombre de récursion et de test mais demande de garder plus de chose en mémoire sur la pile. (je crois ?)
def trouver_sous_modèles_fixesv2(B, r, tab, nB, taillenB, tailleB): #TODO ne marchera pas ? (ou pas mieux que v2).
    combination = combination_tab[taillenB-d]
    if tailleB == combination:
        tab.append(nB)
    else:
        for i in range(r,tailleB):
            Bi = [x for x in B]
            del Bi[i]
            nBi = from_bases_indices_to_point(Bi)
            taillenBi = len(nBi)
            while taillenBi < taillenB:

                trouver_sous_modèles_fixesv2(Bi, i, tab, nBi, taillenBi, tailleB - 1)

'''         Dans cette version, le but est de faire la récurence sur tous les ensembles de bases qui couvrent un sous ensemble de nB et maximaux.'''
def trouver_sous_modèles_fixesv3(B, r, tab, nB, taillenB, tailleB): #TODO à corriger, return aussi les sous-modèles non maximaux (ça veut dire que l'on envoit plusieurs fois les mêmes sous ensemble je pense
    combination = combination_tab[taillenB-d]
    if tailleB == combination:
        tab.append(nB)
    else:

        for i in range(r,taillenB):
            nBi = [x for x in nB]
            del nBi[i]
            tab_base_de_nBi = from_points_to_base(nBi,d)
            Bi = [x for x in B if from_base_indice_to_base(x) in tab_base_de_nBi]
            trouver_sous_modèles_fixesv3(Bi, i, tab, nBi, taillenB - 1, len(Bi)) #TODO il faut vérifier que l'on ne fais pas deux fois les mêmes ensemble





def supprimer_les_bases_d_une_liste_de_point(P,d): #P liste de point, d dimension, retourne la même liste sans les éléments de taille d.
    return [x for x in P if len(x) > d]

def donner_des_points_a_couvrir():
    print("Liste de points à couvrir ?: (1,3,12...)")
    #print_alphabet(n)

    liste_point = input("liste des points:")
    #tab_point = [from_letter_to_number(x) for x in liste_point]
    tab_point = from_string_to_tab(liste_point)
    list_base_des_points = from_points_to_base(tab_point, d)

    '''print("Liste des bases de ces points:")
    print(list_base_des_points)
'''
    print("Liste des indices des bases à prendre:")
    tab_ind = from_bases_to_bases_indices(list_base_des_points)

    for x in tab_ind:
        if x not in tab_base_des_sommets_a_couvrir:
            tab_base_des_sommets_a_couvrir.append(x)
    print(sorted(tab_base_des_sommets_a_couvrir))

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
print("Dimension ?:")
d=int(input("d: "))
list_base = combinations(range(n),d)
tab_base = [[y for y in x] for x in list_base]


print("ensembles des bases:")
for i in range(len(tab_base)):
    print(i,"=",tab_base[i],end=",")
print("")
combination_tab = create_combination_tab(n,d)
print("Tableau des combinaisons", combination_tab)


'''     Si on veut être sur d'avoir au moins un sous modèle fixe qui ne soit pas une base'''
bool_couvrir_des_points = input("Voulez vous la liste des bases pour être sûr de couvrir certains points ?: (o/n)")

tab_base_des_sommets_a_couvrir = []
while bool_couvrir_des_points == 'o':
    donner_des_points_a_couvrir()
    bool_couvrir_des_points = input("Voulez vous la liste des bases pour être sûr de couvrir certains points ?: (o/n)")


print("bases fixes ? (1,3,12...):")
#print_alphabet(len(tab_base))

bases_fixes = input("bases_fixes: ")
#tab_bases_fixes = [from_letter_to_number(x) for x in bases_fixes]
tab_bases_fixes = from_string_to_tab(bases_fixes)
print(tab_bases_fixes)

version = input("Version 1 ou 3 ?")
print("Les sous-modèles fixes sont: ")
start = time.time()
tab_sous_modeles_fixe=[]

if version=='1':
    trouver_sous_modèles_fixesv1(tab_bases_fixes, 0, tab_sous_modeles_fixe)
else:
    trouver_sous_modèles_fixesv3(tab_bases_fixes, 0, tab_sous_modeles_fixe, from_bases_indices_to_point(tab_bases_fixes),
                                 len(from_bases_indices_to_point(tab_bases_fixes)), len(tab_bases_fixes))

end = time.time()
elapsed = end-start
print(f'Le calcul à prit {elapsed:.2}ms')

tab_sous_modeles_fixe_sans_bases = supprimer_les_bases_d_une_liste_de_point(tab_sous_modeles_fixe,d)
print(tab_sous_modeles_fixe)

print("Il y en a :",len(tab_sous_modeles_fixe))

print("et sans les bases: ")
print(tab_sous_modeles_fixe_sans_bases)
print("Il y en a :",len(tab_sous_modeles_fixe_sans_bases))
print("Qui correspondent aux bases: ")
tab_base_des_sous_modeles = [from_points_to_base(x,d) for x in tab_sous_modeles_fixe_sans_bases]
print(tab_base_des_sous_modeles)

print("Et en indice: ")
tab_indice_base_des_sous_modeles = [from_bases_to_bases_indices(x) for x in tab_base_des_sous_modeles]
print(tab_indice_base_des_sous_modeles)

'''print("Et en lettre: ")
tab_lettre_des_sous_modeles = [[from_number_to_letter(y) for y in x] for x in tab_indice_base_des_sous_modeles ]
print(tab_lettre_des_sous_modeles)
'''