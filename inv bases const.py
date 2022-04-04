from math import factorial

"""

fichier pour à partir de l'ensemble des bases constantes avoir l'ensemble des bases non constantes. Le but étant de créer des sous-modèles de duplet non constants.

"""
n = int(input("nombre de point ?"))
d = int(input(" d  ?"))
nom_du_fichier = input("nom du fichier ?")
fichier = open(nom_du_fichier, "r")
bases_fixes_fichier = fichier.readlines()
fichier.close()
tab_bases_fixes = [int(x) for x in bases_fixes_fichier]

taillemax = int(factorial(n)/(factorial(d)*factorial(n-d)))

tab_bases_non_fixes = [x for x in range(0,taillemax) if x not in tab_bases_fixes]


f = open("inv_"+nom_du_fichier, 'w')
for x in tab_bases_non_fixes:
    f.write(str(x)+"\n")

