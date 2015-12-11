import sys
import numpy as np                                      
from scipy import stats                     # for chi2 test
from scipy import spatial                   # for cosine distances
from datetime import datetime               # counting times for running tests
import math
from itertools import combinations as comb  # permutations for old permutation test
import random                               # for random shuffles
from scipy.stats import t

#------------- functions computing Statistics ---------------#

def correctly_classified(ypred, ylabel):   # number of correctly classified instances in blocks
    if(ypred.shape != ylabel.shape):
        raw_input("ypred, ylabel not of same shape!")
        print "Exiting..."
        sys.exit(0)
    blocks = ypred.shape[0]
    blockSize = ypred.shape[1]
    CC = 0
    for i in range(0,blocks):
        for j in range(0, blockSize):
            if(ypred[i][j]==ylabel[i][j]):
                CC += 1
    return CC
    

def difference(X_test, y_test):
    blocks = y_test.shape[0]
    blockSize = y_test.shape[1]
    kw0 = 0
    kw1 = 0
    for i in range(0,blocks):
        for j in range(0, blockSize):
            if(y_test[i][j]==1):
                kw1 += X_test[i][j]
            elif(y_test[i][j]==0):
                kw0 += X_test[i][j]
            else:
                raw_input("More classes than expected")
                print "Exiting..."
                sys.exit(0)
#   print kw1, kw0
    return (kw1 - kw0)

def cosine_distance(X_test, y_test):
    blocks = y_test.shape[0]
    blockSize = y_test.shape[1]
    out0 = np.array([0]*X_test.shape[2])
    out1 = np.array([0]*X_test.shape[2])
    for i in range(0,blocks):
        for j in range(0, blockSize):
#           print y_test[i][j]
#           print X_test[i][j]
            if(y_test[i][j]==1):
                out1 += X_test[i][j]
            elif(y_test[i][j]==0):
                out0 += X_test[i][j]
            else:
                raw_input("More classes than expected")
                print "Exiting..."
                sys.exit(0)
    return spatial.distance.cosine(out0, out1)
        
#------------- helper functions for printing statistics of the data ---------------#

def print_frequencies(X, y, features, topk0, topk1):
    out = np.zeros((2, X.shape[2]))
    for j in range(0, X.shape[0]):
#         print X[j]
#         print y[j]
        for k in range(0, 2):
            out[k] = np.add(out[k], np.sum(X[j][np.where(y[j]==k)], axis=0))
#         print out
#         raw_input("hool")

    print "Frequency of top ads:\n"
    for i in range(0, len(topk0)):
        index = topk0[i]
#         print index,
        features.choose_by_index(index).display()
        print out[:, index]
        print "----------------------------------"
    
    print "%%%%----------------------------------%%%%"
    for i in range(0, len(topk1)):
        index = topk1[i]
#         print index,
        features.choose_by_index(index).display()
        print out[:, index]
        print "----------------------------------"
    print "%%%%----------------------------------%%%%"
            


def find_word_in_collection(collection, words):
    counts = [0,0]
    for col in collection:
        advs = col['adv']
        for adv in advs:
            counts[adv.label] += adv.freq_contains(words)
    return counts

def print_counts(X,y):                                          # check
    print "Number of blocks in log: ", X.shape[0]
    print "Number of agents in a block: ", X.shape[1]
    print "Size of feature vector: ", X.shape[2]
    print "Total count of features: ", int(sum(sum(sum(X))))
    ua,uind=np.unique(y,return_inverse=True)
    count=np.bincount(uind)
    counts = [0]*len(ua)
    ucounts = [0]*len(ua)
    ucounter = [[0.]*X.shape[2]]*len(ua)
    for i in range(0, X.shape[0]):
        for j in range(0, X.shape[1]):
            counts[y[i][j]] += int(sum(X[i][j]))
            ucounter[y[i][j]] += np.sign(X[i][j])
    ucounts = np.sum(np.sign(ucounter), axis=1)
    print "[treatments] [blocks] [features] [unique-features] :: ", ua, count, counts, ucounts
    print ""

def print_mean(array_ind_ad):
    array_price_control = []
    array_price_experimental = []
    max_value_control = {}
    max_value_experimental = {}
    min_value_control = {}
    min_value_experimental = {}
    for ad in array_ind_ad:
        title = ad["title"].translate(None, '|$')
        body = ad["body"].translate(None, '|$')
        label = ad["label"].translate(None, '|$')
        price = ad["price"].translate(None, ' |$')

        if (float(label) == 0):
            try:
                array_price_control.append(float(price))
            except ValueError,e:
                print "error",e
        elif (float(label) == 1):
            try:
                array_price_experimental.append(float(price))
            except ValueError,e:
                print "error",e
    std_control = np.std(array_price_control)
    std_experimental = np.std(array_price_experimental)
######### calculate difference between two means ref: http://onlinestatbook.com/2/tests_of_means/difference_means.html    
    SSE = 0
    df = float(len(array_price_control)-1+len(array_price_experimental)-1)
    for value in array_price_control:
        SSE = SSE + (float(value)-np.mean(array_price_control))**2
    for value in array_price_experimental:
        SSE = SSE + (float(value)-np.mean(array_price_experimental))**2
    MSE = SSE/df
    nh = 1/(1/float(len(array_price_control))+1/float(len(array_price_experimental)))
    SM1M2 = math.sqrt(float(2*MSE/nh))
    t_value = (float(np.mean(array_price_control))-float(np.mean(array_price_experimental)))/SM1M2
    p_value = (1-stats.t.cdf(t_value, df))*2
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "control (chrome): group size = " 
    print len(array_price_control)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "control (chrome): mean = " 
    print np.mean(array_price_control)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "control (chrome): standard deviation = " 
    print std_control
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "experimental (firefox): group size = " 
    print len(array_price_experimental)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "experimental (firefox): mean = " 
    print np.mean(array_price_experimental)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "experimental (firefox): standard deviation = " 
    print std_experimental
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "P-value is"
    print p_value
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    
