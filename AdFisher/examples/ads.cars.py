import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_ads               # interacting with Google ads and Ad Settings
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.ads.cars.txt'
site_file = 'carsalexa.txt'
query_file = 'carsquery.txt'

def make_browser(unit_id, treatment_id):
    b = web.google_ads.GoogleAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=True, proxy = "proxy.pdl.cmu.edu:8080")
    return b

# Control Group treatment
def control_treatment(unit):
    pass

# Experimental Group treatment
def exp_treatment(unit):
    unit.search_and_click(query_file, clickdelay=20, clickcount=10)
    unit.visit_sites(site_file, delay=5)
    pass

# Measurement - Collects ads
def measurement(unit):
    unit.collect_ads(reloads=10, delay=5, site='bbc')
#     unit.collect_ads(reloads=2, delay=5, site='toi')


# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors
def load_results():
    collection, names = converter.reader.read_log(log_file)
    return converter.reader.get_feature_vectors(collection, feat_choice='ads')

def test_stat(observed_values, unit_assignments):
    return analysis.statistics.difference(observed_values, unit_assignments)
#   return statistics.correctly_classified(observed_values, unit_assignments)

# web.pre_experiment.alexa.collect_sites(make_browser, num_sites=50, output_file=site_file,
#     alexa_link="http://www.alexa.com/topsites/category/Top/Shopping/Vehicles")

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=100, num_units=10, timeout=2500,
                        log_file=log_file, exp_flag=True, analysis_flag=True, 
                        treatment_names=["control (female)", "experimental (male)"])

flag=False
fo = open(log_file, "r")
for line in fo:
    tim, linetype, linename, value, unit_id, treatment_id = converter.reader.interpret_log_line(line)
    if (linetype=='error'):
        print "Error detected in", linename
        flag=True
