from subprocess import Popen
import glob, sys
import random
import numpy as np
  
LOG_FILE = "log"

fo = open(LOG_FILE, "w")
fo.close()

test = glob.glob('collector/collect.py')[0]
processes = []

SAMPLES = 2
TREATMENTS = 2
RUNS = 1
RELOADS = 5
DELAY = 5
BROWSER = 'ff'			# ff=firefox, chr=chrome
ROUNDS = 10

#random.seed(123)

def getRandomTable(SAMPLES, TREATMENTS):
	l = np.arange(SAMPLES)
	random.shuffle(l)
	if(SAMPLES % TREATMENTS != 0):
		print "Samples in each round [%s] not divisible by number of treatments [%s]" %(SAMPLES, TREATMENTS)
		print "Hence uneven chunks"
		raw_input("Press enter to continue")
	size = SAMPLES/TREATMENTS
	table = [TREATMENTS]*SAMPLES
	for i in range(0, TREATMENTS):
		for j in range(size*i, size*(i+1)):
			table[l[j]] = i
	return table, l
	
for j in range(0, ROUNDS):
	print "Round ", j+1
	table, l = getRandomTable(SAMPLES, TREATMENTS)		
	print table
	fo = open(LOG_FILE, "a")
	fo.write("g||")
	for i in range(0, SAMPLES-1):
		fo.write(str(l[i]) + "||")
	fo.write(str(l[SAMPLES-1]) + "\n")
	fo.close()

	for i in range(0,SAMPLES):
		print 'python %s %s %s %s %s %s %s %s %s' % (test, i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, j+1)
		processes.append(Popen('python %s %s %s %s %s %s %s %s %s' % (test, i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, j+1), shell=True))

	for process in processes:
		process.wait()