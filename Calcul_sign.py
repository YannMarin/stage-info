from numpy.linalg import det
from numpy import sign
"""

calcul le signe d'un d-uplet dans un ensemble de modèle et compte le nombre de +, de - et de 0.

Pour cela il faut:
    -lire un fichier de la forme
'point 1
coord x_0 y_0 z_0
coord x_1 y_1 z_1
...
'point 2
trouver le numéro du point et garder ses coord, ensuite calculer le sign du determinant.

"""
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

#etape 1: lire le fichier

#nom_du_fichier = input("nom du fichier ?:")
nom_du_fichier = "coordpoint.txt"

#duplet_text = input("d-uplet à tester ? 0,1,2..")
#duplet = from_string_to_tab(duplet_text)
duplet = [0, 4, 6, 14]


f = open(nom_du_fichier,'r')
fichier = f.read().splitlines()
f.close()

print(fichier)

tab_matrix = []
matrix = []
list_signe = []
n=0
for ligne in fichier:
    if ligne[0] == "'": #si on est en train de lire le numéro d'un modele
        n = 0  #on cherche les bons numéro de points
        if matrix != []:
            tab_matrix.append(matrix)
            matrix = []
    else: #si on est en train de lire les coord d'un point
        if n in duplet: #si le numéro du point est bien un point du duplet

            coord = "" #on cherche les coord du point
            row = [] #ligne par ligne
            for t in ligne: #On ajoute les 3 coord dans row
                if t == " ": #si on change de coord
                    row.append(float(coord)) #on ajoute la coord dans row
                    coord = ""
                else: coord=coord+t
            row.append(float(coord))
            row.append(1.0) #on passe en affine
            matrix.append(row) #on ajoute la ligne à matrix
        n=n+1


print("tab_matrix:",len(tab_matrix))


tab_det = [det(M) for M in tab_matrix]
print("tab_det",len(tab_det))


tab_sign = sign(tab_det)
print("tab_sign",len(tab_sign))
print(tab_sign)

tab_plus = [i for i in range(0,len(tab_sign)) if tab_sign[i]==1]
print("tab_plus",len(tab_plus))
print(tab_plus)

tab_zero = [i for i in range(0,len(tab_sign)) if tab_sign[i]==0]
print("tab_zero",len(tab_zero))
print(tab_zero)

tab_moins = [i for i in range(0,len(tab_sign)) if tab_sign[i]==-1]
print("tab_moins",len(tab_moins))
print(tab_moins)

