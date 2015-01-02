import time, re														# time.sleep, re.split
import sys															# some prints
from selenium import webdriver										# for running the driver on websites
from datetime import datetime										# for tagging log with datetime

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
	driver.set_page_load_timeout(60)
	driver.get("http://news.google.com")
	tim = str(datetime.now())
	divs = driver.find_elements_by_xpath(".//td[@class='lt-col']/div/div/div")
	topdivs = divs[0].find_elements_by_xpath(".//div[@class='section-content']/div[not(@class='esc-separator')]")
	print len(topdivs)
	for div in topdivs:
		title = div.find_element_by_xpath(".//div[@class='esc-lead-article-title-wrapper']/h2/a/span").get_attribute('innerHTML')
		print title
		tds = div.find_elements_by_xpath(".//div[@class='esc-lead-article-source-wrapper']/table/tbody/tr/td")
		agency = tds[0].find_element_by_xpath(".//span").get_attribute("innerHTML")
		ago = tds[1].find_element_by_xpath(".//span[@class='al-attribution-timestamp']").get_attribute("innerHTML")
		print agency, ago
		body = div.find_element_by_xpath(".//div[@class='esc-lead-snippet-wrapper']").get_attribute('innerHTML')
		print body	
		print ""
		f = strip_tags("news||"+str(id)+"||"+str(treatmentid)+"||"+tim+"||"+title+"||"+agency+"||"+ago+"||"+body).encode("utf8")
		fo = open(LOG_FILE, "a")
		fo.write(f + '\n')
		fo.close()

		
	time.sleep(100)
	
	

def get_centre_news(driver, id, treatmentid, LOG_FILE):						# get news articles from Google
	driver.set_page_load_timeout(60)
	driver.get("http://news.google.com")
	time.sleep(2)