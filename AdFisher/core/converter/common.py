import re                                       # regular expressions
from stemming.porter2 import stem               # Porter Snowball Stemming
from nltk.corpus import stopwords               # for removing stop-words
import math

#------------- to round off numbers ---------------#

def round_figures(x, n):
    """Returns x rounded to n significant figures."""
    return round(x, int(n - math.ceil(math.log10(abs(x)))))


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

#------------- functions helping Word based analysis ---------------#

def stem_low_wvec(words):               # check return stemmed and lower case words from the input list of words
    for i in range(0, len(words)):
        words[i] = stem(words[i]).lower()
    return words

def unique_words(words):                # check returns a set of unique words from the input list of words
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

def strip_vec(list):                    # check removes the blank '', digits, $, & words
    try:
        if(list[0] == ''):
            del list[-len(list)]
        if(list[len(list)-1] == ''):
            del list[-1]
    except:
        pass
    chars = set('0123456789$&')
    return [x for x in list if not (any((c in chars) for c in x))]
    
#------------- for Vector Operations ---------------#

def cosine_sim(vec1, vec2):     # cosine similarity of two vectors
    return (dot_prod(vec1, vec2)/(vec_mag(vec1)*vec_mag(vec2)))

def vec_mag(vec):               # magnitude of a vector
    sum = 0.0
    for i in vec:
        sum = sum + i*i
    return math.sqrt(sum)

def dot_prod(vec1, vec2):       # dot product of two vectors
    sum = 0.0
    if(len(vec1) != len(vec2)):
        print("Dot product doesnt exist")
        sys.exit()
    for i in range(0, len(vec1)):
        sum = sum + vec1[i]*vec2[i]
    return sum
