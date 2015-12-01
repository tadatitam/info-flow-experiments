import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_news              # interacting with Google News
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.demo.txt'
site_file = 'demo.txt'

def make_browser(unit_id, treatment_id):
    b = web.google_news.GoogleNewsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=False, proxy = None)
    return b






##======================== Make changes inside this block ========================##


# Control Group treatment
def control_treatment(unit):
    pass

# Experimental Group treatment
def exp_treatment(unit):
    pass

# Measurement - Collects ads
def measurement(unit):
    pass

# Load results from the log_file and create feature vectors. feat_choice='ads' or 'news'
def load_results():
    collection, names = converter.reader.read_log(log_file)
    return converter.reader.get_feature_vectors(collection, feat_choice='ads')
    pass

##======================== Make changes inside this block ========================##

##======================== You may want to make edits to  ========================##
##======================== num_blocks and num_units when  ========================##
##======================== calling adfisher.do_experiment()  =====================##





def test_stat(observed_values, unit_assignments):
    pass

# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=20, num_units=4, timeout=2000,
                        log_file=log_file, exp_flag=True, analysis_flag=True, 
                        treatment_names=["control", "experimental"])

