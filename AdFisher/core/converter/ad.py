import re                                       # regular expressions
from stemming.porter2 import stem               # for Porter Stemming 
import common
from datetime import datetime, timedelta            # to read timestamps reloadtimes
    
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

    def __init__(self, value, treatment_id, separator = '@|'):
        chunks = re.split(separator, value)
        self.time = datetime.strptime(chunks[0], "%Y-%m-%d %H:%M:%S.%f")
        self.title = chunks[1]
        self.url = chunks[2]
        self.body = chunks[3]
        self.label = treatment_id
        
#     def __init__(self, ad):
#         self.title = common.strip_tags(ad['Title'])
#         self.url = common.strip_tags(ad['URL'])
#         self.body = common.strip_tags(ad['Body'])
#         self.cat = ad['cat']
#         self.time = ad['Time']
    
    def ad_init(self, t, u, b, c, time, lbl):
        self.title = strip_tags(t)
        self.url = strip_tags(u)
        self.body = strip_tags(b)
        self.cat = c
        self.time = time
        self.label = lbl    
    
    
    def printStuff(self, coeff, C, c):
#       print "\multicolumn{1}{l}{", self.title, "; \url{", self.url, "}} & \multirow{2}{*}{", round(coeff, 3), 
#       print "} & \multirow{2}{*}{", a, "(", round(100.*a/(a+b), 1), "\%)} & \multirow{2}{*}{", b, "(", round(100.*b/(a+b), 1), "\%)}\\\\"
#       print "\multicolumn{1}{l}{", self.body, "}\\\\"
#       print "\hline"
        
#       print "\TitleParbox{", self.title, "; \url{", self.url, "}; ", self.body, "} & ",
#       print round(coeff, 3), " & ", a, "(", round(100.*a/(a+b), 1), "\%) & ", b, "(", round(100.*b/(a+b), 1), "\%) \\\\"
#       print "\hline \\\\"
        
#       print "\multirow{3}{*}{\TitleParbox{", self.title, "; \url{", self.url, "}; ", self.body, "}} & ",
#       print "\multirow{3}{*}{", round(coeff, 3), "} &\n", int(c[0]), " & ", int(c[1]), " & ", int(C[0]), "& ", int(C[1]), " \\\\"
#       print " & ", " & $", int(c[2]), "$ & $", int(c[3]), "$ & $", int(C[2]), "$ & $", int(C[3]), "$ \\\\"
#       print "\cline{3-6}"
#       print " & ", " & $", int(c[4]), "$ & $", int(c[5]), "$ & $", int(C[4]), "$ & $", int(C[5]), "$ \\\\"
#       print "\hline \\\\"
        
        print self.title, " & \url{", self.url, "} & $", round(coeff, 3), "$ & $", 
        print int(c[4]), "$ & $", int(c[5]), "$ & & $", int(C[4]), "$ & $", int(C[5]), "$ \\\\"
        

    
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
#                 print self.label,
#                 self.display()
#                 raw_input("h")
                return True
        return False
                    
    def ad_to_words(self):                          # returns a list of words from an ad
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
        
    def fit_to_feat(self, word_v, wchoice):         # fits an ad to a feature vector, returns a weight vector
        vec = []
        words = self.ad_to_words()
        stemmed_words = common.stem_low_wvec(words)
        words = common.strip_vec(words)
        # print words
        for word in word_v:
            if(wchoice == NUM):
                vec.append(float(words.count(word)))
            elif(wchoice == LOG_NUM):
                vec.append(math.log(float(words.count(word))))
        return vec
