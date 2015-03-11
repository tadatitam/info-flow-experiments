import sys
sys.path.append("../code")
import core.adfisher as adfisher
import web.google_ads
import reader.converter as converter
import analysis.ml as ml
import analysis.statistics as statistics

log_file = 'log.gender.txt'
site_file = 'employment.txt'

def make_browser(unit_id, treatment_id):
    b = web.google_ads.GoogleAdsUnit('firefox', log_file, unit_id, treatment_id)
    return b

# Control Group treatment
def control_treatment(unit, unit_id):
	unit.opt_in()
	unit.set_gender('f')
# 	unit.train_with_sites(site_file)

# Experimental Group treatment
def exp_treatment(unit, unit_id):
	unit.opt_in()
	unit.set_gender('m')
# 	unit.train_with_sites(site_file)



# Measurement - Collects ads
def measurement(unit, unit_id, treatment_id):
	unit.collect_ads(reloads=5, delay=5, site='bbc')


# Shuts down the browser once we are done with it.
def cleanup_browser(unit, unit_id, treatment_id):
    unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors
def load_results():
	collection, names = converter.read_log(log_file)
	collection = collection[:20]
# 	return converter.get_feature_vectors(collection, feat_choice='ads')
	return converter.get_keyword_vectors(collection, keywords=['rehab'])

# If you choose to perform ML, then test_stat is redundant. By default, correctly_classified is used,
# If not, then you can choose something, and that will be used to perform the analysis. 

def test_stat(observed_values, unit_assignments):
	return statistics.keyword_difference(observed_values, unit_assignments)
# 	return statistics.correctly_classified(observed_values, unit_assignments)

# adfisher.collect_sites_from_alexa(nsites=5, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Addictions/Substance_Abuse")

adfisher.do_experiment(make_browser, [control_treatment, exp_treatment], 
                       measurement, cleanup_browser,
                       load_results, test_stat, ml_analysis=False, 
                       num_blocks=20, num_units=2, timeout=120,
                       log_file=log_file, 
                       treatment_names=["control (female)", "experimental (male)"])

