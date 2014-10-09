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
PREF_TR = "SF Fn bft59e"
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
		chunks = re.split("\|\:\|", part)
		if(chunks[0] == 'optout'):
			optOut(driver, id, treatmentid)
		if(chunks[0] == 'optin'):
			optIn(driver, id, treatmentid)
		if(chunks[0] == 'site'):
			train_with_sites(chunks[1], driver, id, treatmentid)
		if(chunks[0] == 'gender'):
			set_gender(chunks[1], driver, id, treatmentid)
		if(chunks[0] == 'age'):
			set_age(int(chunks[1]), driver, id, treatmentid)
		if(chunks[0] == 'interest'):
			print "Adding Interests"
			set_ad_pref(chunks[1], driver, id, treatmentid)
		if(chunks[0] == 'rinterest'):
			print "Removing Interests"
			remove_ad_pref(chunks[1], driver, id, treatmentid)
		time.sleep(5)
	log('training-end', id)

def collectMeasurement(driver, measurement, id, treatmentid):
	m = measurement.str
	log('measurement-start', id)
	parts = re.split("\+", m)
	for part in parts:
		chunks = re.split("\|\|", part)
		if(chunks[0] == 'age'):
			age = get_age(driver)
			log("age"+"||"+str(treatmentid)+"||"+age, id)
		if(chunks[0] == 'gender'):
			gender = get_gender(driver)
			log("gender"+"||"+str(treatmentid)+"||"+gender, id)
		if(chunks[0] == 'language'):
			language = get_language(driver)
			log("language"+"||"+str(treatmentid)+"||"+language, id)
		if(chunks[0] == 'interests'):
			pref = get_ad_pref(driver)
			log("pref"+"||"+str(treatmentid)+"||"+"@".join(pref), id)
		if(chunks[0] == 'ads'):
			collect_ads(int(chunks[2]), int(chunks[3]), LOG_FILE, driver, id, treatmentid, chunks[1])
		time.sleep(5)
		
	log('measurement-end', id)

def optIn(driver, id=-1, treatmentid=-1):													# Opt in to behavioral advertising on Google
	driver.set_page_load_timeout(60)
	driver.get("https://www.google.com/settings/ads")
	driver.find_element_by_xpath(".//div[@class ='"+OPTIN_DIV+"']").click()
	if(id != -1):
		log("optedIn||"+str(treatmentid), id)

def optOut(driver, id=-1, treatmentid=-1):													# Opt out of behavioral advertising on Google
	driver.set_page_load_timeout(60)
	driver.get("https://www.google.com/settings/ads")
	driver.find_element_by_xpath(".//div[@class ='"+OPTOUT_DIV+"']").click()
	time.sleep(2)
	driver.execute_script("document.getElementsByName('ok')[1].click();")	
	if(id != -1):
		log("optedOut||"+str(treatmentid), id)

def login2Google(username, password, driver):
	driver.find_element_by_xpath(".//a[span[span[@class='gbit']]]").click()
	driver.find_element_by_id("Email").send_keys(username)
	driver.find_element_by_id("Passwd").send_keys(password)
	driver.find_element_by_id("signIn").click()
	driver.find_element_by_id("gbi4i").click()
	driver.find_element_by_id("gb_71").click()

def set_gender(gender, driver, id, treatmentid):										# Set gender on Google Ad Settings page
	try:
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
		driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[0].click()
		if(gender == 'm'):
			box = driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='1']/span")[0]			# MALE			
		elif(gender == 'f'):
			box = driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='2']/span")[0]			# FEMALE
		box.click()
		driver.find_elements_by_xpath(".//div[@class='"+SUBMIT_DIV+"']")[0].click()
		log("setGender="+gender+"||"+str(treatmentid), id)
	except:
		print "Could not set gender"

def get_gender(driver):												# Read gender from Google Ad Settings
	inn = ""
	try:
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
		div = driver.find_elements_by_xpath(".//span[@class='"+READ_SPAN+"']")[0]
		inn = str(div.get_attribute('innerHTML'))
	except:
		print "Could not get gender"
	return inn
	
