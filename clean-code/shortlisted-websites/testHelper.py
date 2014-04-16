import unittest, time, re
import sys
import math

# for chi2_contingency test, histograms
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta

# for Porter Stemming and removing stop-words
from stemming.porter2 import stem
from nltk.corpus import stopwords 

## feature selection
from sklearn.svm import LinearSVC
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import RandomizedLogisticRegression

## CV
from sklearn import cross_validation

## Classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression

# Permutation test
from itertools import combinations as comb
from itertools import product


########### CHOICES FOR THE AD-COMPARISON, AD-IDENTIFICATION #############

# Choices for what to uniquely identify an ad with
URL = 1
TITLE_URL = 2
TITLE_BODY = 3
CHOICE = URL

# Choices for measure of similarity
JACCARD = 1
COSINE = 2
SIM_CHOICE = COSINE

# Choices for assigning weight to the vector
NUM = 1
LOG_NUM = 2
SCALED_NUM = 3 # not implemented
W_CHOICE = NUM


########### HELPER CLASSES AND FUNCTIONS #############

#------------- for stripping html tags from html strings ---------------#

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#------------- to generate unique permutations ---------------#

class unique_element:
    def __init__(self,value,occurrences):
        self.value = value
        self.occurrences = occurrences

def perm_unique(elements):
    bins = np.bincount(elements)
    listunique = []
    for i in range(0,len(bins)):
    	listunique.append(unique_element(i, bins[i]))
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

#------------- to round off numbers ---------------#

def round_figures(x, n):
	"""Returns x rounded to n significant figures."""
	return round(x, int(n - math.ceil(math.log10(abs(x)))))

########### AD CLASS #############

class Ad:

	def __init__(self, ad):
		self.title = strip_tags(ad['Title'])
		self.url = strip_tags(ad['URL'])
		self.body = strip_tags(ad['Body'])
		self.cat = ad['cat']
		self.time = ad['Time']
		self.label = ad['label']
	
	def ad_init(self, t, u, b, c, time, lbl):
		self.title = strip_tags(t)
		self.url = strip_tags(u)
		self.body = strip_tags(b)
		self.cat = c
		self.time = time
		self.label = lbl
	
	def printStuff(self, coeff, a, b):
		print "\multicolumn{1}{l}{", self.title, "; \url{", self.url, "}} & \multirow{2}{*}{", round(coeff, 3), 
		print "} & \multirow{2}{*}{", a, "(", round(100.*a/(a+b), 1), "\%)} & \multirow{2}{*}{", b, "(", round(100.*b/(a+b), 1), "\%)}\\\\"
		print "\multicolumn{1}{l}{", self.body, "}\\\\"
		print "\hline"
	
	def display(self):
		print ("Title: "+self.title)
		print ("URL: "+self.url)
		print ("Body: "+self.body+"\n")
		
	def identical_ad(self, ad, choice):
		if(choice == URL):
			if(self.url == ad.url):
				return(True)
		elif(choice == TITLE_URL):
			if(self.url == ad.url and self.title == ad.title):
				return(True)
		elif(choice == TITLE_BODY):
			if(self.body == ad.body and self.title == ad.title):
				return(True)
		else:
			return(False)	
			
	def contains(self, nonces):
		for nonce in nonces:
			if (nonce in self.title.lower() or nonce in self.url.lower() or nonce in self.body.lower()):
				return True
		return False
					
	def ad_to_words(self):							# returns a list of words from an ad
		line = self.title+ " " + self.body
		list = re.split(r'[.(), !<>\/:=?;\-\n]+|', line)
		for i in range(0,len(list)):
			list[i] = list[i].replace('\xe2\x80\x8e', '')
			list[i] = list[i].replace('\xc2\xae', '') 
			list[i] = list[i].replace('\xe2\x84\xa2', '') 
			list[i] = list[i].replace('\xc3\xa9', '') 
			list[i] = list[i].replace('\xc3\xa1', '') 
		list = [x for x in list if len(x)>1]
		return list
		
	def fit_to_feat(self, word_v, choice):			# fits an ad to a feature vector, returns a weight vector
		vec = []
		words = self.ad_to_words()
		stemmed_words = stem_low_wvec(words)
		words = strip_vec(words)
		# print words
		for word in word_v:
			if(choice == NUM):
				vec.append(float(words.count(word)))
			elif(choice == LOG_NUM):
				vec.append(math.log(float(words.count(word))))
		return vec


