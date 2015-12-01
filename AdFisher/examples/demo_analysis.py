import sys
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.demo.analysis.txt'

def make_browser(unit_id, treatment_id):
    pass

def control_treatment(unit):
    pass

def exp_treatment(unit):
    pass

def measurement(unit):
    pass

def cleanup_browser(unit):
    pass

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

def load_results():
    collection, names = converter.reader.read_log(log_file)
    return converter.reader.get_feature_vectors(collection, feat_choice='ads')

def test_stat(observed_values, unit_assignments):
    return analysis.statistics.difference(observed_values, unit_assignments)
#   return statistics.correctly_classified(observed_values, unit_assignments)

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment],
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        log_file=log_file, exp_flag=False, analysis_flag=True, 
                        treatment_names=["control", "experimental"])
                        
print "Demo analysis complete."
