import time, re 							# time.sleep, re.split
import sys 									# some prints
import os, platform 						# for running  os, platform specific function calls
from selenium import webdriver 				# for running the driver on websites
from datetime import datetime 				# for tagging log with datetime
from selenium.webdriver.common.proxy import *		# for proxy settings

class BrowserUnit:

	def __init__(self, browser, log_file, unit_id, treatment_id, proxy=None):
		if(proxy != None):
			sproxy = Proxy({
    			'proxyType': ProxyType.MANUAL,
    			'httpProxy': proxy,
    			'ftpProxy': proxy,
    			'sslProxy': proxy,
    			'noProxy': '' # set this value as desired
   			 	})
		else:
			sproxy = Proxy({
    			'proxyType': ProxyType.MANUAL
   			 	})
			
		if(browser=='firefox'):
			if (platform.system()=='Darwin'):
				self.driver = webdriver.Firefox(proxy=sproxy)
			else:
				print "Unidentified Platform"
				sys.exit(0)
		elif(browser=='chrome'):
			print "WARNING: Expecting chromedriver at specified location !!"
			if (platform.system()=='Darwin'):
				chromedriver = "./chromedriver/chromedriver_mac"
			elif (platform.system() == 'Linux'):
				chromedriver = "./chromedriver/chromedriver_linux"
			else:
				print "Unidentified Platform"
				sys.exit(0)
			os.environ["webdriver.chrome.driver"] = chromedriver
			chrome_option = webdriver.ChromeOptions()
			chrome_option.add_argument("--proxy-server="+proxy)
			self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_option)
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


	def train_with_sites(self, file_name, treatment_id): 
		"""Visits all pages in file_name"""
		fo = open(file_name, "r")
		for line in fo:
			chunks = re.split("\|\|", line)
			site = "http://"+chunks[0].strip()
			try:
				self.driver.set_page_load_timeout(40)
				self.driver.get(site)
				time.sleep(5)
				self.log(site+"||"+str(treatment_id))
							# pref = get_ad_pref(self.driver)
							# self.log("pref"+"||"+str(treatment_id)+"||"+"@".join(pref), self.unit_id)
			except:
				self.log("timedout-"+line.rstrip())


	def wait_for_others(self):
		"""Makes instance with SELF.UNIT_ID wait while others train"""
		fo = open(self.log_file, "r")
		line = fo.readline()
		chunks = re.split("\|\|", line)
		gmarker = 'assign'
		instances = int(chunks[1])
	
		round=0
		fo = open(self.log_file, "r")
		for line in fo:
			chunks = re.split("\|\|", line)
			tim = chunks[0]
			if(tim == 'treatnames'):
				continue
			msg = chunks[1]
			id1 = chunks[2].rstrip()
			if(tim == 'assign'):
				round += 1
# 	print "round: ", round
		
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
	
