import wdud

site_file = 'substance.txt'
log_file = 'log.substance.txt'

## Collect sites from alexa

wdud.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Addictions/Substance_Abuse")

## Set up treatments

treatment1 = wdud.Treatment("substance")
treatment1.visit_sites(site_file)

treatment2 = wdud.Treatment("null")
#treatment2.set_gender("male")
#treatment2.visit_sites(site_file)

## Run Experiment

wdud.run_experiment(treatments=[treatment2, treatment1], samples=10, blocks=100, reloads=10, log_file=log_file)

## Analyze Data

wdud.run_analysis(log_file, verbose=True)
