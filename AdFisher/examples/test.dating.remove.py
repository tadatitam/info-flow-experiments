import core.adfisher as adfisher

site_file = 'site_files/dating.txt'
log_file = 'log.dating.remove.txt'

## Set up treatments

treatment1 = adfisher.Treatment("keptdating")
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("removeddating")
treatment2.visit_sites(site_file)
treatment2.remove_interest("dating")
treatment2.remove_interest("romance")

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_ads(site='bbc', reloads=10, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], measurement=measurement, 
	agents=2, blocks=10, log_file=log_file)

## Analyze Data

adfisher.run_kw_analysis(log_file, keywords=['dating'], verbose=True)
