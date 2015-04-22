import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.google_search            # interacting with Google Search
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.search1.txt'
query_file = 'queries.txt'

def make_browser(unit_id, treatment_id):
    b = web.google_search.GoogleSearchUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=False, proxy = None)
    return b

# Control Group treatment
def control_treatment(unit):
    unit.infinitely_search_for_terms(query_file=query_file, delay=1)

# Experimental Group treatment
def exp_treatment(unit):
    unit.infinitely_search_for_terms(query_file=query_file, delay=1)


# Measurement - Collects ads
def measurement(unit):
    pass


# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors
def load_results():
    pass

def test_stat(observed_values, unit_assignments):
    pass


adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=1, num_units=2, timeout=2000000,
                        log_file=log_file, exp_flag=True, analysis_flag=False, 
                        treatment_names=["delay1", "delay10"])
