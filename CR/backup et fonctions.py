
''' trouve les sous_modèles fixes maximaux
    à partir d'un ensemble d'indice de bases fixes

    variables: B tableau d'indices de base
                nB tableau de points couvert par B
                combination_tab: tableaux des combinaisons précalculé
                combination: le nombre (d parmi nB)
                r sert à réduire le nombre de récursion en ne supprimant que les bases à la rème position ou plus dans l'étape 3.
'''

''' la version 1 est médiocre, elle fait 2^tailleB itérations, mais elle permet de comprendre l'idée de base.
    Elle peut tout de même être utile pour B de petite taille.'''

def trouver_sous_modèles_fixesv1(B, r, tab,recursions): #B un ensemble d'indice, nB l'ensemble des points couvert par B,r indice de récursion, tab tableau du résultat
    recursions[0] +=1
    tailleB = len(B)
    nB = from_bases_indices_to_point(B) #faire un traqueur du nombre d'itérations.
    taillenB = len(nB)
    combination = combination_tab[taillenB-d]
    if tailleB == combination : #on termine la récursion
        tab.append(nB)
    elif tailleB > combination : #Normalement on entre jamais dans cette boucle.
        print("Qu'est-ce qu'il se passe ????")
    else: #cas tailleB < combination #TODO si on peut améliorer l'algorithme c'est ici
        #print("Cas 3!")
        for i in range(r,tailleB):
            Bi = copy.copy(B)
            del Bi[i]
            trouver_sous_modèles_fixesv1(Bi, i, tab,rec)
            '''On test tous les sous-ensemble de B (sauf ceux correspondants à des sous-modèles non maximaux).'''



def from_number_to_letter(x): #x un nombre, return la lettre correspondante en commençant par 0=a
    return chr(ord('`')+x+1)

def from_letter_to_number(L): #L une lettre, return le nombre correspondant en commençant par a=0.
    return int(ord(L)-ord('`')-1)

def print_alphabet(x): #affiche l'alphabet pour ceux qui ne le connaissent pas.
    for x, y in ((x, chr(ord('a') + x)) for x in range(x)):
        print(x,"=",y,end=", ")
    print("")



'''         Dans cette version, le but est de faire la récurence sur tous les ensembles de bases qui couvrent un sous ensemble de nB et maximaux.'''
def trouver_sous_modèles_fixesv2(B, r, tab, nB, taillenB, tailleB,recursions):
    combination = combination_tab[taillenB-d]
    if tailleB == combination:
        tab.append(nB)
    else:

        for i in range(0,r):
            nBi = copy.copy(nB)
            del nBi[i]
            if taillenB-1 >= d:
                Bi = [x for x in B if set(from_base_indice_to_base(x)) <= set(nBi)]
                trouver_sous_modèles_fixesv2(Bi, i, tab, nBi, taillenB - 1, len(Bi),recursions)
    recursions[0] += 1
    if recursions[0]%100 == 0:
        print("\r", recursions[0], end="")

""" backup d'une version qui ne marche pas sur 41 points
def trouver_sous_modèles_fixesv2(B, r, tab, nB, taillenB, tailleB,recursions): 
    recursions[0] += 1
    #print(B)
    print("\r",recursions[0],end="")
    combination = combination_tab[taillenB-d]
    if tailleB == combination:
        tab.append(nB)
    else:

        for i in range(0,r):
            nBi = copy.copy(nB)
            #print("\r",nBi)
            del nBi[i]
            if taillenB-1 >= d:
                tab_base_de_nBi = from_points_to_basev2(nBi,d)
                #print("\r",tab_base_de_nBi)
                Bi = [x for x in B if from_base_indice_to_base(x) in tab_base_de_nBi] #TODO faut changer ça
                #print("\r",Bi)
                print("Bi fini on passe à la suite")
                trouver_sous_modèles_fixesv2(Bi, i, tab, nBi, taillenB - 1, len(Bi),recursions)

"""