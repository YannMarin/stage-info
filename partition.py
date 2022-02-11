'''

Programme pour trouver les 2 ou 3-recouvrements ou les 2 ou 3-partitions de n points à partir d'une liste de sous-ensemble.

A supprimer quand recouvrement sera testé.
'''



def birecouvrement(L,P,R,E): #L liste de sous-ensemble, P un ensemble de L, R la liste des recouvrements. On return les recouvrements qui utilisent P
    PP=[]
    for i in E:
        if i not in P:
            PP.append(i)
    for x in L:
        if set(PP) <= set(x):
            R.append((P,x))


def trouver_tous_les_birecouvrements(L,R,E):
    while len(L)>0:
        birecouvrement(L,L[0],R,E)
        del L[0]

def trirecouvrement_birecouvrement(L,P,X,E): #L liste de sous-ensemble, P un ensemble de L, R la liste des recouvrements. On return les recouvrements qui utilisent P
    PP=[]

    for i in E:
        if i not in X:
            PP.append(i)
    if len(PP)>0:
        List = [(P,X,x) for x in L if x != P and x!= X and set(PP) <= set(x)] #== si partition, <= si recouvrement
        if List != []:
            return List


def trirecouvrement(L,P,R,E):
    EE=[]
    for i in E:
        if i not in P:
            EE.append(i)
    if len(EE)>0:
        for x in L:
            if x != P:
                List = trirecouvrement_birecouvrement(L,P,x,EE)
                if List != None:
                    R.append(trirecouvrement_birecouvrement(L,P,x,EE))

def trouver_tous_les_trirecouvrements(L,R,E):
    while len(L)>0:
        trirecouvrement(L,L[0],R,E)
        del L[0]



print("***Programme pour trouver les 2 ou 3-recouvrements ou les 2 ou 3-partitions de n points à partir d'une liste de sous-ensemble.***")
print("Taille des modèles ?")
n=int(input("n: "))
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
Recouvrement = []
#L = [[0,1,2,3,6,7,8],[0,1,4,5,9],[2,3,4,5,6,9],[1,2,3],[0,1,9]]

trouver_tous_les_birecouvrements(tab_sous_modèles,Recouvrement,[0,2,4,6,8,10,12,14])
#print(Recouvrement)


f = open('16SymRec3.txt', 'w')

for x in Recouvrement:
    for y in x:
        f.write(str(y)+",")
        f.write("\n")
