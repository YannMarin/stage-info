
"""

Pogramme pour avoir les ensembles minimaux d'une liste
(par exemple pour avoir les sous-modèle projetés par des paires de sous-modèles constants maximaux non symétrique minimaux...)

"""
nom_de_fichier = "16PSMC_maxnonsym_minimaux.txt"


#Etape 1 lire le fichier

nom_du_fichier =input("nom du fichier de la liste des modèles ?")
fichier = open(nom_du_fichier,"r")
list_fichier = fichier.readlines()

tab_sous_modèles = []
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
    tab_sous_modèles.append(l)

fichier.close()
print(tab_sous_modèles)
#Etape 2 on garde les éléments minimaux.
tab_sous_modèles_minimaux = []

for P in tab_sous_modèles: #On pourrait voir si c'est mieux en triant au préalable le tableaux.
    count = 0
    for PP in tab_sous_modèles:
        if not set(PP) < set(P):
            count += 1
    if count == len(tab_sous_modèles):
        tab_sous_modèles_minimaux.append(P)


f = open("16P"+"\\"+nom_de_fichier, 'w')

tab_sous_modèles_minimaux.sort()
tab_sous_modèles_minimaux.sort(key=len)

for x in tab_sous_modèles_minimaux:
    for y in x:
        f.write(str(y)+",")
    f.write("\n")
f.close()