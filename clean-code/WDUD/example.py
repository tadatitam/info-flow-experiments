import wdud
import analysis.functions as analyst

site_file = 'substance.txt'
log = 'log.substance.txt'

# wdud.collect_sites_from_alexa(pages=4, output_file=site_file, 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Addictions/Substance_Abuse")
# treatment1 = wdud.Treatment('null')
# treatment2 = wdud.Treatment('pregnancy')
# treatment2.add_site_file(site_file)
# 
# wdud.begin_experiment(treatments=[treatment2, treatment1], samples=2, blocks=2, reloads=2, log_file=log)

# coll = analyst.get_ads_from_log("log_fake.txt", old=True)

coll = analyst.get_ads_from_log("log.substance.txt", old=True)
print len(coll)
print len(coll[0]['adv'][0].data)

analyst.MLAnalysis(coll, featChoice='words')