########### AD VECTOR CLASS #############

class AdVec:

	def __init__(self):
		self.data = []
	
	def index(self, ad):
		return self.data.index(ad)
		
	def size(self):
		return len(self.data)
	
	def add_vec(self, ads):
		for ad in ads.data:
			self.add(ad)
	
	def add(self, ad):
		self.data.append(ad)
		
	def remove(self, ad):
		self.data.remove(ad)
		
	def display(self, choice):
		#print ("Total number of ads: "+str(len(self.data)))
		i = 0
		chunks = re.split("\+", choice)
		for ad in self.data:
			i += 1
			sys.stdout.write("%s " %i)
			if('url' in chunks):
				sys.stdout.write("%s " % ad.url)
			if('title' in chunks):
				sys.stdout.write("%s " % ad.title)
			if('body' in chunks):
				sys.stdout.write("%s " % ad.body)
			if('cat' in chunks):
				sys.stdout.write("%s " % ad.cat)
			if('time' in chunks):
				sys.stdout.write("%s " % ad.time)
			if('label' in chunks):
				sys.stdout.write("%s " % ad.label)
			print ""

	def choose_by_index(self, index):
		return self.data[index]
	
	def countLabels(self, lbl):
		c1=0
		for ad in self.data:
			if(ad.label == lbl):
				c1 += 1
		return c1
		
	def freq_contains(self, nonce):
		count = 0
		for ad in self.data:
			if(ad.contains(nonce)):
				count +=1
		return count
			
	def unique(self):
		uniq = AdVec()
		for ad in self.data:
			present = False
			for un_ad in uniq.data:
				if(ad.identical_ad(un_ad, CHOICE)):
					present = True
					break					
			if(not present):
				uniq.add(ad)
		return uniq
			
	def union(self, ads1):
		temp = AdVec()
		for ad in self.data:
			temp.add(ad)
		for ad in ads1.data:
			temp.add(ad)
		return temp.unique()
		
	def intersect(self, adsp1):					# without duplicates
		temp_int = AdVec()
		ads1 = AdVec()
		ads2 = AdVec()
		ads1.add_vec(self)						# making copies 
		ads2.add_vec(adsp1)						# making copies 
		for ad1 in ads1.data:
			present = False
			for ad2 in ads2.data:
				if(ad1.identical_ad(ad2, CHOICE)):
					present = True
					break
			if(present):
				temp_int.add(ad1)
				ads1.remove(ad1)
				ads2.remove(ad2)
		return temp_int.unique()

	def tot_intersect(self, adsp1):				# with duplicates
		ads1 = AdVec()
		ads2 = AdVec()
		ads1.add_vec(self)
		ads2.add_vec(adsp1)
		for ad1 in ads1.data:
			present = False
			for ad2 in ads2.data:
				if(ad1.identical_ad(ad2, CHOICE)):
					present = True
					break
			if(present):
				self.add(ad1)
				ads2.remove(ad2)
		return self
					
	def ad_weight(self, ad, wchoice):
		count = 0
		for a in self.data:
			if(a.identical_ad(ad, CHOICE)):
				count = count+1
		if(wchoice == NUM):
			return count
		elif(wchoice == LOG_NUM):
			if(count == 0):
				return 0
			else:
				return math.log(count)
		else:
			print("Illegal W_CHOICE")
			raw_input("Press Enter to exit")
			sys.exit()
		
	def gen_word_vec(self, word_v, choice):		# generates a vector of words from advec, fits it to word_v
		vec = []
		words = self.advec_to_words()
		stemmed_words = stem_low_wvec(words)
		words = strip_vec(words)
		# print words
		for word in word_v:
			if(choice == NUM):
				vec.append(float(words.count(word)))
			elif(choice == LOG_NUM):
				vec.append(math.log(float(words.count(word))))
		return vec
	
	def gen_ad_vec(self, ads):					# self is ad_union	# generates a vector of ads from advec
		vec = [0]*self.size()
		for ad in self.data:
			for lad in ads.data:
				if(ad.identical_ad(lad, CHOICE)):
					vec[self.index(ad)] += 1
		return vec	
		
	def gen_temp_ad_vec(self, ads):		# self is ad_union
		vec = [0]*ads.size()
		i = 0
		j = 0
		for ad in ads.data:
			for lad in self.data:
				if(self.same_ads(ad, lad)):
					vec[i] = self.index(lad)
			i += 1
		return vec				
	def advec_to_words(self):
		line = ""
		for ad in self.data:
			line = line + " " + ad.title+ " " + ad.body
		list = re.split(r'[.(), !<>\/:=?;\-\n]+|', line)
		for i in range(0,len(list)):
			list[i] = list[i].replace('\xe2\x80\x8e', '')
			list[i] = list[i].replace('\xc2\xae', '') 
			list[i] = list[i].replace('\xe2\x84\xa2', '') 
			list[i] = list[i].replace('\xc3\xa9', '') 
			list[i] = list[i].replace('\xc3\xa1', '') 
		list = [x for x in list if len(x)>1]
		return list
		
	def gen_ad_words_vec(self, feat):		# Creates a vector of word frequencies for each ad in advec
		vec = []
		for ad in self.data:
			vec.append(ad.fit_to_feat(feat))
		return vec

