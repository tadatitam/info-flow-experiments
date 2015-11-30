import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.adblock_ads              # collecting ads

log_file = 'adblock.log.txt'

# Use a bare AdBlockUnit to fetch the filterlist and load the rules. All instances
# will then share these rules
adblock_rules = web.adblock_ads.AdBlockUnit(log_file=log_file).rules

# Defines the browser that will be used as a "unit" and gives it a copy of the adblock_rules
def make_browser(unit_id, treatment_id):
    b = web.adblock_ads.AdBlockUnit(log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=True,rules=adblock_rules)
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
    #unit.collect_ads("http://www.foxnews.com/us/index.html",reloads=3,delay=5)
    #unit.collect_ads("http://www.bbc.com/news/",reloads=3,delay=5)

    unit.collect_ads("http://www.foxnews.com/us/index.html")
    unit.collect_ads("http://www.bbc.com/news/")

    # from google_ads
    #unit.collect_ads("http://www.foxnews.com/us/index.html")
    #unit.collect_ads("http://www.bloomberg.com/")
    #unit.collect_ads("http://www.reuters.com/news/us")
    #unit.collect_ads("http://www.theguardian.com/us")
    #unit.collect_ads("http://timesofindia.indiatimes.com/international-home")
    #unit.collect_ads("http://www.bbc.com/news/")


    #from bing_ads
    #for site in ["news", "weather", "entertainment", "sports", "money",
    #            "lifestyle", "health", "foodanddrink","travel", "autos"]:
    #    unit.collect_ads("http://www.msn.com/en-us/"+site)

# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.save_data()
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
