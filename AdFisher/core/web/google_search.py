import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
import browser_unit

# Google search page class declarations

GENDER_DIV = "EA yP"
INPUT_ID = "lst-ib"
LI_CLASS = "g"

SIGNIN_A = "gb_70"

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
    
    def search_and_collect(self, query_file, searchdelay=20, pages=2):
        fo = open(query_file, "r")
        for line in fo:     # For all queries in the list, obtain search results on Google
            q = line.strip()
            page = 1
            print "\nsearch query: ", q
            try:
                self.driver.get("http://www.google.com/")
                time.sleep(1)
                self.driver.find_element_by_id(INPUT_ID).clear()
                self.driver.find_element_by_id(INPUT_ID).send_keys(q)
                self.driver.find_element_by_id(INPUT_ID).send_keys(Keys.RETURN)
                time.sleep(2)
                self.log('treatment', 'google search', q)
            except:
                self.log('error', 'google search', q)
                self.driver.save_screenshot(str(self.unit_id)+'_search'+str(s)+'.jpg')
                s+=1
            while(page<=pages):
                tim = str(datetime.now())
                results = self.driver.find_elements_by_css_selector("div.g div.rc")
                print len(results)
                for result in results:
                    t = result.find_element_by_css_selector("h3 a").get_attribute('innerHTML')
                    l = result.find_element_by_css_selector("div.s div div cite").get_attribute('innerHTML')
                    b = result.find_element_by_css_selector("div.s div span.st").get_attribute('innerHTML')
                    r = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
                    self.log('measurement', 'search_result', r)
                self.driver.find_element_by_id("pnnext").click()
                time.sleep(2)
                page += 1
            time.sleep(searchdelay)
        fo.close()
    	
                    
    def search_and_click(self, query_file, clickdelay=20, clickcount=5):
        fo = open(query_file, "r")
        for line in fo:     # For all queries in the list, obtain search results on Google
            s = 0
            r = 0
            q = line.strip()
            print "\nsearch query: ", q
            try:
                self.driver.get("http://www.google.com/")
                time.sleep(1)
                self.driver.find_element_by_id(INPUT_ID).clear()
                self.driver.find_element_by_id(INPUT_ID).send_keys(q)
                self.driver.find_element_by_id(INPUT_ID).send_keys(Keys.RETURN)
                self.log('treatment', 'google search', q)
            except:
                self.log('error', 'google search', q)
                self.driver.save_screenshot(str(self.unit_id)+'_search'+str(s)+'.jpg')
                s+=1
            for y in range(0, clickcount): # How many search results to visit
#                 print y
                try:
                    results = self.driver.find_elements_by_css_selector("div.g div.rc h3.r a")
#                     print "results", len(results)
                    results[y].click()
                    time.sleep(3)
#                     print self.driver.current_url
                    link = self.driver.current_url
                    self.driver.back()
                    self.log('treatment', 'visit page', link)
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    r+=1
                    s=r+0
                except:
                    self.log('error', 'visiting', 'google searchresults')
                    s+=1
                time.sleep(clickdelay)
        fo.close()
