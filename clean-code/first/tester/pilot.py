import testHelper as anna

import unittest, time, re
import sys

from datetime import datetime, timedelta

CAT_FILE = "car_categories.txt"
COMP_FILE = "car_companies.txt"
TERM_FILE = "car_keywords.txt"
# LOG_FILE = "log_10i_50r_linux"



def runAnalyses(index, adv, ass, keywords, sig, times, totv, metrics):
# 	print index
	cos, kw, prc, chi = 0, 1, 2, 3
	FN, FP, TOT = 0,1,2
	
	pcos, tcos 	= anna.testWrapper(adv, ass, keywords, 'coss')
	pkw, tkw 	= anna.testWrapper(adv, ass, keywords, 'kw')
	pprc, tprc 	= anna.testWrapper(adv, ass, keywords, 'prc')
	pchi, tchi 	= anna.testWrapper(adv, ass, keywords, 'chi')
	print("$%s$ & $%.6f$ \t & $%.6f$ \t & $%.6f$ \t & $%s$ \\\\" % (index-1, pcos, pkw, pprc, pchi))
	anna.printCounts(index-1, adv, ass)
 	if(pcos < 0.05):
 		sig[cos] += 1
 #	print pcos
	if(pkw < 0.05):
		sig[kw] += 1
	if(pprc < 0.05):
		sig[prc] += 1
	if(pchi < 0.05):
		sig[chi] += 1
	times[cos] += tcos
	times[kw] += tkw
	times[prc] += tprc
	times[chi] += tchi

 	for i in range(0, INSTANCES):
 		totv.add_vec(adv[i])

# 	anna.temporalPlots([adv[0]])
# 	advm, advf = anna.vec_for_stats(adv, ass)
# 	anna.histogramPlots([advm, advf])
#  	anna.histogramPlots([adv[0], adv[1]])
# 	anna.printTopFeatures(index, adv, ass)

# 	for i in range(0, INSTANCES):
# 		adv[i] = adv[i].retainCat('cars')
# 		print "after:", adv[i].size()
# 		adv[i].display('title')
# 		#raw_input("waiting")
# 	advm, advf = anna.vec_for_stats(adv, ass)
#  	anna.printTopFeatures(index, adv, ass)
#  	pcos, tcos 	= anna.testWrapper(adv, ass, keywords, 'coss')
#  	print pcos
#	anna.findClusters(index, adv, ass, INSTANCES)




if __name__ == "__main__":
	LOG_FILE = sys.argv[1]
	fo = open(LOG_FILE, "r")
	line = fo.readline()
	fo.close()
	chunks = re.split("\|\|", line)
	INSTANCES = len(chunks)-1
	adv = []
	for i in range(0, INSTANCES):
 		adv.append(anna.AdVec())
 	par_adv = []
 
 	totv = anna.AdVec()
	advm = anna.AdVec()
	advf = anna.AdVec()
	
 	keywords = ['bmw', 'audi', 'car', 'vehicle', 'automobile', 'cadillac', 'limo']
	
	fo = open(LOG_FILE, "r")
	r = 0
	significants = [0]*4
	metrics = [0]*4
	totaltimes = [timedelta(minutes=0)]*4
	
	sys.stdout.write("Scanning ads")
	
	for line in fo:
		chunks = re.split("\|\|", line)
		chunks[len(chunks)-1] = chunks[len(chunks)-1].rstrip()
 		if(chunks[0] == 'g' and r >0 ):
 			r += 1
 			par_adv.append({'adv':adv, 'ass':ass})
 			sys.stdout.write(".")
			sys.stdout.flush()
 			#runAnalyses(r-1, adv, ass, keywords, significants, totaltimes, totv, metrics)
			adv = []
			for i in range(0, INSTANCES):
 				adv.append(anna.AdVec())
			ass = chunks[1:]
  			#print ass
		if(chunks[0] == 'g' and r==0):
			r += 1
			ass = chunks[1:]
 			#print ass
		else:
  			try:
  			 	ad = anna.Ad({'Time':datetime.strptime(chunks[2], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[3], 'URL': chunks[4], 'Body': chunks[5].rstrip(), 'cat': "", 'label':chunks[1]})
# 				ad = anna.Ad({'Time':datetime.strptime(chunks[1], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[2], 'URL': chunks[3], 'Body': chunks[4].rstrip(), 'cat': "", 'label':""})
				adv[int(chunks[0])].add(ad)
 			except:
 				pass
 	
 	r += 1
 	par_adv.append({'adv':adv, 'ass':ass})
 	sys.stdout.write(".Scanning complete\n")
 	sys.stdout.flush()
	
	sys.stdout.write("Beginning Analysis\n")
	sys.stdout.flush()
	for i in range(0, len(par_adv)):
		runAnalyses(i+1, par_adv[i]['adv'], par_adv[i]['ass'], keywords, significants, totaltimes, totv, metrics)
	sys.stdout.write("Analysis complete\n")
	print ("%s\t%s\t%s\t%s\t \n" %(significants[0], significants[1], significants[2], significants[3]))

	print totv.size()
	print totv.unique().size()

