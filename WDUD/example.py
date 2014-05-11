import wdud

site_file = 'substance.txt'
log_file = 'log1.substance.txt'

# ## Collect sites from alexa
# 
# wdud.collect_sites_from_alexa(nsites=5, output_file=site_file, 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Addictions/Substance_Abuse")
# 
# ## Set up treatments
# 
# treatment1 = wdud.Treatment('null')
# treatment2 = wdud.Treatment('example')
# treatment2.add_interest("wine")
# treatment2.add_gender("male")
# treatment2.add_site_file(site_file)
# 
# ## Run Experiment
# 
# wdud.run_experiment(treatments=[treatment2, treatment1], samples=2, blocks=1, reloads=2, log_file=log_file)
# 
# ## Analyze Data

wdud.run_analysis(log_file)
