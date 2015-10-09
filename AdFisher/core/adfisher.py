import unittest
import web.pre_experiment.alexa as alexa
import driver.driver as driver
import analysis.permutation_test
import analysis.statistics
import analysis.ml
import sys,os

def do_experiment(make_unit, treatments, measurement, end_unit,
          load_results, test_stat, ml_analysis, 
          num_blocks=1, num_units=2, timeout=2000,
          log_file="log.txt", exp_flag=True, analysis_flag=True, treatment_names=[]): 
    """
    Run an experiment.

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
    ml_analysis -- Should machine learning be used for the analysis?
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
                self.unit.log('event', 'progress-marker', "training-start")         
                treatments[treatment_id](self.unit)
                self.unit.log('event', 'progress-marker', "training-end")   
                            
                self.unit.wait_for_others() 
                    
                self.unit.log('event', 'progress-marker', "measurement-start")      
                measurement(self.unit)
                self.unit.log('event', 'progress-marker', "measurement-end") 
            def tearDown(self):
                end_unit(self.unit)
        test = Test()
        suite = unittest.TestSuite()
        suite.addTest(test)
        unittest.TextTestRunner(verbosity=1).run(suite)

    ntreat = len(treatments)
    if len(treatment_names) != ntreat:
        treatment_names = map(lambda i: str(i), range(0,ntreat))
    
    if(exp_flag):
        driver.run_experiment(exper_body,
                         num_blocks, num_units, timeout,
                         log_file, treatment_names)
    
    if(analysis_flag):
        result = load_results()
        if(len(result)==3):
            X, y, features = result[0], result[1], result[2]
        elif(len(result)==2):
            X, y = result[0], result[1]
        else:
            raw_input("Could not resolve return result from load_results(). Press Enter to exit")
            sys.exit(0)
        analysis.statistics.print_counts(X,y)
        if(ml_analysis):
            classifier, observed_values, unit_assignments = analysis.ml.train_and_test(X, y, 
                                                   splittype='timed', 
                                                   splitfrac=0.2, 
                                                   nfolds=10,
                                                   verbose=True)
            # use classifier and features here to get top ads
#             print "Extracting top features\n"
#             topk0, topk1 = analysis.ml.print_only_top_features(classifier, features, treatment_names, feat_choice="ads")
#             analysis.statistics.print_frequencies(X, y, features, topk0, topk1)
            
            print "Running permutation test\n"
            p_value = analysis.permutation_test.blocked_sampled_test(observed_values, unit_assignments, 
                                                                analysis.statistics.correctly_classified)

        else:
            observed_values, unit_assignments = X, y
            # use test_stat to get the keyword analysis
            print "Running permutation test\n"
            p_value = analysis.permutation_test.blocked_sampled_test(observed_values, unit_assignments, test_stat)
        print "p-value: ", p_value


