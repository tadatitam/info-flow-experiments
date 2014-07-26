import adfisher

site_file = 'employment.txt'
log_file = 'log.genjobs.guardian.txt'

## Collect sites from alexa
# 
# adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

## Set up treatments

treatment1 = adfisher.Treatment("female")
treatment1.opt_in()
treatment1.set_gender("female")
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("male")
treatment2.opt_in()
treatment2.set_gender("male")
treatment2.visit_sites(site_file)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], collection_site="guardian", 
	samples=2, blocks=100, reloads=10, log_file=log_file)
	
## Analyze Data

adfisher.run_analysis(log_file, verbose=True)
