import sys
sys.path.append("../core")			# files from the core 
import adfisher						# adfisher wrapper function
import web.bing_ads				# interacting with Bing ads and Ad Settings
import converter.reader				# read log and create feature vectors
import analysis.statistics			# statistics for significance testing

log_file = 'log.bing.txt'

def make_browser(unit_id, treatment_id):
	b = web.bing_ads.BingAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
		treatment_id=treatment_id, headless=False, proxy = '127.0.0.1:8080')
	return b

# Control Group treatment
def control_treatment(unit):
	unit.collect_msn_ads(10,5, 'travel')

# Experimental Group treatment
def exp_treatment(unit):
	unit.collect_msn_ads(10,5, 'autos')

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
	#collection, names = converter.reader.read_log(log_file)
	return True
	#return converter.reader.get_feature_vectors(collection, feat_choice='ads')

# If you choose to perform ML, then test_stat is redundant. By default, correctly_classified is used,
# If not, then you can choose something, and that will be used to perform the analysis. 

def test_stat(observed_values, unit_assignments):
	return True
# return analysis.statistics.difference(observed_values, unit_assignments)
# 	return statistics.correctly_classified(observed_values, unit_assignments)


adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
						measurement=measurement, end_unit=cleanup_browser,
						load_results=load_results, test_stat=test_stat, ml_analysis=False, 
						num_blocks=1, num_units=2, timeout=2000,
						log_file=log_file,
						treatment_names=["control (auto)", "experimental (auto)"])

