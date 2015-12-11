import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
# import browser_unit
import google_ads                                                # interacting with Google Ads

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

class AmazonPricesUnit(google_ads.GoogleAdsUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        google_ads.GoogleAdsUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)

    def collect_ads(self, reloads, delay, site, file_name=None):
        if file_name == None:
            file_name = self.log_file
        rel = 0
        while (rel < reloads):  # number of reloads on sites to capture all ads
            time.sleep(delay)
            try:
                s = datetime.now()
                if(site == 'amazon'):
                    self.save_ads_amazon(file_name)
                elif(site == 'bbc'):
                    self.save_ads_bbc(file_name)
                else:
                    raw_input("No such site found: %s!" % site)
                e = datetime.now()
                self.log('measurement', 'loadtime', str(e-s))
            except:
                self.log('error', 'collecting ads', 'Error')
            rel = rel + 1

    def save_ads_bbc(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://www.bbc.com/news/")
        tim = str(datetime.now())
        els = driver.find_elements_by_css_selector("div.bbccom_adsense_container ul li")
        for el in els:
            t = el.find_element_by_css_selector("h4 a").get_attribute('innerHTML')
            ps = el.find_elements_by_css_selector("p")
            b = ps[0].get_attribute('innerHTML')
            l = ps[1].find_element_by_css_selector("a").get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)

    def save_ads_amazon(self, file):
        driver = self.driver
        
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://www.amazon.com")
        tim = str(datetime.now())
        els = driver.find_elements_by_css_selector("div#desktop-7 div div.feed-carousel div ul li")
        n=0
####collect the first two ads in the last column
        for el in els:
            n=n+1
            if n >=3:
                break
            ActionChains(driver).move_to_element(el).perform()
            cl = driver.find_element_by_xpath("//span[@id='gw-quick-look-btn']")
            ActionChains(driver).move_to_element(cl).click(cl).perform()
            time.sleep(5)
            t = driver.find_element_by_xpath("//div[@class='byline a-color-tertiary']").get_attribute('innerHTML')
            b = driver.find_element_by_xpath("//div[@class='details']/a[@class='title']").get_attribute('innerHTML')
            l = driver.find_element_by_xpath("//span[@class='a-color-price']").get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'price', ad)
            exit = driver.find_element_by_xpath("//i[@id='gw-popover-close']")
            ActionChains(driver).move_to_element(exit).click(exit).perform()
            time.sleep(5)





