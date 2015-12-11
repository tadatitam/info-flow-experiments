import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_news              # interacting with Google News
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.group_ex2.txt'
site_file = 'group_ex2.txt'

def make_browser(unit_id, treatment_id):
    if treatment_id==0:
        b = web.google_ads.GoogleAdsUnit(browser='chrome', log_file=log_file, unit_id=unit_id, 
            treatment_id=treatment_id, headless=False, proxy = None)
        return b
    else:
        b = web.google_ads.GoogleAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
            treatment_id=treatment_id, headless=False, proxy = None)
        return b




##======================== Make changes inside this block ========================##


# Control Group treatment
def control_treatment(unit):
    unit.search_and_click(query_file = 'group_ex2_queries.txt', clickdelay = 10, clickcount = 3)

# Experimental Group treatment
def exp_treatment(unit):
    unit.search_and_click(query_file = 'group_ex2_queries.txt', clickdelay = 10, clickcount = 3)

# Measurement - Collects ads
def measurement(unit):
    unit.collect_ads(reloads=10, delay=5, site='toi')
    #unit.get_news(type='top', reloads=5, delay=10)

# Load results from the log_file and create feature vectors. feat_choice='ads' or 'news'
def load_results():
    collection, names = converter.reader.read_log(log_file)
    return converter.reader.get_feature_vectors(collection, feat_choice='ads')
    

##======================== Make changes inside this block ========================##

##======================== You may want to make edits to  ========================##
##======================== num_blocks and num_units when  ========================##
##======================== calling adfisher.do_experiment()  =====================##




def test_stat(observed_values, unit_assignments):
    return analysis.statistics.difference(observed_values, unit_assignments)

# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=24, num_units=6, timeout=2000,
                        log_file=log_file, exp_flag=False, analysis_flag=True, 
                        treatment_names=["control (chrome)", "experimental (firefox)"])

