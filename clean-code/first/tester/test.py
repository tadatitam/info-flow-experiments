import testHelper as anna			# test-code
import re							# for splitting strings
import sys							# for system arguments
from datetime import datetime		# to parse time


if __name__ == "__main__":
	if len(sys.argv) != 2:
		raw_input("Enter log file as command line input")
		print "Exiting"
		sys.exit(0)
	
	LOG_FILE = sys.argv[1]			# Input Log file as command line argument
	fo = open(LOG_FILE, "r")
	line = fo.readline()
	fo.close()
	chunks = re.split("\|\|", line)
	INSTANCES = len(chunks)-1
	
	adv = []
	for i in range(0, INSTANCES):
 		adv.append(anna.AdVec())
 	par_adv = []
	
	fo = open(LOG_FILE, "r")
	r = 0	
	sys.stdout.write("Scanning ads")
	for line in fo:
		chunks = re.split("\|\|", line)
		chunks[len(chunks)-1] = chunks[len(chunks)-1].rstrip()
 		if(chunks[0] == 'g' and r >0 ):
 			r += 1
 			par_adv.append({'adv':adv, 'ass':ass})
 			sys.stdout.write(".")
			sys.stdout.flush()
			adv = []
			for i in range(0, INSTANCES):
 				adv.append(anna.AdVec())
			ass = chunks[1:]
		if(chunks[0] == 'g' and r==0):
			r += 1
			ass = chunks[1:]
 			#print ass
		else:
  			try:
				ad = anna.Ad({'Time':datetime.strptime(chunks[2], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[3], 'URL': chunks[4], 'Body': chunks[5].rstrip(), 'cat': "", 'label':chunks[1]})
				adv[int(chunks[0])].add(ad)
 			except:
 				pass
 	
 	r += 1
 	par_adv.append({'adv':adv, 'ass':ass})
 	sys.stdout.write(".Scanning complete\n")
 	sys.stdout.flush()
 	
 	# THE FOLLOWING CODE THROWS OUT DATA POINTS THAT ARE BAD!! LIKE ONES WITH AN INSTANCE COLLECTING NO ADS
 	
#  	new_par_adv = []
#  	print len(par_adv)
#  	for unit in par_adv:
#  		flag=0
#  		for adv in unit['adv']:
#  			if(adv.size() < 1):
#  				flag=1
#  		if(flag==0):
#  			new_par_adv.append(unit)
#  	print len(new_par_adv)
#  	par_adv = new_par_adv
 	
	anna.MLAnalysis(par_adv)
