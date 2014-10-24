import numpy as np

class UniqueElement:
    def __init__(self,value,occurrences):
        self.value = value
        self.occurrences = occurrences

def perm_unique(elements):
    bins = np.bincount(elements)
    listunique = []
    for i in range(0,len(bins)):
    	listunique.append(UniqueElement(i, bins[i]))
    u=len(elements)
    return perm_unique_helper(listunique,[0]*u,u-1)

def perm_unique_helper(listunique,result_list,d):
    if d < 0:
        yield tuple(result_list)
    else:
        for i in listunique:
            if i.occurrences > 0:
                result_list[d]=i.value
                i.occurrences-=1
                for g in  perm_unique_helper(listunique,result_list,d-1):
                    yield g
                i.occurrences+=1

def full_test(X_test, y_test, test_stat): 
    """
    The permutation test done exactly.
    Returns a p-value.
    """
    observed_value = test_stat(X_test, y_test)
    under = 0
    y_permutations = list(perm_unique(y_test))
    for new_y in y_permutations:
        permuted_value = test_stat(X_test, new_y)
        # No need to compute this. prediction X_test doesnt change
        if round(observed_value, 10) <= round(permuted_value, 10):
            under += 1
    return (1.0*under) / (1.0*len(y_permutations))

# def blocked_test(X_test, y_test, alpha=0.01, iterations=100000)

#def block_p_test_mode2(Xtest, ytest, flipped=False, alpha=0.01, iterations=100000):				# block permutation test
#    observed_value_of_test_stat = test_stat(data)
#    
#	Tobs = stat_kw2(Xtest, ytest)
## 	print "----!! Stat is computing treat1 - treat0 !!----"
#	print 'Tobs: ', Tobs
## 	print "----!! Counting number of times Tobs <= Tpi !!----"
#	under = 0
#	for i in range(0,iterations):
#		yperm = get_perm(ytest)
#		Tpi = factor*stat_kw2(Xtest, yperm)
#		if round(Tobs, 10) <= round(Tpi, 10):
#			under += 1
#	print "\nConfidence Interval of p-value:", proportion_confint(under, iterations, alpha, 'beta')
#	return (1.0*under) / (1.0*iterations)
