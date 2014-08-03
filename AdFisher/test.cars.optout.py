import core.adfisher as adfisher

site_file = 'site_files/cars.txt'
log_file = 'log.cars.optout.txt'

## Set up treatments

treatment1 = adfisher.Treatment("optin-cars")
treatment1.opt_in()
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("optin-cars-optout")
treatment2.opt_in()
treatment2.visit_sites(site_file)
treatment2.opt_out()

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_age()
measurement.get_gender()
measurement.get_language()
measurement.get_interests()
measurement.get_ads(site='toi', reloads=10, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], measurement=measurement, 
	agents=2, blocks=100, log_file=log_file)

## Analyze Data

adfisher.run_ml_analysis(log_file, verbose=True)
