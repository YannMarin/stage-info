

def name():
    return 'CSMSymetric'

def signature():
    return([{'name':'vector','desc':'Constant sub-models'},
            {'name':'vector','desc:':'Symetric point'},
            {'name':'vector','desc':'Point partition GCD'}],
           [{'name':'vector','desc':'Vector of CSM that have a symetric CSM'},
            {'name':'vector','desc':'Vector of maximum  Union of two symetric CSM'}])

def description():
    return 'Take a list of CSM, a list of symetric point and a partition GCD ' \
           'and compute a list of CSM that their symetric is a CSM of the list and a list of the maximum union of two symetrics CSM'

def category():
    return 'Constant Sub-model'


def compute(ldkdict, params, queue):
    #get the list of CSM
    tab_SMC = [[int(x) for x in y] for y in params[0]]

    #get the symetrics list
    tab_sym_point = [int(x) for x in params[1]]
    tab_part_point = params[2]

    n = len(tab_sym_point)

    #return the symetric of P a submodel
    def sym(P):
        symP = [tab_sym_point[p] for p in P]
        symP.sort()
        return symP

    #test if symP is in tab_SMC
    def test_est_sym(P):
        return sym(P) in tab_SMC

    #list of P in tab_SMC such that symP is in tab_SMC
    tab_SMC_sym = [x for x in tab_SMC if test_est_sym(x)]

    #list of union of P and symP in tab_SMC_sym
    tab_SMC_Union = []
    for X in tab_SMC_sym:
        Union = []
        for x in X:
            if x not in Union:
                Union.append(x)
            if tab_sym_point[x] not in Union:
                Union.append(tab_sym_point[x])
        Union.sort()
        tab_SMC_Union.append(Union)

    #we keep only maximum set
    tab_Union_max = []

    for x in range(len(tab_SMC_Union)):  # On pourrait faire mieux.
        count = 0
        for y in range(len(tab_SMC_Union)):
            if not set(tab_SMC_Union[x]) < set(tab_SMC_Union[y]):
                count += 1
        if count == len(tab_SMC_Union):
            tab_Union_max.append(tab_SMC_Union[x])

    return [{'content': tab_SMC_sym,
             'infos':'Vector of '+ str(len(tab_SMC_sym))+"symetric CSM"},
            {'content': tab_Union_max,'infos':'Vector of '+str(len(tab_Union_max))
            + 'Union of two symetric CSM.'}]



