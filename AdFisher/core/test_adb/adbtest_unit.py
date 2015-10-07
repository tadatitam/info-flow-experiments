from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from xvfbwrapper import Xvfb    # artificial display for headless experiments
import logging
from adblockparser import AdblockRules
from adblockparser import AdblockRule


class AdbTestUnit:

    def _load_easy_list(self):
        with open('easylist.txt') as f:
            lines = f.read().splitlines()
        logging.info("Loaded easy list: {} items".format(len(lines)))
        return lines


    def __init__(self,headless=False,easyList=True):
        if headless:
            self.vdisplay = Xvfb(width=1280, height=720)
            self.vdisplay.start()
        self.driver = webdriver.Firefox(
                firefox_binary = webdriver.firefox.firefox_binary.FirefoxBinary(
                log_file = open ('/tmp/selenium.log', 'w')))

        logging.basicConfig(filename='log.adbtest_unit.txt',level=logging.DEBUG)
        if easyList:
            self.rules = AdblockRules(self._load_easy_list())
            self.all_options = {opt:True for opt in AdblockRule.BINARY_OPTIONS}
        else:
            logging.info("skipping easy list")

    def visit_url(self,url):
        driver = self.driver
        logging.info("Trying: {}".format(url))
        driver.get(url)
        logging.info("Visited: {}".format(url))

    def check_block(self, url, source="href", options=None):
        logging.info("Checking:{}:{}".format(source, url))
        if self.rules.should_block(url, options):
            print "Blocked type {} at address {}".format(source, url)
            logging.info("Ad:{}:{}".format(source, url))
            return True
        return False

    def find_href_ads(self):
        driver = self.driver
        links = driver.find_elements_by_xpath("//*[@href]")
        links = set([link.get_attribute("href") for link in links])
        count = 0
        options = self.all_options
        for link in links:
            if self.check_block(url=link, options=options):
                count+=1
        print "href search found: {}".format(count)

    def find_src_ads(self):
        driver = self.driver
        links = driver.find_elements_by_xpath("//*[@src]")
        links = set([link.get_attribute("src") for link in links])
        count = 0
        options = self.all_options
        for link in links:
            if self.check_block(url=link, source="src", options=options):
                count+=1
        print "src search found: {}".format(count)

    def check_tag(self,tag_name):
        driver = self.driver
        tags = driver.find_elements_by_tag_name(tag_name)
        urls = set([link.get_attribute("src") for link in tags])
        logging.info("number of tags:{}:{}".format(tag_name,len(urls)))
        count = 0
        options = {'script': True,'image': True}
        for link in urls:
            if link != None and "http" in link:
                if self.check_block(url=link, source=tag_name, options=options):
                    count+=1
            else:
                logging.info("Discarding:{}:{}".format(tag_name,link))
        print "{} search found: {}".format(tag_name,count)


    def screenshot(self,filename):
        driver = self.driver
        driver.save_screenshot(filename)

def treat_cmd(browser, cmd):
    if cmd[0] == "visit":
        if len(cmd) < 2:
            print "Incomplete command"
            return
        if cmd[1] == "cnn":
            url = "http://www.cnn.com/"
        elif cmd[1] == "bbc":
            url = "http://www.bbc.com/"
        elif cmd[1] == "fox":
            url = "http://www.foxnews.com/"
        elif cmd[1] == "href":
            if len(cmd) < 3:
                print "Please specify an address"
                return
            url = cmd[2]
        else:
            print "Unknown address shortcut - Type visit href url to specify another address"
            return
        print "Visiting {}".format(url)
        browser.visit_url(url)
    elif cmd[0] == "collect":
        if len(cmd) < 2:
            print "Incomplete command"
            return
        if cmd[1] == "href":
            print "Collecting href ads"
            browser.find_href_ads()
        elif cmd[1] == "src":
            print "Collecting src ads"
            browser.find_src_ads()
        else:
            print "Collecting {} ads".format(cmd[1])
            browser.check_tag(cmd[1])
    elif cmd[0] == "check":
        if len(cmd) < 2:
            print "Incomplete command"
            return
        source = "href"
        options = {}
        if len(cmd) > 2:
            source = cmd[2]
        if len(cmd) > 3:
            for opt in cmd[3].split(","):
                opt = opt.split(":")
                options[opt[0]] = len(opt) == 1 or opt[1] == "True"
        print "Checking {} from source {} with options {} for ads".format(cmd[1], source, str(options))
        print "\t -> {}".format(browser.check_block(url=cmd[1], source=source, options=options))
    elif cmd[0] == "read":
        if len(cmd) < 2:
            print "Incomplete command"
            return
        with open(cmd[1]) as f:
            lines = f.read().splitlines()
            for line in lines:
                treat_cmd(browser, line.split())
    else:
        print "Unknown command"
            

if __name__ == "__main__":
    browser = AdbTestUnit(headless=False)
    print "Browser ready - Enter commands"
    line = ""
    try:
        while line != "quit":
            cmd = line.split()
            if len(cmd) > 1:
                treat_cmd(browser, cmd)
            line = raw_input("adbtest: ")
        print "Received quit command. Exiting..."
    finally:
        browser.driver.quit()


