import re, sys                                      # regular expressions
from stemming.porter2 import stem               # for Porter Stemming 
import common
from datetime import datetime, timedelta            # to read timestamps reloadtimes
    
########### CHOICES FOR THE NEWS-COMPARISON, NEWS-IDENTIFICATION #############

# Choices for what to uniquely identify a news with
AGENCY = 1
TITLE_AGENCY = 2
TITLE_BODY = 3
TITLE_HEADING = 4
CHOICE = TITLE_AGENCY

# Choices for measure of similarity
JACCARD = 1
COSINE = 2
SIM_CHOICE = COSINE

# Choices for assigning weight to the vector
NUM = 1
LOG_NUM = 2
SCALED_NUM = 3 # not implemented
W_CHOICE = NUM

########### NEWS CLASS #############

class News:
    
    def __init__(self, value, treatment_id, separator = '@|'):
        chunks = re.split(separator, value)
        self.time = datetime.strptime(chunks[0], "%Y-%m-%d %H:%M:%S.%f")
        self.heading = chunks[1]
        self.title = chunks[2]
        self.agency = chunks[3]
        self.ago = chunks[4]
        self.body = chunks[5]
        self.label = treatment_id
    
#     def __init__(self, news):
#         self.title = common.strip_tags(news['Title'])
#         self.agency = common.strip_tags(news['Agency'])
#         self.ago = common.strip_tags(news['Ago'])
#         self.body = common.strip_tags(news['Body'])
#         self.time = news['Time']
#         self.label = news['Label']
    
    
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
        
        print self.title, " & ", self.agency, " & $", round(coeff, 3), "$ & $", 
        print int(c[4]), "$ & $", int(c[5]), "$ & & $", int(C[4]), "$ & $", int(C[5]), "$ \\\\"
    def display(self):
        print ("Title: "+self.title)
        print ("Agency: "+self.agency)
        print ("Body: "+self.body+"\n")
        
    def identical_news(self, news, choice):
        if(choice == AGENCY):
            if(self.agency == news.agency):
                return(True)
        elif(choice == TITLE_AGENCY):
            if(self.agency == news.agency and self.title == news.title):
                return(True)
        elif(choice == TITLE_BODY):
            if(self.body == news.body and self.title == news.title):
                return(True)
        elif(choice == TITLE_HEADING):
            if(self.heading == news.heading and self.title == news.title):
                return(True)
        else:
            return(False)   
            
    def contains(self, nonces):
        for nonce in nonces:
            if (nonce in self.title.lower() or nonce in self.agency.lower() or nonce in self.body.lower()):
                return True
        return False
                    
    def news_to_words(self):                            # returns a list of words from an news
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
        
    def fit_to_feat(self, word_v, wchoice):         # fits an news to a feature vector, returns a weight vector
        vec = []
        words = self.news_to_words()
        stemmed_words = common.stem_low_wvec(words)
        words = common.strip_vec(words)
        # print words
        for word in word_v:
            if(wchoice == NUM):
                vec.append(float(words.count(word)))
            elif(wchoice == LOG_NUM):
                vec.append(math.log(float(words.count(word))))
        return vec

########### NEWSVECTOR CLASS #############

