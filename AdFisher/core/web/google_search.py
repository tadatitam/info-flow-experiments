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
        
    def login(self, username, password):
        """Login to Google with username and password"""
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("https://www.google.com")
            self.driver.find_element_by_xpath(".//a[@id='"+SIGNIN_A+"']").click()
            self.driver.find_element_by_id("Email").send_keys(username)
            self.driver.find_element_by_id("Passwd").send_keys(password)
            self.driver.find_element_by_id("signIn").click()
            self.log('treatment', 'login', username)
        except:
            self.log('error', 'logging in', username)
            
    def search_and_click(self, query_file, clickdelay=20, clickcount=5):
        s = 0
        r = 0
        fo = open(query_file, "r")
        for line in fo:     # For all queries in the list, obtain search results on Google
            q = line.strip()
            print q, self.unit_id
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
            for y in range(1, clickcount+1): # How many search results to visit
                print y
                try:
                    self.driver.find_element_by_css_selector("ol#rso li:nth-of-type("+str(y)+") div h3 a").click()
                    time.sleep(3)
                    print self.driver.current_url
                    link = self.driver.current_url
                    self.driver.back()
                    self.log('treatment', 'visit page', link)
                except:
                    self.log('error', 'collecting', 'google searchresults')
                    self.driver.save_screenshot(str(self.unit_id)+'_visit'+str(r)+'.jpg')
                    r+=1
                time.sleep(clickdelay)
        fo.close()
                
    def infinitely_search_for_terms(self, query_file, delay):
        s = 0
        r = 0
        while(s<50 and r<50):
            fo = open(query_file, "r")
            for line in fo:     # For all queries in the list, obtain search results on Google
                q = line.strip()
                print q, self.unit_id
                try:
                    self.driver.get("http://www.google.com/")
                    self.driver.find_element_by_id(INPUT_ID).clear()
                    self.driver.find_element_by_id(INPUT_ID).send_keys(q)
                    self.driver.find_element_by_id(INPUT_ID).send_keys(Keys.RETURN)
                    self.log('treatment', 'google search', q)
                except:
                    self.log('error', 'google search', q)
                    self.driver.save_screenshot(str(self.unit_id)+'_search'+str(s)+'.jpg')
                    s+=1
                try:
#               time.sleep(200)
                    lis = self.driver.find_elements_by_css_selector("li."+LI_CLASS+"")
                    for li in lis:
                        self.log('measurement', 'google search', strip_tags(li.get_attribute('innerHTML')).encode("utf8"))
                except:
                    self.log('error', 'collecting', 'google searchresults')
                    self.driver.save_screenshot(str(self.unit_id)+'_result'+str(r)+'.jpg')
                    r+=1
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
    
    
    
    
    
    