def get_age(driver):												# Read age from Google Ad Settings
	inn = ""
	try:
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
		div = driver.find_elements_by_xpath(".//span[@class='"+READ_SPAN+"']")[1]
		inn = str(div.get_attribute('innerHTML'))
	except:
		print "Could not get age"
	return inn
		
def get_language(driver):												# Read language from Google Ad Settings
	inn = ""
	try:
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
		div = driver.find_elements_by_xpath(".//span[@class='"+READ_SPAN+"']")[2]
		inn = str(div.get_attribute('innerHTML'))
	except:
		print "Could not get language"
	return inn
	
def set_age(age, driver, id, treatmentid):										# Set age on Google Ad Settings page
	try:
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
		driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[1].click()
		if(age>=18 and age<=24):
			box = driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='1']/span")[1]
		elif(age>=25 and age<=34):	
			box = driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='2']/span")[1]
		elif(age>=35 and age<=44):	
			box = driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='3']/span")[0]
		elif(age>=45 and age<=54):	
			box = driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='4']/span")[0]
		elif(age>=55 and age<=64):
			box = driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='5']/span")[0]
		elif(age>=65):
			box = driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='6']/span")[0]
		box.click()
		driver.find_elements_by_xpath(".//div[@class='"+SUBMIT_DIV+"']")[1].click()
		log("setAge="+str(age)+"||"+str(treatmentid), id)
	except:
		print "Could not set age"


def remove_ad_pref(pref, driver, id, treatmentid, choice=2):
	try:
		prefs = get_ad_pref(driver)
		log("prepref"+"||"+str(treatmentid)+"||"+"@".join(prefs), id)
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
		if (choice == 1):
			driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	#For search related preferences
		elif (choice == 2):
			driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
		rem = []
		while(1):
			trs = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
			flag=0
			for tr in trs:
				td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']")
				div = tr.find_element_by_xpath(".//td[@class='Wq']/div")
				int = td.get_attribute('innerHTML')
				if pref.lower() in div.get_attribute('aria-label').lower():
					flag=1
					hover = ActionChains(driver).move_to_element(td)
					hover.perform()
					time.sleep(1)
					td.click()
					div.click()
					rem.append(int)
					time.sleep(2)
					break
			if(flag == 0):
				break
		driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
		log("remInterest="+"@".join(rem)+"||"+str(treatmentid), id)
	except:
		print "No interests matched '%s'. Skipping." %(pref)

def set_ad_pref(pref, driver, id, treatmentid, choice=2):									# Set an ad pref
	try:
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
		if (choice == 1):
			driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	#For search related preferences
		elif (choice == 2):
			driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
		driver.find_element_by_xpath(".//input[@class='"+PREF_INPUT+"']").send_keys(pref)
		driver.find_element_by_xpath(".//div[@class='"+PREF_INPUT_FIRST+"']").click()
		time.sleep(1)
		trs = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
		for tr in trs:
			td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']").get_attribute('innerHTML')
			print td
			log("setInterests="+td+"||"+str(treatmentid), id)
		driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
	except:
		print "Error setting interests containing '%s'. Skipping." %(pref)
	
def get_ad_pref(driver, choice=2):									# Returns list of Ad preferences
	pref = []
	try:
		driver.set_page_load_timeout(40)
		driver.get("https://www.google.com/settings/ads")
		if (choice == 1):
			driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	#For search related preferences
		elif (choice == 2):
			driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
		ints = driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']/td[@class='"+PREF_TD+"']")
	# 	print ints
		for interest in ints:
			pref.append(str(interest.get_attribute('innerHTML')))
			#raw_input("Waiting...")
	except:
		print "Could not get any interests"
		pass
	return pref	

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
	

