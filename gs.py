# Jeffrey
# Python implementation of stable matching problem
# Homework 1 Starter Code
# CYB 2013

def gs(men, women, pref, excluded):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of preferred names in sorted order)
            blocked (list of (man,woman) tuples that are unacceptable matches)
    Output: dictionary of stable matches
    """
    # preprocessing
    ## build the rank dictionary
    rank={}
    for w in women:
        rank[w] = {}
        i = 1
        for m in pref[w]:
            rank[w][m]=i
            i+=1
    ## create a "pointer" to the next woman to propose
    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)    #initially all men and women are free
    numpartners = len(men) 
    S = {}           #build dictionary to store engagements 

    #run the algorithm
    while freemen:
        m = freemen.pop()
        #get the highest ranked woman that has not yet been proposed to
        w = pref[m][prefptr[m]]
        prefptr[m]+=1
        if w not in S: S[w] = m
        else:
            mprime = S[w]
            if rank[w][m] < rank[w][mprime]:
                S[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
    return S

def gs_block(men, women, pref, blocked):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of preferred names in sorted order)
            blocked (list of (man,woman) tuples that are unacceptable matches)
    Output: dictionary of stable matches
    """
rank={}
    for w in women:
        rank[w] = {}
        i = 1
        for m in pref[w]:
            rank[w][m]=i
            i+=1
    # create a "pointer" to the next woman to propose
    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)    #initially all men and women are free
    S = {}           #build dictionary to store engagements 

    #run the algorithm
    while freemen:
        m = freemen.pop()
        
        # If the man has proposed to everyone he will be unmatched
        if prefptr[m] >= len(pref[m]):
            continue
            
        # get the next free woman
        w = pref[m][prefptr[m]]
        prefptr[m] += 1
        
        # Check if the pariing is blocked
        if (m, w) in blocked:
            freemen.add(m)
            continue
            
        if w not in S: 
            S[w] = m
        else:
            mprime = S[w]
            if rank[w][m] < rank[w][mprime]:
                S[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
                
    return S
    return "test"

def gs_tie(men, women, preftie):
    """
    Gale-shapley algorithm, modified to exclude unacceptable matches
    Inputs: men (list of men's names)
            women (list of women's names)
            pref (dictionary of preferences mapping names to list of sets of preferred names in sorted order)
    Output: dictionary of stable matches

    """

    # Flatten the list of sets into a standard list. If a man is indifferent 
    # between two women, the order he proposes to them doesn't matter for stability.
    women_rank = {}
    for w in women:
        women_rank[w] = {}
        i = 1
        for tie_group in preftie[w]:
            for m in tie_group:
                women_rank[w][m] = i
            i += 1

    # 2. Preprocess Men's Preferences
    men_flat_pref = {}
    for m in men:
        men_flat_pref[m] = []
        for tie_group in preftie[m]:
            men_flat_pref[m].extend(list(tie_group))

    # points to next woman the man will propose to
    prefptr = {}
    for m in men:
        prefptr[m] = 0

    freemen = set(men)    
    S = {}                

    # run the algorithm
    while freemen:
        m = freemen.pop()
        
        if prefptr[m] >= len(men_flat_pref[m]):
            continue
            
        w = men_flat_pref[m][prefptr[m]]
        prefptr[m] += 1
            
        if w not in S: 
            S[w] = m
        else:
            mprime = S[w]
            if women_rank[w][m] < women_rank[w][mprime]:
                S[w] = m
                freemen.add(mprime)
            else:
                freemen.add(m)
                
    return S
    return "test"

if __name__=="__main__":
    #input data
    themen = ['xavier','yancey','zeus']
    thewomen = ['amy','bertha','clare']

    thepref = {'xavier': ['amy','bertha','clare'],
           'yancey': ['bertha','amy','clare'],
           'zeus': ['amy','bertha','clare'],
           'amy': ['yancey','xavier','zeus'],
           'bertha': ['xavier','yancey','zeus'],
           'clare': ['xavier','yancey','zeus']
           }
    thepreftie = {'xavier': [{'bertha'},{'amy'},{'clare'}],
           'yancey': [{'amy','bertha'},{'clare'}],
           'zeus': [{'amy'},{'bertha','clare'}],
           'amy': [{'zeus','xavier','yancey'}],
           'bertha': [{'zeus'},{'xavier'},{'yancey'},],
           'clare': [{'xavier','yancey'},{'zeus'}]
           }
    
    blocked = {('xavier','clare'),('zeus','clare'),('zeus','amy')}

    #eng
    match = gs(themen,thewomen,thepref)
    print(match)
    
    match_block = gs_block(themen,thewomen,thepref,blocked)
    print(match_block)

    match_tie = gs_tie(themen,thewomen,thepreftie)
    print(match_tie)
