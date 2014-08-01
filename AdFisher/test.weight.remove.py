import adfisher

site_file = 'weight.txt'
target_file = "int_"+site_file
log_file = 'log.weight.remove.txt'

## Collect sites from alexa

# adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Weight_Loss")

adfisher.shortlist_sites(site_file, target_file, timeout=100)

## Set up treatments

treatment1 = adfisher.Treatment("keptweight")
treatment1.visit_sites(target_file)

treatment2 = adfisher.Treatment("removedweight")
treatment2.visit_sites(target_file)
treatment2.remove_interest("fitness")
treatment2.remove_interest("weight")

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], 
	samples=10, blocks=10, reloads=10, log_file=log_file, timeout=1000)

## Analyze Data

adfisher.run_analysis(log_file, verbose=True)
