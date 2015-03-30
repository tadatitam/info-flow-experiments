Examples
=========

We have provided scripts to run some of the experiments we have carried out. 
Run the `demo_exp.py` and `demo_analysis.py` scripts to check everything is working. 

This document is mostly based on the script `test.gender.jobs.py`, which performs an experiment to check how two groups of browser instances visiting the same websites about jobs, but differing on the gender specified, receive different ads served by Google on bbc.com. 

### Importing files

```python
import sys
sys.path.append("../core")      # files from the core 
import adfisher                 # adfisher wrapper function
import web.google_ads           # interacting with Google ads and Ad Settings
import converter.reader         # read log and create feature vectors
import analysis.statistics      # statistics for significance testing
```
You can add or edit functions specified in `web.google_ads`, `converter.reader` or `analysis.statistics` to satisfy their specific requirements. 

### Creating units

```python
def make_browser(unit_id, treatment_id):
	b = web.google_ads.GoogleAdsUnit(browser='firefox', log_file="log.gender.jobs.txt", unit_id=unit_id, treatment_id=treatment_id, headless=True, proxy = "a.bb.ccc.dddd:8080")
	return b
```
GoogleAdsUnit is a class defined in `web.google_ads` which has functions to interact with websites to collect ads served by Google, and to add/edit Google Ad Settings. 
- You can specify the *browser* to be either 'firefox' or 'chrome'. 
- The *log_file* specifies where the  log of the experiment is stored. 
- *unit_id* is the unique id assigned to a particular browser instance, and *treatment_id* records which treatment is applied to the browser instance. These are assigned by AdFisher are provided as inputs to this function. These are not to be modified by the user.
- Set *headless* to True if you would like to run experiments in the headless mode.
- You can set a proxy with the *proxy* argument. If you do not want to use a proxy, set it to `None`, or simply do not specify it.

You can create other classes (like GoogleAdsUnit) and create experimental units using them. 

### Specifying treatments

```python
# Control Group treatment
def control_treatment(unit):
	unit.opt_in()
	unit.set_gender('f')
	unit.visit_sites(site_file="jobs.txt")

# Experimental Group treatment
def exp_treatment(unit):
	unit.opt_in()
	unit.set_gender('m')
	unit.visit_sites(site_file="jobs.txt")
```

The two functions *control_treatment()* and *exp_treatment()* specify what actions browsers receiving these treatments will perform. Taking the *control_treatment* as an example, it take a unit as an argument, then specifies that it first opt in to behavioral advertising on Google Ad Settings, then set gender to male, then visit all the websites listed in the site file. In this example, *opt_in*, *set_gender*, and *visit_sites* are methods in the GoogleAdsUnit class.

### Collecting measurements

```python
# Measurement - Collects ads
def measurement(unit):
	unit.collect_ads(reloads=10, delay=5, site='bbc')
	unit.get_interests()
```
The *measurement()* function specified which measurements should be collected by the experimental units. Here, the units collect ads served on the *site* bbc.com/news over ten successive *reloads*, each reload separated by a *delay* of 5 seconds. Our implementation of GoogleAdUnits provides functionalities for collecting text ads served by Google on 'bbc', 'guardian', 'reuters', 'bloomberg', and 'toi' (Times of India). 

### Closing units
```python
# Shut down the browser once we are done with it.
def cleanup_browser(unit):
	unit.quit()
```
Currently, this example simply has quit the unit. However, this function may be extended to perform other cleanup actions before killing units. 

### Load results
```python
# Load results reads the log_file, and creates feature vectors
def load_results():
	collection, treat_names = converter.reader.read_log(log_file="log.txt")
	return converter.reader.get_feature_vectors(collection, feat_choice='ads')
```
For loading resutls, this example uses the *read_log()* to read the log_file and return a collection of all measurements, as well as the names of the two treatments. It returns feature vectors of ads served to each unit. You may create feature vectors of your choice by modifying the relevant methods in the `reader.py` file in the converter module. In its current implementation, AdFisher can create feature vectors of words, ads, interests on Ad Settings, or news served on Google News. 

### Test statistic
```python
# Test statistic to be used by permutation test if classifier-based analysis is not used
def test_stat(observed_values, unit_assignments):
	return analysis.statistics.difference(observed_values, unit_assignments)
```
AdFisher performs permutation testing to determine significance of its findings. Permutation testing allows a user to select a test statistic. The *test_stat* function allows a user to specify the test statistic. The function *difference()* simply computes the difference between the aggregated observed values in units receiving the two treatments. 

However, if you choose to perform our Classifier based analysis, by default the accuracy of the classifier (which is an appropriate test statistic) is used as the test statistic. 

### Do experiment
```python
adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
						measurement=measurement, end_unit=cleanup_browser,
						load_results=load_results, test_stat=test_stat, ml_analysis=True, 
						num_blocks=100, num_units=10, timeout=2000,
						log_file=log_file, 
						treatment_names=["control (female)", "experimental (male)"])
```
Once all the specifications have been made, we make call the adfisher.do_experiment() function to perform all aspects of the experiment. It takes as inputs the following:
- *make_unit* which specifies how experimental units (in this case browser instances) are created.
- the *treatments* as a list.
- the *measurement*, *end_unit*, *load_results*, and *test_stat* specifications.
- the boolean *ml_analysis*, which specifies whether to perform our Classifier based analysis.
- *num_blocks* indicating the number of blocks in the experiment.
- *num_units* indicating the number of units in each block.
- *timeout* specifying the maximum time allotted for each block, at the end of which all units are killed and the next block started.
- *log_file*.
- the booleans *exp_flag* and *analysis_flag* indicate whether to perform the experiment or analysis. If *exp_flag* is True, then the experiment is performed. If *analysis_flag* is True, the analysis is performed. Both are set to True by default. 
- the *treatment_names* as a list, in the same order as spcified in *treatments*. 
