import sys
sys.path.append("../code")
import core.adfisher as adfisher
import web.google_ads
import reader.converter as converter
import analysis.ml as ml
import analysis.statistics as statistics

log_file = 'log.new.gender.jobs.txt'
site_file = 'employment.txt'

def make_browser(unit_id, treatment_id):
    b = web.google_ads.GoogleAdsUnit('firefox', log_file, unit_id, treatment_id)
    b.opt_in()
    return b

# Control Group treatment
def control_grp(unit, unit_id):
	unit.set_gender('f')
	unit.train_with_sites(site_file)

# Experimental Group treatment
def exp_grp(unit, unit_id):
	unit.set_gender('m')
# 	unit.train_with_sites(site_file)



# Measurement - Collects ads
def measure_ads(unit, unit_id, treatment_id):
	unit.collect_ads(reloads=5, delay=5, site='bbc')


# Shuts down the browser once we are done with it.
def cleanup_browser(unit, unit_id, treatment_id):
    unit.driver.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def load_results():
	collection, names = converter.read_log(log_file)
# 	collection = collection[:20]
	
	# perform ml here, then update the observed values with predictions
	X, y, features = converter.get_feature_vectors(collection, feat_choice='ads')
	classifier, observed_values, unit_assignments = ml.train_and_test(X, y, splittype='timed', 
		splitfrac=0.1, nfolds=10, verbose=True)
		
	# use classifier here to get top ads
	return observed_values, unit_assignments


def test_stat(observed_values, unit_assignments):
	return statistics.correctly_classified(observed_values, unit_assignments)

#adfisher.collect_sites_from_alexa(nsites=5, output_file=site_file, browser="firefox", 
#	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Addictions/Substance_Abuse")

adfisher.do_experiment(make_browser, [control_grp, exp_grp], 
                       measure_ads, cleanup_browser,
                       load_results, test_stat,
                       num_blocks=1, num_units=2, timeout=120,
                       log_file=log_file, 
                       treatment_names=["control (female)", "experimental (male)"])

