import sys, os
from datetime import datetime							# for getting times for computation

import experiment.alexa as alexa
import experiment.planner as planner
import experiment.trials as trials
import experiment.shortlist as short

import analysis.converter as converter
import analysis.stat as stat
import analysis.ml as ml
import analysis.plot as plot

import numpy as np										# eventually move it

class Treatment:

	def __init__(self, name):
		self.name = name
		self.count=0
		self.str = "" 

	def visit_sites_on_msn(self, link):
		if(self.count==0):
			self.str += "msn||"+link
		else:
			self.str += "|+|msn||"+link
		self.count += 1
		
	def visit_sites(self, file):
		if(self.count==0):
			self.str += "site||"+file
		else:
			self.str += "|+|site||"+file
		self.count += 1
	
	def opt_out(self):
		if(self.count==0):
			self.str += "optout||"
		else:
			self.str += "|+|optout||"
		self.count += 1	
		
	def opt_in(self):
		if(self.count==0):
			self.str += "optin||"
		else:
			self.str += "|+|optin||"
		self.count += 1
		
	def set_gender(self, gender='m'):
		if (gender.lower()=='m' or gender.lower()=='male'):
			gender = 'm'
		elif (gender.lower()=='f' or gender.lower()=='female'):
			gender = 'f'
		else:
			print "Gender option not available. Exiting."
			sys.exit(0)
		if(self.count==0):
			self.str += "gender||"+gender
		else:
			self.str += "|+|gender||"+gender
		self.count += 1
	
	def set_age(self, age):
		if(age<18):
			print "Age under 18 cannot be set. Exiting."
			sys.exit(0)
		if(self.count==0):
			self.str += "age||"+str(age)
		else:
			self.str += "|+|age||"+str(age)
		self.count += 1
	
	def add_interest(self, interest='Auto'):
		if(self.count==0):
			self.str += "interest||"+interest
		else:
			self.str += "|+|interest||"+interest
		self.count += 1

	def remove_interest(self, interest='Auto'):
		if(self.count==0):
			self.str += "rinterest||"+interest
		else:
			self.str += "|+|rinterest||"+interest
		self.count += 1
		
	def read_articles(self, keyword="Fox News", count=5):
		if(self.count==0):
			self.str += "readnews||"+keyword+"||"+str(count)
		else:
			self.str += "|+|readnews||"+keyword+"||"+str(count)
		self.count += 1
	

class Measurement:

	def __init__(self):
		self.count=0
		self.str = "" 
		
	def get_age(self):
		if(self.count==0):
			self.str += "age"
		else:
			self.str += "+age"
		self.count += 1
		
	def get_gender(self):
		if(self.count==0):
			self.str += "gender"
		else:
			self.str += "+gender"
		self.count += 1
			
	def get_language(self):
		if(self.count==0):
			self.str += "language"
		else:
			self.str += "+language"
		self.count += 1
		
	def get_interests(self):
		if(self.count==0):
			self.str += "interests"
		else:
			self.str += "+interests"
		self.count += 1		
		
	def get_ads(self, site='toi', reloads=10, delay=5):
		if(site != "toi" and site != "bbc" and site != "fox" and
		site != "guardian" and site != "reuters" and site != "bloomberg"):
			print "Illegal collection_site ", collection_site, ". Exiting."
			sys.exit(0)
		if(self.count==0):
			self.str += "ads||"+site+"||"+str(reloads)+"||"+str(delay)
		else:
			self.str += "+ads||"+site+"||"+str(reloads)+"||"+str(delay)
		self.count += 1
				
	def get_bing_ads(self, term, reloads=10, delay=5):
		if(self.count==0):
			self.str += "bads||"+term+"||"+str(reloads)+"||"+str(delay)
		else:
			self.str += "+bads||"+term+"||"+str(reloads)+"||"+str(delay)
		self.count += 1	
					
	def get_news(self, type, reloads=10, delay=5):
		if(self.count==0):
			self.str += "news||"+type+"||"+str(reloads)+"||"+str(delay)
		else:
			self.str += "+news||"+type+"||"+str(reloads)+"||"+str(delay)
		self.count += 1

def collect_sites_from_display_planner(words="Depression", 
		output_file="depression.txt", nsites=100, browser="firefox"):
	if(browser != "firefox" and browser != "chrome"):
		print "Illegal browser choice", browser
		return
	PATH="./"+output_file
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % output_file)
		if response == 'n':
			sys.exit(0)
	fo = open(output_file, "w")
	fo.close()
	print "Beginning Collection"
# 	os.system("python experimenter/alexa.py %s %s %s" % (output_file, alexa_link, n))
	planner.run_script(words, output_file, nsites, browser)
	print "Collection Complete. Results stored in ", output_file

def collect_sites_from_alexa(alexa_link="http://www.alexa.com/topsites", 
		output_file="out.txt", nsites=5, browser="firefox"):
	if(browser != "firefox" and browser != "chrome"):
		print "Illegal browser choice", browser
		return
	PATH="./"+output_file
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % output_file)
		if response == 'n':
			sys.exit(0)
	fo = open(output_file, "w")
	fo.close()
	print "Beginning Collection"
