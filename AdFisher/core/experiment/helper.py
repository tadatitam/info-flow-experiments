import time, re														# time.sleep, re.split
import sys															# some prints
from selenium import webdriver										# for running the driver on websites
from datetime import datetime										# for tagging log with datetime
from selenium.webdriver.common.keys import Keys						# to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains	# to move mouse over

			
import google_helper as google										# functions from GoogleHelper
import google_news as gnews										# functions from GoogleNews
import bing_helper as bing											# functions from BingHelper

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

def setLogFile(FILE):
	global LOG_FILE
	LOG_FILE = FILE

def applyTreatment(driver, treatmentprof, id, treatmentid):
	treatment = treatmentprof.str
	if(treatment==''):						# null treatment
		time.sleep(5)
		return
	log('training-start', id)
	parts = re.split("\|\+\|", treatment)
	for part in parts:
		chunks = re.split("\|\\|", part)
		if(chunks[0] == 'msn'):
			bing.visit_sites(chunks[1].strip(), driver, id, treatmentid, LOG_FILE)
		if(chunks[0] == 'optout'):
			google.optOut(driver, id, treatmentid, LOG_FILE)
		if(chunks[0] == 'optin'):
			google.optIn(driver, id, treatmentid, LOG_FILE)
		if(chunks[0] == 'gender'):
			google.set_gender(chunks[1], driver, id, treatmentid, LOG_FILE)
		if(chunks[0] == 'age'):
			google.set_age(int(chunks[1]), driver, id, treatmentid, LOG_FILE)
		if(chunks[0] == 'interest'):
			print "Adding Interests"
			google.set_ad_pref(chunks[1], driver, id, treatmentid, LOG_FILE)
		if(chunks[0] == 'rinterest'):
			print "Removing Interests"
			google.remove_ad_pref(chunks[1], driver, id, treatmentid, LOG_FILE)
		if(chunks[0] == 'site'):
			train_with_sites(chunks[1], driver, id, treatmentid)
		if(chunks[0] == 'readnews'):
			gnews.read_articles(chunks[1], int(chunks[2]), driver, id, treatmentid, LOG_FILE)
		time.sleep(2)
	log('training-end', id)

def collectMeasurement(driver, measurement, id, treatmentid):
	m = measurement.str
	log('measurement-start', id)
	parts = re.split("\+", m)
	for part in parts:
		chunks = re.split("\|\|", part)
		if(chunks[0] == 'age'):
			age = google.get_age(driver)
			log("age"+"||"+str(treatmentid)+"||"+age, id)
		if(chunks[0] == 'gender'):
			gender = google.get_gender(driver)
			log("gender"+"||"+str(treatmentid)+"||"+gender, id)
		if(chunks[0] == 'language'):
			language = google.get_language(driver)
			log("language"+"||"+str(treatmentid)+"||"+language, id)
		if(chunks[0] == 'interests'):
			google.get_ad_pref(driver, id, treatmentid, LOG_FILE)
		if(chunks[0] == 'ads'):
			google.collect_ads(int(chunks[2]), int(chunks[3]), LOG_FILE, driver, id, treatmentid, chunks[1])
		if(chunks[0] == 'bads'):
			bing.collect_ads(int(chunks[2]), int(chunks[3]), LOG_FILE, driver, id, treatmentid, chunks[1])
		if(chunks[0] == 'news'):
			gnews.get_news(int(chunks[2]), int(chunks[3]), driver, id, treatmentid, LOG_FILE, chunks[1])
	log('measurement-end', id)


def train_with_sites(FILE, driver, id, treatmentid):					# Visits all pages in FILE
	fo = open(FILE, "r")
	for line in fo:
		chunks = re.split("\|\|", line)
		site = "http://"+chunks[0].strip()
		try:
			driver.set_page_load_timeout(40)
			driver.get(site)
			time.sleep(5)
			log(site+"||"+str(treatmentid), id)
# 			pref = get_ad_pref(driver)
# 			log("pref"+"||"+str(treatmentid)+"||"+"@".join(pref), id)
		except:
			log("timedout-"+line.rstrip(), id)

def log(msg, id):													# Maintains a log of visitations
	fo = open(LOG_FILE, "a")
	fo.write(str(datetime.now())+"||"+msg+"||"+str(id) + '\n')
	fo.close()   

def wait_for_others(instances, id, round):							# Makes instance with ID 'id' wait while others train 
	clear = False
	count = 0
	round = int(round)
	while(not clear):
		count += 1
		if(count > 500):
			log('breakingout', id)
			break
		c = [0]*instances
		curr_round = 0
		fo = open(LOG_FILE, "r")
		for line in fo:
			chunks = re.split("\|\|", line)
			tim = chunks[0]
			if(tim == 'treatnames'):
				continue
			msg = chunks[1]
			id1 = chunks[2].rstrip()
			if(tim == 'assign'):
				curr_round += 1
			if(round == curr_round):
				if(msg=='training-start'):
					c[int(id1)-1] += 1
				if(msg=='training-end'):
					c[int(id1)-1] -= 1
		fo.close()
		time.sleep(5)
		clear = True
		for i in range(0, instances):
			if(c[i] == 0):
				clear = clear and True
			else:
				clear = False
	

# Sweeney's experiment

def adsFromNames(NAME_FILE, OUT_FILE, reloads, driver):				# Search names, Collect ads, for Sweeney's study
	lines = [line.strip() for line in open(NAME_FILE)]
	nlist = lines[::2]
	total=0
	driver.set_page_load_timeout(10)
	driver.get("http://www.reuters.com/")
	count=0
	for q in nlist:
		count += 1
		print count
		time.sleep(5)
		sys.stdout.write(NAME_FILE[0])
		sys.stdout.flush()
		rel=0
		while(rel<reloads):
			try:
				driver.set_page_load_timeout(10)
				driver.find_element_by_id("searchfield").clear()
				driver.find_element_by_id("searchfield").send_keys(q)
				driver.find_element_by_id("searchbuttonNav").click()
				board = driver.find_element_by_css_selector("div#adcontainer1 iframe")
				driver.switch_to.frame(board)
				ads = driver.find_elements_by_css_selector("div#adBlock div div div div.adStd")
				for ad in ads:
					samay = str(datetime.now())
					a = ad.find_elements_by_xpath(".//a")
					t = (a[0].get_attribute('innerHTML'))
					l = (a[1].get_attribute('innerHTML'))
					span = ad.find_element_by_xpath(".//span")
					b = (span.get_attribute('innerHTML'))
					f = strip_tags(samay+"||"+t+"||"+l+"||"+b).encode("utf8")
					#print f
					fo = open(OUT_FILE, "a")
					fo.write(f + '\n')
					fo.close()
				driver.switch_to.default_content()
				rel = rel+1
			except:
				print "Timed Out"
				pass
