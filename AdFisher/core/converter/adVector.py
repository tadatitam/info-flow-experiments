import re, sys, math
import ad, common


########### CHOICES FOR THE AD-COMPARISON, AD-IDENTIFICATION #############

# Choices for what to uniquely identify an ad with
URL = 1
TITLE_URL = 2
TITLE_BODY = 3
CHOICE = TITLE_URL

# Choices for measure of similarity
JACCARD = 1
COSINE = 2
SIM_CHOICE = COSINE

# Choices for assigning weight to the vector
NUM = 1
LOG_NUM = 2
SCALED_NUM = 3 # not implemented
W_CHOICE = NUM

########### AD VECTOR CLASS #############

class AdVector:

    def __init__(self):
        self.data = []
        self.label = -1
    
    def setLabel(self, lbl):
        self.label = lbl
        
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
    
    def filter_by_keywords(self, keywords):
        if(keywords == None):
            return self
        filtered = AdVector()
        filtered.setLabel(self.label)
        for ad in self.data:
            if(ad.contains(keywords)):
                filtered.add(ad)
        return filtered
    
    def freq_contains(self, nonces):
        count = 0
        for ad in self.data:
            if(ad.contains(nonces)):
                count +=1
        return count
            
    def unique(self):
        uniq = AdVector()
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
        temp = AdVector()
        for ad in self.data:
            temp.add(ad)
        for ad in ads1.data:
            temp.add(ad)
        return temp.unique()
        
    def intersect(self, adsp1):                 # without duplicates
        temp_int = AdVector()
        ads1 = AdVector()
        ads2 = AdVector()
        ads1.add_vec(self)                      # making copies 
        ads2.add_vec(adsp1)                     # making copies 
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

    def tot_intersect(self, adsp1):             # with duplicates
        ads1 = AdVector()
        ads2 = AdVector()
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
            sys.exit(0)
        
    def gen_word_vec(self, word_v, wchoice=W_CHOICE):       # check generates a vector of words from AdVector, fits it to word_v
        vec = []
        words = self.advec_to_words()
        stemmed_words = common.stem_low_wvec(words)
        words = common.strip_vec(words)
        # print words
        for word in word_v:
            if(wchoice == NUM):
                vec.append(float(words.count(word)))
            elif(wchoice == LOG_NUM):
                vec.append(math.log(float(words.count(word))))
        return vec
    
    def gen_ad_vec(self, ads, choice=CHOICE):               # check self is ad_union    # generates a vector of ads from AdVector
        vec = [0]*self.size()
        for ad in self.data:
            for lad in ads.data:
                if(ad.identical_ad(lad, choice)):
                    vec[self.index(ad)] += 1.
        return vec  
        
    def gen_temp_ad_vec(self, ads, choice=CHOICE):      # self is ad_union
        vec = [0]*ads.size()
        i = 0
        j = 0
        for ad in ads.data:
            for lad in self.data:
                if(ad.identical_ad(lad, choice)):
                    vec[i] = self.index(lad)
            i += 1
        return vec      
                
    def advec_to_words(self):                       # check
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
        
    def gen_ad_words_vec(self, feat):       # Creates a vector of word frequencies for each ad in AdVector
        vec = []
        for ad in self.data:
            vec.append(ad.fit_to_feat(feat))
        return vec

#------------- Guha's functions for AdVec Comparison ---------------#

def ad_sim(ads1, ads2):                             # check
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
    return (float(ad_int.size())/float(ad_union.size()))

def ad_cosine_sim(ads1, ads2):                      # check
    ad_union = ads1.union(ads2)
    vec1 = []
    vec2 = []
    for ad in ad_union.data:
        vec1.append(ads1.ad_weight(ad, W_CHOICE))
        vec2.append(ads2.ad_weight(ad, W_CHOICE))
    return common.cosine_sim(vec1, vec2)
    