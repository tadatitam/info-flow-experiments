import core.adfisher as adfisher

log_file = 'log.news.login.fake.txt'
username1 = "amitdatta49"
password1 = "?^aZBTDp7Gzvmk37"
username2 = "anzornog"
password2 = "anzor1234"

## Collect sites from alexa

# adfisher.collect_sites_from_alexa(nsites=100, output_file=site_file, browser="firefox", 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

## Set up treatments

treatment1 = adfisher.Treatment("amit")
# treatment1.opt_in()
# treatment1.read_articles(keyword="USA TODAY", count=5)
treatment1.login_to_google(username1, password1)

treatment2 = adfisher.Treatment("anzor")
# treatment2.opt_in()
treatment2.login_to_google(username2, password2)

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_news(type='all', reloads=5, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], measurement=measurement, 
	agents=10, blocks=100, runs=1, log_file=log_file, timeout=2000)

# adfisher.run_experiment(treatments=[treatment1], measurement=measurement, 
# 	agents=1, blocks=1, log_file=log_file, timeout=20000000)

## Analyze Data

# adfisher.run_ml_analysis(log_file, verbose=True)

# adfisher.analyze_news(log_file)
