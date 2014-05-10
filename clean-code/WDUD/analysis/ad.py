import re										# regular expressions
from stemming.porter2 import stem				# for Porter Stemming 
from nltk.corpus import stopwords 				# for removing stop-words
import common
	
########### CHOICES FOR THE AD-COMPARISON, AD-IDENTIFICATION #############

# Choices for what to uniquely identify an ad with
URL = 1
TITLE_URL = 2
TITLE_BODY = 3

# Choices for assigning weight to the vector
NUM = 1
LOG_NUM = 2

########### AD CLASS #############

class Ad:

	def __init__(self, ad):
		self.title = common.strip_tags(ad['Title'])
		self.url = common.strip_tags(ad['URL'])
		self.body = common.strip_tags(ad['Body'])
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
# 		print "\multicolumn{1}{l}{", self.title, "; \url{", self.url, "}} & \multirow{2}{*}{", round(coeff, 3), 
# 		print "} & \multirow{2}{*}{", a, "(", round(100.*a/(a+b), 1), "\%)} & \multirow{2}{*}{", b, "(", round(100.*b/(a+b), 1), "\%)}\\\\"
# 		print "\multicolumn{1}{l}{", self.body, "}\\\\"
# 		print "\hline"
		
		print "\TitleParbox{", self.title, "; \url{", self.url, "}; ", self.body, "} & ",
		print round(coeff, 3), " & ", a, "(", round(100.*a/(a+b), 1), "\%) & ", b, "(", round(100.*b/(a+b), 1), "\%) \\\\"
		print "\hline \\\\"

	
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
		stemmed_words = common.stem_low_wvec(words)
		words = common.strip_vec(words)
		# print words
		for word in word_v:
			if(choice == NUM):
				vec.append(float(words.count(word)))
			elif(choice == LOG_NUM):
				vec.append(math.log(float(words.count(word))))
		return vec