"""

Programme qui prend en entrée une liste de bases (constantes ou non), deux SMC, et renvois les d-uplets qui ont exactement un seul point dans l'un des deux SMC.

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


n = int(input("nombre de point ?"))
d = int(input(" d  ?"))
nom_du_fichier = input("nom du fichier ?")
fichier = open(nom_du_fichier, "r")
bases_fixes_fichier = fichier.readlines()
fichier.close()
tab_bases_fixes = [int(x) for x in bases_fixes_fichier]
SMC = [0,1,4,5,6,7,8,9]
SMC2 = [2,3,10,11,12,13,14,15]

list_base = combinations(range(n),d)
tab_base = [[y for y in x] for x in list_base]

tab_ind_duplet = []
tab_duplet = []





for b in tab_bases_fixes:
    un_seul_sommet = False
    nbr_sommet = 0
    for p in tab_base[b]:
        """if p == 10 or p == 11 or p==8 or p == 9:
            nbr_sommet = 10
            break"""
        if p in SMC:
            nbr_sommet +=1
    if nbr_sommet == 1:
        tab_ind_duplet.append(b)
        tab_duplet.append(tab_base[b])
"""
##SI on utilise la version sur les deux SMC
for b in tab_bases_fixes:
    un_seul_sommet = False
    for p in tab_base[b]:
        if p == 10 or p == 11 or p==8 or p == 9:
            un_seul_sommet = False
            break
        if p in SMC2:
            if not un_seul_sommet:
                un_seul_sommet = True
            else:
                un_seul_sommet = False
                break
    if un_seul_sommet:
        tab_ind_duplet.append(b)
        tab_duplet.append(tab_base[b])
"""
tab_duplet.sort()
tab_ind_duplet.sort()
print("tab_ind_duplet:",len(tab_ind_duplet))
print(tab_ind_duplet)
print("tab_duplet:",len(tab_duplet))
print(tab_duplet)


f = open("extraction_ind31v1", 'w')
for x in tab_ind_duplet:
    f.write(str(x)+"\n")
f.close()

f = open("extraction_duplet31v1",'w')
for x in tab_duplet:
    for y in x:
        f.write(str(y)+" ")
    f.write("\n")
f.close()