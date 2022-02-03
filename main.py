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

def create_combination_reverse(N,d): #donne les combinaisons dans l'ordre : d'abord les k parmis k puis k parmi k+1...k parmi n, utiliser pour le critère de sous-modèle fixe.
    list_tab_combinations_reverse = combinations(range(N),d)
    tab_combinations_reverse = [[y for y in x] for x in list_tab_combinations_reverse]
    return [[N-y-1 for y in x[::-1]] for x in tab_combinations_reverse[::-1]]

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

    variables: B tableau d'indices de base
                nB tableau de points couvert par B
                combination_tab: tableaux des combinaisons précalculé
                combination: le nombre (d parmi nB)
                r sert à réduire le nombre de récursion en ne supprimant que les bases à la rème position ou plus dans l'étape 3.
'''

''' la version 1 est médiocre, elle fait 2^tailleB itérations, mais elle permet de comprendre l'idée de base.
    Elle peut tout de même être utile pour B de petite taille.'''

def trouver_sous_modèles_fixesv1(B, r, tab,recursions): #B un ensemble d'indice, nB l'ensemble des points couvert par B,r indice de récursion, tab tableau du résultat
    recursions[0] +=1
    tailleB = len(B)
    nB = from_bases_indices_to_point(B) #faire un traqueur du nombre d'itérations.
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
            trouver_sous_modèles_fixesv1(Bi, i, tab,rec)
            '''On test tous les sous-ensemble de B (sauf ceux correspondants à des sous-modèles non maximaux).'''



'''         Dans cette version, le but est de faire la récurence sur tous les ensembles de bases qui couvrent un sous ensemble de nB et maximaux.'''
def trouver_sous_modèles_fixesv2(B, r, tab, nB, taillenB, tailleB,recursions):
    combination = combination_tab[taillenB-d]
    if tailleB == combination:
        tab.append(nB)
    else:

        for i in range(0,r):
            nBi = copy.copy(nB)
            del nBi[i]
            if taillenB-1 >= d:
                Bi = [x for x in B if set(from_base_indice_to_base(x)) <= set(nBi)]
                trouver_sous_modèles_fixesv2(Bi, i, tab, nBi, taillenB - 1, len(Bi),recursions)
    recursions[0] += 1
    if recursions[0]%100 == 0:
        print("\r", recursions[0], end="")

""" backup d'une version qui ne marche pas sur 41 points
def trouver_sous_modèles_fixesv2(B, r, tab, nB, taillenB, tailleB,recursions): 
    recursions[0] += 1
    #print(B)
    print("\r",recursions[0],end="")
    combination = combination_tab[taillenB-d]
    if tailleB == combination:
        tab.append(nB)
    else:

        for i in range(0,r):
            nBi = copy.copy(nB)
            #print("\r",nBi)
            del nBi[i]
            if taillenB-1 >= d:
                tab_base_de_nBi = from_points_to_basev2(nBi,d)
                #print("\r",tab_base_de_nBi)
                Bi = [x for x in B if from_base_indice_to_base(x) in tab_base_de_nBi] #TODO faut changer ça
                #print("\r",Bi)
                print("Bi fini on passe à la suite")
                trouver_sous_modèles_fixesv2(Bi, i, tab, nBi, taillenB - 1, len(Bi),recursions)

"""

def test_sous_modèles_fixes(PBr,tab,recursions,L):
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
                del nBi[i]
                Bi = [x for x in B if set(from_base_indice_to_base(x)) <= set(nBi)]
                L.append((nBi,Bi,i))



def test_sous_modèles_fixesv2(PBr,tab,recursions,L):
    nB = PBr[0]
    B = PBr[1]
    r = PBr[2]
    taillenB = len(nB)
    if taillenB - 1 >= d:
        for i in range(0, r):
            nBi = copy.copy(nB)
            p=nBi[i]
            del nBi[i]
            Bi = [x for x in B if  p not in from_base_indice_to_base(x)]
            taillenBi = len(nBi)
            tailleBi = len(Bi)
            combination = combination_tab[taillenBi-d]
            if tailleBi == combination:
                tab.append(nBi)
            else:
                L.append((nBi,Bi,i))
            recursions[0] += 1
            if recursions[0] % 50000 == 0 or taillenB < recursions[1]:
                recursions[1] = taillenB
                print("\r", recursions[0], " len(L) :", len(L), "len(B): ",tailleBi," len tab :", len(tab),"On est à l'étape ",n-recursions[1], "sur", n, ".", end="")
'''
def bool_sous_model_fixe(PBr,tab,recursions):
    nB = PBr[0]
    B = PBr[1]
    taillenB = len(nB)
    tailleB = len(B)
    combination = combination_tab[taillenB - d]
    if tailleB == combination:
        tab.append(nB)
        recursions[0]+=1
        return True
    else:
        return False
