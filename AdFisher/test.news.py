import core.adfisher as adfisher

log_file = 'log.news1.txt'

## Collect sites from alexa

# adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

## Set up treatments

treatment1 = adfisher.Treatment("null1")

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_news(type='top', reloads=200, delay=30)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment1], measurement=measurement, 
	agents=2, blocks=1, log_file=log_file, timeout=20000000)

## Analyze Data

# adfisher.run_ml_analysis(log_file, verbose=True)

# adfisher.analyze_news(log_file)
