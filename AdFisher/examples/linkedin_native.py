import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.linkedin_ads
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.linkedin.txt'


def make_browser(unit_id, treatment_id):
  b = web.linkedin_ads.LinkedInAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, treatment_id=treatment_id, headless=False, proxy = None)
  return b


# Control Group treatment
def control_treatment(unit):
  unit.create_user('female','software engineer')

# Experimental Group treatment
def exp_treatment(unit):
  unit.create_user('male','software engineer')


# Measurement - Collects ads
def measurement(unit):
  unit.collect_ads(reloads=2, delay=2)


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
  pass



adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=13, num_units=2, timeout=1000, log_file=log_file, exp_flag=True,
                        treatment_names=["control (female)", "experimental (male)"])




