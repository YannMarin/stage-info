"""

Même programme que test_sous_model mais pour un ensemble de SMC

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

nom_du_fichier =input("nom du fichier de la liste des SMC?")
fichier = open(nom_du_fichier,"r")
list_fichier = fichier.readlines()
fichier.close()

tab_SMC = []
for x in list_fichier:
    l=[]
    m=''
    for y in x:
        if y != ',':
            m=m+y

        else:
            if m!='':
                l.append(int(m))
                m=''
    tab_SMC.append(l)

print("tab_SMC",len(tab_SMC))
print(tab_SMC)

nom_du_fichier =input("nom du fichier des d-uplets constants ?")
fichier = open(nom_du_fichier,"r")
bases_fixes_fichier = fichier.readlines()
fichier.close()
tab_bases_fixes = [int(x) for x in bases_fixes_fichier]
print("d-uplets constants:",len(tab_bases_fixes))

##Etape 2:

tab_d_uplet= [from_points_to_base(P) for P in tab_SMC]

##Etape 3:
tab_constant_nonconstant = []
for P in tab_d_uplet:
    constant_nonconstant = [0,0]
    for duplet in P:

        if from_base_to_base_indice(duplet) in tab_bases_fixes:
            constant_nonconstant[0]+=1
        else:
            constant_nonconstant[1]+=1
    tab_constant_nonconstant.append(constant_nonconstant)

print("tab_const_nonconstant:",len(tab_constant_nonconstant))
print(tab_constant_nonconstant)
##on écrit les fichiers
f = open("test_const_non_const", 'w')

for x in tab_constant_nonconstant:
    for y in x:
        f.write(str(y)+",")
        f.write("\n")

f.close()


