import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_ads               # collecting ads

log_file = 'orig.adblock.log.txt'

# Defines the browser that will be used as a "unit" and gives it a copy of the adblock_rules
def make_browser(unit_id, treatment_id):
    b = web.google_ads.GoogleAdsUnit(log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=True, browser="firefox")
    return b

# Control Group treatment (blank)
def control_treatment(unit):
    pass

# Experimental Group treatment (blank)
def exp_treatment(unit):
    pass

# Measurement - Collects ads
# checks all the sites that adfisher could previously collect on
# (~10 minutes for src and href)
def measurement(unit):

    sites = ['toi','bbc','guardian','reuters','bloomberg']
    for site in sites:
        unit.collect_ads(site=site, reloads=2, delay=5)

# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

# Blank analysis
def load_results():
    pass

# Blank analysis
def test_stat(observed_values, unit_assignments):
    pass

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=False, 
                        num_blocks=1, num_units=4, timeout=2000,
                        log_file=log_file, exp_flag=True, analysis_flag=False, 
                        treatment_names=["control", "experimental"])
