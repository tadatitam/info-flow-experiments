import time, re # time.sleep, re.split
import sys # some prints
import os, platform # for running  os, platform specific function calls
from selenium import webdriver # for running the driver on websites
from datetime import datetime # for tagging log with datetime
from selenium.webdriver.common.keys import Keys # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains # to move mouse over

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


class BrowserUnit:

    # Google ad settings page class declarations


    def __init__(self, browser, log_file, unit_id):
        if(browser=='firefox'):
            if (platform.system()=='Darwin'):
                self.driver = webdriver.Firefox()
            elif (platform.system()=='Linux'):
                self.driver = webdriver.Firefox()
            else:
                print "Unidentified Platform"
                sys.exit(0)
        elif(browser=='chrome'):
            print "WARNING: Expecting chromedriver at specified location !!"
            if (platform.system()=='Darwin'):
                chromedriver = "./chromedriver/chromedriver_mac"
                os.environ["webdriver.chrome.driver"] = chromedriver
                self.driver = webdriver.Chrome(executable_path=chromedriver)
            elif (platform.system() == 'Linux'):
                chromedriver = "./chromedriver/chromedriver_linux"
                os.environ["webdriver.chrome.driver"] = chromedriver
                chrome_option = webdriver.ChromeOptions()
                chrome_option.add_argument("--proxy-server=yogi.pdl.cmu.edu:3128" )
                self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_option)
            else:
                print "Unidentified Platform"
                sys.exit(0)
        else:
            print "Unsupported Browser"
            sys.exit(0)
        self.driver.implicitly_wait(10)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.driver.set_page_load_timeout(40)
        self.accept_next_alert = True
        self.log_file = log_file
        self.unit_id = unit_id
        self.treatment_id = treatment_id


    def log(self, msg):	
        """Maintains a log of visitations"""
        fo = open(self.log_file, "a")
        fo.write(str(datetime.now())+"||"+msg+"||"+str(self.unit_id) + '\n')
        fo.close()   


    def applyTreatment(self, treatmentprof):
        driver = self.driver
        treatment = treatmentprof.str
        if(treatment==''):						# null treatment
            time.sleep(5)
            return
        log('training-start')

    def collectMeasurement(self, driver, measurement):
	m = measurement.str
	log('measurement-start')
	parts = re.split("\+", m)
	for part in parts:
		chunks = re.split("\|\|", part)
		if(chunks[0] == 'age'):
			age = get_age(driver)
			log("age"+"||"+str(self.treatment_id)+"||"+age)
		if(chunks[0] == 'gender'):
			gender = get_gender(driver)
			log("gender"+"||"+str(self.treatment_id)+"||"+gender)
		if(chunks[0] == 'language'):
			language = get_language(driver)
			log("language"+"||"+str(self.treatment_id)+"||"+language)
		if(chunks[0] == 'interests'):
			pref = get_ad_pref(driver)
			log("pref"+"||"+str(self.treatment_id)+"||"+"@".join(pref))
		if(chunks[0] == 'ads'):
			collect_ads(int(chunks[2]), int(chunks[3]), LOG_FILE, driver, self.unit_id, self.treatment_id, chunks[1])
		time.sleep(5)
		
	log('measurement-end')

    def opt_in(self):
        """Opt in to behavioral advertising on Google"""
	self.driver.set_page_load_timeout(60)
	self.driver.get("https://www.google.com/settings/ads")
	self.driver.find_element_by_xpath(".//div[@class ='"+OPTIN_DIV+"']").click()
	if(self.unit_id != -1):
		self.log("optedIn||"+str(self.treatment_id))

    def opt_out(self): 
        """Opt out of behavioral advertising on Google"""
	self.driver.set_page_load_timeout(60)
	self.driver.get("https://www.google.com/settings/ads")
	self.driver.find_element_by_xpath(".//div[@class ='"+OPTOUT_DIV+"']").click()
	time.sleep(2)
	self.driver.execute_script("document.getElementsByName('ok')[1].click();")	
	if(self.unit_id != -1):
		self.log("optedOut||"+str(self.treatment_id))

    def login2Google(self, username, password):
	self.driver.find_element_by_xpath(".//a[span[span[@class='gbit']]]").click()
	self.driver.find_element_by_id("Email").send_keys(username)
	self.driver.find_element_by_id("Passwd").send_keys(password)
	self.driver.find_element_by_id("signIn").click()
	self.driver.find_element_by_id("gbi4i").click()
	self.driver.find_element_by_id("gb_71").click()

    def set_gender(self, gender):
        """Set gender on Google Ad Settings page"""
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            self.driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[0].click()
            if(gender == 'm'): # MALE	
                box = self.driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='1']/span")[0]	 
            elif(gender == 'f'): # FEMALE
                box = self.driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='2']/span")[0]	
            box.click()
            self.driver.find_elements_by_xpath(".//div[@class='"+SUBMIT_DIV+"']")[0].click()
            self.log("setGender="+gender+"||"+str(self.treatment_id))
        except:
            print "Could not set gender"

    def get_gender(self):
        """Read gender from Google Ad Settings"""
        inn = ""
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            div = self.driver.find_elements_by_xpath(".//span[@class='"+READ_SPAN+"']")[0]
            inn = str(div.get_attribute('innerHTML'))
        except:
            print "Could not get gender"
        return inn
	
    def get_age(self):
        """Read age from Google Ad Settings"""
	inn = ""
	try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            div = self.driver.find_elements_by_xpath(".//span[@class='"+READ_SPAN+"']")[1]
            inn = str(div.get_attribute('innerHTML'))
	except:
            print "Could not get age"
	return inn
		
    def get_language(self):	
        """Read language from Google Ad Settings"""
	inn = ""
	try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            div = self.driver.find_elements_by_xpath(".//span[@class='"+READ_SPAN+"']")[2]
            inn = str(div.get_attribute('innerHTML'))
	except:
            print "Could not get language"
	return inn
	
    def set_age(self, age):	
        """Set age on Google Ad Settings page"""
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            self.driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[1].click()
            if(age>=18 and age<=24):
                box = self.driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='1']/span")[1]
            elif(age>=25 and age<=34):	
                box = self.driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='2']/span")[1]
            elif(age>=35 and age<=44):	
                box = self.driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='3']/span")[0]
            elif(age>=45 and age<=54):	
                box = self.driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='4']/span")[0]
            elif(age>=55 and age<=64):
                box = self.driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='5']/span")[0]
            elif(age>=65):
                box = self.driver.find_elements_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='6']/span")[0]
            box.click()
            self.driver.find_elements_by_xpath(".//div[@class='"+SUBMIT_DIV+"']")[1].click()
            self.log("setAge="+str(age)+"||"+str(self.treatment_id))
        except:
            print "Could not set age"


    def remove_ad_pref(self, pref, choice=2):
	try:
            prefs = get_ad_pref(self.driver)
            self.log("prepref"+"||"+str(self.treatment_id)+"||"+"@".join(prefs))
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            if (choice == 1):
                # For search related preferences
                self.driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	
            elif (choice == 2):
                    self.driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
            rem = []
            while(1):
                    trs = self.driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
                    flag=0
                    for tr in trs:
                            td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']")
                            div = tr.find_element_by_xpath(".//td[@class='Wq']/div")
                            int = td.get_attribute('innerHTML')
                            if pref.lower() in div.get_attribute('aria-label').lower():
                                    flag=1
                                    hover = ActionChains(self.driver).move_to_element(td)
                                    hover.perform()
                                    time.sleep(1)
                                    td.click()
                                    div.click()
                                    rem.append(int)
                                    time.sleep(2)
                                    break
                    if(flag == 0):
                            break
            self.driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
            self.log("remInterest="+"@".join(rem)+"||"+str(self.treatment_id))
	except:
            print "No interests matched '%s'. Skipping." %(pref)

    def set_ad_pref(self, pref, choice=2): 
        """Set an ad pref"""
	try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            if (choice == 1):
                # For search related preferences
                self.driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	
            elif (choice == 2):
                    self.driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
            self.driver.find_element_by_xpath(".//input[@class='"+PREF_INPUT+"']").send_keys(pref)
            self.driver.find_element_by_xpath(".//div[@class='"+PREF_INPUT_FIRST+"']").click()
            time.sleep(1)
            trs = self.driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
            for tr in trs:
                    td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']").get_attribute('innerHTML')
                    print td
                    self.log("setInterests="+td+"||"+str(self.treatment_id))
            self.driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
	except:
            print "Error setting interests containing '%s'. Skipping." %(pref)
	
    def get_ad_pref(self, choice=2):									
        """Returns list of Ad preferences"""
	pref = []
	try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            if (choice == 1):
                # For search related preferences
                self.driver.find_element_by_css_selector("div.Vu div.bd div.Qc div div div.cc").click()	
            elif (choice == 2):
                self.driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
            ints = self.driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']/td[@class='"+PREF_TD+"']")
            # 	print ints
            for interest in ints:
                    pref.append(str(interest.get_attribute('innerHTML')))
                    #raw_input("Waiting...")
	except:
            print "Could not get any interests"
            pass
	return pref	

    def train_with_sites(self, file_name): 
        """Visits all pages in file_name"""
	fo = open(file_name, "r")
	for line in fo:
		chunks = re.split("\|\|", line)
		site = "http://"+chunks[0].strip()
		try:
			self.driver.set_page_load_timeout(40)
			self.driver.get(site)
			time.sleep(5)
			self.log(site+"||"+str(self.treatment_id))
                        # pref = get_ad_pref(self.driver)
                        # self.log("pref"+"||"+str(treatment_id)+"||"+"@".join(pref), self.unit_id)
		except:
			self.log("timedout-"+line.rstrip())


    def wait_for_others(self, instances, round):
        """Makes instance with SELF.UNIT_ID 'self.unit_id' wait while others train"""
	clear = False
	count = 0
	round = int(round)
	while(not clear):
		count += 1
		if(count > 500):
			self.log('breakingout')
			break
		c = [0]*instances
		curr_round = 0
		fo = open(self.log_file, "r")
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
	

    def collect_ads(self, reloads, delay, site, file_name=None):
        """
        file_name is the log_file.
        """
        if file_name == None:
            file_name = self.log_file
	rel = 0
	while (rel < reloads):	# number of reloads on sites to capture all ads
		time.sleep(delay)
		try:
			for i in range(0,1):
				s = datetime.now()
				if(site == 'toi'):
					save_ads_toi(file_name, self.driver, self.unit_id, self.treatment_id)
				elif(site == 'bbc'):
					save_ads_bbc(file_name, self.driver, self.unit_id, self.treatment_id)
				elif(site == 'guardian'):
					save_ads_guardian(file_name, self.driver, self.unit_id, self.treatment_id)
				elif(site == 'reuters'):
					save_ads_reuters(file_name, self.driver, self.unit_id, self.treatment_id)
				elif(site == 'bloomberg'):
					save_ads_bloomberg(file_name, self.driver, self.unit_id, self.treatment_id)
				else:
					raw_input("No such site found: %s!" % site)
				e = datetime.now()
				self.log('loadtime||'+str(e-s))
				self.log('reload')
		except:
			self.log('errorcollecting')
			pass
		rel = rel + 1

    def save_ads_bloomberg(self, file_name):
	sys.stdout.write(".")
	sys.stdout.flush()
	self.driver.set_page_load_timeout(60)
	self.driver.get("http://www.bloomberg.com/")	
	tim = str(datetime.now())
	frame0 = self.driver.find_element_by_xpath(".//iframe[@src='/bcom/home/iframe/google-adwords']")
	self.driver.switch_to.frame(frame0)
	frame1 = self.driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
	self.driver.switch_to.frame(frame1)
	time.sleep(2)
	frame2 = self.driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
	self.driver.switch_to.frame(frame2)
	lis = self.driver.find_elements_by_css_selector("div#adunit div#ads ul li")
	for li in lis:
		t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
		l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
		b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
		f = strip_tags("ad||"+str(self.unit_id)+"||"+str(self.treatment_id)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file_name, "a")
		fo.write(f + '\n')
		fo.close()
	self.driver.switch_to.default_content()
	self.driver.switch_to.default_content()
	self.driver.switch_to.default_content()

    def save_ads_reuters(self, file_name):
	sys.stdout.write(".")
	sys.stdout.flush()
	self.driver.set_page_load_timeout(60)
	self.driver.get("http://www.reuters.com/news/us")	
	tim = str(datetime.now())
	frame0 = self.driver.find_element_by_xpath(".//iframe[@id='pmad-rt-frame']")
	self.driver.switch_to.frame(frame0)
	frame1 = self.driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
	self.driver.switch_to.frame(frame1)
	time.sleep(2)
	frame2 = self.driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
	self.driver.switch_to.frame(frame2)
	lis = self.driver.find_elements_by_css_selector("div#adunit div#ads ul li")
	for li in lis:
		t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
		l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
		b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
		f = strip_tags("ad||"+str(self.unit_id)+"||"+str(self.treatment_id)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file_name, "a")
		fo.write(f + '\n')
		fo.close()
	self.driver.switch_to.default_content()
	self.driver.switch_to.default_content()
	self.driver.switch_to.default_content()

    def save_ads_guardian(self, file_name):
	sys.stdout.write(".")
	sys.stdout.flush()
	self.driver.set_page_load_timeout(60)
	self.driver.get("http://www.theguardian.com/us")	
	time = str(datetime.now())
	els = self.driver.find_elements_by_css_selector("div#google-ads-container div.bd ul li")
	for el in els:
		t = el.find_element_by_css_selector("p.t6 a").get_attribute('innerHTML')
		ps = el.find_elements_by_css_selector("p")
		b = ps[1].get_attribute('innerHTML')
		l = ps[2].find_element_by_css_selector("a").get_attribute('innerHTML')
		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(self.treatment_id)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file_name, "a")
		fo.write(t + '\n')
		fo.close()

    def save_ads_toi(self, file_name):
	sys.stdout.write(".")
	sys.stdout.flush()
	self.driver.set_page_load_timeout(60)
	self.driver.get("http://timesofindia.indiatimes.com/international-home")
	time = str(datetime.now())
	frames = self.driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_right.html']")
	self.driver.switch_to.frame(frames[0])
	ads = self.driver.find_elements_by_xpath(".//tbody/tr/td/table")
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(self.treatment_id)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file_name, "a")
		fo.write(t + '\n')
		fo.close()
	self.driver.switch_to.default_content()
	frames = self.driver.find_elements_by_xpath(".//iframe[@id='adhomepage']")
	self.driver.switch_to.frame(frames[0])
	ads = self.driver.find_elements_by_xpath(".//tbody/tr/td/table")
	time = str(datetime.now())
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(self.treatment_id)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file_name, "a")
		fo.write(t + '\n')
		fo.close()
	self.driver.switch_to.default_content()
	frames = self.driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_bottom.html']")
	self.driver.switch_to.frame(frames[0])
	ads = self.driver.find_elements_by_xpath(".//tbody/tr/td/table")
	time = str(datetime.now())
	for ad in ads:
		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(self.treatment_id)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
		fo = open(file_name, "a")
		fo.write(t + '\n')
		fo.close()
	self.driver.switch_to.default_content()

    def save_ads_bbc(self, file_name):
	sys.stdout.write(".")
	sys.stdout.flush()
