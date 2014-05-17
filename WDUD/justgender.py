import wdud

# site_file = 'cars2.txt'
log_file = 'log.gender.txt'
# 
# ## Collect sites from alexa
# 
# wdud.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Weight_Loss")
# 
# ## Set up treatments
# 
treatment1 = wdud.Treatment("male")
treatment1.opt_in()
treatment1.set_gender("male")

treatment2 = wdud.Treatment("female")
treatment2.opt_in()
treatment2.set_gender("female")

# 
# ## Run Experiment
# 
wdud.run_experiment(treatments=[treatment2, treatment1], samples=2, blocks=100, reloads=10, log_file=log_file, timeout=1000)
# 
# ## Analyze Data

# wdud.run_analysis(log_file, verbose=True)
