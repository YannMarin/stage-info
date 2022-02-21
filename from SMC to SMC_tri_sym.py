
import os
"""

Programme pour passer d'une liste de sous-modèles constants max (symétriques ou non )à cette liste trié dans l'ordre suivant:
-D'abord les paires croisées max non contenus dans des sous modèles de la list.
-Ensuite les intrinséques max non contenus dans des croisés.
-Ensuite les paires séparés max non contenus dans des intrinséques.


D'abord on doit créer une liste des sommets symétriques.
Après ça il nous faut la liste des labels.
Après ça, on doit lire la liste des sous modèles.
Puis on test dans l'ordre: Est-ce que c'est des sous modèle symétrique ? (ie il existe un sous-modèle qui soit le symétrique de P)
    Si oui: est-ce que c'est un symétrique séparé ? -> On ajoute dans  NbrPSMCSymSéparé.txt
    est-ce que c'est un symétrique intrinséque ? -> On ajoute dans NbrPSMCSymInt.txt
    sinon on ajoute dans NbrPSMCSymCr.txt
"""
#Nom des fichiers:
nom_de_dossier = "P"
nom_de_fichier_Cr = "SMC_Cr_Max.txt"
nom_de_fichier_Intra ="SMC_Intra_Max.txt"
nom_de_fichier_Sep = "SMC_Sep_Max.txt"
nom_de_fichier_nonSym = "test.txt"



print("Taille des modèles ?")
n=int(input("n: "))

##Etape 1 On prend la liste des symétriques des points
nom_du_fichier =input("nom du fichier des symétriques des points ?")
fichier = open(nom_du_fichier,"r")
points_fichier = fichier.readlines()
fichier.close()
tab_sym_point = [int(x) for x in points_fichier]


##Etape 2 On prend la liste des labels des points
nom_du_fichier = input("non du fichier des labels des points ?")
fichier = open(nom_du_fichier,"r")
labels_fichier = fichier.readlines()
fichier.close()
tab_label = [x for  x in labels_fichier]

##Etape 3 on prend la liste des SMC.
nom_du_fichier =input("nom du fichier de la liste des SMC?")
fichier = open(nom_du_fichier,"r")
list_fichier = fichier.readlines()
fichier.close()

bool_list_est_sym = input("est-ce que les sous modèles fixes sont symétriques ? (o/n)")

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

##Etape 4: On créer les fonctions de test


def sym(P):
    symP = [tab_sym_point[p] for p in P]
    symP.sort()
    return symP

def test_est_sym(P):
    return sym(P) in tab_SMC

def test_sym_separe(P):
    est_sym_sep  = True
    i=0
    while tab_label[P[i]]=='c' and i<len(P):
        i=i+1
    l = tab_label[P[i]]
    for p in P:
        if tab_label[p] != l and tab_label[p] != 'c':
            est_sym_sep = False
    return est_sym_sep

def test_sym_int(P):
    symP = sym(P)
    return P == symP


def from_cr_to_intra(P):
    symP=sym(P)
    intra = [p for p in P if p in symP]
    if len(intra) >=4:
        tab_intra_from_tab_cr.append(intra)

def from_cr_to_sep(P):
    return ([p for p in P if (tab_label[p]=='g' or tab_label[p]=='c')],[p for p in P if (tab_label[p]=='d' or tab_label[p]=='c')])

##Etape 4:
tab_sym = []
tab_sep = []
tab_int = []
tab_cr = []
tab_notsym = []

def tri_des_SMC_sym(): #On suppose que bool_list_SMC_est_sym est vrai.
    for P in tab_SMC:
        if test_sym_separe(P):
            tab_sep.append(P)
            #del tab_SMC[tab_SMC.index(sym(P))]
        elif test_sym_int(P):
            tab_int.append(P)
        else:
            tab_cr.append(P)
            #del tab_SMC[tab_SMC.index(sym(P))]


def tri_des_SMC(): #On suppose que bool_list_SMC_est_sym est vrai.
    for P in tab_SMC:
        if test_est_sym(P):
            tab_sym.append(P)
            if test_sym_separe(P):
                tab_sep.append(P)
                #del tab_SMC[tab_SMC.index(sym(P))]
            elif test_sym_int(P):
                tab_int.append(P)
            else:
                tab_cr.append(P)
                #del tab_SMC[tab_SMC.index(sym(P))]
        else:
            tab_notsym.append(P)


##Etape 5 on créer les fichiers Output.

if bool_list_est_sym == 'o':
    tri_des_SMC_sym()
else:
    tri_des_SMC()
print("Tab_SMC:",len(tab_SMC))
print(tab_SMC)
print("Tab_sep:",len(tab_sep))
print(tab_sep)
print("Tab_int:",len(tab_int))
print(tab_int)
print("Tab_cr",len(tab_cr))
print(tab_cr)

print("Il y avait",len(tab_SMC)," SMC. et il y a ", len(tab_sym)," SMC symétriques.")
if (bool_list_est_sym == 'n'):
    print("Tab_notsym:",len(tab_notsym))
    print(tab_notsym)

##Etape 6: à partir des cr max on créer les intra max et les sep max.
tab_sep_from_tab_cr = []
tab_intra_from_tab_cr = []


for P in tab_cr:
    from_cr_to_intra(P)
    Psep = from_cr_to_sep(P)
    if Psep != ([],[]):
        tab_sep_from_tab_cr.append(Psep)

print("A partir des croisés on à créer:")
print("tab_sep (from tab_cr):",len(tab_sep_from_tab_cr))
print(tab_sep_from_tab_cr)
print("tab_intra (from tab_cr):",len(tab_intra_from_tab_cr))
print(tab_intra_from_tab_cr)


try:
   os.mkdir(str(n)+nom_de_dossier)
except:
    print("Le dossier existe déjà")

f = open(str(n)+nom_de_dossier+"\\"+str(n)+nom_de_fichier_Cr, 'w')
for x in tab_cr:
    for y in x:
        f.write(str(y)+",")
    f.write("\n")
f.close()

f = open(str(n)+nom_de_dossier+"\\"+str(n)+nom_de_fichier_nonSym, 'w')
for x in tab_notsym:
    for y in x:
        f.write(str(y) + ",")
    f.write("\n")
f.close()