# 		global ad_int
	self.driver.set_page_load_timeout(60)
	self.driver.get("http://www.bbc.com/news/")
	time = str(datetime.now())
	els = self.driver.find_elements_by_css_selector("div#bbccom_adsense_mpu div ul li")
	for el in els:
		t = el.find_element_by_css_selector("h4 a").get_attribute('innerHTML')
		ps = el.find_elements_by_css_selector("p")
		b = ps[0].get_attribute('innerHTML')
		l = ps[1].find_element_by_css_selector("a").get_attribute('innerHTML')
		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(self.treatment_id)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
		fo = open(file_name, "a")
		fo.write(t + '\n')
		fo.close()

# Sweeney's experiment

    def adsFromNames(self, NAME_FILE, OUT_FILE, reloads):
        """Search names, Collect ads, for Sweeney's study"""
	lines = [line.strip() for line in open(NAME_FILE)]
	nlist = lines[::2]
	total=0
	self.driver.set_page_load_timeout(10)
	self.driver.get("http://www.reuters.com/")
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
				self.driver.set_page_load_timeout(10)
				self.driver.find_element_by_id("searchfield").clear()
				self.driver.find_element_by_id("searchfield").send_keys(q)
				self.driver.find_element_by_id("searchbuttonNav").click()
				board = self.driver.find_element_by_css_selector("div#adcontainer1 iframe")
				self.driver.switch_to.frame(board)
				ads = self.driver.find_elements_by_css_selector("div#adBlock div div div div.adStd")
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
				self.driver.switch_to.default_content()
				rel = rel+1
			except:
				print "Timed Out"
				pass
