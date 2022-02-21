
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

def base_est_sym(P):
    est_sym = True
    for p in P:
        if tab_sym_point[p] not in P:
            est_sym = False
    return est_sym

##Etape 1 On prend la liste des symétriques des points
nom_du_fichier =input("nom du fichier des symétriques des points ?")
fichier = open(nom_du_fichier,"r")
points_fichier = fichier.readlines()
fichier.close()
tab_sym_point = [int(x) for x in points_fichier]

print("Taille des modèles ?")
n=int(input("n: "))
list_base = combinations(range(n),4)
tab_base = [[y for y in x] for x in list_base]

print("tab_base:",len(tab_base))
print(tab_base)

String_SM=input("Sous-modèle à tester ? (0,1,2,14 ..):")
SM=from_string_to_tab(String_SM)
print("Sous-modèle:")
print(SM)

symSM=[tab_sym_point[p] for p in SM]
symSM.sort()
print("Sous-modèle symétrique:")
print(symSM)


UnionSM = list(set(SM+symSM))
print("Union des deux sous-modèles:")
print(UnionSM)

Base_SM = from_points_to_base(SM)
Base_symSM = from_points_to_base(symSM)
Base_UnionSM = from_points_to_base(UnionSM)

nom_du_fichier =input("nom du fichier des d-uplets constants ?")
fichier = open(nom_du_fichier,"r")
bases_fixes_fichier = fichier.readlines()
fichier.close()
tab_bases_fixes = [int(x) for x in bases_fixes_fichier]
print("d-uplets constants:",len(tab_bases_fixes))


base_nonbase = [0,0]
liste_base_test = []
for P in Base_UnionSM:
    if P not in Base_SM and P not in Base_symSM:
        if not base_est_sym(P):
            if from_base_to_base_indice(P) in tab_bases_fixes: #test ici
                base_nonbase[0]+=1
                liste_base_test.append(P)
            else:
                base_nonbase[1]+=1
                liste_base_test.append(P)

print(base_nonbase)
print(liste_base_test)



