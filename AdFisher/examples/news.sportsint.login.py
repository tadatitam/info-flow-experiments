import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.google_news          # interacting with Google Search
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.sportsint.login.txt'

usern1="louisekatranjiev"
passw1="louise1234"
usern2="tziviakloeter"
passw2="tzivia1234"

def make_browser(unit_id, treatment_id):
#     b = web.google_news.GoogleNewsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
#                                        treatment_id=treatment_id, headless=False, 
#                                        proxy = None)
    b = web.google_news.GoogleNewsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
                                        treatment_id=treatment_id, headless=True, 
                                        proxy = "proxy.pdl.cmu.edu:8080")
    return b

# Control Group treatment
def control_treatment(unit):
    unit.opt_in()
    unit.login(username=usern1, password=passw1)

# Experimental Group treatment
def exp_treatment(unit):
    unit.opt_in()
    unit.login(username=usern2, password=passw2)
    unit.add_interest("sport", count=25, signedin=1)


# Measurement - Collects ads
def measurement(unit):
    unit.get_news(type='all', reloads=5, delay=5)


# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors
def load_results():
    pass

def test_stat(observed_values, unit_assignments):
    pass

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=100, num_units=10, timeout=2000,
                        log_file=log_file, exp_flag=True, analysis_flag=False, 
                        treatment_names=["optin-login", "optin-login-sportsint"])
