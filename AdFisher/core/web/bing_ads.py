import time, re                             # time.sleep, re.split
import sys                              # some prints
from selenium import webdriver                      # for running the driver on websites
from datetime import datetime                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys             # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import browser_unit

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

class BingAdsUnit(browser_unit.BrowserUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        
#   def collect_ads(self, reloads, delay, file_name=None):
#       if file_name == None:
#           file_name = self.log_file
#       rel = 0
#       while (rel < reloads):  # number of reloads on sites to capture all ads
#           time.sleep(delay)
#           try:
#               for i in range(0,1):
#                   s = datetime.now()
#                   sys.stdout.write("x")
#                   sys.stdout.flush()
#                   click_ad_msn_auto(file_name)
#                   e = datetime.now()
#                   self.log('measurement', 'loadtime', str(e-s))
#           except:
#               self.log('error', 'collecting ads', 'Error')
#           rel = rel + 1

    def click_ad_msn_auto(self, file):
        #try:
            driver = self.driver
            id = self.unit_id
            sys.stdout.write(".")
            sys.stdout.flush()
            driver.set_page_load_timeout(60)
            driver.get("http://www.msn.com/en-us/autos")
            mainHandle = driver.current_window_handle
            tim = str(datetime.now())
            adframes = driver.find_elements(By.XPATH, "//div[@class='adcontainer']//iframe")
            adf = adframes[0]
            driver.switch_to_frame(adf)
            adobj = self.driver.find_element_by_xpath("//a" )
            adobj.click()
            for handle in driver.window_handles:
                if handle != mainHandle:
                    driver.switch_to_window(handle)
                    title = driver.title.encode('utf8')
                    self.log('measurement', 'ad', title)
                    driver.close()
            driver.switch_to_window(mainHandle)
            driver.switch_to_default_content()
            driver.close()      
        #except:
        #   print "Unexpected error:", sys.exc_info()[0]
        #   self.log('error', 'collecting ads', 'Error')