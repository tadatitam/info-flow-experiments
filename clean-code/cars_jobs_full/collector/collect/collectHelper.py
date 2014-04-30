import time, re							# time.sleep, re.split
import sys								# some prints
from selenium import webdriver			# for running the driver on websites
from datetime import datetime			# for tagging ads with datetime

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

def optOut(driver):													# Opt out of behavioral advertising on Google
	driver.set_page_load_timeout(20)
	driver.get("https://www.google.com/settings/ads")
	driver.find_element_by_xpath(".//div[@class ='lh amHZad Ld']").click()
	time.sleep(2)
	driver.execute_script("document.getElementsByName('ok')[1].click();")
	

def optIn(driver):													# Opt in to behavioral advertising on Google
	driver.set_page_load_timeout(20)
	driver.get("https://www.google.com/settings/ads")
	driver.find_element_by_xpath(".//div[@class ='lh Ld oXMGic']").click()

def login2Google(username, password, driver):
	driver.find_element_by_xpath(".//a[span[span[@class='gbit']]]").click()
	driver.find_element_by_id("Email").send_keys(username)
	driver.find_element_by_id("Passwd").send_keys(password)
	driver.find_element_by_id("signIn").click()
	driver.find_element_by_id("gbi4i").click()
	driver.find_element_by_id("gb_71").click()

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
				driver.switch_to_frame(board)
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
				driver.switch_to_default_content()
				rel = rel+1
			except:
				print "Timed Out"
				pass

def set_gender(gender, driver):										# Set gender on Google Ad Settings page
	driver.get("https://www.google.com/settings/ads")
	driver.find_element_by_xpath(".//div[@class='jf Uh']/div[@class='Uc']/div/div[@class='lh Ld c-X-Aa c-X-Ac']").click()
	s = driver.find_elements_by_xpath(".//div[@class='Wn xm']/div[@class='jy']/div/span[@class='a-p-ga']")
	if(gender == '1'):
		s[0].click()						# MALE			
	elif(gender == '0'):
		s[1].click()						# FEMALE
	driver.find_element_by_xpath(".//div[@class='Sg c-X-M']/div[@class='Dh']/div[@class='c-ca-ba a-b a-b-E Suvpmb']").click()

def get_gender(driver):												# Read gender from Google Ad Settings
	driver.get("https://www.google.com/settings/ads")
	div = driver.find_element_by_xpath(".//div[@class='jf Uh']/div[@class='Uc']/div/span[@class='PJzbEd']")
	inn = str(div.get_attribute('innerHTML'))
	return inn[0]

def get_ad_pref(choice, driver):									# Returns list of Ad preferences
	pref = []
# 		try:
	driver.get("https://www.google.com/settings/ads")
	if (choice == 1):
		driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	#For search related preferences
	elif (choice == 2):
		driver.find_element_by_xpath(".//div[@class='Rg hF']/div[@class='wf']/div[@class='jf Uh']/div[@class='Uc']/div/div[@class='lh Ld c-X-Aa c-X-Ac']").click()	#For website related preferences
	idiv = driver.find_element_by_xpath(".//div[@class='Sg kiLTY c-X-M'][@style='']")
	ints = idiv.find_elements_by_xpath(".//table[@class='wUOaYd']/tbody[@class='p4tSkf']/tr[@class='J8YeRd zm']/td[@class='b1VwRc zRvkrf']")
	for interest in ints:
		pref.append(str(interest.get_attribute('innerHTML')))
		#raw_input("Waiting...")
# 		except:
# 			pass
	return pref	

def train_with_sites(FILE, driver, id, TREATMENT):					# Visits all pages in FILE
	log('training-start', id)
	fo = open(FILE, "r")
	for line in fo:
		chunks = re.split("\|\|", line)
		site = chunks[0].strip()
		try:
			driver.set_page_load_timeout(20)
			driver.get(site)
			time.sleep(5)
			log(site, str(id)+"||"+TREATMENT)
		except:
			log("timedout-"+line.rstrip(), str(id)+"||"+TREATMENT)
			pass
	log('training-end', id)

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
			break
		c = [0]*instances
		curr_round = 0
		fo = open(LOG_FILE, "r")
		for line in fo:
			chunks = re.split("\|\|", line)
			tim = chunks[0]
			msg = chunks[1]
			id1 = chunks[2].rstrip()
			if(tim == 'g'):
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
	

def collect_ads(reloads, delay, file, driver, id, TREATMENT):
	rel = 0
	while (rel < reloads):	# number of reloads on sites to capture all ads
		time.sleep(delay)
		try:
			for i in range(0,1):
				save_ads_toi(file, driver, id, TREATMENT)
				log('reload', id)
		except:
			pass
		rel = rel + 1

def save_ads_toi(file, driver, id, TREATMENT):
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://timesofindia.indiatimes.com/international-home")
	frames = driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_right.html']")
	driver.switch_to_frame(frames[0])
	ads = driver.find_elements_by_xpath(".//tbody/tr/td/table")
	time = str(datetime.now())
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags(str(id)+"||"+str(TREATMENT)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
	driver.switch_to_default_content()
	frames = driver.find_elements_by_xpath(".//iframe[@id='adhomepage']")
	driver.switch_to_frame(frames[0])
	ads = driver.find_elements_by_xpath(".//tbody/tr/td/table")
	time = str(datetime.now())
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags(str(id)+"||"+str(TREATMENT)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
	driver.switch_to_default_content()
	frames = driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_bottom.html']")
	driver.switch_to_frame(frames[0])
	ads = driver.find_elements_by_xpath(".//tbody/tr/td/table")
	time = str(datetime.now())
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags(str(id)+"||"+str(TREATMENT)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file, "a")
		fo.write(t + '\n')
		fo.close()
	driver.switch_to_default_content()
