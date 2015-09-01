import re, sys                                      
import numpy as np
from datetime import datetime, timedelta            # to read timestamps reloadtimes
import adVector, ad, common, interest, news         # common, ad ad_vector, interest, news classes
from nltk.corpus import stopwords                   # for removing stop-words


#------------- to convert Ad Vectors to feature vectors ---------------#

def word_vectors(list):                                 # returns a frequency vector of words, when input a list of adVecs
    ad_union = adVector.AdVector()
    for ads in list:
        ad_union = ad_union.union(ads)
    words = ad_union.advec_to_words()
    stemmed_words = common.stem_low_wvec(words)
    filtered_words = [w for w in stemmed_words if not w in stopwords.words('english')]
    word_v = common.unique_words(filtered_words)
    word_v = common.strip_vec(word_v)
    wv_list = []
    labels = []
    for ads in list:
        wv_list.append(ads.gen_word_vec(word_v))
        labels.append(ads.label)
    return wv_list, labels, word_v                      ## Returns word_v as feature

def ad_vectors(list, filtered_by = None):                                   # returns a frequency vector of ads, when input a list of adVecs
    ad_union = adVector.AdVector()
    if(filtered_by == None):
        new_list = list
    else:
        new_list = []
        for ads in list:
            new_ads = ads.filter_by_keywords(filtered_by)
            new_list.append(new_ads)
    for ads in new_list:    
        ad_union = ad_union.union(ads)
    av_list = []
    labels = []
    for ads in new_list:
        av_list.append(ad_union.gen_ad_vec(ads))
        labels.append(ads.label) 
    return av_list, labels, ad_union                    ## Returns entire ad as feature

def freq_news_vectors(list):                                    # returns a frequency vector of news, when input a list of newsVecs
    news_union = news.NewsVector()
    for newsv in list:
        news_union = news_union.union(newsv)
    av_list = []
    labels = []
    for newsv in list:
        av_list.append(news_union.gen_news_vec(newsv))
        labels.append(newsv.label)
    return av_list, labels, news_union                  ## Returns entire ad as feature
    
def temp_ad_vectors(list):
    ad_union = adVector.AdVector()
    for ads in list:
        ad_union = ad_union.union(ads)
    tav_list = []
    labels = []
    for ads in list:
        tav_list.append(ad_union.gen_temp_ad_vec(ads))
        labels.append(ads.label)
    return tav_list, labels, ad_union

def temp_news_vectors(list):
    news_union = news.NewsVector()
    for newsv in list:
        news_union = news_union.union(newsv)
    tav_list = []
    labels = []
    for newsv in list:
        tav_list.append(news_union.gen_temp_news_vec(newsv))
        labels.append(newsv.label)
    return tav_list, labels, news_union
    
def interest_vectors(list):                         # returns a frequency vector of interests, when input a list of interessts
    int_union = interest.Interests()
    for ints in list:
        int_union = int_union.union(ints)
    i_list = []
    labels = []
    for ints in list:
        i_list.append(int_union.gen_int_vec(ints))
        labels.append(ints.label)
    return i_list, labels, int_union

def keyword_vectors(list, keywords):
    kw_list = []
    labels = []
    for ads in list:
        kw_list.append(ads.freq_contains(keywords))
        labels.append(ads.label)
#       ads.display("title+url+body")
#       print kw_list
#       print labels
#       raw_input("wait")
    return kw_list, labels
        

def get_interest_vectors(advdicts):
    list = []
    sys.stdout.write("Creating interest vectors")
    sys.stdout.write("-->>")
    sys.stdout.flush()
    for advdict in advdicts:
        list.extend(advdict['interests'])
    X, labels, feat = interest_vectors(list)
    if(labels[0] == ''):
        for advdict in advdicts:
            ass = advdict['assignment']
            y1 = [0]*len(ass)
            for i in ass[0:len(ass)/2]:
                y1[int(i)] = 1
            y.extend(y1)
    else:
        y = [int(i) for i in labels]
    try:
        feat.data[feat.data.index('')] = 'None'
    except:
        pass
    print "Complete"
    return np.array(X), np.array(y), feat
    
