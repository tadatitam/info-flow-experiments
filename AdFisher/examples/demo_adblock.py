import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.adblock_ads              # collecting ads

log_file = 'log.demo.txt'
site_file = 'demo.txt'

# Use a bare AdBlockUnit to fetch the filterlist and load the rules. All instances
# will then share these rules
adblock_rules = web.adblock_ads.AdBlockUnit().rules

# Defines the browser that will be used as a "unit" and gives it a copy of the adblock_rules
def make_browser(unit_id, treatment_id):
    b = web.adblock_ads.AdBlockUnit(log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=False, easylist=adblock_rules)
    return b

# Control Group treatment
def control_treatment(unit):
    pass

# Experimental Group treatment
def exp_treatment(unit):
    unit.visit_sites(site_file)

# Measurement - Collects ads
# checks all the sites that adfisher could previously collect on
# (~10 minutes for src and href)
def measurement(unit):
    # from google_ads
    unit.collect_ads("http://www.foxnews.com/us/index.html")
    unit.collect_ads("http://www.bloomberg.com/")
    unit.collect_ads("http://www.reuters.com/news/us")
    unit.collect_ads("http://www.theguardian.com/us")
    unit.collect_ads("http://timesofindia.indiatimes.com/international-home")
    unit.collect_ads("http://www.bbc.com/news/")

    #from bing_ads
    for site in ["news", "weather", "entertainment", "sports", "money",
                "lifestyle", "health", "foodanddrink","travel", "autos"]:
        unit.collect_ads("http://www.msn.com/en-us/"+site)

# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

# Blank analysis
def load_results():
    pass

# Blank analysis
def test_stat(observed_values, unit_assignments):
    pass

web.pre_experiment.alexa.collect_sites(make_browser, num_sites=1, output_file=site_file,
    alexa_link="http://www.alexa.com/topsites")

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=False, 
                        num_blocks=1, num_units=2, timeout=2000,
                        log_file=log_file, exp_flag=True, analysis_flag=False, 
                        treatment_names=["control", "experimental"])
