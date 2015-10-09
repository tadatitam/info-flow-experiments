import numpy as np
import random											# for random shuffles
from datetime import datetime							# for getting times for computation
from scipy import stats									# for confidence_interval computation

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
    
    
	
def get_perm(ylabel):								
    """
    Generate a permutation for block_p_test.
    """
    blocks = ylabel.shape[0]
    yret = np.copy(ylabel)
    for i in range(0,blocks):
        random.shuffle(yret[i])
    return yret
	
def blocked_sampled_test(observed_values, unit_assignments, test_stat, alpha=0.01, iterations=10000):
    """
    Run a block permutation test.
    """
    s = datetime.now()
    Tobs = test_stat(observed_values, unit_assignments)
    print 'Tobs: ', Tobs
    under = 0
    for i in range(0,iterations):
        permuted_assignments = get_perm(unit_assignments)
        Tpi = test_stat(observed_values, permuted_assignments)
        if round(Tobs, 10) <= round(Tpi, 10):
            under += 1
    e = datetime.now()
    print "---Time for running permutation test: ", str(e-s)
    print "\nConfidence Interval of p-value:", proportion_confint(under, iterations, alpha, 'beta')
    return (1.0*under) / (1.0*iterations)


def proportion_confint(count, nobs, alpha=0.05, method='normal'):
    q_ = count * 1. / nobs
    alpha_2 = 0.5 * alpha

    if method == 'normal':
        std_ = np.sqrt(q_ * (1 - q_) / nobs)
        dist = stats.norm.isf(alpha / 2.) * std_
        ci_low = q_ - dist
        ci_upp = q_ + dist

    elif method == 'binom_test':
        # inverting the binomial test
        def func(qi):
            #return stats.binom_test(qi * nobs, nobs, p=q_) - alpha #/ 2.
            return stats.binom_test(q_ * nobs, nobs, p=qi) - alpha
        # Note: only approximate, step function at integer values of count
        # possible problems if bounds are too narrow
        # problem if we hit 0 or 1
        #    brentq fails ValueError: f(a) and f(b) must have different signs
        ci_low = optimize.brentq(func, q_ * 0.1, q_)
        #ci_low = stats.binom_test(qi_low * nobs, nobs, p=q_)
        #ci_low = np.floor(qi_low * nobs) / nobs
        ub = np.minimum(q_ + 2 * (q_ - ci_low), 1)
        ci_upp = optimize.brentq(func, q_, ub)
        #ci_upp = stats.binom_test(qi_upp * nobs, nobs, p=q_)
        #ci_upp = np.ceil(qi_upp * nobs) / nobs
        # TODO: check if we should round up or down, or interpolate

    elif method == 'beta':
        ci_low = stats.beta.ppf(alpha_2 , count, nobs - count + 1)
        ci_upp = stats.beta.isf(alpha_2, count + 1, nobs - count)

    elif method == 'agresti_coull':
        crit = stats.norm.isf(alpha / 2.)
        nobs_c = nobs + crit**2
        q_c = (count + crit**2 / 2.) / nobs_c
        std_c = np.sqrt(q_c * (1. - q_c) / nobs_c)
        dist = crit * std_c
        ci_low = q_c - dist
        ci_upp = q_c + dist

    elif method == 'wilson':
        crit = stats.norm.isf(alpha / 2.)
        crit2 = crit**2
        denom = 1 + crit2 / nobs
        center = (q_ + crit2 / (2 * nobs)) / denom
        dist = crit * np.sqrt(q_ * (1. - q_) / nobs + crit2 / (4. * nobs**2))
        dist /= denom
        ci_low = center - dist
        ci_upp = center + dist

    elif method == 'jeffrey':
        ci_low, ci_upp = stats.beta.interval(1 - alpha,  count + 0.5,
                                             nobs - count + 0.5)

    else:
        raise NotImplementedError('method "%s" is not available' % method)
    return ci_low, ci_upp