class NewsVector:


    def __init__(self):
        self.data = []
        self.label = -1
    
    def setLabel(self, lbl):
        self.label = lbl
        
    def index(self, news):
        return self.data.index(news)
        
    def size(self):
        return len(self.data)
    
    def add_vec(self, newsv):
        for news in newsv.data:
            self.add(news)
    
    def add(self, news):
        self.data.append(news)
        
    def remove(self, news):
        self.data.remove(news)
        
    def get_indices(self, keyword):     # special purpose use
        indices = []
        for news in self.data:
            if(news.agency == keyword):
                indices.append(self.index(news))
        return indices
    
    def display(self, choice):
        #print ("Total number of newss: "+str(len(self.data)))
        i = 0
        chunks = re.split("\+", choice)
        for news in self.data:
            i += 1
            sys.stdout.write("%s " %i)
            if('agency' in chunks):
                sys.stdout.write("%s " % news.agency)
            if('title' in chunks):
                sys.stdout.write("%s " % news.title)
            if('body' in chunks):
                sys.stdout.write("%s " % news.body)
            if('ago' in chunks):
                sys.stdout.write("%s " % news.ago)
            if('time' in chunks):
                sys.stdout.write("%s " % news.time)
            if('label' in chunks):
                sys.stdout.write("%s " % news.label)
            print ""

    def choose_by_index(self, index):
        return self.data[index]
    
    def countLabels(self, lbl):
        c1=0
        for news in self.data:
            if(news.label == lbl):
                c1 += 1
        return c1
        
    def freq_contains(self, nonces):
        count = 0
        for news in self.data:
            if(news.contains(nonces)):
                count +=1
        return count
            
    def unique(self):
        uniq = NewsVector()
        for news in self.data:
            present = False
            for un_news in uniq.data:
                if(news.identical_news(un_news, CHOICE)):
                    present = True
                    break                   
            if(not present):
                uniq.add(news)
        return uniq
            
    def union(self, newsv1):
        temp = NewsVector()
        for news in self.data:
            temp.add(news)
        for news in newsv1.data:
            temp.add(news)
        return temp.unique()
        
    def intersect(self, newsvp1):                   # without duplicates
        temp_int = NewsVector()
        newsv1 = NewsVector()
        newsv2 = NewsVector()
        newsv1.add_vec(self)                        # making copies 
        newsv2.add_vec(newsvp1)                     # making copies 
        for news1 in newsv1.data:
            present = False
            for news2 in newsv2.data:
                if(news1.identical_news(news2, CHOICE)):
                    present = True
                    break
            if(present):
                temp_int.add(news1)
                newsv1.remove(news1)
                newsv2.remove(news2)
        return temp_int.unique()

    def tot_intersect(self, newsvp1):               # with duplicates
        newsv1 = NewsVector()
        newsv2 = NewsVector()
        newsv1.add_vec(self)
        newsv2.add_vec(newsvp1)
        for news1 in newsv1.data:
            present = False
            for news2 in newsv2.data:
                if(news1.identical_news(news2, CHOICE)):
                    present = True
                    break
            if(present):
                self.add(news1)
                newsv2.remove(news2)
        return self
                    
    def news_weight(self, news, wchoice):
        count = 0
        for a in self.data:
            if(a.identical_news(news, CHOICE)):
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
            sys.exit(0)
        
    def gen_word_vec(self, word_v, wchoice=W_CHOICE):       # check generates a vector of words from NewsVector, fits it to word_v
        vec = []
        words = self.newsvec_to_words()
        stemmed_words = common.stem_low_wvec(words)
        words = common.strip_vec(words)
        # print words
        for word in word_v:
            if(wchoice == NUM):
                vec.append(float(words.count(word)))
            elif(wchoice == LOG_NUM):
                vec.append(math.log(float(words.count(word))))
        return vec
    
    def gen_news_vec(self, newsv, choice=CHOICE):               # check self is news_union  # generates a vector of newss from NewsVector
        vec = [0]*self.size()
        for news in self.data:
            for lnews in newsv.data:
                if(news.identical_news(lnews, choice)):
                    vec[self.index(news)] += 1.
        return vec  
        
    def gen_temp_news_vec(self, newsv, choice=CHOICE):      # self is news_union
        vec = [0]*newsv.size()
        i = 0
        j = 0
        for news in newsv.data:
            for lnews in self.data:
                if(news.identical_news(lnews, choice)):
                    vec[i] = self.index(lnews)
            i += 1
        return vec      
                
    def newsvec_to_words(self):                     # check
        line = ""
        for news in self.data:
            line = line + " " + news.title+ " " + news.body
        list = re.split(r'[.(), !<>\/:=?;\-\n]+|', line)
        for i in range(0,len(list)):
            list[i] = list[i].replace('\xe2\x80\x8e', '')
            list[i] = list[i].replace('\xc2\xae', '') 
            list[i] = list[i].replace('\xe2\x84\xa2', '') 
            list[i] = list[i].replace('\xc3\xa9', '') 
            list[i] = list[i].replace('\xc3\xa1', '') 
        list = [x for x in list if len(x)>1]
        return list
        
    def gen_news_words_vec(self, feat):     # Creates a vector of word frequencies for each news in NewsVector
        vec = []
        for news in self.data:
            vec.append(news.fit_to_feat(feat))
        return vec

#------------- Guha's functions for newsVec Comparison ---------------#

def news_sim(newsv1, newsv2):                               # check
    if(SIM_CHOICE == JACCARD):
        return jaccard_index(newsv1, newsv2)
    elif(SIM_CHOICE == COSINE):
        return news_cosine_sim(newsv1, newsv2)
    else:
        print("Illegal SIM_CHOICE")
        raw_input("Press Enter to Exit")
        sys.exit()

def jaccard_index(newsv1, newsv2):
    news_union = newsv1.union(newsv2)
    news_int = newsv1.intersect(newsv2)
    return (float(news_int.size())/float(news_union.size()))

def news_cosine_sim(newsv1, newsv2):                        # check
    news_union = newsv1.union(newsv2)
    vec1 = []
    vec2 = []
    for news in news_union.data:
        vec1.append(newsv1.news_weight(news, W_CHOICE))
        vec2.append(newsv2.news_weight(news, W_CHOICE))
    return common.cosine_sim(vec1, vec2)
    