from multiprocessing import Process
import glob, sys
import random
import numpy as np
import collect

def begin(treatments, measurement, agents=2, blocks=1, runs=1, 
		browser='firefox', timeout=2000, log_file="log.txt"):
	ntreat = len(treatments)
	#random.seed(123)
	
	treatnames = ""
	for i in range(0,len(treatments)):
		if(i==0):
			treatnames += treatments[i].name
		else:
			treatnames += "||"+treatments[i].name
	
	def getRandomTable(agents, ntreat):
		l = np.arange(agents)
		random.shuffle(l)
		if(agents % ntreat != 0):
			print "Warning: agents in each round [%s] not divisible by number of treatments [%s]" %(agents, ntreat)
			print "Assignment done randomly"
			raw_input("Press enter to continue")
		size = agents/ntreat
		table = [ntreat]*agents
		for i in range(0, ntreat):
			for j in range(size*i, size*(i+1)):
				table[l[j]] = i
		return table, l
	
	fo = open(log_file, "a")
	fo.write("config||"+str(agents)+"||"+str(ntreat)+"\n")
	fo.write("treatnames||"+treatnames+"\n")
	for j in range(0, blocks):
		print "Block ", j+1
		table, l = getRandomTable(agents, ntreat)		
# 		print table
		fo = open(log_file, "a")
		fo.write("assign||")
		fo.write(str(j)+"||")
		for i in range(0, agents-1):
			fo.write(str(l[i]) + "||")
		fo.write(str(l[agents-1]) + "\n")
		fo.close()
		
		procs = []
		for i in range(0,agents):
			procs.append(Process(target=collect.run_script, args=(i, agents, table[i], runs, browser, log_file, j+1, treatments, measurement, timeout, )))
		map(lambda x: x.start(), procs)
		map(lambda x: x.join(), procs)