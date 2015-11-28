import sys, os
sys.path.append("/vagrant/core/web")
import adblock_ads as ab

log_file = 'adblock.log.txt'
rules = ab.AdBlockUnit(log_file=log_file).rules
site = "http://www.bbc.com/news/"
a = ab.AdBlockUnit(headless=True,rules=rules,log_file=log_file)

a.collect_ads(site)
a.save_data()
a.quit()
