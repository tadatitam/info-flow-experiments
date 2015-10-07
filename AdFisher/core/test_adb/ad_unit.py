from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from xvfbwrapper import Xvfb    # artificial display for headless experiments
import logging
from adblockparser import AdblockRules


class AdUnit:

    def _load_easy_list(self):
        with open('easylist.txt') as f:
            lines = f.read().splitlines()
        logging.info("Loaded easy list: {} items".format(len(lines)))
        return lines


    def __init__(self,easyList=False):
 
        #self.vdisplay = Xvfb(width=1280, height=720)
        #self.vdisplay.start()
        self.driver = webdriver.Firefox(
                firefox_binary = webdriver.firefox.firefox_binary.FirefoxBinary(
                log_file = open ('/tmp/selenium.log', 'a')))

        logging.basicConfig(filename='log.ad_unit.txt',level=logging.DEBUG)
        if easyList:
            self.rules = AdblockRules(self._load_easy_list())
        else:
            logging.info("skipping easy list")

    def visit_url(self,url):
        driver = self.driver
        logging.info("Trying: {}".format(url))
        driver.get(url)
        logging.info("Visited: {}".format(url))



    def find_ads(self):
        driver = self.driver
        links = driver.find_elements_by_xpath("//*[@href]")
        links = set([link.get_attribute("href") for link in links])
        count = 0
        for link in links:
            logging.info("Checking:href:{}".format(link))
            if self.rules.should_block(link,{'script': True}):
                logging.info("Ad:href:{}".format(link))
                count+=1
        print "href search found: {}".format(count)

    def check_tag(self,tag_name):
        driver = self.driver
        tags = driver.find_elements_by_tag_name(tag_name)
        urls = set([link.get_attribute("src") for link in tags])
        logging.info("number of tags:{}:{}".format(tag_name,len(urls)))
        count = 0
        for link in urls:
            if link != None and "http" in link:
                logging.info("Checking:{}:{}".format(tag_name,link))
                if self.rules.should_block(link,{'script': True,'image': True}):
                    logging.info("Ad:{}:{}".format(tag_name,link))
                    count+=1
            else:
                logging.info("Discarding:{}:{}".format(tag_name,link))
        print "{} search found: {}".format(tag_name,count)


    def screenshot(self,filename):
        driver = self.driver
        driver.save_screenshot(filename)
