import core.adfisher as adfisher

site_file = 'substance.txt'
log_file = 'log.substance.txt'

## Collect sites from alexa

adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Addictions/Substance_Abuse")

## Set up treatments

treatment1 = adfisher.Treatment("substance")
treatment1.opt_in()
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("null")
treatment2.opt_in()

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_age()
measurement.get_gender()
measurement.get_language()
measurement.get_interests()
measurement.get_ads(site='bbc', reloads=10, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], measurement=measurement, 
	agents=10, blocks=100, log_file=log_file)
	
## Analyze Data

adfisher.run_ml_analysis(log_file, verbose=True)