# 
#     def collect_ads(self, reloads, delay, treatment_id, site, file_name=None):
#         """
#         file_name is the log_file.
#         """
#         if file_name == None:
#             file_name = self.log_file
# 	rel = 0
# 	while (rel < reloads):	# number of reloads on sites to capture all ads
# 		time.sleep(delay)
# 		#try:
# 		for i in range(0,1):
# 			s = datetime.now()
# 			if(site == 'toi'):
# 				save_ads_toi(file_name, self.driver, self.unit_id, treatment_id)
# 			elif(site == 'bbc'):
# 				self.save_ads_bbc(file_name, treatment_id)
# 			elif(site == 'guardian'):
# 				save_ads_guardian(file_name, self.driver, self.unit_id, treatment_id)
# 			elif(site == 'reuters'):
# 				save_ads_reuters(file_name, self.driver, self.unit_id, treatment_id)
# 			elif(site == 'bloomberg'):
# 				save_ads_bloomberg(file_name, self.driver, self.unit_id, treatment_id)
# 			else:
# 				raw_input("No such site found: %s!" % site)
# 			e = datetime.now()
# 			self.log('loadtime||'+str(e-s))
# 			self.log('reload')
# 		#except:
# 		#	self.log('errorcollecting')
# 		#	pass
# 		rel = rel + 1
# 
#     def save_ads_bloomberg(self, file_name, treatment_id):
# 	sys.stdout.write(".")
# 	sys.stdout.flush()
# 	self.driver.set_page_load_timeout(60)
# 	self.driver.get("http://www.bloomberg.com/")	
# 	tim = str(datetime.now())
# 	frame0 = self.driver.find_element_by_xpath(".//iframe[@src='/bcom/home/iframe/google-adwords']")
# 	self.driver.switch_to.frame(frame0)
# 	frame1 = self.driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
# 	self.driver.switch_to.frame(frame1)
# 	time.sleep(2)
# 	frame2 = self.driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
# 	self.driver.switch_to.frame(frame2)
# 	lis = self.driver.find_elements_by_css_selector("div#adunit div#ads ul li")
# 	for li in lis:
# 		t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
# 		l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
# 		b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
# 		f = strip_tags("ad||"+str(self.unit_id)+"||"+str(treatment_id)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
# 		fo = open(file_name, "a")
# 		fo.write(f + '\n')
# 		fo.close()
# 	self.driver.switch_to.default_content()
# 	self.driver.switch_to.default_content()
# 	self.driver.switch_to.default_content()
# 
#     def save_ads_reuters(self, file_name, treatment_id):
# 	sys.stdout.write(".")
# 	sys.stdout.flush()
# 	self.driver.set_page_load_timeout(60)
# 	self.driver.get("http://www.reuters.com/news/us")	
# 	tim = str(datetime.now())
# 	frame0 = self.driver.find_element_by_xpath(".//iframe[@id='pmad-rt-frame']")
# 	self.driver.switch_to.frame(frame0)
# 	frame1 = self.driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
# 	self.driver.switch_to.frame(frame1)
# 	time.sleep(2)
# 	frame2 = self.driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
# 	self.driver.switch_to.frame(frame2)
# 	lis = self.driver.find_elements_by_css_selector("div#adunit div#ads ul li")
# 	for li in lis:
# 		t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
# 		l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
# 		b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
# 		f = strip_tags("ad||"+str(self.unit_id)+"||"+str(treatment_id)+"||"+tim+"||"+t+"||"+l+"||"+b).encode("utf8")
# 		fo = open(file_name, "a")
# 		fo.write(f + '\n')
# 		fo.close()
# 	self.driver.switch_to.default_content()
# 	self.driver.switch_to.default_content()
# 	self.driver.switch_to.default_content()
# 
#     def save_ads_guardian(self, file_name, treatment_id):
# 	sys.stdout.write(".")
# 	sys.stdout.flush()
# 	self.driver.set_page_load_timeout(60)
# 	self.driver.get("http://www.theguardian.com/us")	
# 	time = str(datetime.now())
# 	els = self.driver.find_elements_by_css_selector("div#google-ads-container div.bd ul li")
# 	for el in els:
# 		t = el.find_element_by_css_selector("p.t6 a").get_attribute('innerHTML')
# 		ps = el.find_elements_by_css_selector("p")
# 		b = ps[1].get_attribute('innerHTML')
# 		l = ps[2].find_element_by_css_selector("a").get_attribute('innerHTML')
# 		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(treatment_id)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
# 		fo = open(file_name, "a")
# 		fo.write(t + '\n')
# 		fo.close()
# 
#     def save_ads_toi(self, file_name, treatment_id):
# 	sys.stdout.write(".")
# 	sys.stdout.flush()
# 	self.driver.set_page_load_timeout(60)
# 	self.driver.get("http://timesofindia.indiatimes.com/international-home")
# 	time = str(datetime.now())
# 	frames = self.driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_right.html']")
# 	self.driver.switch_to.frame(frames[0])
# 	ads = self.driver.find_elements_by_xpath(".//tbody/tr/td/table")
# 	for ad in ads:
# 		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
# 		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
# 		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(treatment_id)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
# 		fo = open(file_name, "a")
# 		fo.write(t + '\n')
# 		fo.close()
# 	self.driver.switch_to.default_content()
# 	frames = self.driver.find_elements_by_xpath(".//iframe[@id='adhomepage']")
# 	self.driver.switch_to.frame(frames[0])
# 	ads = self.driver.find_elements_by_xpath(".//tbody/tr/td/table")
# 	time = str(datetime.now())
# 	for ad in ads:
# 		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
# 		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
# 		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(treatment_id)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
# 		fo = open(file_name, "a")
# 		fo.write(t + '\n')
# 		fo.close()
# 	self.driver.switch_to.default_content()
# 	frames = self.driver.find_elements_by_xpath(".//iframe[@src='http://timesofindia.indiatimes.com/configspace/ads/TOI_INTL_home_bottom.html']")
# 	self.driver.switch_to.frame(frames[0])
# 	ads = self.driver.find_elements_by_xpath(".//tbody/tr/td/table")
# 	time = str(datetime.now())
# 	for ad in ads:
# 		aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
# 		bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
# 		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(treatment_id)+"||"+time+"||"+aa[0].get_attribute('innerHTML')+ "||" + aa[1].get_attribute('innerHTML')+ "||" + bb[0].get_attribute('innerHTML')).encode("utf8")
# 		fo = open(file_name, "a")
# 		fo.write(t + '\n')
# 		fo.close()
# 	self.driver.switch_to.default_content()
# 
#     def save_ads_bbc(self,file_name,treatment_id):
# 	sys.stdout.write(".")
# 	sys.stdout.flush()
# # 		global ad_int
# 	self.driver.set_page_load_timeout(60)
# 	self.driver.get("http://www.bbc.com/news/")
# 	time = str(datetime.now())
# 	els = self.driver.find_elements_by_css_selector("div#bbccom_adsense_mpu div ul li")
#     #print "Outside for loop", len(els)
# 	for el in els:
# 		t = el.find_element_by_css_selector("h4 a").get_attribute('innerHTML')
# 		ps = el.find_elements_by_css_selector("p")
# 		b = ps[0].get_attribute('innerHTML')
# 		l = ps[1].find_element_by_css_selector("a").get_attribute('innerHTML')
# 		t = strip_tags("ad||"+str(self.unit_id)+"||"+str(treatment_id)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
#         #print "Inside for loop"
#         #print t
# 		fo = open(file_name, "a")
# 		fo.write(t + '\n')
# 		fo.close()
