import adfisher

site_file = 'dating_all.txt'
log_file = 'log.shortdate.txt'

adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
	alexa_link="http://www.alexa.com/topsites/category/Top/Society/Relationships/Dating")

adfisher.shortlist_sites(site_file, target_file="int_"+site_file, timeout=100)

## Set up treatments

treatment1 = adfisher.Treatment("keptdating")
treatment1.visit_sites("int_"+site_file)

treatment2 = adfisher.Treatment("removeddating")
treatment2.visit_sites("int_"+site_file)
treatment2.remove_interest("dating")
treatment2.remove_interest("romance")
treatment2.remove_interest("relationship")

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], samples=10, blocks=100, reloads=10, log_file=log_file, timeout=1000)

## Analyze Data

adfisher.run_analysis(log_file, verbose=True)
