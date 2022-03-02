"""

Module pour créer un tableau HTML à partir d'une liste


"""
from tabulate import tabulate



nom_du_fichier =input("nom du fichier de la liste ?")
fichier = open(nom_du_fichier,"r")
list_fichier = fichier.readlines()
fichier.close()

tab_list = []
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
    tab_list.append(l)

print("tab_SMC",len(tab_list))
print(tab_list)

if not sorted(tab_list):
    tab_list.sort()

def creer_tab_taille(tab): ##Créer un tableau tab_taille des différentes taille d'une liste triée.
    taille_min = len(tab[0])
    taille_max = len(tab[-1])
    tab_taille = []
    for t in range(0,taille_max-taille_min+1):
        tab_taille.append(t+taille_min)
    return tab_taille

def creer_tab_nombre_par_taille(tab,tab_taille): ##Créer un tableau taille_nbr_par_taille qui donne le nombre d'ensemble de chaque taille d'une liste triée
    taille_nbr_par_taille = []
    nbr = 0
    lenP = len(tab[0])
    for P in tab:
        if len(P) == lenP:
            nbr+=1
        else:
            lenP=len(P)
            taille_nbr_par_taille.append(nbr)
            nbr=0
    taille_nbr_par_taille.append(nbr)
    return taille_nbr_par_taille
"""
def creer_tab_HTML(tab,tab_taille,tab_nbr_par_taille):
    f = open(nom_du_fichier+"_HTML"+".html", 'w')
    f.write("<table>")
    for i in range(0,tab_taille):
        f.write("<tr><td>"+"\n")
        f.write("</td><td>".join(tab_taille[i])+"\n")
        f.write("</td></tr>"+"\n")
        f.write("</table>")
    f.close()"""

tab_taille = creer_tab_taille(tab_list)
tab_nbr_par_taille = creer_tab_nombre_par_taille(tab_list,tab_taille)
type_of_tab = input("HTML (html) ou LateX (latex) ?")
text = tabulate([tab_taille,tab_nbr_par_taille],tablefmt=type_of_tab,headers='firstrow')
print(tab_taille)
print(tab_nbr_par_taille)
print(text)
f= open(nom_du_fichier+"_"+type_of_tab+".html", 'w')
f.write(text)

