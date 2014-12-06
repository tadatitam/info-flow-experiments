import time, re														# time.sleep, re.split
import sys															# some prints
from selenium import webdriver										# for running the driver on websites
from datetime import datetime										# for tagging log with datetime
from selenium.webdriver.common.keys import Keys						# to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains	# to move mouse over

# Google ad settings page class declarations

OPTIN_DIV = "ri Lf ZK"
OPTOUT_DIV = "ri wy Lf"
EDIT_DIV = "ri Lf c-ea-pb c-ea-Ub"
READ_SPAN = "uh"
RADIO_DIV = "a-o ow RL"
SUBMIT_DIV = "c-T-S a-b a-b-B zo"

PREF_INPUT = "XL a-oa TF"
PREF_INPUT_FIRST = "QF NF na"
PREF_TR = "SF Fn"
PREF_TD = "Vq UL"
PREF_OK_DIV = "c-T-S a-b a-b-B XE ty"


# strip html

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def log(msg, id):													# Maintains a log of visitations
	fo = open(LOG_FILE, "a")
	fo.write(str(datetime.now())+"||"+msg+"||"+str(id) + '\n')
	fo.close()   

def visit_sites(link, driver, id, treatmentid, log_file):
	global LOG_FILE 
	LOG_FILE = log_file
	
	for i in range(0,10):
		driver.get(link)
		els = driver.find_elements_by_css_selector("li.skylinehl1u1 a")
		try:
			els[i].click()
			time.sleep(5)
			print driver.current_url
			site = driver.current_url
			log(site+"||"+str(treatmentid), id)
		except:
			print i, "failed"
			print "Error:", sys.exc_info()[0]
	
	for i in range(0,8):
		driver.get(link)
		els = driver.find_elements_by_css_selector("li.hl1u1 a")
		try:
# 			print els[i].get_attribute('innerHTML')
			els[i].click()
			time.sleep(5)
			print driver.current_url
			site = driver.current_url
			log(site+"||"+str(treatmentid), id)
		except:
			print i, "failed"
			print "Error:", sys.exc_info()[0]
	
	for i in range(0,3):
		driver.get(link)
		els = driver.find_elements_by_css_selector("li.hl1u3b a")
		try:
			els[i].click()
			time.sleep(5)
			print driver.current_url
			site = driver.current_url
			log(site+"||"+str(treatmentid), id)
		except:
			print i, "failed"
			print "Error:", sys.exc_info()[0]
	
def collect_ads(reloads, delay, file, driver, id, treatmentid, term):	
	for rel in range(0,reloads):
		sys.stdout.write(".")
		sys.stdout.flush()
		driver.get("http://www.bing.com/")
		driver.find_element_by_id("sb_form_q").send_keys(term)
		driver.find_element_by_id("sb_form_go").click()
		samay = str(datetime.now())
		
		els = driver.find_elements_by_css_selector("div#b_content ol#b_results li.b_ad ul li div.sb_add.sb_adTA ")
# 		print len(els)
		for el in els:
			try:
				t = el.find_element_by_css_selector("h2 a").get_attribute("innerHTML")
				l = el.find_element_by_css_selector("div.b_caption div.b_attribution cite a").get_attribute("innerHTML")
				b = el.find_element_by_css_selector("div.b_caption p.sb_addesc a").get_attribute("innerHTML")
				t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+samay+"||"+t+"||"+l+"||"+b).encode("utf8")
# 				print t
				fo = open(file, "a")
				fo.write(t + '\n')
				fo.close()
			except:
				print el.get_attribute("innerHTML")
				print "Error:", sys.exc_info()[0]
		
		els = driver.find_elements_by_css_selector("ol#b_context li.b_ad ul li div.sb_add.sb_adTA ")
# 		print len(els)
		for el in els:
			try:
				t = el.find_element_by_css_selector("h2 a").get_attribute("innerHTML")
				l = el.find_element_by_css_selector("div.b_caption div.b_attribution cite a").get_attribute("innerHTML")
				b = el.find_element_by_css_selector("div.b_caption p.sb_addesc a").get_attribute("innerHTML")
				t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+samay+"||"+t+"||"+l+"||"+b).encode("utf8")
# 				print t
				fo = open(file, "a")
				fo.write(t + '\n')
				fo.close()
			except:
				print el.get_attribute("innerHTML")
				print "Error:", sys.exc_info()[0]
		
		time.sleep(delay)
