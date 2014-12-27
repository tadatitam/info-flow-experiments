import core.adfisher as adfisher

log_file = 'log.influence.txt'
site_file = "site_files/cars.txt"

## Collect sites from alexa

# adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

## Set up treatments

treatment1 = adfisher.Treatment("male18")
treatment1.opt_in()
treatment1.set_gender("male")
treatment1.set_age(18)
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("male35")
treatment2.opt_in()
treatment2.set_age(35)
treatment2.set_gender("male")
treatment2.visit_sites(site_file)

treatment3 = adfisher.Treatment("male55")
treatment3.opt_in()
treatment3.set_age(55)
treatment3.set_gender("male")
treatment3.visit_sites(site_file)

treatment4 = adfisher.Treatment("female18")
treatment4.opt_in()
treatment4.set_age(18)
treatment4.set_gender("female")
treatment4.visit_sites(site_file)

treatment5 = adfisher.Treatment("female35")
treatment5.opt_in()
treatment5.set_age(35)
treatment5.set_gender("female")
treatment5.visit_sites(site_file)

treatment6 = adfisher.Treatment("female55")
treatment6.opt_in()
treatment6.set_age(55)
treatment6.set_gender("female")
treatment6.visit_sites(site_file)

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_ads(site='bbc', reloads=10, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2, treatment3, treatment4, treatment5, treatment6], measurement=measurement, 
	agents=6, blocks=100, log_file=log_file)

## Analyze Data

# adfisher.run_ml_analysis(log_file, verbose=True)
