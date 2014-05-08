from subprocess import Popen
import glob, sys
import random
import numpy as np

if __name__ == "__main__":
	LOG_FILE = sys.argv[1]
	SITE_FILE = sys.argv[2]
	COLLECT_PY = sys.argv[3]
	SAMPLES = int(sys.argv[4])
	TREATMENTS = int(sys.argv[5])
	BLOCKS = int(sys.argv[6])

	test = glob.glob(COLLECT_PY)[0]
	processes = []

	RUNS = 1
	RELOADS = 10
	DELAY = 5
	BROWSER = 'ff'			# ff=firefox, chr=chrome

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
	
	fo = open(LOG_FILE, "a")
	fo.write("config||"+int(SAMPLES)+"||"+int(TREATMENTS)+"\n")
	for j in range(0, BLOCKS):
		print "Round ", j+1
		table, l = getRandomTable(SAMPLES, TREATMENTS)		
		print table
		fo = open(LOG_FILE, "a")
		fo.write("assign||")
		fo.write(str(j)+"||")
		for i in range(0, SAMPLES-1):
			fo.write(str(l[i]) + "||")
		fo.write(str(l[SAMPLES-1]) + "\n")
		fo.close()

		for i in range(0,SAMPLES):
			print 'python %s %s %s %s %s %s %s %s %s %s %s' % (test, i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, LOG_FILE, SITE_FILE, j+1)
			processes.append(Popen('python %s %s %s %s %s %s %s %s %s %s %s' % (test, i, SAMPLES, table[i], RUNS, RELOADS, DELAY, BROWSER, LOG_FILE, SITE_FILE, j+1), shell=True))

		for process in processes:
			process.wait()