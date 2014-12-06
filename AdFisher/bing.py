import core.adfisher as adfisher

log_file = 'log.bing.auto.txt'

## Collect sites from alexa

# adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

## Set up treatments

treatment1 = adfisher.Treatment("auto")
treatment1.visit_sites_on_msn("http://www.msn.com/en-us/autos")

treatment2 = adfisher.Treatment("null")

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_bing_ads(term='used cars', reloads=10, delay=5)
measurement.get_bing_ads(term='new cars', reloads=10, delay=5)
measurement.get_bing_ads(term='cars for sale', reloads=10, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], measurement=measurement, 
	agents=2, blocks=1, log_file=log_file)

## Analyze Data

# adfisher.run_ml_analysis(log_file, verbose=True)
