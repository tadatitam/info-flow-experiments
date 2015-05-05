import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
# import browser_unit
import google_ads

# Google ad settings page class declarations


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

class ExposureSitesUnit(google_ads.GoogleAdsUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        google_ads.GoogleAdsUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
#         browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        
    def login_dailystrength(self, username, password):
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("http://www.dailystrength.org/")
            div = self.driver.find_element_by_xpath(".//div[@id ='login_tab_ds']")
            div.find_element_by_xpath(".//input[@id='mod_login_username']").send_keys(username)
            div.find_element_by_xpath(".//input[@id='mod_login_password']").send_keys(password)
            div.find_element_by_xpath(".//input[@id='mod_login_password']").send_keys(Keys.RETURN)
            self.log('treatment', 'login to dailystrength', username)
        except:
            self.log('error', 'logging in to dailystrength', username)
            
    def login_psychforums(self, username, password):
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("http://www.psychforums.com/ucp.php?mode=login")
            self.driver.find_element_by_id("username").send_keys(username)
            self.driver.find_element_by_id("password").send_keys(password)
            self.driver.find_element_by_id("password").send_keys(Keys.RETURN)
            self.log('treatment', 'login to psychforums', username)
        except:
            self.log('error', 'logging in to psychforums', username)
             
    def login_intherooms(self, username, password):
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("http://www.intherooms.com/")
            self.driver.find_element_by_id("login").click()
            time.sleep(2)
            form = self.driver.find_element_by_xpath(".//form[@id ='itr-login']")
            form.find_element_by_xpath(".//input[@name='username']").send_keys(username)
            form.find_element_by_xpath(".//input[@name='password']").send_keys(password)
            form.find_element_by_xpath(".//input[@name='password']").send_keys(Keys.RETURN)
            self.log('treatment', 'login to intherooms', username)
        except:
            self.log('error', 'logging in to intherooms', username)
    
    def login_addictiontribe(self, username, password):
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("http://www.addictiontribe.com/member/")
            self.driver.find_element_by_xpath(".//input[@id='login1']").send_keys(username)
            self.driver.find_element_by_xpath(".//input[@id='login2']").send_keys(password)
            self.driver.find_element_by_xpath(".//input[@id='login2']").send_keys(Keys.RETURN)
            self.log('treatment', 'login to addictiontribe', username)  
        except:
            self.log('error', 'logging in to addictiontribe', username)      
            
            
            
            
            
            
            
            
            
            