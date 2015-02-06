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

# eventually move these:
import numpy as np										# eventually move it
from scipy import spatial								# for computing cosine_distance
import itertools 										# for combinations of attributes


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
		
	def login_to_google(self, username, password):
		if(self.count==0):
			self.str += "login||"+username+"||"+password
		else:
			self.str += "|+|login||"+username+"||"+password
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
		
	def set_language(self, language):
# 		if(age<18):
# 			print "Age under 18 cannot be set. Exiting."
# 			sys.exit(0)
		if(self.count==0):
			self.str += "language||"+str(language)
		else:
			self.str += "|+|language||"+str(language)
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
	
# 	feat.display("title+url")
# 	raw_input("wait")
	
	print X.shape, y.shape
	out = np.array([[0.]*X.shape[2]]*len(names))
	print out.shape
	
	samples=1
	attributes = {'gender':["male","female"], 'age':[18,35,55], 'language':["English", "Spanish"]}
	for key, value in attributes.items():
		samples = samples*len(value)
	
	if not(samples == len(names)):
		raw_input("samples != len(names)")
	
	for i in range(0, X.shape[0]):
		for j in range(0, X.shape[1]):
			out[j] = out[j] + X[i][np.where(y[i]==j)]
	print out
	
	print "Total ads: ", np.sum(out)
	
	total = np.sum(out, axis=0)
	
# 	sortt = np.sort(total)
# 	import matplotlib.pyplot as plt
# 	import matplotlib.dates as mdates
# 	import matplotlib
# 	for t in out:
# 		sortt = np.sort(t)
# 		colors = ['b', 'r', 'g', 'm', 'k', 'b', 'r', 'g', 'm', 'k']							# Can plot upto 5 different colors
# 		pos = np.arange(1, len(out[0])+1)
# 		width = 0.5     # gives histogram aspect to the bar diagram
# 		gridLineWidth=0.1
# 		fig, ax = plt.subplots()
# 		ax.xaxis.grid(True, zorder=0)
# 		ax.yaxis.grid(True, zorder=0)
# 		plt.bar(pos, sortt, width, color=colors[0], alpha=0.5)
# 		plt.legend()
# 		plt.show()
	
	print total
# 	feat.display("url+title")
# 	raw_input("wait")
	removal = np.where(total < 100)[0]				# parameter
	out = np.delete(out,removal,axis=1)
	feat.delete(removal)
	feat.display("url+title")
	raw_input("wait")
# 			out[:,i] = 0
# 	print out
	
	
	def removekey(d, key):
		r = dict(d)
		del r[key]
		return r
	
	def normalize(vector):
		diff = max(vector) - min(vector)
		print diff
		return (vector - min(vector))/diff
	
	def normalize_max(out):
		print out
		max = np.amax(out, axis=0)
		z = out/max
		print z
		raw_input("norm")
		return z
		
	def normalize_uni(out):
		print out
		max = np.amax(out, axis=0)
		min = np.amin(out, axis=0)
		print max
		print min
		z = (out-min)/(max-min)
		print z
		raw_input("norm")
		return z
		
	def compute_influence(attributes, vector):
		print vector
		influences = []
		for key, value in attributes.items():			# for i
			print key, value
			print "Computing ", key, " influence"
			sum = np.array([0.]*vector.shape[1])
			num = 0
			copy = removekey(attributes, key)
# 			print attributes
# 			print copy
			for attrcomp in list(itertools.combinations(attributes[key], 2)):		# for b
# 				print attrcomp
				for comb in list(itertools.product(*copy.values())):
					name0=''
					name1=''
					for idx, val in enumerate(comb):
						if(idx == attributes.keys().index(key)):
							name0 = name0+str(attrcomp[0])
							name1 = name1+str(attrcomp[1])
						name0 = name0+str(val)
						name1 = name1+str(val)
					if(attributes.keys().index(key) == len(copy)):
						name0 = name0+str(attrcomp[0])
						name1 = name1+str(attrcomp[1])
