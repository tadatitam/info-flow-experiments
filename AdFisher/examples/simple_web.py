import unittest

# Tell the experiment script where to find AdFisher
import sys
sys.path.append("../code")
import core.adfisher as adfisher
import web.browser_unit as browser_unit

log_file = 'simple_web.log.txt'

def unit_maker(unit_id):
    b = browser_unit.BrowserUnit('firefox', log_file, unit_id)
    b.opt_in()
    return b

def control(unit, unit_id):
    unit.set_gender('f', 'control')

def exper(unit, unit_id):
    unit.set_gender('m', 'exper')

def measure_age(unit, unit_id, treatment_id):
    with open(log_file, "a") as fo:
        fo.write('response: ' + str(unit_id) + ' ' + str(treatment_id) + ' ' + str(unit.get_gender()) + '\n')    


def cleanup(unit, unit_id, treatment_id):
    unit.driver.quit()


def load_results():
    observed_values = []
    observed_assignment = []
    with open(log_file, 'r') as fo:
        for line in fo:
            tokens = line.split()
            if tokens[0] == 'response:':
                unit_id = int(tokens[1])
                treatment_id = int(tokens[2])
                response_value = tokens[3]
                observed_values.append(response_value)
                observed_assignment.append(treatment_id)
    return observed_values, observed_assignment

def test_stat(observed_values, unit_assignment):
    value = 0
    for i in range(0,len(observed_values)):
        observed_num = 0
        if(observed_values[i] == 'Male'):
            observed_num = 1
        value +=  observed_num * unit_assignment[i]
    return value

adfisher.do_experiment(unit_maker, [control, exper], measure_age, cleanup, 
                       load_results, test_stat,
                       num_blocks=1, num_units=2, timeout=120,
                       log_file=log_file, treatment_names=["control", "experimental"])
