import adfisher

site_file = 'cars.txt'
log_file = 'log.cars.optout.txt'

## Set up treatments

treatment1 = adfisher.Treatment("optin-cars")
treatment1.opt_in()
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("optin-cars-optout")
treatment2.opt_in()
treatment2.visit_sites(site_file)
treatment2.opt_out()


## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], samples=10, blocks=100, reloads=10, log_file=log_file, timeout=1000)

## Analyze Data

adfisher.run_analysis(log_file, verbose=True)
