import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_ads               # interacting with Google ads and Ad Settings
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.demo.txt'
site_file = 'demo.txt'

def make_browser(unit_id, treatment_id):
    b = web.google_ads.GoogleAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=True, proxy = None)
    return b

# Control Group treatment
def control_treatment(unit):
#     unit.opt_in()
#     unit.set_gender('f')
#     unit.set_age(22)
#     unit.set_language('English')
    unit.visit_sites(site_file)

# Experimental Group treatment
def exp_treatment(unit):
#     unit.opt_in()
#     unit.add_interest('basketball')
#     unit.add_interest('dating')
#     unit.remove_interest('basketball')
    unit.visit_sites(site_file)


# Measurement - Collects ads
def measurement(unit):
#     unit.get_gender()
#     unit.get_age()
#     unit.get_language()
#     unit.get_interests()
    unit.collect_ads(reloads=2, delay=5, site='bbc')


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

web.pre_experiment.alexa.collect_sites(make_browser, num_sites=5, output_file=site_file,
    alexa_link="http://www.alexa.com/topsites")

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=1, num_units=2, timeout=2000,
                        log_file=log_file, exp_flag=True, analysis_flag=False, 
                        treatment_names=["control (female)", "experimental (male)"])

flag=False
fo = open(log_file, "r")
for line in fo:
    tim, linetype, linename, value, unit_id, treatment_id = converter.reader.interpret_log_line(line)
    if (linetype=='error'):
        print "Error detected in", linename
        flag=True

if(not flag):
    print "Demo experiment complete. No known errors."
fo.close()

print "Cleaning up files"
os.remove(log_file)
os.remove(site_file)