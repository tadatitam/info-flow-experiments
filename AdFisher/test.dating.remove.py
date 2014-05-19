import wdud

site_file = 'dating.txt'
log_file = 'log.dating.remove.txt'

treatment1 = wdud.Treatment("keptdating")
treatment1.visit_sites(site_file)

treatment2 = wdud.Treatment("removeddating")
treatment2.visit_sites(site_file)
treatment2.remove_interest("dating")
treatment2.remove_interest("romance")

## Run Experiment

wdud.run_experiment(treatments=[treatment1, treatment2], samples=10, blocks=100, reloads=10, log_file=log_file, timeout=1000)

## Analyze Data

wdud.run_analysis(log_file, verbose=True)
