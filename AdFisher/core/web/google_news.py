import time, re														# time.sleep, re.split
import sys															# some prints
from selenium import webdriver										# for running the driver on websites
from datetime import datetime										# for tagging log with datetime
from selenium.webdriver.common.keys import Keys						# to press keys on a webpage
# import browser_unit
import google_ads

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

class GoogleNewsUnit(google_ads.GoogleAdsUnit):

	def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
		google_ads.GoogleAdsUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
# 		browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
		

	def get_topstories(self):						# get top news articles from Google
		sys.stdout.write(".")
		sys.stdout.flush()
		self.driver.set_page_load_timeout(60)
		self.driver.get("http://news.google.com")
		tim = str(datetime.now())
		divs = self.driver.find_elements_by_xpath(".//td[@class='lt-col']/div/div/div")
		topdivs = divs[0].find_elements_by_xpath(".//div[@class='section-content']/div[not(@class='esc-separator')]")
		print len(topdivs)
		for div in topdivs:
			title = div.find_element_by_xpath(".//div[@class='esc-lead-article-title-wrapper']/h2/a/span").get_attribute('innerHTML')
	# 		print title
			tds = div.find_elements_by_xpath(".//div[@class='esc-lead-article-source-wrapper']/table/tbody/tr/td")
			agency = tds[0].find_element_by_xpath(".//span").get_attribute("innerHTML")
			ago = tds[1].find_element_by_xpath(".//span[@class='al-attribution-timestamp']").get_attribute("innerHTML")
	# 		print agency, ago
			body = div.find_element_by_xpath(".//div[@class='esc-lead-snippet-wrapper']").get_attribute('innerHTML')
	# 		print body	
	# 		print ""
# 			f = strip_tags("news||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+title+"||"+agency+"||"+ago+"||"+body).encode("utf8")
			news = strip_tags(tim+"@|"+title+"@|"+agency+"@|"+ago+"@|"+body).encode("utf8")
			self.log('measurement', 'news', news)
	
	def get_allstories(self):						# get all news articles from Google
		sys.stdout.write(".")
		sys.stdout.flush()
		self.driver.set_page_load_timeout(60)
		self.driver.get("http://news.google.com")
		tim = str(datetime.now())
		divs = self.driver.find_elements_by_xpath(".//td[@class='lt-col']/div/div/div")
		topdivs = divs[1].find_elements_by_css_selector("div.section-list-content div div.blended-wrapper.blended-wrapper-first.esc-wrapper")
		tds = self.driver.find_elements_by_xpath(".//td[@class='esc-layout-article-cell']")
		print len(tds)
		for td in tds:
			title = td.find_element_by_xpath(".//div[@class='esc-lead-article-title-wrapper']/h2/a/span").get_attribute('innerHTML')
	# 		print title
			tds1 = td.find_elements_by_xpath(".//div[@class='esc-lead-article-source-wrapper']/table/tbody/tr/td")
			agency = tds1[0].find_element_by_xpath(".//span").get_attribute("innerHTML")
			ago = tds1[1].find_element_by_xpath(".//span[@class='al-attribution-timestamp']").get_attribute("innerHTML")
	# 		print agency, ago
			body = td.find_element_by_xpath(".//div[@class='esc-lead-snippet-wrapper']").get_attribute('innerHTML')
	# 		print body	
	# 		print ""
			heading = "Top News"
			try:
				heading = td.find_element_by_xpath("../../../../../../../../../div[@class='section-header']/div/div/h2/a/span").get_attribute('innerHTML')
			except:
				pass
		
	# 		heading = td.find_element_by_xpath("../../../../../../../../../div[@class='section-header']/div/div/h2/a/span").get_attribute('innerHTML')
# 			print heading
# 			time.sleep(2)
			if ("Suggested" in heading):
				print "Skipping Suggested news"
				continue
# 			print "entering"
			news = strip_tags(tim+"@|"+heading+"@|"+title+"@|"+agency+"@|"+ago+"@|"+body).encode("utf8")
			self.log('measurement', 'news', news)
	
	def read_articles(self, keyword, count):			# click on articles having a keyword
		self.driver.set_page_load_timeout(60)
		self.driver.get("http://news.google.com")
		tim = str(datetime.now())
		i = 0
		for i in range(0, count):
	# 		links = self.driver.find_elements_by_link_text(keyword)
			links = self.driver.find_elements_by_xpath(".//div[@class='esc-lead-article-source-wrapper'][contains(.,'"+keyword+"')]")
			print len(links)
			if(i>=len(links)):
				break
			print links[i].get_attribute("innerHTML")
			links[i].find_element_by_xpath("../div[@class='esc-lead-article-title-wrapper']/h2/a/span").click()
	# 		links[i].send_keys(Keys.CONTROL + Keys.RETURN)
	# 		links[i].click()
			for handle in self.driver.window_handles:
				print "Handle = ",handle
				self.driver.switch_to.window(handle);
				print self.driver.title
				if not(self.driver.title.strip() == "Google News"):
					time.sleep(20)
					site = self.driver.current_url
					self.log('treatment', 'read news', site)
# 					log(site+"||"+str(treatmentid), id, LOG_FILE)
					print "closing", handle
					self.driver.close()
					self.driver.switch_to.window(self.driver.window_handles[0])
				
	
	

	def get_news(self,type, reloads, delay):						# get news articles from Google
		rel = 0
		while (rel < reloads):	# number of reloads on sites to capture all ads
			time.sleep(delay)
	# 		try:
			for i in range(0,1):
				s = datetime.now()
				if(type == 'top'):
					self.get_topstories()
				elif(type == 'all'):
					self.get_allstories()
				else:
					raw_input("No such site found: %s!" % site)
				e = datetime.now()
				self.log('measurement', 'loadtime', str(e-s))
	# 		except:
	# 			log('errorcollecting', id, LOG_FILE)
	# 			pass
			rel = rel + 1

