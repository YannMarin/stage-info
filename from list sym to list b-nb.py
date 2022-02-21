
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

tab_symSMC = []
tab_UnionSMC = []
for P in tab_SMC:
    symSMC=[tab_sym_point[p] for p in P]
    symSMC.sort()
    tab_symSMC.append(symSMC)
    UnionSMC=list(set(P+symSMC))
    tab_UnionSMC.append(UnionSMC)

print("tab Sous-modèle symétrique:",len(tab_symSMC))
print(tab_symSMC)
print("tab union des SMC", len(tab_UnionSMC))
print(tab_UnionSMC)

tab_Base_SM = []
tab_Base_symSM = []
tab_Base_UnionSM = []
for i in range(0,len(tab_SMC)):
    Base_SM = from_points_to_base(tab_SMC[i])
    Base_symSM = from_points_to_base(tab_symSMC[i])
    Base_UnionSM = from_points_to_base(tab_UnionSMC[i])
    tab_Base_SM.append(Base_SM)
    tab_Base_symSM.append(Base_symSM)
    tab_Base_UnionSM.append(Base_UnionSM)

nom_du_fichier =input("nom du fichier des d-uplets constants ?")
fichier = open(nom_du_fichier,"r")
bases_fixes_fichier = fichier.readlines()
fichier.close()
tab_bases_fixes = [int(x) for x in bases_fixes_fichier]
print("d-uplets constants:",len(tab_bases_fixes))

tab_base_nonbase = []


for i in range(0,len(tab_Base_UnionSM)):
    base_nonbase = [0, 0]
    for P in tab_Base_UnionSM[i]:
        if P not in tab_Base_SM[i] and P not in tab_Base_symSM[i]:
            if not base_est_sym(P):
                if from_base_to_base_indice(P) in tab_bases_fixes: #Test ici
                    base_nonbase[0]+=1
                else:
                    base_nonbase[1]+=1
    tab_base_nonbase.append(base_nonbase)

print("tab_base_nonbase",len(tab_base_nonbase))
print(tab_base_nonbase)




