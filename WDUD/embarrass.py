import wdud

site_file = 'weight2.txt'
log_file = 'log2.weight.txt'
# 
# ## Collect sites from alexa
# 
# wdud.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Weight_Loss")
# 
# ## Set up treatments
# 
treatment1 = wdud.Treatment("null")

treatment2 = wdud.Treatment("weight")
treatment2.visit_sites(site_file)
treatment2.remove_interest("fitness")
# 
# ## Run Experiment
# 
wdud.run_experiment(treatments=[treatment2, treatment1], samples=2, blocks=10, reloads=1, log_file=log_file)
# 
# ## Analyze Data

# wdud.run_analysis(log_file, verbose=True)
