import core.adfisher as adfisher
import itertools 						# for combinations of attributes

log_file = 'log.influence.test.txt'
site_file = "site_files/cars.txt"

## Collect sites from alexa

# adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

## Set up treatments

samples=1
treatments = []

attributes = {'gender':["male","female"], 'age':[18,35,55], 'language':["English", "Spanish"]}
for key, value in attributes.items():
	samples = samples*len(value)
	
for comb in list(itertools.product(*attributes.values())):
	name = ''.join([str(i) for i in comb])
	treatment = adfisher.Treatment(name)
	treatment.opt_in()
	treatment.set_gender(comb[attributes.keys().index('gender')])
	treatment.set_age(comb[attributes.keys().index('age')])
	treatment.set_language(comb[attributes.keys().index('language')])
	treatments.append(treatment)

# print len(treatments)
# raw_input("wait")

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_interests()
measurement.get_ads(site='bbc', reloads=10, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=treatments[0:2], measurement=measurement, 
	agents=2, blocks=100, log_file=log_file)

## Analyze Data

print log_file
# adfisher.run_ml_analysis(log_file)
# adfisher.compute_influence(log_file)
