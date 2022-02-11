"""

Programme pour projeter les SM sur le côté G,
par exemple pour faire l'union de deux symétrique
ou pour projeté un SMC non symétrique sur G et recouvrir G avec des projection de SMC non symétrique.


Etape 1: Prendre les fichiers en entrée
Il nous faut:
La liste des symétriques des points
La liste des sous-modèles à traiter.

Etape 2: Créer la liste des projection sur G
Pour tout p dans P un SMC, si p est dans G ou C on le garde, si p est dans D on prend p' à la place.

Etape 3: On créer le fichier.

"""
##Nom de fichier
nom_de_fichier = "16PNONSymProjG.txt"


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
tab_label = [x.rstrip('\n') for  x in labels_fichier]

##Etape 3 on prend la liste des SMC.
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

##Etape 4: On créer la liste des projections sur G:

tab_proj = []

def projection_sur_G(P): #P un SM, return le projeté de P sur GC
    proj_p = []
    for p in P:
        if tab_label[p] == 'g' or tab_label[p] == 'c':
            if p not in proj_p:
                proj_p.append(p)
        else:
            if tab_label[p] == 'd':
                if tab_sym_point[p] not in proj_p:
                    proj_p.append(tab_sym_point[p])
    proj_p.sort()
    return proj_p

for P in tab_SMC:
    proj = projection_sur_G(P)
    if proj not in tab_proj:
        tab_proj.append(proj)

print("Tab_sym_points",len(tab_sym_point))
print(tab_sym_point)
print("Tab_Label",len(tab_label))
print(tab_label)
print("Tab_SMC:",len(tab_SMC))
print(tab_SMC)
print("Tab_proj_G:",len(tab_proj))
print(tab_proj)


##On écris les fichiers


f = open(nom_de_fichier, 'w')
for x in tab_proj:
    for y in x:
        f.write(str(y)+",")
    f.write("\n")
f.close()