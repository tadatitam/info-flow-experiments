import sys

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

def correctly_classified(ypred, ylabel):									# number of correctly classified instances in blocks
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
	
def block_p_test_mode2(Xtest, ytest, flipped=False, alpha=0.01, iterations=100000):				# block permutation test
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
	print "\nConfidence Interval of p-value:", proportion_confint(under, iterations, alpha, 'beta')
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
	print "\nConfidence Interval of p-value:", proportion_confint(under, iterations, alpha, 'beta')
	return (1.0*under) / (1.0*iterations)

#------------- helper functions for printing statistics of the data ---------------#


def find_word_in_collection(collection, words):
	counts = [0,0]
	for col in collection:
		advs = col['adv']
		for adv in advs:
			counts[adv.label] += adv.freq_contains(words)
	return counts

def print_counts(X,y):											# check
	print "Number of blocks in log: ", X.shape[0]
	print "Number of agents in a block: ", X.shape[1]
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
	print "[treatments] [blocks] [features] [unique-features] :: ", ua, count, counts, ucounts
	print ""




