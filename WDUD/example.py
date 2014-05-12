import wdud

site_file = 'employment.txt'
log_file = 'log.test.txt'

## Collect sites from alexa

wdud.collect_sites_from_alexa(nsites=5, output_file=site_file, browser="firefox", 
	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

## Set up treatments

treatment1 = wdud.Treatment("female")
treatment1.set_gender("female")
treatment1.visit_sites(site_file)

treatment2 = wdud.Treatment("male")
treatment2.set_gender("male")
treatment2.visit_sites(site_file)

## Run Experiment

wdud.run_experiment(treatments=[treatment2, treatment1], samples=2, blocks=10, reloads=2, log_file=log_file)

## Analyze Data

wdud.run_analysis(log_file, verbose=True)
