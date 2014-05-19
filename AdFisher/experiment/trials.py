from multiprocessing import Process
import glob, sys
import random
import numpy as np
import collect

def begin(log_file="log.txt", samples=2, 
		treatments=[], blocks=1, runs=1, col_site='toi', reloads=10, delay=5, browser='firefox', timeout=2000):
	ntreat = len(treatments)
	#random.seed(123)
	
	treatnames = ""
	for i in range(0,len(treatments)):
		if(i==0):
			treatnames += treatments[i].name
		else:
			treatnames += "||"+treatments[i].name
	
	def getRandomTable(samples, ntreat):
		l = np.arange(samples)
		random.shuffle(l)
		if(samples % ntreat != 0):
			print "Warning: Samples in each round [%s] not divisible by number of treatments [%s]" %(samples, ntreat)
			print "Assignment done randomly"
			raw_input("Press enter to continue")
		size = samples/ntreat
		table = [ntreat]*samples
		for i in range(0, ntreat):
			for j in range(size*i, size*(i+1)):
				table[l[j]] = i
		return table, l
	
	fo = open(log_file, "a")
	fo.write("config||"+str(samples)+"||"+str(ntreat)+"\n")
	fo.write("treatnames||"+treatnames+"\n")
	for j in range(0, blocks):
		print "Block ", j+1
		table, l = getRandomTable(samples, ntreat)		
# 		print table
		fo = open(log_file, "a")
		fo.write("assign||")
		fo.write(str(j)+"||")
		for i in range(0, samples-1):
			fo.write(str(l[i]) + "||")
		fo.write(str(l[samples-1]) + "\n")
		fo.close()
		
		procs = []
		for i in range(0,samples):
			procs.append(Process(target=collect.run_script, args=(i, samples, table[i], runs, col_site, reloads, delay, browser, log_file, j+1, treatments, timeout, )))
		map(lambda x: x.start(), procs)
		map(lambda x: x.join(), procs)