# 					print name0, "vs", name1
# 					print names.index(name0), "vs", names.index(name1)
					num += 1
# 					distance = spatial.distance.cosine(out[names.index(name0)],out[names.index(name1)])		# can use any distance function
					distance = abs(vector[names.index(name0)] - vector[names.index(name1)])
					sum += distance
# 					print distance
# 					raw_input("distance")
# 					print out[names.index(name0)]
# 					print out[names.index(name1)]
# 			print sum
# 			print num
			influence = sum/num
			print influence
# 			normed = normalize(influence)
# 			print normed
# 			influences.append(normed)
			influences.append(influence)
			raw_input("wait")
		return np.array(influences)
		
	def get_max_diffs(influences):
		diffs = []
		for i in range(0, len(influences)):
			rem = np.delete(influences, i, axis=0)
			max = np.amax(rem, axis=0)
			diffs.append(influences[i] - max)
		return diffs
	
	
	norm_out = normalize_max(out)
	influences = compute_influence(attributes, norm_out)
	
	diffs = get_max_diffs(influences)
	
	
	# remove
	diffs = influences
	
# 	raw_input("wait")
# # 	total = out[0]+out[1]+out[2]+out[3]+out[4]+out[5]
# # 	print total
# # 	raw_input("wait")
# 	print "Computing gender influence"
# 	diff = (abs(out[0] - out[3]) + abs(out[1] - out[4]) + abs(out[2] - out[5]))/3# /total
# # 	for i in range(0,len(total)):
# # 		diff[i] = diff[i]*1.0/total[i]
# 	print diff
# 	
# 	print "Computing age influence"
# 	diff2 = (abs(out[0] - out[1]) + abs(out[1] - out[2]) + abs(out[2] - out[0]) + abs(out[3] - out[4]) + abs(out[4] - out[5]) + abs(out[5] - out[3]))/6 #/total
# 	print diff2
# 	
# 	male = out[0]+out[1]+out[2]
# 	female = out[3]+out[4]+out[5]
# 	print "-------"
# 	print male
# 	print female
# 	print "-------"
# 	print "total ads:", out.sum()
# 	print "Computing age influence"
# 	diff = abs(out[0] - out[3]) + abs(out[1] - out[4]) + abs(out[2] - out[5])
# 	print diff
# 	feat.display("url+title")
	for diff in diffs:
		print "-----------------------------"
		sortdiff = np.sort(diff)
		sortdiff = sortdiff[::-1]
# 		print sortdiff
		count = 0
		for i in sortdiff:
			if(i<=0):
				break
# 			print "out:-----", i
	# 		print np.where(diff==i)
			for j in np.where(diff==i)[0]:
				count += 1
# 				print "index:", j, "diff:", i, "---", 
				print "infl:", i
# 				print "m:", male[j], "f:", female[j]
				feat.choose_by_index(j).display()
				print out[:,j]
# 				print norm_out[:,j]
			if count > 10:
				break;
			
# 	X2 = np.array([[[0.]*X.shape[2]]*2]*X.shape[0])
# 	y2 = np.array([[0]*2]*y.shape[0])
# 	print X.shape, 
# 	print X2.shape
# 	names2 = ['m18', 'f35']
# 	
# 	for i in range(0, X.shape[0]):
# 		k = np.where(y[i]%4==0)
# 		X2[i] = X[i][k]
# 		y2[i] = y[i][k]/4
# 		
# # 	print X2
# # 	print y2
# # 	print X2.shape, y2.shape
# # 	raw_input("wait")
# 	ml.run_ml_analysis(X2, y2, feat, names2, feat_choice="ads", nfeat=5, splitfrac=0.1, 
# 		nfolds=10, verbose=False)
	

