import numpy as np
import stat

## CV
from sklearn import cross_validation
from itertools import product

## Classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC


#------------- functions for Machine Learning Analyses ---------------#

def split_data(X, y, splittype, splitfrac, verbose=False):	
	if(splittype == 'rand'):
		rs1 = cross_validation.ShuffleSplit(len(X), n_iter=1, test_size=splitfrac)
		for train, test in rs1:
			if(verbose):
				print test, train
			X_train, y_train, X_test, y_test = X[train], y[train], X[test], y[test]
	elif(splittype == 'timed'):
		split = int((1.-splitfrac)*len(X))
		if(verbose):
			print "Split at block ", str(split)	
		X_train, y_train, X_test, y_test = X[:split], y[:split], X[split:], y[split:]
	else:
		raw_input("Split type ERROR")	
	return X_train, y_train, X_test, y_test

def select_and_fit_classifier(nfolds, algos, X_train, y_train, splittype, splitfrac, blocked, verbose):	
	max_score = 0
	for algo in algos.keys():
		score, mPar, clf = crossVal_algo(nfolds, algo, algos[algo], X_train, y_train, splittype, splitfrac, blocked)
		if(verbose):
			print score, mPar
		if(score > max_score):
			max_clf = clf
			max_score = score
	if(verbose):
		print "Max score: ", max_score
		print "Selected Classifier: "
		print max_clf
	if(blocked==1):
		X_train = np.array([item for sublist in X_train for item in sublist])
		y_train = np.array([item for sublist in y_train for item in sublist])
	max_clf.fit(X_train, y_train)
	return max_clf, max_score

def test_accuracy(clf, X_test, y_test, blocked):
	if(blocked==1):
		X_test = np.array([item for sublist in X_test for item in sublist])
		y_test = np.array([item for sublist in y_test for item in sublist])
		
	return clf.score(X_test, y_test)

def train_and_test(algos, X, y, splittype='timed', splitfrac=0.1, nfolds=10, blocked=1, 
		ptest=1, verbose=False):
	X_train, y_train, X_test, y_test = split_data(X, y, splittype, splitfrac, verbose)
	if(verbose):
		print "Training Set size: ", len(y_train), "blocks"
		print "Testin Set size: ", len(y_test), "blocks"
	clf, CVscore = select_and_fit_classifier(nfolds, algos, X_train, y_train, splittype, splitfrac, blocked, verbose)
	print "CVscore: ", CVscore
	print "Test accuracy: ", test_accuracy(clf, X_test, y_test, blocked)
	pvalue = stat.block_p_test(X_test, y_test, clf)
	print "p-value: ", pvalue
	return clf

def print_top_features(X, y, feat, treatnames, max_clf, featChoice, k=5, blocked=1):		# prints top k features from max_clf+some numbers
	if(blocked==1):
		X = np.array([item for sublist in X for item in sublist])
		y = np.array([item for sublist in y for item in sublist])
	A = np.array([0.]*len(X[0]))
	B = np.array([0.]*len(X[0]))
	for i in range(len(X)):
		if(y[i] == 1):
			A = A + X[i]
		elif(y[i] == 0):
			B = B + X[i]
	n_classes = max_clf.coef_.shape[0]
	if(n_classes == 1):
		topk1 = np.argsort(max_clf.coef_[0])[::-1][:k]
		print "\nFeatures for class %s:" %(str(treatnames[1]))
		for i in topk1:
			if(featChoice == 'ads'):
				feat.choose_by_index(i).printStuff(max_clf.coef_[0][i], A[i], B[i])
			elif(featChoice == 'words'):
				print feat[i]
		topk0 = np.argsort(max_clf.coef_[0])[:k]
		print "\n\nFeatures for class %s:" %(str(treatnames[0]))
		for i in topk0:
			if(featChoice == 'ads'):
				feat.choose_by_index(i).printStuff(max_clf.coef_[0][i], A[i], B[i])
			elif(featChoice == 'words'):
				print feat[i]
	else:
		for i in range(0,n_classes):
			topk = np.argsort(max_clf.coef_[i])[::-1][:k]
			print "Features for class %s:" %(str(treatnames[i]))
			for j in topk:
				if(featChoice == 'ads'):
					feat.choose_by_index(j).display()
				elif(featChoice == 'words'):
					print feat[j]
			print "coefs: ", max_clf.coef_[i][topk]
	

def crossVal_algo(k, algo, params, X, y, splittype, splitfrac, blocked, verbose=False):				# performs cross_validation
	if(splittype=='rand'):
		rs2 = cross_validation.ShuffleSplit(len(X), n_iter=k, test_size=splitfrac)
	elif(splittype=='timed'):
		rs2 = cross_validation.KFold(n=len(X), n_folds=k)
	max, max_params = 0, {}
	par = []
	for param in params.keys():
		par.append(params[param])
	for p in product(*par):
		if(verbose):
 			print "val=", p
		score = 0.0
		for train, test in rs2:
			X_train, y_train, X_test, y_test = X[train], y[train], X[test], y[test]
			if(blocked==1):
				X_train = np.array([item for sublist in X_train for item in sublist])
				y_train = np.array([item for sublist in y_train for item in sublist])
				X_test = np.array([item for sublist in X_test for item in sublist])
				y_test = np.array([item for sublist in y_test for item in sublist])
			#print X_train.shape, y_train.shape, X_test.shape, y_test.shape
			if(algo == 'svc'):
				clf = LinearSVC(C=p[params.keys().index('C')],
					penalty="l1", dual=False)				## Larger C increases model complexity
			if(algo=='kNN'):
				clf = KNeighborsClassifier(n_neighbors=p[params.keys().index('k')], 
					warn_on_equidistant=False, p=p[params.keys().index('p')])
			if(algo=='linearSVM'):
				clf = svm.SVC(kernel='linear', C=p[params.keys().index('C')])
			if(algo=='polySVM'):
				clf = svm.SVC(kernel='poly', degree = p[params.keys().index('degree')], 
					C=p[params.keys().index('C')])
			if(algo=='rbfSVM'):
				clf = svm.SVC(kernel='rbf', gamma = p[params.keys().index('gamma')], 
					C=p[params.keys().index('C')])			## a smaller gamma gives a decision boundary with a smoother curvature
			if(algo=='logit'):
				clf = LogisticRegression(penalty=p[params.keys().index('penalty')], dual=False, 
					C=p[params.keys().index('C')])
			clf.fit(X_train, y_train)
			score += clf.score(X_test, y_test)
		score /= k
		if(verbose):
 			print score
		if score>max:
			max = score
			max_params = p
			classifier = clf
	return max, max_params, classifier

def run_ml_analysis(X, y, feat, treatnames, featChoice='ads', nfeat=5, splittype='timed', splitfrac=0.1, 
		nfolds=10, blocked=1, ptest=1, verbose=False):				# main function, calls cross_validation, then runs chi2

	algos = {	
				'logit':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'penalty':['l1', 'l2']},
# 				'svc':{'C':np.logspace(-5.0, 15.0, num=21, base=2)}	
# 				'kNN':{'k':np.arange(1,20,2), 'p':[1,2,3]}, 
# 				'polySVM':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'degree':[1,2,3,4]},
# 				'rbfSVM':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'gamma':np.logspace(-15.0, 3.0, num=19, base=2)}

				
			}
	clf = train_and_test(algos, X, y, splittype, splitfrac, nfolds, blocked, ptest, verbose)
	print_top_features(X, y, feat, treatnames, clf, featChoice, nfeat, blocked)
