import unittest

# Tell the experiment script where to find AdFisher
import sys
sys.path.append("../code")
import core.adfisher as adfisher

log_file = 'simple_test.log.txt'

def unit_maker(unit_id):
    return []

def control(unit, unit_id):
    pass

def exper(unit, unit_id):
    unit.append('expr')

def measure_len(unit, unit_id, treatment_id):
    with open(log_file, "a") as fo:
        fo.write('response: ' + str(unit_id) + ' ' + str(treatment_id) + ' ' + str(len(unit)) + '\n')

def cleanup(unit, unit_id, treatment_id):
    pass

def load_results():
    observed_values = []
    observed_assignment = []
    with open(log_file, 'r') as fo:
        for line in fo:
            tokens = line.split()
            if tokens[0] == 'response:':
                unit_id = int(tokens[1])
                treatment_id = int(tokens[2])
                response_value = int(tokens[3])
                observed_values.append(response_value)
                observed_assignment.append(treatment_id)
    return observed_values, observed_assignment

def test_stat(observed_values, unit_assignment):
    value = 0
    for i in range(0,len(observed_values)):
        value += observed_values[i] * unit_assignment[i]
    return value

adfisher.do_experiment(unit_maker, [control, exper], measure_len, cleanup,
                       load_results, test_stat,
                       num_blocks=2, num_units=4, timeout=2000,
                       log_file=log_file, treatment_names=["control", "experimental"])
