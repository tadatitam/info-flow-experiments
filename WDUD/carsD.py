import wdud

site_file = 'cars2.txt'
log_file = 'log2.carsD.txt'
# 
# ## Collect sites from alexa
# 
# wdud.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Weight_Loss")
# 
# ## Set up treatments
# 
treatment1 = wdud.Treatment("in-cars")
treatment1.opt_in()
treatment1.visit_sites(site_file)

treatment2 = wdud.Treatment("in-cars-out")
treatment2.opt_in()
treatment2.visit_sites(site_file)
treatment2.opt_out()

# 
# ## Run Experiment
# 
wdud.run_experiment(treatments=[treatment2, treatment1], samples=10, blocks=100, reloads=10, log_file=log_file, timeout=1000)
# 
# ## Analyze Data

# wdud.run_analysis(log_file, verbose=True)
