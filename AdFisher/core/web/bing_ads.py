import time, re                             # time.sleep, re.split
import sys                              # some prints
from selenium import webdriver                      # for running the driver on websites
from datetime import datetime                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys             # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bing_search

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

class BingAdsUnit(bing_search.BingSearchUnit):

	def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
		bing_search.BingSearchUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
		
	def collect_msn_ads(self, reloads, delay, site, file_name=None):
		if file_name == None:
			file_name = self.log_file
		rel = 0
		while (rel < reloads):	# number of reloads on sites to capture all ads
			time.sleep(delay)
			for i in range(0,1):
				s = datetime.now()
				self.click_ad_msn(file_name, site)
				e = datetime.now()
				self.log('measurement', 'loadtime', str(e-s))
			#self.log('error', 'collecting ads', 'Error')
			rel = rel + 1

	#Get the name of all other tabs open	
	def get_other_page_title(self, mainHandle):
		driver = self.driver
		for handle in driver.window_handles:
			if handle != mainHandle:
				driver.switch_to_window(handle)
				title = driver.title.encode('utf8')
				self.log('measurement', 'ad', title)
				driver.close()
		driver.switch_to_window(mainHandle)

	# Clicks all ads on an msn page
	def click_ad_msn(self, file, site):
		#try:
			driver = self.driver
			id = self.unit_id
			sys.stdout.write(".")
			sys.stdout.flush()
			driver.set_page_load_timeout(60)
			if(site == "home"):
				driver.get("http://www.msn.com/en-us")
			if(site in ["news", "weather", "entertainment", "sports", "money",
					"lifestyle", "health", "foodanddrink","travel", "autos"]):
				driver.get("http://www.msn.com/en-us/" + site)
			mainHandle = driver.current_window_handle
			tim = str(datetime.now())
			#Slowly scroll though page so that advertisements load
			time.sleep(.5)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight/5);")
			time.sleep(.5)
			driver.execute_script("window.scrollTo(0, 2*document.body.scrollHeight/5);")
			time.sleep(.5)
			driver.execute_script("window.scrollTo(0, 3*document.body.scrollHeight/5);")
			time.sleep(.5)
			driver.execute_script("window.scrollTo(0, 4*document.body.scrollHeight/5);")
			time.sleep(.5)
			driver.execute_script("window.scrollTo(0, 5*document.body.scrollHeight/5);")
			time.sleep(1)

			#Find all of the advertisements and click on them, then get the name of the popup
			adframes = driver.find_elements(By.XPATH, "//div[@class='adcontainer']//iframe")
 			for advert in adframes:
				if(advert.is_displayed):
					try:
						advert.click()
						time.sleep(.5)
						self.get_other_page_title(mainHandle)
						time.sleep(1)
					except:
						pass
	#	except:
	#		print "Unexpected error:", sys.exc_info()[0]
 	#		self.log('error', 'collecting ads', 'Error')
