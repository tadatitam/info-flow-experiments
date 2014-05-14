import wdud

site_file = 'babies.txt'
log_file = 'log.babies.txt'

## Collect sites from alexa

#wdud.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
#	alexa_link="http://www.alexa.com/topsites/category/Top/Home/Family/Babies")

## Set up treatments

treatment1 = wdud.Treatment("babies")
treatment1.visit_sites(site_file)

treatment2 = wdud.Treatment("null")
#treatment2.set_gender("male")
#treatment2.visit_sites(site_file)

## Run Experiment

wdud.run_experiment(treatments=[treatment2, treatment1], samples=10, blocks=100, reloads=10, log_file=log_file)

## Analyze Data

wdud.run_analysis(log_file, verbose=True)