########### FUNCTIONS TO CARRY OUT ANALYSIS #############

#------------- for Ad Set Comparison ---------------#

def ad_sim(ads1, ads2):
	if(SIM_CHOICE == JACCARD):
		return jaccard_index(ads1, ads2)
	elif(SIM_CHOICE == COSINE):
		return ad_cosine_sim(ads1, ads2)
	else:
		print("Illegal SIM_CHOICE")
		raw_input("Press Enter to Exit")
		sys.exit()

def jaccard_index(ads1, ads2):
	ad_union = ads1.union(ads2)
	ad_int = ads1.intersect(ads2)
# 	ad_int.tot_intersect(ads1, ads2)
	return (float(ad_int.size())/float(ad_union.size()))

def ad_cosine_sim(ads1, ads2):
	ad_union = ads1.union(ads2)
	vec1 = []
	vec2 = []
	for ad in ad_union.data:
		vec1.append(ads1.ad_weight(ad, W_CHOICE))
		vec2.append(ads2.ad_weight(ad, W_CHOICE))
	return cosine_sim(vec1, vec2)
	

#------------- for Vector Operations ---------------#

def cosine_sim(vec1, vec2):		# cosine similarity of two vectors
	return (dot_prod(vec1, vec2)/(vec_mag(vec1)*vec_mag(vec2)))

def vec_mag(vec):				# magnitude of a vector
	sum = 0.0
	for i in vec:
		sum = sum + i*i
	return math.sqrt(sum)

def dot_prod(vec1, vec2):		# dot product of two vectors
	sum = 0.0
	if(len(vec1) != len(vec2)):
		print("Dot product doesnt exist")
		sys.exit()
	for i in range(0, len(vec1)):
		sum = sum + vec1[i]*vec2[i]
	return sum


#------------- to convert Ad Vectors to feature vectors ---------------#

def word_vectors(list):
	ad_union = AdVec()
	for ads in list:
		ad_union = ad_union.union(ads)
	words = ad_union.advec_to_words()
	stemmed_words = stem_low_wvec(words)
	filtered_words = [w for w in stemmed_words if not w in stopwords.words('english')]
	word_v = unique_words(filtered_words)
	word_v = strip_vec(word_v)
	wv_list = []
	labels = []
	for ads in list:
		wv_list.append(ads.gen_word_vec(word_v, W_CHOICE))
# 		labels.append(ads.choose_by_index(0).label)
	return wv_list, labels, word_v				## Returning word_v as feature

def ad_vectors(list):
	ad_union = AdVec()
	for ads in list:
		ad_union = ad_union.union(ads)
	av_list = []
	labels = []
	for ads in list:
		av_list.append(ad_union.gen_ad_vec(ads))
# 		labels.append(ads.choose_by_index(0).label)
	return av_list, labels, ad_union			## Returning entire ads as feature

def temp_ad_vectors(list):
	ad_union = AdVec()
	for ads in list:
		ad_union.union(ads, ad_union)
# 	ad_union.display('title')
	tav_list = []
	for ads in list:
		tav_list.append(ad_union.gen_temp_ad_vec(ads))
	return tav_list, ad_union

#------------- functions helping Word based analysis ---------------#

def stem_low_wvec(words):				# return stemmed and lower case words from the input list of words
	for i in range(0, len(words)):
		words[i] = stem(words[i]).lower()
	return words

