from subprocess import Popen
import glob, sys
import random
import numpy as np

if __name__ == "__main__":
	AD_FILE = sys.argv[1]
	SITE_FILE = sys.argv[2]
	COLLECT_PY = sys.argv[3]

	fo = open(AD_FILE, "w")
	fo.close()
	
	fo = open("log", "w")			# hard coded log-file, to be used by collectHelper.
	fo.close()
	
	test = glob.glob(COLLECT_PY)[0]
	processes = []

	SAMPLES = 10
	TREATMENTS = 2
	RUNS = 1
	RELOADS = 10
	DELAY = 5
	BROWSER = 'ff'			# ff=firefox, chr=chrome
	ROUNDS = 200

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
		fo = open(AD_FILE, "a")
		fo.write("g||")
		for i in range(0, SAMPLES-1):
			fo.write(str(l[i]) + "||")
		fo.write(str(l[SAMPLES-1]) + "\n")
		fo.close()

		for i in range(0,SAMPLES):
			print 'python %s %s %s %s %s %s %s %s %s %s %s' % (test, i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, AD_FILE, SITE_FILE, j+1)
			processes.append(Popen('python %s %s %s %s %s %s %s %s %s %s %s' % (test, i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, AD_FILE, SITE_FILE, j+1), shell=True))

		for process in processes:
			process.wait()