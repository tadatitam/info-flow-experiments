import sys
import adVector, ad, common

import numpy as np										
from scipy import stats									# for chi2 test
from datetime import datetime							# counting times for running tests

from itertools import combinations as comb				# permutations for old permutation test
import random											# for random shuffles


#------------- functions computing Statistics ---------------#

def stat_prc(adv, ass, keywords):							# prc statistic, which doesn't give very good results		
	presence = []
	for i in range(0, len(adv)):
		if(adv[i].freq_contains(keywords) > 0):
			presence.append(1)
		else:
			presence.append(0)
	ct,cu=0,0
	for i in range(0, len(adv)):
		if(str(i) in ass[0:len(ass)/2]):
			ct += presence[i]
		else:
			cu += presence[i]
	return (ct-cu)

def stat_kw(adv, ass, keywords):							# keyword_diff based statistic
	advm, advf = vec_for_stats(adv, ass)
	return (advm.freq_contains(keywords) - advf.freq_contains(keywords))
	
def stat_sim(adv, ass, keywords):							# cosine similarity based statistic
	advm, advf = vec_for_stats(adv, ass)
	return -ad_sim(advm, advf)
 
def stat_ML(X_test, y_test, clf):							# classifier based statistic
	g1 = [X_test[i] for i in range(0,len(X_test)) if y_test[i]==1]
	g2 = [X_test[i] for i in range(0,len(X_test)) if y_test[i]==0]		# CAn REduce RUN TIME by 50%!!!
	return sum(clf.predict(g1)) - sum(clf.predict(g2))

def stat_CC(ypred, ylabel):									# number of correctly classified instances in blocks
	if(ypred.shape != ylabel.shape):
		raw_input("ypred, ylabel not of same shape!")
		print "Exiting..."
		sys.exit(0)
	blocks = ypred.shape[0]
	blockSize = ypred.shape[1]
	CC = 0
	for i in range(0,blocks):
		for j in range(0, blockSize):
			if(ypred[i][j]==ylabel[i][j]):
				CC += 1
	return CC

def stat_kw2(X_test, y_test):
	blocks = y_test.shape[0]
	blockSize = y_test.shape[1]
	kw0 = 0
	kw1 = 0
	for i in range(0,blocks):
		for j in range(0, blockSize):
			if(y_test[i][j]==1):
				kw1 += X_test[i][j]
			elif(y_test[i][j]==0):
				kw0 += X_test[i][j]
			else:
				raw_input("More classes than expected")
				print "Exiting..."
				sys.exit(0)
# 	print kw1, kw0
	return (kw1 - kw0)
	
#------------- Permutation Tests ---------------#

def old_p_test(adv, ass, keywords, stat):					# oakland permutation test
	if(stat == 'coss'):
		Tobs = stat_sim(adv, ass, keywords)
	elif(stat == 'kw'):
		Tobs = stat_kw(adv, ass, keywords)
	elif(stat == 'prc'):
		Tobs = stat_prc(adv, ass, keywords)
	#print "Tobs="+str(Tobs)
	under = 0
	org_ass = ass
	for count, per in enumerate(comb(ass, len(ass)/2), 1):
		new_ass = list(per)+list(set(ass)-set(per))
		if(stat == 'coss'):
			Tpi = stat_sim(adv, new_ass, keywords)
		elif(stat == 'kw'):
			Tpi = stat_kw(adv, new_ass, keywords)
		elif(stat == 'prc'):
			Tpi = stat_prc(adv, new_ass, keywords)
		#print "Tpi="+str(Tpi)
		if round(Tobs, 10) <= round(Tpi, 10):
			under += 1
	return (1.0*under) / (1.0*count)


def new_p_test(X_test, y_test, clf):							# permutation test
	Tobs = stat_ML(X_test, y_test, clf)
	under = 0
	a = list(common.perm_unique(y_test))
	for new_y_test in a:
		Tpi = stat_ML(X_test, np.array(new_y_test), clf)			# No need to compute this. prediction X_test doesnt change
		if round(Tobs, 10) <= round(Tpi, 10):
			under += 1
	return (1.0*under) / (1.0*len(a))
	
def block_p_test_mode2(Xtest, ytest, flipped=False, alpha=0.01, iterations=1000):	# block p-test with kw
	factor = 1
	if(flipped):
		factor = -1
	Tobs = factor*stat_kw2(Xtest, ytest)
# 	print "----!! Stat is computing treat1 - treat0 !!----"
	print 'Tobs: ', Tobs
# 	print "----!! Counting number of times Tobs <= Tpi !!----"
	under = 0
	for i in range(0,iterations):
		yperm = get_perm(ytest)
		Tpi = factor*stat_kw2(Xtest, yperm)
		if round(Tobs, 10) <= round(Tpi, 10):
			under += 1
	print proportion_confint(under, iterations, alpha, 'beta')
	return (1.0*under) / (1.0*iterations)
		
