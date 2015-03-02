import unittest

# Tell the experiment script where to find AdFisher
import sys
sys.path.append("../code")
import core.adfisher as adfisher
import web.browser_unit as browser_unit
import core.analysis.converter as converter

log_file = 'simple_web.log.txt'

def unit_maker(unit_id):
    b = browser_unit.BrowserUnit('firefox', log_file, unit_id)
    b.opt_in()
    return b

def control(unit):
    unit.treatment_id = '0'
    unit.set_gender('f', 'control')

def exper(unit):
    unit.treatment_id = '1'
    unit.set_gender('m', 'exper')

def measure_age(unit):
    collect_ads(reloads=1, delay=5, treatment_id=unit.treatment_id, site='bbc'):

def cleanup(unit):
    unit.driver.quit()

def load_results():
    keywords = ['hi', 'bye']
    collection, names = converter.get_ads_from_log(log_file)
    # print stat.find_word_in_collection(collection, keywords)
    X,y = converter.get_keyword_vectors(collection, keywords)
    return X,y

def stat_difference_in_keywords(keyword_counts, unit_assignment):
    blocks = unit_assignment.shape[0]
    blockSize = unit_assignment.shape[1]
    kw0 = 0
    kw1 = 0
    for i in range(0,blocks):
        for j in range(0, blockSize):
            if(unit_assignment[i][j]==1):
                kw1 += keyword_counts[i][j]
            elif(unit_assignment[i][j]==0):
                kw0 += keyword_counts[i][j]
            else:
                raw_input("More classes than expected")
                print "Exiting..."
                sys.exit(0)
        # 	print kw1, kw0
    return (kw1 - kw0)


adfisher.do_experiment(unit_maker, [control, exper], measure_age, cleanup, 
                       load_results, stat_difference_in_keywords,
                       num_blocks=1, num_units=2, timeout=120,
                       log_file=log_file, treatment_names=['0', '1'])