def unique_words(words):				# returns a set of unique words from the input list of words
	unq = []
	for word in words:
		present = False
		for un in unq:
			if (un == word):
				present = True
				break
		if(not present):
			unq.append(word)
	return unq

def strip_vec(list):					# removes the blank '', digits, $, & words
	try:
		if(list[0] == ''):
			del list[-len(list)]
		if(list[len(list)-1] == ''):
			del list[-1]
	except:
		pass
	chars = set('0123456789$&')
	return [x for x in list if not (any((c in chars) for c in x))]


#------------- functions to plot figures ---------------#

def histogramPlots(list):
	a, b = ad_vectors(list)
	obs = np.array(a)
	l = []
	colors = ['b', 'r', 'g', 'm', 'k']							# Can plot upto 5 different colors
	for i in range(0, len(list)):
		l.append([int(i) for i in obs[i]])
	pos = np.arange(1, len(obs[0])+1)
	width = 0.5     # gives histogram aspect to the bar diagram
	gridLineWidth=0.1
	fig, ax = plt.subplots()
	ax.xaxis.grid(True, zorder=0)
	ax.yaxis.grid(True, zorder=0)
	for i in range(0, len(list)):
		lbl = "ads"+str(i)
		plt.bar(pos, l[i], width, color=colors[i], alpha=0.5, label = lbl)
	#plt.xticks(pos+width/2., obs[0], rotation='vertical')		# useful only for categories
	#plt.axis([-1, len(obs[2]), 0, len(ran1)/2+10])
	plt.legend()
	plt.show()
	
def temporalPlots(list):
	obs = np.array(temp_ad_vectors(list))
	#obs = np.array(ad_temp_category(list))
	print obs[0]
	dates = []
	colors = ['r.', 'b.', 'g.', 'm.', 'k.']
	for j in range(0, len(list)):
		dates.append(matplotlib.dates.date2num([list[j].data[i].time for i in range(0, len(list[j].data))]))
	pos = np.arange(len(obs[0]))
	gridLineWidth=0.1
	fig, ax = plt.subplots()
	ax.xaxis.grid(True, zorder=0)
	ax.yaxis.grid(True, zorder=0)
	for i in range(0, len(list)):
		lbl = "ads"+str(i)
		obs[i] = [j+1 for j in obs[i]]
		plt.plot(obs[i], dates[i], colors[i], alpha=0.5, label = lbl)
# 		plt.xticks(pos+width/2., obs[2], rotation='vertical')		# useful only for categories
	#plt.axis([-1, 500, 0, 700])
	plt.legend()
	plt.show()
	
#------------- functions for Statistics and Statistical Tests ---------------#

def stat_prc(adv, ass, keywords):				# prc statistic, which doesn't give very good results		
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

def stat_kw(adv, ass, keywords):				# keyword_diff based statistic
	advm, advf = vec_for_stats(adv, ass)
	return (advm.freq_contains(keywords) - advf.freq_contains(keywords))
	
def stat_sim(adv, ass, keywords):				# cosine similarity based statistic
	advm, advf = vec_for_stats(adv, ass)
	return -ad_sim(advm, advf)

def permutationTest(adv, ass, keywords, stat):
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


def vec_for_stats(adv, ass):					# aggregates the control group and experiment group into single ad vectors
	advm = AdVec()
	advf = AdVec()
	for i in range(0, len(adv)):
		if(str(i) in ass[0:len(ass)/2]):
			#print "c"+str(i)
			advm.add_vec(adv[i])
		else:
			#print "t"+str(i)
			advf.add_vec(adv[i])
	return (advm, advf)
	
def table_22(adv, ass, keywords):				# creates 2x2 contingency table using keywords
	advm, advf = vec_for_stats(adv, ass)
	kt = advm.freq_contains(keywords)
	ku = advf.freq_contains(keywords)
	nt = advm.size() - kt
	nu = advf.size() - ku
	return [kt, nt, ku, nu]

def testWrapper(adv, ass, keywords, type):
	if(not type == 'chi'):
		s = datetime.now()
		res = permutationTest(adv, ass, keywords, type)
		e = datetime.now()
	else:
		s = datetime.now()
		vec = table_22(adv, ass, keywords)
		chi2, p, dof, ex = stats.chi2_contingency(cont_table, correction=True)
		res = p
		e = datetime.now()
	return round_figures(res, 6), e-s
	
