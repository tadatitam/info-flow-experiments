import core.adfisher as adfisher

site_file = 'mct.employment.txt'

# Collect sites from alexa

adfisher.collect_sites_from_alexa(nsites=2, output_file=site_file,
    alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

# Set up treatments

treatment1 = adfisher.Treatment("female")
treatment1.set_gender("female")
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("male")
treatment2.set_gender("male")
treatment2.visit_sites(site_file)

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_age()
measurement.get_gender()
measurement.get_language()
measurement.get_interests()
measurement.get_ads(site="toi", reloads=2, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], measurement=measurement, 
    agents=2, blocks=12, log_file="log.mct.txt")  
# Analyze Data

adfisher.run_ml_analysis(log_file="log.mct.txt")
