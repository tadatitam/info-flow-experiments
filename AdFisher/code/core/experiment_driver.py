import sys, os
from multiprocessing import Process
from datetime import datetime  # for getting times for computation
import numpy as np
import random
import unittest
import signal  # for timing out external calls


def treatments_to_string(treatment_names):
	"""
	Converts list of strings in a single string.
	"""
	treatment_names_string = ""
	for i in range(0,len(treatment_names)):
		if(i==0):
			treatment_names_string += treatment_names[i]
		else:
			treatment_names_string += "||" + treatment_names[i]
	return treatment_names_string

def getRandomTable(num_agents, ntreat):
	l = np.arange(num_agents)
	random.shuffle(l)
	if(num_agents % ntreat != 0):
		print "Warning: agents in each round [%s] not divisible by number of treatments [%s]" %(num_agents, ntreat)
		print "Assignment done randomly"
		raw_input("Press enter to continue")
	size = num_agents/ntreat
	table = [ntreat]*num_agents
	for i in range(0, ntreat):
		for j in range(size*i, size*(i+1)):
			table[l[j]] = i
	return table, l

def run_experiment(exper_body,
		   num_blocks, num_agents, timeout,
		   log_file="log.txt", treatment_names=[]):	
	PATH="./"+log_file
	if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
		response = raw_input("This will overwrite file %s... Continue? (Y/n)" % log_file)
		if response == 'n':
			sys.exit(0)
	fo = open(log_file, "w")
	fo.close()
	print "Starting Experiment"

	ntreat = len(treatment_names)
	treatment_names_string = treatments_to_string(treatment_names)
	
	fo = open(log_file, "a")
	fo.write("config||"+str(num_agents)+"||"+str(ntreat)+"\n")
	fo.write("treatnames||"+treatment_names_string+"\n")
	for block_id in range(0, num_blocks):
		print "Block ", block_id+1
		table, l = getRandomTable(num_agents, ntreat)		
# 		print table
		fo = open(log_file, "a")
		fo.write("assign||")
		fo.write(str(block_id)+"||")
		for i in range(0, num_agents-1):
			fo.write(str(l[i]) + "||")
		fo.write(str(l[num_agents-1]) + "\n")
		fo.close()
		
		procs = []
		for agent_id in range(0,num_agents):
			procs.append(Process(target=drive_unit, 
					     args = (exper_body,
						     block_id+1, agent_id, table[agent_id], timeout,
						     log_file, treatment_names,)))
					     #  args=(i, num_agents, table[i], num_runs, log_file, j+1, treatment_names, measurement_name, timeout)))
		map(lambda x: x.start(), procs)
		map(lambda x: x.join(timeout+5), procs)
	print "Experiment Complete"

class TimeoutException(Exception): 
    pass 

def drive_unit(exper_body,
	       block_id, agent_id, treatment_id, timeout,
	       log_file, treatment_names):	

	def signal_handler(signum, frame):
		print "Timeout!"
		fo = open(log_file, "a")
		fo.write(str(datetime.now())+"||TimedOut||"+str(treatment_id)+"||"+str(agent_id)+"\n")
		fo.close()
		raise TimeoutException("Timed out!")
	
	old_handler = signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(timeout)
	try:
		exper_body(agent_id, treatment_id)
	except TimeoutException:
		return
	finally:
		print "Instance", agent_id, "exiting!"
		signal.signal(signal.SIGALRM, old_handler)
	
	signal.alarm(0)



