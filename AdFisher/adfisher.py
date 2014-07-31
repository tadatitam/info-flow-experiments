import sys, os
from datetime import datetime							# for getting times for computation

import experiment.alexa as alexa
import experiment.trials as trials
import experiment.shortlist as short

import analysis.converter as converter
import analysis.stat as stat
import analysis.ml as ml
import analysis.plot as plot

class Treatment:

	def __init__(self, name):
		self.name = name
		self.count=0
		self.str = "" 

	def visit_sites(self, file):
		if(self.count==0):
			self.str += "site|:|"+file
		else:
			self.str += "|+|site|:|"+file
		self.count += 1
	
	def opt_out(self):
		if(self.count==0):
			self.str += "optout|:|"
		else:
			self.str += "|+|optout|:|"
		self.count += 1	
		
	def opt_in(self):
		if(self.count==0):
			self.str += "optin|:|"
		else:
			self.str += "|+|optin|:|"
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
			self.str += "gender|:|"+gender
		else:
			self.str += "|+|gender|:|"+gender
		self.count += 1
	
	def set_age(self, age):
		if(age<18):
			print "Age under 18 cannot be set. Exiting."
			sys.exit(0)
		if(self.count==0):
			self.str += "age|:|"+str(age)
		else:
			self.str += "|+|age|:|"+str(age)
		self.count += 1
	
	def add_interest(self, interest='Auto'):
		if(self.count==0):
			self.str += "interest|:|"+interest
		else:
			self.str += "|+|interest|:|"+interest
		self.count += 1

	def remove_interest(self, interest='Auto'):
		if(self.count==0):
			self.str += "rinterest|:|"+interest
		else:
			self.str += "|+|rinterest|:|"+interest
		self.count += 1


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

def run_experiment(treatments, log_file="log.txt", blocks=20, samples=2, 
		runs=1, collection_site="toi", reloads=10, delay=5, browser="firefox", timeout=2000):	
	if(browser != "firefox" and browser != "chrome"):
		print "Illegal browser choice", browser
		return
	if(collection_site != "toi" and collection_site != "bbc" and 
		collection_site != "guardian" and collection_site != "reuters" and collection_site != "bloomberg"):
		print "Illegal collection_site ", collection_site
		return
	PATH="./"+log_file
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % log_file)
		if response == 'n':
			sys.exit(0)
	fo = open(log_file, "w")
	fo.close()
	print "Starting Experiment"
	trials.begin(log_file, samples, treatments, blocks, runs, collection_site, reloads, delay, browser, timeout)
	print "Experiment Complete"

def shortlist_sites(site_file, target_file, browser='firefox'):
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
		short.shortlist_sites(site, target_file)

def run_analysis(log_file="log.txt", splitfrac=0.1, nfolds=10, 
		feat_choice="ads", nfeat=5, verbose=False):
	if(feat_choice != "ads" and feat_choice != "words"):
		print "Illegal feat_choice", feat_choice
		return
	collection, names = converter.get_ads_from_log(log_file)
	collection = collection[:100]
# 	print stat.find_word_in_collection(collection, ['rehabilitation'])
	if len(collection) < nfolds:
		print "Too few blocks (%s). Analysis requires at least as many blocks as nfolds (%s)." % (len(collection), nfolds)
		return
# 	intX, inty, intFeat = converter.get_interest_vectors(collection)
# 	plot.treatment_feature_histogram(intX, inty, intFeat, names)
	s = datetime.now()
	X,y,feat = converter.get_feature_vectors(collection, feat_choice='ads')
	e = datetime.now()
	if(verbose):
		print "Time for constructing feature vectors: ", str(e-s)
		stat.print_counts(X,y)
	ml.run_ml_analysis(X, y, feat, names, feat_choice, nfeat, splitfrac=splitfrac, 
		nfolds=nfolds, verbose=verbose)
	
	
	
	
	
	
	
	