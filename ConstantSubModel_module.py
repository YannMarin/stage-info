#from sympy import binomial
from scipy.special import comb
import time
import copy



def name():
    return 'ConstantSubModel'

def signature():
    return([{'name': 'vector','desc': 'Vector of fixed bases'},
            {'name': 'int','desc' : 'Number of points'},
            {'name' :'int','desc': 'Dimension+1','param': 4}],
           [{'name' : 'vector','desc': 'Constant Sub-model'}])

def description():
    return 'Compute constant sub-model from a set of fixed bases'

def category():
    return 'Constant Sub-model'

def combinations(iterable, r): #piqué ici https://docs.python.org/3/library/itertools.html#itertools.combinations
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def create_combination_tab(N,d):
    #tab_combinations = [binomial(n,d) for n in range(d,N+1)]
    tab_combinations = [comb(n,d,exact=True) for n in range(d,N+1)]
    return tab_combinations





def compute(ldkdict, params, queue):
    #get the sublist of constant bases
    sublist_bases = [int(x) for x in params[0][1]]

    #get the number of point and dimension+1
    n = params[1]
    d = params[2]

    #list of d in i for d<=i<=n, used to minimise calculation
    combination_tab = create_combination_tab(n, d)

    #list of the d in n combinations, used to get base points from base indices
    list_base = combinations(range(n), d)
    tab_base = [[y for y in x] for x in list_base]

    #put bigger models to test in the fifo list, used in "trouver_sous_modèles_fixes".
    def ajouter_les_modèles_plus_grand(P, B, L):
        tailleP = len(P)
        bool_est_max = True
        for i in range(P[-1], n):
            Pi = copy.copy(P)
            Pi.append(i)
            Bi = copy.copy(B)
            count_ = 0
            j = 0
            while j < len(Bi):
                if set(tab_base[Bi[j]]) < set(Pi):
                    count_ = count_ + 1
                    del Bi[j]
                    j = j - 1
                j = j + 1
            if count_ + combination_tab[tailleP - d] == combination_tab[tailleP - d + 1]:
                bool_est_max = False
                L.append((Pi, Bi))
        return bool_est_max

    #find the constant sub models, more details in https://github.com/YannMarin/stage-info/blob/master/CR/Feuille_de_route_programme_2.pdf
    def trouver_sous_modèles_fixes(B, tab, recursions):
        L = [(tab_base[b], B[0:B.index(b)] + B[B.index(b) + 1:]) for b in B]
        while len(L) > 0:
            if ajouter_les_modèles_plus_grand(L[0][0], L[0][1], L):
                tab.append(L[0][0])
            tailleP = len(L[0][0])
            tailleB = len(L[0][1])
            recursions[0] = recursions[0] + 1
            if recursions[0] % 500 == 0 or tailleP > recursions[1]:
                recursions[1] = tailleP
                """print("\r", recursions[0], " len(L) :", len(L), "len(B): ", tailleB, " len tab :", len(tab),
                      "On est à l'étape ", recursions[1], "sur", n, "au maximum.", end="")"""
            #queue.put(recursions[0]) #Comment fonctionne l'affichage ?
            del L[0]
    #list of constant sub model
    tab_SMC = []

    #rec[0]= number of recursion, rec[n]=k when we are testing the len (k in n) combination,
    #used to show how the caclulation is running
    rec = [0, n]

    #time calculation
    start = time.time()

    #do the calculation
    trouver_sous_modèles_fixes(sublist_bases, tab_SMC, rec)

    #time calculation bis
    end = time.time()
    elapsed = end - start


    #cleaning tab_SMC
    tab_SMC_sans_doublon = []
    tab_SMC_sans_doublon = [x for x in tab_SMC if x not in tab_SMC_sans_doublon]
    tab_SMC = tab_SMC_sans_doublon

    tab_SMC_max = []
    for x in range(len(tab_SMC)):  # On pourrait faire mieux.
        count = 0
        for y in range(len(tab_SMC)):
            if not set(tab_SMC[x]) < set(tab_SMC[y]):
                count += 1
        if count == len(tab_SMC):
            tab_SMC_max.append(tab_SMC[x])

    tab_SMC = tab_SMC_max

    #eliminating bases
    tab_SMC_without_bases = [x for x in tab_SMC if len(x) > d]


    return [{'content': tab_SMC,
             'infos':'Vector of '+str(len(tab_SMC))+"maximal constants sub models ("
                     + str(len(tab_SMC_without_bases))+"without bases) from len"+ len(tab_SMC[0]) + "to" + len(tab_SMC[-1])}]