def collect_ads(reloads, delay, file, driver, id, treatmentid, site):
	rel = 0
	while (rel < reloads):	# number of reloads on sites to capture all ads
		time.sleep(delay)
		try:
			for i in range(0,1):
				s = datetime.now()
				if(site == 'toi'):
					save_ads_toi(file, driver, id, treatmentid)
				elif(site == 'bbc'):
					save_ads_bbc(file, driver, id, treatmentid)
				elif(site == 'guardian'):
					save_ads_guardian(file, driver, id, treatmentid)
				elif(site == 'reuters'):
					save_ads_reuters(file, driver, id, treatmentid)
				elif(site == 'bloomberg'):
					save_ads_bloomberg(file, driver, id, treatmentid)
				else:
					raw_input("No such site found: %s!" % site)
				e = datetime.now()
				log('loadtime||'+str(e-s), id)
				log('reload', id)
		except:
			log('errorcollecting', id)
			pass
		rel = rel + 1

def save_ads_bloomberg(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://www.bloomberg.com/")	
	tim = str(datetime.now())
	frame0 = driver.find_element_by_xpath(".//iframe[@src='/bcom/home/iframe/google-adwords']")
	driver.switch_to.frame(frame0)
	frame1 = driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
	driver.switch_to.frame(frame1)
	time.sleep(2)
	frame2 = driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
	driver.switch_to.frame(frame2)
	lis = driver.find_elements_by_css_selector("div#adunit div#ads ul li")
	for li in lis:
		t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
		l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
		b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
		f = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file, "a")
		fo.write(f + '\n')
		fo.close()
	driver.switch_to.default_content()
	driver.switch_to.default_content()
	driver.switch_to.default_content()

def save_ads_reuters(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://www.reuters.com/news/us")	
	tim = str(datetime.now())
	frame0 = driver.find_element_by_xpath(".//iframe[@id='pmad-rt-frame']")
	driver.switch_to.frame(frame0)
	frame1 = driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
	driver.switch_to.frame(frame1)
	time.sleep(2)
	frame2 = driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
	driver.switch_to.frame(frame2)
	lis = driver.find_elements_by_css_selector("div#adunit div#ads ul li")
	for li in lis:
		t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
		l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
		b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
		f = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file, "a")
		fo.write(f + '\n')
		fo.close()
	driver.switch_to.default_content()
	driver.switch_to.default_content()
	driver.switch_to.default_content()

def save_ads_guardian(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://www.theguardian.com/us")	
	time = str(datetime.now())
	els = driver.find_elements_by_css_selector("div#google-ads-container div.bd ul li")
	for el in els:
		t = el.find_element_by_css_selector("p.t6 a").get_attribute('innerHTML')
		ps = el.find_elements_by_css_selector("p")
		b = ps[1].get_attribute('innerHTML')
		l = ps[2].find_element_by_css_selector("a").get_attribute('innerHTML')
		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()

def save_ads_toi(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://timesofindia.indiatimes.com/international-home")
	time = str(datetime.now())
	frames = driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_right.html']")
	driver.switch_to.frame(frames[0])
	ads = driver.find_elements_by_xpath(".//tbody/tr/td/table")
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
	driver.switch_to.default_content()
	frames = driver.find_elements_by_xpath(".//iframe[@id='adhomepage']")
	driver.switch_to.frame(frames[0])
	ads = driver.find_elements_by_xpath(".//tbody/tr/td/table")
	time = str(datetime.now())
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
	driver.switch_to.default_content()
	frames = driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_bottom.html']")
	driver.switch_to.frame(frames[0])
	ads = driver.find_elements_by_xpath(".//tbody/tr/td/table")
	time = str(datetime.now())
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
	driver.switch_to.default_content()

def save_ads_bbc(file, driver, id, treatmentid):
	sys.stdout.write(".")
	sys.stdout.flush()
# 		global ad_int
	driver.set_page_load_timeout(60)
	driver.get("http://www.bbc.com/news/")
	time = str(datetime.now())
	els = driver.find_elements_by_css_selector("div#bbccom_adsense_mpu div ul li")
	for el in els:
		t = el.find_element_by_css_selector("h4 a").get_attribute('innerHTML')
		ps = el.find_elements_by_css_selector("p")
		b = ps[0].get_attribute('innerHTML')
		l = ps[1].find_element_by_css_selector("a").get_attribute('innerHTML')
		t = strip_tags("ad||"+str(id)+"||"+str(treatmentid)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()

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
