import sys
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_ads               # interacting with Google ads and Ad Settings
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.group_baseline.txt'
site_file = 'group_baseline.txt'

def make_browser(unit_id, treatment_id):
    #b = web.google_ads.GoogleAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
    #    treatment_id=treatment_id, headless=False, proxy = None)
    #return b
    if treatment_id==0:
        b = web.google_ads.GoogleAdsUnit(browser='chrome', log_file=log_file, unit_id=unit_id, 
            treatment_id=treatment_id, headless=False, proxy = None)
        return b
    else:
        b = web.google_ads.GoogleAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
            treatment_id=treatment_id, headless=False, proxy = None)
        return b
web.pre_experiment.alexa.collect_sites(make_browser, num_sites=5, output_file=site_file,
    alexa_link="http://www.alexa.com/topsites/category/Top/Business/Accounting")
    
    
# Control Group treatment
def control_treatment(unit):
    pass
    #unit.visit_sites(site_file)
# Experimental Group treatment
def exp_treatment(unit):
    #unit.visit_sites(site_file)
    pass

# Measurement - Collects ads
def measurement(unit):
    unit.collect_ads(reloads=10, delay=5, site='bbc')
    

# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

# Load results reads the log_file, and creates feature vectors
def load_results():
    collection, names = converter.reader.read_log(log_file)
    return converter.reader.get_feature_vectors(collection, feat_choice='ads')

# If you choose to perform ML, then test_stat is redundant. By default, correctly_classified is used,
# If not, then you can choose something, and that will be used to perform the analysis. 

def test_stat(observed_values, unit_assignments):
    return analysis.statistics.difference(observed_values, unit_assignments)
#   return statistics.correctly_classified(observed_values, unit_assignments)

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=20, num_units=4, timeout=2000,
                        log_file=log_file, exp_flag=False, analysis_flag=True, 
                        treatment_names=["control (chrome)", "experimental (firefox)"])

