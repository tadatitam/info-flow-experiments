import adfisher

site_file = 'dating_all.txt'
# log_file = 'log.gender.txt'

adfisher.shortlist_sites(site_file, target_file="int_"+site_file)

log_file = 'log.dating.remove.txt'

## Set up treatments

treatment1 = adfisher.Treatment("keptdating")
treatment1.visit_sites("int_"+site_file)

treatment2 = adfisher.Treatment("removeddating")
treatment2.visit_sites("int_"+site_file)
treatment2.remove_interest("dating")
treatment2.remove_interest("romance")

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], samples=10, blocks=100, reloads=10, log_file=log_file, timeout=1000)

## Analyze Data

adfisher.run_analysis(log_file, verbose=True)
