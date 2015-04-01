import time, re														# time.sleep, re.split
import sys															# some prints
from selenium import webdriver										# for running the driver on websites
from datetime import datetime										# for tagging log with datetime
from selenium.webdriver.common.keys import Keys						# to press keys on a webpage
import browser_unit

# Google search page class declarations

GENDER_DIV = "EA yP"
INPUT_ID = "lst-ib"
LI_CLASS = "g"

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

class GoogleSearchUnit(browser_unit.BrowserUnit):

	def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
		browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
		
	def infinitely_search_for_terms(self, query_file, delay):
		while(True):
			fo = open(query_file, "r")
			for line in fo:		# For all queries in the list, obtain search results on Google
				q = line.strip()
				print q
				try:
					self.driver.get("http://www.google.com/")
					self.driver.find_element_by_id(INPUT_ID).clear()
					self.driver.find_element_by_id(INPUT_ID).send_keys(q)
					self.driver.find_element_by_id(INPUT_ID).send_keys(Keys.RETURN)
					self.log('treatment', 'google search', q)
				except:
					self.log('error', 'google search', q)
# 				try:
# 				time.sleep(200)
				lis = self.driver.find_elements_by_css_selector("li."+LI_CLASS+"")
				print len(lis)
				for li in lis:
					self.log('measurement', 'google search', strip_tags(li.get_attribute('innerHTML')).encode("utf8"))
# 				except:
# 					self.log('error', 'collecting', 'google searchresults')
				time.sleep(delay)

			fo.close()
	
	def collect_results():
		flag = 0
		for t in range(0,1):
			for y in range(1, visits): # How many search results to visit
				print y
				try:
					driver.find_element_by_css_selector("ol#rso li:nth-of-type("+str(y)+") div h3 a").click()
					time.sleep(3)
					print driver.current_url
					driver.back()
				except:
					pass
			if flag == 1:
				break
			flag = 1
			try:
				driver.get("https://www.google.com/")
				driver.find_element_by_id(INPUT_ID).clear()
				driver.find_element_by_id(INPUT_ID).send_keys(q)
				driver.find_element_by_id(INPUT_ID).send_keys(Keys.RETURN)
				driver.find_element_by_css_selector("a#pnnext.pn").click()
			except:
				raw_input("Google Waiting..")
	
	
	
	
	
	