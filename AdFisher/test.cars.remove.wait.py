import adfisher
import time

site_file = 'cars.txt'
log_file = 'log.cars.remove.wait.txt'

## Set up treatments

treatment1 = adfisher.Treatment("cars-removeall")
treatment1.opt_in()
treatment1.visit_sites(site_file)
treatment1.remove_interest("")

treatment2 = adfisher.Treatment("null")
treatment2.opt_in()

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], samples=10, blocks=100, reloads=10, log_file=log_file, timeout=1000)

## Analyze Data

adfisher.run_analysis(log_file, verbose=True)
