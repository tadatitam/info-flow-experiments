import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
import browser_unit

# Bing search constants

INPUT_ID = "sb_form_q"


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

class BingSearchUnit(browser_unit.BrowserUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        
    def login(self, username, password):
        """Login to Bing with username and password"""
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("https://www.login.live.com")
            self.driver.find_element_by_id("idDiv_PWD_UsernameTb").send_keys(username)
            self.driver.find_element_by_id("idDiv_PWD_PasswordTb").send_keys(password)
            self.driver.find_element_by_id("idSIButton9").click()
            self.log('treatment', 'login', username)
        except:
            self.log('error', 'logging in', username)
            
    def search_and_click(self, query_file, clickdelay=20, clickcount=5):
        s = 0
        r = 0
        fo = open(query_file, "r")
        for line in fo:     # For all queries in the list, obtain search results on Bing
            q = line.strip()
            print q, self.unit_id
            try:
                self.driver.get("http://www.bing.com/")
                time.sleep(1)
                self.driver.find_element_by_id(INPUT_ID).clear()
                self.driver.find_element_by_id(INPUT_ID).send_keys(q)
                self.driver.find_element_by_id(INPUT_ID).send_keys(Keys.RETURN)
                self.log('treatment', 'bing search', q)
            except:
                self.log('error', 'bing search', q)
                self.driver.save_screenshot(str(self.unit_id)+'_search'+str(s)+'.jpg')
                s+=1
            linklist = self.driver.find_elements_by_css_selector("h2 a")
            for y in range(1, clickcount+1): # How many search results to visit
                print y
                try:
                    linklist[y-1].click()
                    time.sleep(3)
                    print self.driver.current_url
                    link = self.driver.current_url
                    self.driver.back()
                    self.log('treatment', 'visit page', link)
                except:
                    self.log('error', 'collecting', 'bing searchresults')
                    self.driver.save_screenshot(str(self.unit_id)+'_visit'+str(r)+'.jpg')
                    r+=1
                time.sleep(clickdelay)
        fo.close()
               
    def get_muid(self):
            self.driver.get("http://www.bing.com")
            self.log('measure', 'muid', self.driver.get_cookie('MUID')['value'])
 
#    def infinitely_search_for_terms(self, query_file, delay):
#        s = 0
#        r = 0
#        while(s<50 and r<50):
#            fo = open(query_file, "r")
#            for line in fo:     # For all queries in the list, obtain search results on Bing
#                q = line.strip()
#                print q, self.unit_id
#                try:
#                    self.driver.get("http://www.bing.com/")
#                    self.driver.find_element_by_id(INPUT_ID).clear()
#                    self.driver.find_element_by_id(INPUT_ID).send_keys(q)
#                    self.driver.find_element_by_id(INPUT_ID).send_keys(Keys.RETURN)
#                    self.log('treatment', 'bing search', q)
#                except:
#                    self.log('error', 'bin search', q)
#                    self.driver.save_screenshot(str(self.unit_id)+'_search'+str(s)+'.jpg')
#                    s+=1
#                try:
#                    lis = self.driver.find_elements_by_css_selector("li."+LI_CLASS+"")
#                    for li in lis:
#                        self.log('measurement', 'bing search', strip_tags(li.get_attribute('innerHTML')).encode("utf8"))
#                except:
#                    self.log('error', 'collecting', 'bing searchresults')
#                    self.driver.save_screenshot(str(self.unit_id)+'_result'+str(r)+'.jpg')
#                    r+=1
#                time.sleep(delay)
#            fo.close()
