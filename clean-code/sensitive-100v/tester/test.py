import testHelper as anna						# test-code
import re										# for splitting strings
import sys										# for system arguments
from datetime import datetime, timedelta		# to parse time; add, subtract time differences

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
	TREATMENTS = int(chunks[1])
	INSTANCES = len(chunks)-1
	
	adv = []
	for i in range(0, INSTANCES):
 		adv.append(anna.AdVec())
 	loadtimes = [timedelta(minutes=0)]*INSTANCES
 	reloads = [0]*INSTANCES
 	errors = [0]*INSTANCES
 	xvfbfails = []
 	breakout = False
 	par_adv = []
	
	fo = open(LOG_FILE, "r")
	r = 0	
	sys.stdout.write("Scanning ads")
	for line in fo:
		chunks = re.split("\|\|", line)
		chunks[len(chunks)-1] = chunks[len(chunks)-1].rstrip()
		if(chunks[0] == 'assign' and r==0):
			r += 1
			ass = chunks[2:]
 			#print ass
 		elif(chunks[0] == 'assign' and r >0 ):
 			r += 1
 			par_adv.append({'adv':adv, 'ass':ass, 'xf':xvfbfails, 
 						'break':breakout, 'loadtimes':loadtimes, 'reloads':reloads, 'errors':errors})
 			sys.stdout.write(".")
			sys.stdout.flush()
			adv = []
			for i in range(0, INSTANCES):
 				adv.append(anna.AdVec())
 			loadtimes = [timedelta(minutes=0)]*INSTANCES
			reloads = [0]*INSTANCES
			errors = [0]*INSTANCES
 			xvfbfails = []
 			breakout = False
			ass = chunks[2:]
 		elif(chunks[0] == 'Xvfbfailure'):
 			xtreat, xid = chunks[1], chunks[2]
 			xvfbfails.append(xtreat)
 		elif(chunks[1] == 'breakingout'):
 			breakout = True
 		elif(chunks[1] == 'loadtime'):
 			t = (datetime.strptime(chunks[2], "%H:%M:%S.%f"))
 			delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
 			id = int(chunks[3])
 			loadtimes[id] += delta
 		elif(chunks[1] == 'reload'):
 			id = int(chunks[2])
 			reloads[id] += 1
 		elif(chunks[1] == 'errorcollecting'):
 			id = int(chunks[2])
 			errors[id] += 1 		
		else:
  			try:
				ad = anna.Ad({'Time':datetime.strptime(chunks[2], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[3], 
						'URL': chunks[4], 'Body': chunks[5].rstrip(), 'cat': "", 'label':chunks[1]})
# 				ad = anna.Ad({'Time':datetime.strptime(chunks[1], "%Y-%m-%d %H:%M:%S.%f"), 'Title':chunks[2], 
#						'URL': chunks[3], 'Body': chunks[4].rstrip(), 'cat': "", 'label':""})
				adv[int(chunks[0])].add(ad)
 			except:
 				pass
 	
 	r += 1
 	par_adv.append({'adv':adv, 'ass':ass, 'xf':xvfbfails, 
 			'break':breakout, 'loadtimes':loadtimes, 'reloads':reloads, 'errors':errors})
 	sys.stdout.write(".Scanning complete\n")
 	sys.stdout.flush()
 	
#  	for unit in par_adv:
#  		printNewsMetrics(unit)
 	
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