def printCounts(index, adv, ass):				# returns detailed counts of #ads within a round
	advm, advf = a.vec_for_stats(adv, ass)
	sys.stdout.write("%s\t AD_t size=%s uniq=%s, AD_u size=%s uniq=%s \n" %(index, advm.size(), 
							advm.unique().size(), advf.size(), advf.unique().size()))
	for i in range(0, INSTANCES):
		sys.stdout.write("%s \t" %(adv[i].size()))
	print("")

#------------- functions for Machine Learning Analyses ---------------#

def getVectorsFromRun(adv, ass, featChoice):			# returns observation vector from a round
	if featChoice == 'word':
		X, labels, feat = np.array(word_vectors(adv))
	elif featChoice == 'ad':
		X, labels, feat = np.array(ad_vectors(adv))
	y = [0]*len(ass)
	for i in ass[0:len(ass)/2]:
		y[int(i)] = 1
	print y
	X = np.array(X)
	y = np.array(y)
	return X, y, feat

def getVectorsFromExp(advdicts, featChoice):			# returns observation vector from a list of rounds
	n = len(advdicts[0]['ass'])
	list = []
	y = []
	for advdict in advdicts:
		list.extend(advdict['adv'])
	if(featChoice == 'words'):
		X, labels, feat = word_vectors(list)
	elif(featChoice == 'ads'):
		X, labels, feat = ad_vectors(list)
	for advdict in advdicts:
		ass = advdict['ass']
		y1 = [0]*len(ass)								# !! need to change this to set the label vector from labels in the ads
		for i in ass[0:len(ass)/2]:
			y1[int(i)] = 1
		y.extend(y1)
	X = [X[i:i+n] for i in range(0,len(X),n)]
	y = [y[i:i+n] for i in range(0,len(y),n)]
# 	print feat[0].title, feat[0].url
	return np.array(X), np.array(y), feat	

def trainTest(algos, X, y, splittype, splitfrac, nfolds, list, ptest, chi2, verbose=False):
	
	### Split data into training and testing data based on splittype

	if(splittype == 'rand'):
		rs1 = cross_validation.ShuffleSplit(len(X), n_iter=1, test_size=splitfrac)
		for train, test in rs1:
			if(verbose):
				print test, train
			X_train, y_train, X_test, y_test = X[train], y[train], X[test], y[test]
	elif(splittype == 'timed'):
		split = int((1.-splitfrac)*len(X))
		X_train, y_train, X_test, y_test = X[:split], y[:split], X[split:], y[split:]
	else:
		raw_input("Split type ERROR")	
		
	### Model selection via cross-validation from training data
	
	max_score = 0
	for algo in algos.keys():
		score, mPar, clf = crossVal_algo(nfolds, algo, algos[algo], X_train, y_train, splittype, splitfrac, list)
		if(verbose):
			print score, mPar, clf
		if(score > max_score):
			max_clf = clf
			max_score = score
	if(verbose):
		print max_score, max_clf, max_clf.coef_.shape
	if(ptest==1):
		oXtest, oytest = X_test, y_test	
	if(list==1):
		X_test = np.array([item for sublist in X_test for item in sublist])
		y_test = np.array([item for sublist in y_test for item in sublist])	
		X_train = np.array([item for sublist in X_train for item in sublist])
		y_train = np.array([item for sublist in y_train for item in sublist])
		
	### Fit model to training data and compute test accuracy
	
	np.set_printoptions(threshold=sys.maxint)
	max_clf.fit(X_train, y_train)
# 	print "test-score: ", max_clf.score(X_test, y_test)
	print max_clf.score(X_test, y_test)
	if(ptest==1):
		for i in range(0,len(oXtest)):
			print MLpTest(oXtest[i], oytest[i], clf)
	
	if(chi2==1):
		cont_table = genContTable(X_test, y_test, max_clf)
		print cont_table
		chi2, p, dof, ex = stats.chi2_contingency(cont_table, correction=True)
		print chi2, p, dof, ex
		print ("Chi-Square = "+str(chi2))
		print ("p-value = "+str(p))
			
	return max_clf

