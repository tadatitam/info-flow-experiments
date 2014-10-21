import unittest

import experiment_driver
import permutation_test

def do_experiment(make_unit, treatments, measurement, end_unit,
		  load_results, test_stat,
		  num_blocks=1, num_units=2, timeout=2000,
		  log_file="log.txt", treatment_names=[]): 
	"""
	make_unit   -- Function that return a unit given a unit_id number (int).  
	               To keep the units exechangable, the unit_id should only be used as a label in logging.
	treatments  -- List of functions each of which that takes a unit and does some treatment to it.
	measurement -- A function that takes a unit and makes some measurements of it.
	               Should log the results.
	end_unit    -- A function that takes a unit and cleans it up.
	load_results-- Load the results from a log file into a pair vectors:
	                (1) one for each unit's response value
		        (2) one for the treatment assigned to each unit
		       with the units in the same order.
	test_stat   -- Takes a pair of vectors as above and computes a number.
	num_blocks  -- Number of blocks (rounds) used in the experiment.
	num_units   -- Number of units in each block.  
                       num_blocks * num_units is the sample size.
	timeout     -- How long to wait before giving up on a unit.
        log_file    -- File in which to store measurement and other helpful messages.  measurement should print to it.
	treatment_names -- names of the treatments in the list treatments in the same order.  
                           Optionally makes logs look better.
	
	For each block, do_experiment 
         (1) creates num_units units with make_unit,
         (2) subjects each of them to a function in treatments at random,
         (3) calls measurement on each of them to record some response, and
	 (4) calls end_unit on each of them.
	After doing this for every block, 
        it uses test_stat to run a permutation test on the results using that as the test statistic.
	"""
	def exper_body(unit_id, treatment_id):
		class Test(unittest.TestCase):
			def setUp(self):
				self.unit = make_unit(unit_id, treatment_id)
			def runTest(self):
				treatments[treatment_id](self.unit, unit_id)
			def tearDown(self):
				print "measurment: ", measurement(self.unit, unit_id, treatment_id)
				end_unit(self.unit, unit_id, treatment_id)
		test = Test()
		suite = unittest.TestSuite()
		suite.addTest(test)
		unittest.TextTestRunner(verbosity=1).run(suite)

	ntreat = len(treatments)
	if len(treatment_names) != ntreat:
		treatment_names = map(lambda i: str(i), range(0,ntreat))

	experiment_driver.run_experiment(exper_body,
					 num_blocks, num_units, timeout,
					 log_file, treatment_names)
	observed_values, observed_assignment = load_results()
	p_value = permutation_test.full_test(observed_values, observed_assignment, test_stat)
	print "p-value: ", p_value

	#do_experiment(exper_body,
	#	      num_blocks, num_agents, timeout,
	#	log_file, treatment_names)



#def treatments_to_string(treatment_names):
#	"""
#	Converts list of strings in a single string.
#	"""
#	treatment_names_string = ""
#	for i in range(0,len(treatment_names)):
#		if(i==0):
#			treatment_names_string += treatment_names[i]
#		else:
#			treatment_names_string += "||" + treatment_names[i]
#	return treatment_names_string
#
#def getRandomTable(num_agents, ntreat):
#	l = np.arange(num_agents)
#	random.shuffle(l)
#	if(num_agents % ntreat != 0):
#		print "Warning: agents in each round [%s] not divisible by number of treatments [%s]" %(num_agents, ntreat)
#		print "Assignment done randomly"
#		raw_input("Press enter to continue")
#	size = num_agents/ntreat
#	table = [ntreat]*num_agents
#	for i in range(0, ntreat):
#		for j in range(size*i, size*(i+1)):
#			table[l[j]] = i
#	return table, l
#
#def run_experiment_funct(make_unit, treatments, measurement, end_unit,
#			 num_blocks=20, num_agents=2, timeout=2000,
#			 log_file="log.txt", treatment_names=[]):	
#	def exper_body(treatment_id):
#		unit = make_unit()
#		treatments[treatment_id](unit)
#		print "measurment: ", measurement(unit)
#		end_unit(unit)
#	ntreat = len(treatments)
#	if len(treatment_names) != ntreat:
#		treatment_names = map(lambda i: str(i), range(0,ntreat))
#
#	run_experiment(exper_body,
#		       num_blocks, num_agents, timeout,
#		       log_file, treatment_names)
#
#def run_experiment_unit_test(unit_test, treatment_names,
#			     num_blocks=20, num_agents=2, timeout=2000,
#			     log_file="log.txt"):
#	def exper_body(treatment_id):
#		# suite = unittest.TestLoader().loadTestsFromTestCase(Webdriver)
#		# unittest.TextTestRunner(verbosity=1).run(suite)
#		test = unit_test(treatment_names[treatment_id])
#		suite = unittest.TestSuite()
#		suite.addTest(test)
#		unittest.TextTestRunner(verbosity=1).run(suite)
#	run_experiment(exper_body,
#		       num_blocks, num_agents, timeout,
#		       log_file, treatment_names)
#
#def run_experiment(exper_body,
#		   num_blocks=20, num_agents=2, timeout=2000,
#		   log_file="log.txt", treatment_names=[]):	
#	PATH="./"+log_file
#	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
#		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % log_file)
#		if response == 'n':
#			sys.exit(0)
#	fo = open(log_file, "w")
#	fo.close()
#	print "Starting Experiment"
#
#	ntreat = len(treatment_names)
#	treatment_names_string = treatments_to_string(treatment_names)
#	
#	fo = open(log_file, "a")
#	fo.write("config||"+str(num_agents)+"||"+str(ntreat)+"\n")
#	fo.write("treatnames||"+treatment_names_string+"\n")
#	for block_id in range(0, num_blocks):
#		print "Block ", block_id+1
#		table, l = getRandomTable(num_agents, ntreat)		
## 		print table
#		fo = open(log_file, "a")
#		fo.write("assign||")
#		fo.write(str(block_id)+"||")
#		for i in range(0, num_agents-1):
#			fo.write(str(l[i]) + "||")
#		fo.write(str(l[num_agents-1]) + "\n")
#		fo.close()
#		
#		procs = []
#		for agent_id in range(0,num_agents):
#			procs.append(Process(target=unit_driver.drive_unit, 
#					     args = (exper_body,
#						     block_id+1, agent_id, table[agent_id], 2000,
#						     log_file, treatment_names,)))
#		map(lambda x: x.start(), procs)
#		map(lambda x: x.join(), procs)
#	print "Experiment Complete"
