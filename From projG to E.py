
##Etape 1 On prend la liste des symétriques des points
nom_du_fichier =input("nom du fichier des symétriques des points ?")
fichier = open(nom_du_fichier,"r")
points_fichier = fichier.readlines()
fichier.close()
tab_sym_point = [int(x) for x in points_fichier]


##Etape 2 On prend la liste des SMC à transformer
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


##Etape 3:

tab_SMC_sur_E = []
for P in tab_SMC:
    PP = []
    for p in P:
        PP.append(p)
        PP.append(tab_sym_point[p])
    PP.sort()
    tab_SMC_sur_E.append(PP)

print("tab_SMC",len(tab_SMC))
print(tab_SMC)
print("tab_SMC_sur_E",len(tab_SMC_sur_E))
print(tab_SMC_sur_E)

f = open("projGtoE.txt", 'w')

for x in tab_SMC_sur_E:
    for y in x:
        f.write(str(y)+",")
    f.write("\n")
f.close()