'''
def trouver_sous_modèles_fixesv3(B,tab,nB,recursions):

    L=[(nB,B,len(nB))] #list FIFO pour le parcourt en largeur.
    while len(L) !=0:
        test_sous_modèles_fixesv2(L[0],tab,recursions,L)
        del L[0]





def intersection(P1,P2): #P1 P2 deux ensembles de points, return l'intersection des deux ensembles.
    return [x for x in P1 if x in P2]

def intersections(tabP): #tabP ensemble d'ensemble de points. return toutes les intersections deux à  qui sont de taille tabP[0]-1, sans doublons.
    tab_intersections = [intersection(tabP[i],tabP[j]) for i in range(0,len(tabP)-1) for j in range(i+1,len(tabP))]
    tab_intersections_sans_doublons = []
    for x in tab_intersections:
        if x not in tab_intersections_sans_doublons:
            tab_intersections_sans_doublons.append(x)
    return [x for x in tab_intersections_sans_doublons if len(x)== len(tabP[0])-1]



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
pE = 2**n
print("On va devoir tester au maximum 2^n = ",pE," sous ensemble. Espérons moins !")
print("Dimension ?:")
d=int(input("d: "))

list_base = combinations(range(n),d)
tab_base = [[y for y in x] for x in list_base]
tab_base_ordered = create_combination_reverse(n,d)

if n < 10:
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
elif lecture_bases_fixes == "npy":
    print("c est bon ")
    fichier = np.load('sur41points.npy')
    print(fichier)
    tab_bases_fixes = [int(x) for x in fichier]



#print_alphabet(len(tab_base))


#tab_bases_fixes = [from_letter_to_number(x) for x in bases_fixes]
if n <10:
    print(tab_bases_fixes)

version = input("Version 1 (SI nbr base <<n) ou version 2 (SI n << nbr base) ou v3 (test)")


tab_sous_modeles_fixe=[]
rec = [0,n]
start = time.time()
if version=='1':
    trouver_sous_modèles_fixesv1(tab_bases_fixes, 0, tab_sous_modeles_fixe,rec)
elif version == '2':
    trouver_sous_modèles_fixesv2(tab_bases_fixes, len(from_bases_indices_to_point(tab_bases_fixes)), tab_sous_modeles_fixe, from_bases_indices_to_point(tab_bases_fixes),
                                 len(from_bases_indices_to_point(tab_bases_fixes)), len(tab_bases_fixes),rec)
elif version =='3':
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

if n<10:
    print("Les sous-modèles fixes sont: ")
    print(tab_sous_modeles_fixe)

print("Il y a  :",len(tab_sous_modeles_fixe),"sous modèles fixes")



tab_sous_modeles_fixe_sans_bases = sorted(tab_sous_modeles_fixe_sans_bases)
if n<10:
    print(tab_sous_modeles_fixe_sans_bases)

print("Et sans les bases il y en a :",len(tab_sous_modeles_fixe_sans_bases))
if n<10:
    print("et sans les bases: ")
    print("Qui correspondent aux bases: ")
tab_base_des_sous_modeles = [from_points_to_base(x,d) for x in tab_sous_modeles_fixe_sans_bases]
if n<10:
    print(tab_base_des_sous_modeles)

tab_indice_base_des_sous_modeles = [from_bases_to_bases_indices(x) for x in tab_base_des_sous_modeles]

if n<10:
    print("Et en indice: ")
    print(tab_indice_base_des_sous_modeles)


'''print("Et en lettre: ")
tab_lettre_des_sous_modeles = [[from_number_to_letter(y) for y in x] for x in tab_indice_base_des_sous_modeles ]
print(tab_lettre_des_sous_modeles)
'''
np.save('sous_modeles_maximum.npy',tab_sous_modeles_fixes_max)