def get_feature_vectors(advdicts, feat_choice, filtered_by=None):         # returns observation vector from a list of rounds
    n = len(advdicts[0]['assignment'])
    list = []
    y = []
    sys.stdout.write("Creating feature vectors")
    sys.stdout.write("-->>")
    sys.stdout.flush()
    s = datetime.now()
    if(feat_choice == 'words'):
        for advdict in advdicts:
            list.extend(advdict['advector'])
        X, labels, feat = word_vectors(list)
    elif(feat_choice == 'ads'):
        for advdict in advdicts:
            list.extend(advdict['advector'])
        X, labels, feat = ad_vectors(list, filtered_by)
    elif(feat_choice == 'news'):
        for advdict in advdicts:
            list.extend(advdict['newsvector'])
        X, labels, feat = freq_news_vectors(list)
        
    if(labels[0] == ''):
        for advdict in advdicts:
            ass = advdict['assignment']
            y1 = [0]*len(ass)
            for i in ass[0:len(ass)/2]:
                y1[int(i)] = 1
            y.extend(y1)
    else:
        y = [int(i) for i in labels]
    X = [X[i:i+n] for i in range(0,len(X),n)]
    y = [y[i:i+n] for i in range(0,len(y),n)]
#   print feat[0].title, feat[0].url
    print "Complete"
    e = datetime.now()
    print "---Time for getting feature vectors: ", str(e-s)
    return np.array(X), np.array(y), feat

def get_keyword_vectors(advdicts, keywords):
    n = len(advdicts[0]['assignment'])
    list = []
    y = []
    sys.stdout.write("Creating keyword vectors")
    sys.stdout.write("-->>")
    sys.stdout.flush()
    for advdict in advdicts:
        list.extend(advdict['advector'])
    X, y = keyword_vectors(list, keywords)
    X = [X[i:i+n] for i in range(0,len(X),n)]
    y = [y[i:i+n] for i in range(0,len(y),n)]
    print "Complete"
    return np.array(X),np.array(y)
    
    
#------------- to read from log file into Ad Vectors ---------------#


def apply_labels_to_vecs(adv, ints, newsv, ass, samples, treatments):           # check
    size = samples/treatments
    for i in range(0, treatments):
        for j in range(0, size):
            adv[int(ass[i*size+j])].setLabel(i)
            ints[int(ass[i*size+j])].setLabel(i)
            newsv[int(ass[i*size+j])].setLabel(i)

def interpret_log_line(line):
    """Interprets a line of the log, and returns six components
        For lines containing meta-data, the unit_id and treatment_id is -1
    """
    chunks = re.split("\|\|", line)
    tim = chunks[0]
    linetype = chunks[1]
    linename = chunks[2]
    value = chunks[3].strip()
    if(len(chunks)>5):
        unit_id = chunks[4]
        treatment_id = chunks[5].strip()
    else:
        unit_id = -1
        treatment_id = -1
    return tim, linetype, linename, value, unit_id, treatment_id

def read_log(log_file):
    par_adv = []
    measured = False
    sys.stdout.write("Reading log")
    fo = open(log_file, "r")
    for line in fo:
#       print line
        tim, linetype, linename, value, unit_id, treatment_id = interpret_log_line(line)
        if (linetype == 'meta'):
            if(linename == 'agents'):
                num_agents = int(value)
            elif(linename == 'treatnames'):
                treatnames = re.split("\@\|", value)
#               print "Treatments: ", treatnames
            elif(linename == 'block_id start'):
                sys.stdout.write(".")
                sys.stdout.flush()
                block_id = int(value)
                adv = []
                ints = []
                newsv = []
                for i in range(0, num_agents):
                    adv.append(adVector.AdVector())
                    ints.append(interest.Interests())
                    newsv.append(news.NewsVector())
#               print block_id
            elif(linename == 'assignment'):
                assignment = [int(x) for x in re.split("\@\|", value)]
            elif(linename == 'block_id end'):
                apply_labels_to_vecs(adv, ints, newsv, assignment, num_agents, len(treatnames))
                par_adv.append({'advector':adv, 'newsvector':newsv, 'assignment':assignment, 'intvector':ints})
        elif(linetype == 'treatment'):
            pass
        elif(linetype == 'measurement'):
            if(linename == 'ad'):
                ind_ad = ad.Ad(value, treatment_id)
                adv[int(unit_id)].add(ind_ad)
            if(linename == 'interest'):
                ints[int(unit_id)].set_from_string(value)
            if(linename == 'news'):
                ind_news = news.News(value, treatment_id)
                newsv[int(unit_id)].add(ind_news)
        elif(linetype == 'error'):
#           print "Error in block", block_id, ": ", line.strip()
            pass
    sys.stdout.write(".Reading complete\n")
    print "Treatments: ", treatnames
    return par_adv, treatnames

