"""
Programme pour trouver tous les SMC d'une liste contenu dans un SMC.



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

##Etape 1:
String_SM=input("Sous-modèle à tester ? (0,1,2,14 ..):")
SM=from_string_to_tab(String_SM)
print("Sous-modèle:",len(SM))
print(SM)



nom_du_fichier =input("nom du fichier des SMC ?")
fichier = open(nom_du_fichier,"r")
SMC_fichier = fichier.readlines()
fichier.close()
tab_SMC = []
for x in SMC_fichier:
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

print("liste des SMC à tester:",len(tab_SMC))
print(tab_SMC)

##Etape 2:

tab_SMC_inf = []
for P in tab_SMC:
    if set(P) <= set(SM):
        tab_SMC_inf.append(P)

print("lite des SMC inf:",len(tab_SMC_inf))
print(tab_SMC_inf)