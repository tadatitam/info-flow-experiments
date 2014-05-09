import wdud
import analysis.functions as analyst

file = 'substance.txt'
log = 'log.substance.txt'

# wdud.collect_sites_from_alexa(pages=1, output_file=file, 
# 	alexa_link="http://www.alexa.com/topsites/category/Top/Health/Reproductive_Health/Pregnancy_and_Birth")
# treatment1 = wdud.Treatment('null')
# treatment2 = wdud.Treatment('pregnancy')
# treatment2.add_site_file(file)

# wdud.begin_experiment(treatments=[treatment2, treatment1], samples=2, blocks=2, reloads=2, log_file=log)

coll = analyst.get_ads_from_log("log_10i_245r_linux", old=True)
# print coll
print len(coll)
print len(coll[0]['adv'][0].data)
# print len(coll[0]['adv'].data)
analyst.MLAnalysis(coll)