def analyze_news(log_file="log.txt", splitfrac=0.1, nfolds=10, 
		feat_choice="ads", nfeat=5, verbose=True):
	collection, names = converter.read_log(log_file)	
	print len(collection)	
	collection = collection[:50]
	
	X,y,feat = converter.get_news_vectors(collection)
	print X.shape
	print y.shape
	out = np.array([[0.]*X.shape[2]]*len(names))
	print out.shape
	for i in range(0, X.shape[0]):
# 		print "i:", i
# 		print X[i]
# 		print y[i]
		for j in range(0, len(names)):
# 			print "j:", j
			out[j] = out[j] + X[i][np.where(y[i]==j)].sum(axis=0)
# 			print out[j]
# 			raw_input("wait")
			
	
	print sum(out[0])
	print sum(out[1])
	raw_input("Sums")
	import matplotlib.pyplot as plt
	import matplotlib.dates as mdates
	import matplotlib
	sortt1 = np.sort(out[0])
	inds = out[0].argsort()
	sortt2 = out[1][inds]
	colors = ['b.', 'r.', 'g.', 'm.', 'k.', 'b.', 'r.', 'g.', 'm.', 'k.']							# Can plot upto 5 different colors
	pos = np.arange(1, len(out[0])+1)
	width = 0.5     # gives histogram aspect to the bar diagram
	gridLineWidth=0.1
	fig, ax = plt.subplots()
	ax.xaxis.grid(True, zorder=0)
	ax.yaxis.grid(True, zorder=0)
	plt.plot(pos, sortt1, colors[0], width, alpha=0.5, label = names[0])
	plt.plot(pos, sortt2, colors[1], width, alpha=0.5, label = names[1])
	#plt.xticks(pos+width/2., obs[0], rotation='vertical')		# useful only for categories
	#plt.axis([-1, len(obs[2]), 0, len(ran1)/2+10])
# 	plt.legend()
	plt.show()

	sortt1 = np.sort(out[1])
	inds = out[1].argsort()
	sortt2 = out[0][inds]
	colors = ['b.', 'r.', 'g.', 'm.', 'k.', 'b.', 'r.', 'g.', 'm.', 'k.']							# Can plot upto 5 different colors
	pos = np.arange(1, len(out[0])+1)
	width = 0.5     # gives histogram aspect to the bar diagram
	gridLineWidth=0.1
	fig, ax = plt.subplots()
	ax.xaxis.grid(True, zorder=0)
	ax.yaxis.grid(True, zorder=0)
	plt.plot(pos, sortt1, colors[1], width, alpha=0.5, label = names[0])
	plt.plot(pos, sortt2, colors[0], width, alpha=0.5, label = names[1])
	#plt.xticks(pos+width/2., obs[0], rotation='vertical')		# useful only for categories
	#plt.axis([-1, len(obs[2]), 0, len(ran1)/2+10])
# 	plt.legend()
	plt.show()	
		
# 	print collection[0]['ass']
	print names
	s = datetime.now()
	X,y,feat = converter.get_news_vectors(collection)
	print X.shape
	print y.shape
	e = datetime.now()
	if(verbose):
		print "Time for constructing feature vectors: ", str(e-s)
		stat.print_counts(X,y)
	ml.run_ml_analysis(X, y, feat, names, feat_choice, nfeat, splitfrac=splitfrac, 
		nfolds=nfolds, verbose=verbose)
		
# 	index = feat.get_indices("USA TODAY")
# 	raw_input("wait")
# 	print X
# 	print X.shape
# 	newX = X[:,:,index]
# 	print newX
# 	print newX.shape
# 	print y
# 	print stat.block_p_test_mode2(newX, y, flipped=True, iterations=10000)
# 	print stat.block_p_test_cosine(X, y, iterations=10000)
# 	print "done"
# 	plot.temporalPlots(collection[0]['newsv'], names)
# # 	plot.histogramPlots(collection[0]['newsv'], names)

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
	
	
	
	
	
	
	