# 	os.system("python experimenter/alexa.py %s %s %s" % (output_file, alexa_link, n))
	alexa.run_script(alexa_link, output_file, nsites, browser)
	print "Collection Complete. Results stored in ", output_file

def run_experiment(treatments, measurement, log_file="log.txt", blocks=20, agents=2, 
		runs=1, browser="firefox", timeout=700):	
	if(browser != "firefox" and browser != "chrome"):
		print "Illegal browser choice", browser
		return
	PATH="./"+log_file
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % log_file)
		if response == 'n':
			sys.exit(0)
	fo = open(log_file, "w")
	fo.close()
	print "Starting Experiment"
	trials.begin(treatments=treatments, measurement=measurement, 
		agents=agents, blocks=blocks, runs=runs, browser=browser, timeout=timeout, log_file=log_file)
	print "Experiment Complete"

def shortlist_sites(site_file, target_file, browser='firefox', timeout=100):
	PATH="./"+target_file
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % target_file)
		if response == 'n':
			sys.exit(0)
	fo = open(target_file, "w")
	fo.close()
	fo = open(site_file, "r")
	for line in fo:
		site = line.strip()
		short.shortlist_sites(site, target_file, timeout=timeout)

def compute_influence(log_file="log.txt"):							## eventually move it to analysis
	collection, names = converter.read_log(log_file)
	print names
# 	collection = collection[:1]
	X,y,feat = converter.get_feature_vectors(collection, feat_choice='ads')
	print X.shape, y.shape
	out = np.array([[0]*X.shape[2]]*len(names))
	print out.shape
	for i in range(0, X.shape[0]):
		for j in range(0, X.shape[1]):
			out[j] = out[j] + X[i][np.where(y[i]==j)]
# 	print out
	print "Computing gender influence"
	diff = abs(out[0] - out[3]) + abs(out[1] - out[4]) + abs(out[2] - out[5])
	print diff
	
	male = out[0]+out[1]+out[2]
	female = out[3]+out[4]+out[5]
	print "-------"
	print out
	print "-------"
	print male
	print female
	print "-------"
	print "total ads:", out.sum()
# 	print "Computing age influence"
# 	diff = abs(out[0] - out[3]) + abs(out[1] - out[4]) + abs(out[2] - out[5])
# 	print diff
# 	feat.display("url+title")
	sortdiff = np.sort(diff)
	sortdiff = sortdiff[::-1]
	print sortdiff
	count = 0
	for i in sortdiff:
		print "out:-----", i
# 		print np.where(diff==i)
		for j in np.where(diff==i)[0]:
			count += 1
			print "index:", j, "infl:", i, "---", 
			print "m:", male[j], "f:", female[j]
			print out[0][j], out[1][j], out[2][j], out[3][j], out[4][j], out[5][j]
			feat.choose_by_index(j).display()
		if count > 20:
			break;
# 	print y
# 	print names
# 	y2 = y/3
# 	names2 = ['male', 'female']
# 	ml.run_ml_analysis(X, y2, feat, names2, feat_choice="ads", nfeat=5, splitfrac=0.1, 
# 		nfolds=10, verbose=False)
	

def analyze_news(log_file="log.txt"):
	collection, names = converter.read_log(log_file)	
	print len(collection)
# 	print collection[0]['news']
	print names
	plot.temporalPlots(collection[0]['newsv'])

def run_ml_analysis(log_file="log.txt", splitfrac=0.1, nfolds=10, 
		feat_choice="ads", nfeat=5, verbose=False):
	if(feat_choice != "ads" and feat_choice != "words"):
		print "Illegal feat_choice", feat_choice
		return
	collection, names = converter.read_log(log_file)	
# 	collection = collection[:100]
# 	print collection[0]['adv']
# 	plot.temporalPlots(collection[0]['adv'][0:1])
# 	raw_input("wait")
	if len(collection) < nfolds:
		print "Too few blocks (%s). Analysis requires at least as many blocks as nfolds (%s)." % (len(collection), nfolds)
		return
# 	intX, inty, intFeat = converter.get_interest_vectors(collection)
# 	plot.treatment_feature_histogram(intX, inty, intFeat, names)
	s = datetime.now()
	X,y,feat = converter.get_feature_vectors(collection, feat_choice='ads')
	print X.shape
	print y.shape
	e = datetime.now()
	if(verbose):
		print "Time for constructing feature vectors: ", str(e-s)
		stat.print_counts(X,y)
	ml.run_ml_analysis(X, y, feat, names, feat_choice, nfeat, splitfrac=splitfrac, 
		nfolds=nfolds, verbose=verbose)

def run_kw_analysis(log_file="log.txt", keywords=[], flipped=False, verbose=False):	
	collection, names = converter.read_log(log_file)
	print stat.find_word_in_collection(collection, keywords)
	X,y = converter.get_keyword_vectors(collection, keywords)
	s = datetime.now()
	print "p-value:"
	print stat.block_p_test_mode2(X, y, flipped=flipped, iterations=10000)
	e = datetime.now()
	if(verbose):
		print "Time for permutation test: ", str(e-s)
	
	
	
	
	
	
	