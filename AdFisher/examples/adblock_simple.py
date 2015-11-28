import sys, os
sys.path.append("/vagrant/core/web")
import adblock_ads as ab

rules = ab.AdBlockUnit().rules
site =  site="http://www.bbc.com/news/"
a = ab.AdBlockUnit(headless=True,easylist=rules)

a.collect_ads(site)
a.quit()
