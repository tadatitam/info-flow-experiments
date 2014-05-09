from subprocess import Popen
from multiprocessing import Process
import glob, sys
import random
import numpy as np
import collect

def begin(log_file="log.txt", samples=2, 
		treatments=[], blocks=1, runs=1, reloads=10, delay=5, browser='firefox'):
	LOG_FILE = log_file
	COLLECT_PY = "experimenter/collect.py"
	SAMPLES = samples
	TREATMENTS = len(treatments)
	BLOCKS = blocks

	test = glob.glob(COLLECT_PY)[0]
	processes = []

	RUNS = runs
	RELOADS = reloads
	DELAY = delay
	BROWSER = browser

	#random.seed(123)
	
	treatnames = ""
	for i in range(0,len(treatments)):
		if(i==0):
			treatnames += treatments[i].name
		else:
			treatnames += "||"+treatments[i].name
	
	def getRandomTable(SAMPLES, TREATMENTS):
		l = np.arange(SAMPLES)
		random.shuffle(l)
		if(SAMPLES % TREATMENTS != 0):
			print "Warning: Samples in each round [%s] not divisible by number of treatments [%s]" %(SAMPLES, TREATMENTS)
			print "Assignment done randomly"
			raw_input("Press enter to continue")
		size = SAMPLES/TREATMENTS
		table = [TREATMENTS]*SAMPLES
		for i in range(0, TREATMENTS):
			for j in range(size*i, size*(i+1)):
				table[l[j]] = i
		return table, l
	
	fo = open(LOG_FILE, "a")
	fo.write("config||"+str(SAMPLES)+"||"+str(TREATMENTS)+"\n")
	fo.write("treatnames||"+treatnames+"\n")
	for j in range(0, BLOCKS):
		print "Block ", j+1
		table, l = getRandomTable(SAMPLES, TREATMENTS)		
# 		print table
		fo = open(LOG_FILE, "a")
		fo.write("assign||")
		fo.write(str(j)+"||")
		for i in range(0, SAMPLES-1):
			fo.write(str(l[i]) + "||")
		fo.write(str(l[SAMPLES-1]) + "\n")
		fo.close()
		
		procs = []
		for i in range(0,SAMPLES):
			procs.append(Process(target=collect.run_script, args=(i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, LOG_FILE, j+1, treatments,)))
#     	procs.append(Process(target=func_1, args=('sir',)))
		map(lambda x: x.start(), procs)
		map(lambda x: x.join(), procs)
# 		for i in range(0,SAMPLES):
# 			print 'python %s %s %s %s %s %s %s %s %s %s %s' % (test, i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, LOG_FILE, j+1, treatments)
# 			processes.append(Popen('python %s %s %s %s %s %s %s %s %s %s %s' % (test, i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, LOG_FILE, j+1, treatments), shell=True))
# 
# 		for process in processes:
# 			process.wait()