import time, re														# time.sleep, re.split
import sys															# some prints
from selenium import webdriver										# for running the driver on websites
from datetime import datetime										# for tagging log with datetime
from selenium.webdriver.common.keys import Keys						# for sending keys

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

def log(msg, id, LOG_FILE):													# Maintains a log of visitations
	fo = open(LOG_FILE, "a")
	fo.write(str(datetime.now())+"||"+msg+"||"+str(id) + '\n')
	fo.close()   

def get_topstories(driver, id, treatmentid, LOG_FILE):						# get top news articles from Google
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://news.google.com")
	tim = str(datetime.now())
	divs = driver.find_elements_by_xpath(".//td[@class='lt-col']/div/div/div")
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
		f = strip_tags("news||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+title+"||"+agency+"||"+ago+"||"+body).encode("utf8")
		fo = open(LOG_FILE, "a")
		fo.write(f + '\n')
		fo.close()
	
def get_allstories(driver, id, treatmentid, LOG_FILE):						# get top news articles from Google
	sys.stdout.write(".")
	sys.stdout.flush()
	driver.set_page_load_timeout(60)
	driver.get("http://news.google.com")
	tim = str(datetime.now())
	divs = driver.find_elements_by_xpath(".//td[@class='lt-col']/div/div/div")
	topdivs = divs[1].find_elements_by_css_selector("div.section-list-content div div.blended-wrapper.blended-wrapper-first.esc-wrapper")
	tds = driver.find_elements_by_xpath(".//td[@class='esc-layout-article-cell']")
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
		f = strip_tags("news||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+title+"||"+agency+"||"+ago+"||"+body).encode("utf8")
		fo = open(LOG_FILE, "a")
		fo.write(f + '\n')
		fo.close()
	
def read_articles(keyword, count, driver, id, treatmentid, LOG_FILE):			# click on articles having a keyword
	driver.set_page_load_timeout(60)
	driver.get("http://news.google.com")
	tim = str(datetime.now())
	i = 0
	for i in range(0, count):
		links = driver.find_elements_by_link_text(keyword)
		print len(links)
		if(i>=len(links)):
			break
# 		links[i].send_keys(Keys.CONTROL + Keys.RETURN)
		links[i].click()
		for handle in driver.window_handles:
			print "Handle = ",handle
			driver.switch_to.window(handle);
			print driver.title
			if not(driver.title.strip() == "Google News"):
				time.sleep(20)
				site = driver.current_url
				log(site+"||"+str(treatmentid), id, LOG_FILE)
				print "closing", handle
				driver.close()
				driver.switch_to.window(driver.window_handles[0])
				
# 		driver.get("http://news.google.com")
# 		site = links[i].get_attribute('url')
# 		driver.switch_to_window("main_window")
		time.sleep(3)
	
	

def get_news(reloads, delay, driver, id, treatmentid, LOG_FILE, type):						# get news articles from Google
	rel = 0
	while (rel < reloads):	# number of reloads on sites to capture all ads
		time.sleep(delay)
# 		try:
		for i in range(0,1):
			s = datetime.now()
			if(type == 'top'):
				get_topstories(driver, id, treatmentid, LOG_FILE)
			elif(type == 'all'):
				get_allstories(driver, id, treatmentid, LOG_FILE)
				time.sleep(1000)
			else:
				raw_input("No such site found: %s!" % site)
			e = datetime.now()
			log('loadtime||'+str(e-s), id, LOG_FILE)
			log('reload', id, LOG_FILE)
# 		except:
# 			log('errorcollecting', id, LOG_FILE)
# 			pass
		rel = rel + 1