import numpy as np

"""

Programme pour extraire certaines bases d'une matrice npy de bases.
Prend en entrée un ensemble d'incides de bases.


"""

nom_du_fichier = input("nom_du_fichier des indices des d-uplets à extraire:")
fichier = open(nom_du_fichier, "r")
bases_fichier = fichier.read().splitlines()
fichier.close()

tab_bases = [[int(x) for x in X if x!=' '] for X in bases_fichier]



nom_du_fichier = input("nom_du_fichier de la liste des d-uplets non constants:")
fichier = open(nom_du_fichier, "r")
bases_fichier = fichier.read().splitlines()
fichier.close()
tab_duplets = [[int(x) for x in X if x!=' ']  for X in bases_fichier]

tab_indices = []
for x in tab_bases:
    i=0
    for y in tab_duplets:
        if x==y:
            tab_indices.append(i)
        else:
            i=i+1


print(tab_bases)
print(tab_duplets)
print(tab_indices)

matrix = np.load('5.npy')
print(matrix.shape)

sub_matrix = []
sub_matrix = [matrix[y][x] for y in range(matrix.shape[0]) for x in tab_indices] #c'est ça et pas l'inverse !
sub_matrix=np.array(sub_matrix)


print(sub_matrix.shape)
sub_matrix = sub_matrix.reshape(matrix.shape[0], len(tab_indices))
print(sub_matrix.shape)

print(sub_matrix)
print("stop")
print(matrix)

np.save('submatrix31v1.npy',sub_matrix)

