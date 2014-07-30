import adfisher

site_file = 'cars.txt'
log_file = 'log.cars.choice3.txt'

## Set up treatments

treatment1 = adfisher.Treatment("cars")
treatment1.opt_in()
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("cars-removeall")
treatment2.opt_in()
treatment2.visit_sites(site_file)
treatment2.remove_interest("")

treatment3 = adfisher.Treatment("null")
treatment3.opt_in()


## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2, treatment3], 
	samples=12, blocks=100, reloads=10, log_file=log_file, timeout=1000)

## Analyze Data

adfisher.run_analysis(log_file, verbose=True)