def featureSelection(X,y,feat,featChoice,splittype,splitfrac,nfolds,nfeat,list):

	algos = {	
				'logit':{'C':np.logspace(-5.0, 15.0, num=1, base=2), 'penalty':['l1']},
# 				'svc':{'C':np.logspace(-5.0, 15.0, num=21, base=2)}		
			}

	clf = trainTest(algos, X, y, splittype, splitfrac, nfolds, list, ptest=0, chi2=0)
	
	printTopKFeatures(X, y, feat, featChoice, clf, nfeat, list)
	for k in range(1, 50):
		topk1 = np.argsort(clf.coef_[0])[::-1][:k]
		topk0 = np.argsort(clf.coef_[0])[:k]
		kX = X[:,:,np.append(topk1,topk0)]
		print k, "\t", 
		CVPtest(kX, y, feat, splittype, splitfrac, nfolds, list, ptest=0, chi2=0)
# 	varyingK(X_train, y_train, X_test, y_test, max_clf)


def CVPtest(X, y, feat, splittype, splitfrac, nfolds, list, ptest=1, chi2=1):				# main function, calls cross_validation, then runs chi2

	algos = {	
				'logit':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'penalty':['l1', 'l2']},
# 				'kNN':{'k':np.arange(1,20,2), 'p':[1,2,3]}, 
# 				'polySVM':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'degree':[1,2,3,4]},
# 				'rbfSVM':{'C':np.logspace(-5.0, 15.0, num=21, base=2), 'gamma':np.logspace(-15.0, 3.0, num=19, base=2)}
				
			}
	clf = trainTest(algos, X, y, splittype, splitfrac, nfolds, list, ptest=ptest, chi2=chi2)


def printTopKFeatures(X, y, feat, featChoice, max_clf, k, list):		# prints top k features from max_clf+some numbers
	if(list==1):
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
		print "\nFeatures for class 1:"
		for i in topk1:
			if(featChoice == 'ads'):
				feat.choose_by_index(i).printStuff(max_clf.coef_[0][i], A[i], B[i])
			elif(featChoice == 'words'):
				print feat[i]
		topk0 = np.argsort(max_clf.coef_[0])[:k]
		print "\n\nFeatures for class 0:"
		for i in topk0:
			if(featChoice == 'ads'):
				feat.choose_by_index(i).printStuff(max_clf.coef_[0][i], A[i], B[i])
			elif(featChoice == 'words'):
				print feat[i]
	else:
		for i in range(0,n_classes):
			topk = np.argsort(max_clf.coef_[i])[::-1][:k]
			print "Features for class %s:" %(i+1)
			for j in topk:
				if(featChoice == 'ads'):
					feat.choose_by_index(j).display()
				elif(featChoice == 'words'):
					print feat[j]
			print "coefs: ", max_clf.coef_[i][topk]
	

def crossVal_algo(k, algo, params, X, y, splittype, splitfrac, list, verbose=False):				# performs cross_validation
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
			if(list==1):
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

def stat_ML(X_test, y_test, clf):
	g1 = [X_test[i] for i in range(0,len(X_test)) if y_test[i]==1]
	g2 = [X_test[i] for i in range(0,len(X_test)) if y_test[i]==0]		# CAn REduce RUN TIME by 50%!!!
	return sum(clf.predict(g1)) - sum(clf.predict(g2))

def MLpTest(X_test, y_test, clf):									# permutation test
	Tobs = stat_ML(X_test, y_test, clf)
# 	print Tobs
	under = 0
	a = list(perm_unique(y_test))
	for new_y_test in a:
		Tpi = stat_ML(X_test, np.array(new_y_test), clf)			# No need to compute this. prediction X_test doesnt change
# 		print new_y_test
# 		print "Tpi="+str(Tpi)
		if round(Tobs, 10) <= round(Tpi, 10):
			under += 1
	return (1.0*under) / (1.0*len(a))

def genContTable(X, y, clf):										# generates contingency table
	try:
		n_classes = clf.coef_.shape[0]								# for linear classifiers
	except:
		n_classes = clf.dual_coef_.shape[0]							# for rbf classifiers
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

def MLAnalysis(par_adv):
	featChoice = 'ads'
	splitfrac = 0.1
	splittype = 'timed' #'timed'/'rand'
	X,y,feat = getVectorsFromExp(par_adv, featChoice)
	print X.shape
	print sum(sum(sum(X)))
	print y.shape
	ua,uind=np.unique(y,return_inverse=True)
	count=np.bincount(uind)
	print ua, count
	featureSelection(X,y,feat,featChoice,splittype,splitfrac,nfolds=10,nfeat=5,list=1)
	print "CVPtest"
	CVPtest(X, y, feat, splittype, splitfrac, nfolds=10, list=1)
	
