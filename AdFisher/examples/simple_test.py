# A very simple example of using AdFisher.  The experiments ran in
# this simple example are contrived.  We look at whether a treatment
# of appending a string to a list results in a change in that list's
# length.  (It does.)

# First, tell this experiment script where to find AdFisher
import sys
sys.path.append("../code")
import core.adfisher as adfisher

# We set the file where the results of measuring the experimental
# units will be stored.  AdFisher stores measurements in files, rather
# than passing them directly to the analysis, to save them even if an
# error crashes the program.
log_file = 'simple_test.log.txt'

# This function makes new experimental units.  The unit_id is a number
# assigned to the unit for keeping track of it.  To keep units
# exchangeable (identical), this value should only be used for
# identification.
def unit_maker(unit_id):
    return []

# The control treatment.  It does nothing: a common control.
def control(unit, unit_id):
    pass

# The experimental treatment.  It increases the length of the list.
def exper(unit, unit_id):
    unit.append('I got the experimental treatment')

# The measurement to take of units after they get one of the
# treatments.  Note that instead of returning the value of the
# measurement, it writes out to the log file.  Since a lot of stuff
# gets written to the log file, we preface our message with the tag
# 'response:' to pick it out of the file.  It then write the unit's id
# number, the id number of treatment it got, and the actual value of
# the measurement.  Printing all this out on one line makes
# reassembling the results from the log file easier, but it's not
# required.
def measure_len(unit, unit_id, treatment_id):
    measurement_value = len(unit)
    with open(log_file, "a") as fo:
        fo.write('response: ' + 
                 str(unit_id) + ' ' + 
                 str(treatment_id) + ' ' +
                 str(measurement_value) + '\n')


# A function that cleans up after experimental units.  Since our units
# are just lists and this is a garbage collected language, there's
# nothing to do.
def cleanup(unit, unit_id, treatment_id):
    pass

# A function that loads the results from the log file.  It should open
# the log, parse it, and extract the measurements.  Thus, it's sort of
# an inverse of the measurement function measure_len.  It returns two
# lists.  The first holds the measurements (the lengths of various
# lists used as experimental units).  The second holds which treatment
# each unit got.  They are both in the same order.  That is,
# observed_values[i] is the length of some unit U and
# observed_assignment[i] is the treatment that U got.  Note that the
# order is not necessarily in order by the unit_ids and doesn't need
# to be.
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

# A function that takes the two vectors created by load_results() and
# produces a number (i.e., a statistic of the data).  This test
# statistic produces the total length of all the units that got the
# second treatment (treatment id of 1).  Due to the order in which the
# control and experimental treatments are passed into the
# do_experiments function below, we know that the control treatment
# (first treatment) will be numbered 0 and that the experimental
# treatment (second treatment) will be numbered 1.  So, this is
# counting up the total length of the units in experimental group.
def test_stat(observed_values, unit_assignment):
    value = 0
    for i in range(0,len(observed_values)):
        value += observed_values[i] * unit_assignment[i]
    return value

# Now, we run the experiment and analyzes the results.  The first line
# of arguments provides the key steps of the experiment.  The second
# sets up the data analysis.  The third says how large of an
# experiment we want and how long we will wait for units that are
# taking a long time (not an issue in this experiment).  The fourth
# says where to log and provides an optional set of human readable
# names for the treatments (provided in the same order as they were on
# the first line).  The p-value for the experiment gets printed to the
# common line.  You can read simple_test.log.txt to see what got
# logged.
adfisher.do_experiment(unit_maker, [control, exper], measure_len, cleanup,
                       load_results, test_stat,
                       num_blocks=2, num_units=4, timeout=2000,
                       log_file=log_file, treatment_names=["control", "experimental"])
