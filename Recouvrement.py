import os

"""

Programme pour calculer les 2-3 recouvrements/partitions à partir d'une liste d'ensemble.

Pour cela:
Etape 1: Initialisation
-On demande à l'utilisateur la liste des ensembles
-Les points à couvrir
-si on recherche des recouvrements ou des partitions.
-La taille 2 ou 3 des recouvrements ou partitions.
-Si la taille est >3 on utilise l'algo glouthon pour donner 1 solution (A faire).

Etape 2:
Pour les 2 recouvrements:
-On calcul tous les 2-recouvrements/partition d'une liste d'ensemble à partir d'un set et d'un indice d'incrémentation dans la liste des ensembles.
Pour les 3 recouvrements:
On calcul les 3 recouvrements en appellant la fonction des 2 recouvrements sur chaque ensemble de la liste.

Etap 3: On écris les fichiers.
"""
##Noms des fichiers à écrire:
nom_de_dossier ="16P"
fichier_recouvrement = "SMC_seuil_rec.txt"


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

##Etape 1: Initialisation:
print("***Programme pour trouver les 2 ou 3-recouvrements ou les 2 ou 3-partitions de n points à partir d'une liste de sous-ensemble.***")
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

print("liste des points à couvrir ? (1,4,5 ou n).")
input_liste_des_points = input("liste_des_points:")
liste_des_points = []
if len(input_liste_des_points) <=3:
    liste_des_points = [i for i in range(0,int(input_liste_des_points))]
else:
    liste_des_points = from_string_to_tab(input_liste_des_points)
print(liste_des_points)

rec_ou_part = input("Voulez vous des recouvrements ou des partitions ? (r,p)")
taille_des_recouvrements = input("Quelle taille de recouvrement ? (2 ou 3 pour liste exhaustive >3 pour greedy)")
##Etape 2:

def test_exist_un_recouvrement(E):
    setR = set({})
    for P in tab_sous_modèles:
        setR = setR|set(P)
    if setR < E:
        print("Il ne peut pas y avoir de recouvrement !")
        return False
    else:
        print("Il y a peut être des recouvrements !")
        return True

def birecouvrement(E,r,tab): #E un set, r un indice d'incrémentation #TODO a tester
    for i in range(r,len(tab_sous_modèles)-1):
             if rec_ou_part=='r' or set(tab_sous_modèles[i]) <= E:
                for j in range(i+1,len(tab_sous_modèles)):
                    if rec_ou_part == 'r' or set(tab_sous_modèles[j]) <=E:
                        ti = tab_sous_modèles[i]
                        tj = tab_sous_modèles[j]
                        if set(ti+tj)>=E:
                            if rec_ou_part=='r' or len(set(ti))+len(set(tj))==len(set(ti+tj)):
                                tab.append((ti,tj))


tab_recouvrement = []
def trirecouvrement(E): #TODO a tester
    for i in range(0,len(tab_sous_modèles)):
        tab_i = [tab_sous_modèles[i]]
        birecouvrement(E-set(tab_sous_modèles[i]),i+1,tab_i)
        if len(tab_i)>1:
            tab_recouvrement.append(tab_i)


if test_exist_un_recouvrement(set(liste_des_points)):
    if int(taille_des_recouvrements) == 2:
        birecouvrement(set(liste_des_points),0,tab_recouvrement)
    if int(taille_des_recouvrements) ==3:
        trirecouvrement(set(liste_des_points))
    if int(taille_des_recouvrements) >3:
        print("Pas encore implémenté !")
    print(tab_recouvrement)

##Etape 3: On écris les fichiers:

    try:
        os.mkdir(nom_de_dossier)
    except:
        print("Le dossier existe déjà")

    f = open(nom_de_dossier + "\\" + fichier_recouvrement, 'w')

    for x in tab_recouvrement:
        for y in x:
            f.write(str(y)+",")
            f.write("\n")

    f.close()
