import sys, os, psutil
from multiprocessing import Process
from datetime import datetime           # for getting times for logging
import numpy as np
import random
import unittest
import signal                   # for timing out external calls


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
    fo.write(str(datetime.now())+"||meta||agents||"+str(num_agents)+"\n")
    fo.write(str(datetime.now())+"||meta||treatnames||"+"@|".join(treatment_names)+"\n")
    for block_id in range(0, num_blocks):
        print "Block ", block_id+1
        table, l = getRandomTable(num_agents, ntreat)       
#       print table
        fo = open(log_file, "a")
        fo.write(str(datetime.now())+"||meta||block_id start||"+str(block_id)+"\n")
        fo.write(str(datetime.now())+"||meta||assignment||")
        for i in range(0, num_agents-1):
            fo.write(str(l[i]) + "@|")
        fo.write(str(l[num_agents-1]) + "\n")
        fo.close()
        
        procs = []
        for agent_id in range(0,num_agents):
            procs.append(Process(target=drive_unit, 
                         args = (exper_body,
                             block_id+1, agent_id, table[agent_id], timeout,
                             log_file, treatment_names,)))
        map(lambda x: x.start(), procs)
        map(lambda x: x.join(timeout+5), procs)
        for proc in procs:
            if proc.is_alive():
                kill_proc_tree(proc.pid)
        fo = open(log_file, "a")
        fo.write(str(datetime.now())+"||meta||block_id end||"+str(block_id)+"\n")
        fo.close()
    print "Experiment Complete"
#   os.system('kill %d' % os.getpid())
            

class TimeoutException(Exception): 
    pass 

def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    for child in parent.get_children(recursive=True):
        child.kill()
    if including_parent:
        parent.kill()
        
def drive_unit(exper_body,
           block_id, agent_id, treatment_id, timeout,
           log_file, treatment_names):  
    
#   exper_body(agent_id, treatment_id)
    
    def signal_handler(signum, frame):
        print "Timeout!"
        fo = open(log_file, "a")
        fo.write(str(datetime.now())+"||error||block timeout||Error||"+str(treatment_id)+"||"+str(agent_id)+"\n")
        fo.close()
        print "Killing process", os.getpid()
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
#       os.kill(os.getpid(), 1)
    
    signal.alarm(0)