def block_p_test(oXtest, oytest, clf, alpha=0.01, iterations=1000000):				# block permutation test
	blockSize = oXtest.shape[1]
	blocks = oXtest.shape[0]
	ypred = np.array([[-1]*blockSize]*blocks)
	for i in range(0,blocks):
		ypred[i] = clf.predict(oXtest[i])
	Tobs = stat_CC(ypred, oytest)
	print 'Tobs: ', Tobs
	under = 0
	for i in range(0,iterations):
		yperm = get_perm(oytest)
		Tpi = stat_CC(ypred, yperm)
		if round(Tobs, 10) <= round(Tpi, 10):
			under += 1
	print proportion_confint(under, iterations, alpha, 'beta')
	return (1.0*under) / (1.0*iterations)

#------------- helper functions for Statistics and Statistical Tests ---------------#

def vec_for_stats(adv, ass):						# aggregates the control group and experiment group into single ad vectors
	advm = adVector.AdVector()
	advf = adVector.AdVector()
	for i in range(0, len(adv)):
		if(str(i) in ass[0:len(ass)/2]):
			#print "c"+str(i)
			advm.add_vec(adv[i])
		else:
			#print "t"+str(i)
			advf.add_vec(adv[i])
	return (advm, advf)
	
def table_22(adv, ass, keywords):					# creates 2x2 contingency table using keywords
	advm, advf = vec_for_stats(adv, ass)
	kt = advm.freq_contains(keywords)
	ku = advf.freq_contains(keywords)
	nt = advm.size() - kt
	nu = advf.size() - ku
	return [kt, nt, ku, nu]
	
def get_perm(ylabel):								# generates a permutation for block_p_test
	blocks = ylabel.shape[0]
	yret = np.copy(ylabel)
	for i in range(0,blocks):
		random.shuffle(yret[i])
	return yret

def gen_cont_table(X, y, clf):						# generates contingency table for chi2 test
	try:
		n_classes = clf.coef_.shape[0]				# for linear classifiers
	except:
		n_classes = clf.dual_coef_.shape[0]			# for rbf classifiers
	if(n_classes == 1):
		cont_tab = [[0]*2]*2
	else:
		cont_tab = [[0]*n_classes]*n_classes
	cont_tab = np.array(cont_tab)
	print cont_tab.shape
	y_pred = clf.predict(X)
	if(not len(y_pred) == len(y)):
		raw_input("Dimension error!")
	for i in range(0,len(y)):											
																	#				y=0			y=1
		cont_tab[y_pred[i]][y[i]] = cont_tab[y_pred[i]][y[i]]+1		#	y_pred=0	tab[0,0]	tab[0,1]
																	#	y_pred=1	tab[1,0]	tab[1,1]
	return cont_tab

def oakland_test_wrapper(adv, ass, keywords, type):			# oakland styled tests
	if(not type == 'chi'):
		s = datetime.now()
		try:
			res = old_p_test(adv, ass, keywords, type)
		except:
			res = 100
		e = datetime.now()
	else:
		s = datetime.now()
		vec = table_22(adv, ass, keywords)
		try:
			chi2, p, dof, ex = stats.chi2_contingency(vec, correction=True)
			res = p
		except:
			res = 100
# 		print vec
# 		print chi2, p, ex
		e = datetime.now()
	return common.round_figures(res, 6), e-s

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

def find_word_in_collection(collection, words):
	counts = [0,0]
	for col in collection:
		advs = col['adv']
		for adv in advs:
			counts[adv.label] += adv.freq_contains(words)
	return counts

def print_counts_in_block(index, adv, ass):							# returns detailed counts of #ads within a round
	advm, advf = vec_for_stats(adv, ass)
	sys.stdout.write("%s\t AD_t size=%s uniq=%s, AD_u size=%s uniq=%s \n" %(index, advm.size(), 
							advm.unique().size(), advf.size(), advf.unique().size()))
	for i in range(0, len(ass)):
		sys.stdout.write("%s \t" %(adv[i].size()))
	print("")

def print_counts(X,y):											# check
	print "Number of blocks in log: ", X.shape[0]
	print "Number of samples in a block: ", X.shape[1]
	print "Size of feature vector: ", X.shape[2]
	print "Total count of features: ", int(sum(sum(sum(X))))
	ua,uind=np.unique(y,return_inverse=True)
	count=np.bincount(uind)
	counts = [0]*len(ua)
	ucounts = [0]*len(ua)
	ucounter = [[0.]*X.shape[2]]*len(ua)
	for i in range(0, X.shape[0]):
		for j in range(0, X.shape[1]):
			counts[y[i][j]] += int(sum(X[i][j]))
			ucounter[y[i][j]] += np.sign(X[i][j])
	ucounts = np.sum(np.sign(ucounter), axis=1)
	print ucounts
	print "[treatments] [instances] [features] [uniq] :: ", ua, count, counts, ucounts




