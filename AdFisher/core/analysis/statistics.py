import sys

import numpy as np                                      
from scipy import stats                     # for chi2 test
from scipy import spatial                   # for cosine distances
from datetime import datetime               # counting times for running tests

from itertools import combinations as comb  # permutations for old permutation test
import random                               # for random shuffles


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