def read_old_log(log_file):                         
    treatnames = []
    fo = open(log_file, "r")
    line = fo.readline()
    chunks = re.split("\|\|", line)
    if(chunks[0] == 'g'):
        old = True
        gmarker = 'g'
        treatments = 2
        treatnames = ['0', '1']
        samples = len(chunks)-1
    else:
        old = False
        gmarker = 'assign'
        treatments = int(chunks[2])
        samples = int(chunks[1])
        line = fo.readline()
        chunks = re.split("\|\|", line)
        for i in range(1, len(chunks)):
            treatnames.append(chunks[i].strip())
    fo.close()
    assert treatments == len(treatnames)
    for i in range(0, treatments):
        print "Treatment ", i, " = ", treatnames[i]
    adv = []
    ints = []
    newsv = []
    for i in range(0, samples):
        adv.append(adVector.AdVector())
        ints.append(interest.Interests())
        newsv.append(news.NewsVector())
    loadtimes = [timedelta(minutes=0)]*samples
    reloads = [0]*samples
    errors = [0]*samples
    xvfbfails = []
    breakout = False
    par_adv = []
    ass = []
        
    fo = open(log_file, "r")
    r = 0   
    sys.stdout.write("Scanning ads")
    for line in fo:
        chunks = re.split("\|\|", line)
        chunks[len(chunks)-1] = chunks[len(chunks)-1].rstrip()
        if(chunks[0] == gmarker and r==0):
            r += 1
            ass = chunks[2:]
            if(old):    
                ass = chunks[1:]
            assert len(ass) == samples
            apply_labels_to_vecs(adv, ints, newsv, ass, samples, treatments)
            #print ass
        elif(chunks[0] == gmarker and r >0 ):
            r += 1
            par_adv.append({'advector':adv, 'newsvector':newsv, 'assignment':ass, 'xf':xvfbfails, 'intvector':ints, 
                        'break':breakout, 'loadtimes':loadtimes, 'reloads':reloads, 'errors':errors})
            sys.stdout.write(".")
            sys.stdout.flush()
            adv = []
            ints = []
            newsv = []
            for i in range(0, samples):
                adv.append(adVector.AdVector())
                ints.append(interest.Interests())
                newsv.append(news.NewsVector())
            loadtimes = [timedelta(minutes=0)]*samples
            reloads = [0]*samples
            errors = [0]*samples
            xvfbfails = []
            breakout = False
            ass = chunks[2:]
            if(old):    
                ass = chunks[1:]
            assert len(ass) == samples
            apply_labels_to_vecs(adv, ints, newsv, ass, samples, treatments)
        elif(chunks[0] == 'Xvfbfailure'):
            xtreat, xid = chunks[1], chunks[2]
            xvfbfails.append(xtreat)
        elif(chunks[1] == 'breakingout'):
            breakout = True
        elif(chunks[1] == 'loadtime'):
            t = (datetime.strptime(chunks[2], "%H:%M:%S.%f"))
            delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            id = int(chunks[3])
            loadtimes[id] += delta
        elif(chunks[1] == 'reload'):
            id = int(chunks[2])
            reloads[id] += 1
        elif(chunks[1] == 'errorcollecting'):
            id = int(chunks[2])
            errors[id] += 1
        elif(chunks[1] == 'prepref'):
            id = int(chunks[4])
            ints[id].remove_interest()
        elif(chunks[1] == 'pref'):
            id = int(chunks[4])
            int_str = chunks[3]
            ints[id].set_from_string(int_str)
        elif(chunks[0] == 'news'):
            ind_news = news.News({'Time':datetime.strptime(chunks[3], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[4], 
                    'Agency': chunks[5], 'Ago': chunks[6], 'Body': chunks[7].rstrip(), 'Label':chunks[2]})
            newsv[int(chunks[1])].add(ind_news)
        elif(chunks[0] == 'ad'):
            ind_ad = ad.Ad({'Time':datetime.strptime(chunks[3], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[4], 
                    'URL': chunks[5], 'Body': chunks[6].rstrip(), 'cat': "", 'Label':chunks[2]})
            adv[int(chunks[1])].add(ind_ad)
        else:                           # to analyze old log files
            try:
                ind_ad = ad.Ad({'Time':datetime.strptime(chunks[2], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[3], 
                        'URL': chunks[4], 'Body': chunks[5].rstrip(), 'cat': "", 'label':chunks[1]})
#               ind_ad = ad.Ad({'Time':datetime.strptime(chunks[1], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[2], 
#                       'URL': chunks[3], 'Body': chunks[4].rstrip(), 'cat': "", 'label':""})
                adv[int(chunks[0])].add(ind_ad)
            except:
                pass
    
    r += 1
    par_adv.append({'advector':adv, 'newsvector':newsv, 'assignment':ass, 'xf':xvfbfails, 'intvector':ints, 
            'break':breakout, 'loadtimes':loadtimes, 'reloads':reloads, 'errors':errors})
    sys.stdout.write(".Scanning complete\n")
    sys.stdout.flush()
    return par_adv, treatnames