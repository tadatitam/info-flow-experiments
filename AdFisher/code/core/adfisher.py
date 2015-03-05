import unittest

import alexa.alexa as alexa
import experiment_driver
import permutation_test
import sys,os

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
				self.unit.log("training-start")			
				treatments[treatment_id](self.unit, unit_id)
				self.unit.log("training-end")	
							
				self.unit.wait_for_others()	
					
				self.unit.log("measurement-start")		
				measurement(self.unit, unit_id, treatment_id)
				self.unit.log("measurement-end")				
			def tearDown(self):
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
	p_value = permutation_test.blocked_sampled_test(observed_values, observed_assignment, test_stat)
	print "p-value: ", p_value


# this should go into browser_unit

def collect_sites_from_alexa(output_file="out.txt", nsites=5, browser="firefox",alexa_link="http://www.alexa.com/topsites"):
	if(browser != "firefox" and browser != "chrome"):
		print "Illegal browser choice", browser
		return
	PATH="./"+output_file
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % output_file)
		if response == 'n':
			sys.exit(0)
	fo = open(output_file, "w")
	fo.close()
	print "Beginning Collection"
# 	os.system("python experimenter/alexa.py %s %s %s" % (output_file, alexa_link, n))
	alexa.run_script(alexa_link, output_file, nsites, browser)
	print "Collection Complete. Results stored in ", output_file

	#do_experiment(exper_body,
	#	      num_blocks, num_agents, timeout,
	#	log_file, treatment_names)
