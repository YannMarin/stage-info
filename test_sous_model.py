"""

Programme qui donne les d-uplets constants et non constants d'un sous-modèle.

Etape 1:
prend ne entrée une taille
Prend en entrée un sous modèle sous la forme 1,2,3...
Prend en entrée une liste de base

Etape 2:
créer la liste des 4uplets sur n points
calcul la liste des 4uplets sur le sous modèle

Etape 3:
Calcul quelle sont les 4-uplets de X dans le sous modèle
Calcul les d-uplets du sous modèle qui ne sont pas dans X.

Etape 4:
print les résultats.
"""

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

def from_points_to_base(P): #P ensemble de point, d dimension, return l'ensemble des bases sur ces points.
    list_bases = combinations(range(len(P)),4)
    tab_bases = [[y for y in x] for x in list_bases]
    return [[P[y] for y in x] for x in tab_bases]

def from_base_to_base_indice(b):
    i=0
    while tab_base[i] != b:
        i+=1
    return i


##Etape 1:
print("Taille des modèles ?")
n=int(input("n: "))
list_base = combinations(range(n),4)
tab_base = [[y for y in x] for x in list_base]

print("tab_base:",len(tab_base))
print(tab_base)

String_SM=input("Sous-modèle à tester ? (0,1,2,14 ..):")
SM=from_string_to_tab(String_SM)
print("Sous-modèle:",len(SM))
print(SM)

nom_du_fichier =input("nom du fichier des d-uplets constants ?")
fichier = open(nom_du_fichier,"r")
bases_fixes_fichier = fichier.readlines()
fichier.close()
tab_bases_fixes = [int(x) for x in bases_fixes_fichier]
print("d-uplets constants:",len(tab_bases_fixes))

##Etape 2:

d_uplet_SM = from_points_to_base(SM)
print("d-uplet_SM:",len(d_uplet_SM))

##Etape 3:

tab_non_const = []
tab_const = []

for P in d_uplet_SM:
    if from_base_to_base_indice(P) in tab_bases_fixes:
        tab_const.append(P)
    else:
        tab_non_const.append(P)

print("tab_const:",len(tab_const))
print(tab_const)

print("tab_non_const:",len(tab_non_const))
print(tab_non_const)


