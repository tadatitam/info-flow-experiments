import sys
sys.path.append("../core")			# files from the core 
import adfisher						# adfisher wrapper function
import web.google_ads				# interacting with Google ads and Ad Settings
import converter.reader				# read log and create feature vectors
import analysis.statistics			# statistics for significance testing

log_file = 'log.gender.jobs.new2.txt'
site_file = 'jobs.txt'

def make_browser(unit_id, treatment_id):
	b = web.google_ads.GoogleAdsUnit('firefox', log_file, unit_id, treatment_id, headless=True, proxy = "proxy.pdl.cmu.edu:8080")
	return b

# Control Group treatment
def control_treatment(unit, unit_id):
	unit.opt_in()
	unit.set_gender('f')
	unit.train_with_sites(site_file)

# Experimental Group treatment
def exp_treatment(unit, unit_id):
	unit.opt_in()
	unit.set_gender('m')
	unit.train_with_sites(site_file)



# Measurement - Collects ads
def measurement(unit, unit_id, treatment_id):
	unit.collect_ads(reloads=10, delay=5, site='bbc')
	unit.get_interests()


# Shuts down the browser once we are done with it.
def cleanup_browser(unit, unit_id, treatment_id):
	unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors
def load_results():
	collection, names = converter.reader.read_log(log_file)
# 	collection = collection[:20]
	X,y,feat = converter.reader.get_feature_vectors(collection, feat_choice='ads')
	print X.shape, y.shape
	return X,y,feat
# 	return reader.get_keyword_vectors(collection, keywords=['rehab'])

# If you choose to perform ML, then test_stat is redundant. By default, correctly_classified is used,
# If not, then you can choose something, and that will be used to perform the analysis. 

def test_stat(observed_values, unit_assignments):
	return analysis.statistics.keyword_difference(observed_values, unit_assignments)
# 	return statistics.correctly_classified(observed_values, unit_assignments)

adfisher.collect_sites_from_alexa(nsites=50, output_file=site_file, browser="firefox", 
	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

adfisher.do_experiment(make_browser, [control_treatment, exp_treatment], 
						measurement, cleanup_browser,
						load_results, test_stat, ml_analysis=True, 
						num_blocks=100, num_units=10, timeout=2000,
						log_file=log_file, 
						treatment_names=["control (female)", "experimental (male)"])

