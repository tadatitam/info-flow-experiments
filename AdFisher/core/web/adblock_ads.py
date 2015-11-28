import logging
import datetime
import os
import urllib
import shutil
import time

# base class we inherit from and extend
import browser_unit

# imports to use selenium
import selenium
from selenium import webdriver
from xvfbwrapper import Xvfb    # artificial display for headless experiments

# imports to parse easylist
from adblockparser import AdblockRules
from adblockparser import AdblockRule

# imports to parse url
from urlparse import urlparse, parse_qs

# imports to log ad data
import json

class AdBlockUnit(browser_unit.BrowserUnit):

    EASYLIST = 'easylist.txt'
    EASYLIST_URL = "https://easylist-downloads.adblockplus.org/easylist.txt"

    def _easylist_version(self,path=EASYLIST):
        '''
        Reads the version from the current easylist, or a file that is passed in
        '''
        if os.path.isfile(path):
            with open(path) as f:
                lines = f.read().splitlines()
                return lines[2].split(':')[1].strip()
        else:
            return -1

    def _fetch_easylist(self):
        '''
        Downloads the latest version of easylist, and if newer replaces any
        existing one.
        '''
        tmp_easylist = "tmp_"+self.EASYLIST
        cur_version = self._easylist_version()

        # download latest easylist from the Internet
        urllib.urlretrieve(self.EASYLIST_URL,tmp_easylist)
        tmp_version = self._easylist_version(path=tmp_easylist)
        
        # if necessary update
        if tmp_version > cur_version and cur_version != -1:
            os.remove(self.EASYLIST)
            shutil.move(tmp_easylist,self.EASYLIST)
            self.logger.info("Updated easylist from {} to {}".format(cur_version,tmp_version))
        elif cur_version == -1:
            shutil.move(tmp_easylist,self.EASYLIST)
            self.logger.info("New easylist {}".format(tmp_version))
        else:
            os.remove(tmp_easylist)
            self.logger.info("Easylist already up to date at: {}".format(tmp_version))

    def _load_easylist(self):
        '''
        Reads in easylist from a file and parses it into lines to be passed to
        abblockparser.
        '''
        with open(self.EASYLIST) as f:
            lines = f.read().splitlines()
        self.logger.info("Loaded easylist version: {} with : {} items".format(self._easylist_version(),len(lines)))
        return lines


    def __init__(self, browser="firefox", log_file="log.txt", unit_id=0, treatment_id=0, headless=False, proxy=None,rules=None):
        
        logging.basicConfig(filename=log_file,level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # if easylist is not passed in, then consider this is a bare unit that 
        # that should only be used to fetch easylist and then parse into
        # adblockplus rules for use with adblockparser.
        if rules == None:
            self._fetch_easylist()
            self.filterlist = self._load_easylist()
            self.rules = AdblockRules(self.filterlist)
        else:
            # call parent constructor
            browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)

            self.session = self.driver.session_id
            print("Running adblock unit session: {}".format(self.session))
            
            # set rules to those that where passed in
            self.rules = rules
            self.all_options = {opt:True for opt in AdblockRule.BINARY_OPTIONS}

            # internal ad data structure 
            self.data = {}

            # dictionary to memoize url checks
            self.memo = {}

    def save_data(self):
        json_file = os.path.splitext(self.log_file)[0]+"."+self.session+".json"
        with open(json_file, 'w') as outfile:
            json.dump(self.data, outfile)
        self.logger.info("save_data:{}:{}:{}".format(self.unit_id,self.treatment_id,self.session))

    def log_element(self,element,source):
        '''
        Input: An element that has been identified as an ad and how it was identified
        Result: Inserts appropriate information into the log
        '''
        url = element.get_attribute(source)
        html = element.get_attribute('outerHTML').encode('utf-8')
        tag = element.tag_name
        link_text = element.text
        link_location = element.location
        url_query = urlparse(url).query
        query_args = parse_qs(url_query)
         
        # update internal datastore
        #element_data = (url,tag,link_text,link_location,query_args)
        element_data = (link_text,link_location,tag)
        if url in self.data:
            row = self.data[url]
            row.append(element_data)
        else:
            row = [element_data,]
        
        # store to internal data structure
        self.data[url] = row

        # store log line
        self.logger.debug("Ad:Data:{}".format(element_data))

    def check_elements(self, elements, source, options=None):
        '''
        Input: Given an element in the currently active page and an attribute to query on
        Result: Queries the given attribute (source) and checks the url against the 
        filterlist. Logs any identified elements and returns the count.
        '''
        count = 0
        for e in elements:
            try:
                url = e.get_attribute(source)
                if url != None:
                    self.logger.debug("Checking:{}:{}".format(source, url))
                    # check if we have evaluated this ad before
                    if url not in self.memo:
                        # actually check the url against the filter list
                        self.memo[url] = self.rules.should_block(url, options)

                    if self.memo[url]:
                        self.log_element(e,source)
                        count+=1

            # occurs with stale elements that no longer exist in the DOM
            except selenium.common.exceptions.StaleElementReferenceException as e:
                self.logger.error(e)
        return count


    def check_href(self):
        '''
        Identifies and captures ads based on HTML hyperlink tags.
        These are considered "text" ads.
        '''
        driver = self.driver
        ### xpath could be less performant than other find_* methods
        # common tags: <a>,<link>
        elements = driver.find_elements_by_xpath("//*[@href]")
        count = self.check_elements(elements,"href", self.all_options)
        self.logger.debug("href search found: {}".format(count))
    

    def check_src(self):
        '''
        Identifies and captures ads based on tags with a 'src' attribute
        These are considered "media" ads and are often img, iframe,script
        tags
        '''
        driver = self.driver
        ### xpath could be less performant than other find_* methods
        # common tags: <img>, <iframe>, <frame>, <embed>, <script>
        elements = driver.find_elements_by_xpath("//*[@src]")
        count = self.check_elements(elements, "src", self.all_options)
        self.logger.debug("src search found: {}".format(count))


    def check_iframe(self,parents=()):
        '''
        Functionality to check within nested iframes for ad related resources.
        Invariants: expects webdriver to enter at the level defined by parents
        resets webdriver to top level contents prior to leaving
        Input: a tuple describing the iframe name attribute of parent levels
        '''

        driver = self.driver
        children = driver.find_elements_by_tag_name('iframe')

        for child in children:

            try:
                driver.switch_to.frame(child)

                # check in the iframe for ads
                self.check_href()
                self.check_src()

                # set parent for children we check
                nesting = parents + (child,)
                self.check_iframe(parents=nesting)

            except selenium.common.exceptions.StaleElementReferenceException as e:
                self.logger.error(e)

            # return to correct level of nesting
            driver.switch_to_default_content()

            for p in parents:
                try:
                    driver.switch_to.frame(p)
                except selenium.common.exceptions.NoSuchElementException as e:
                    # this should not occur but just in case, preserve invariant
                    # of function leaving at top level
                    self.logger.error("resetting level in iframe recursion")
                    driver.switch_to_default_content()


        # always reset to top level content prior to exiting
        driver.switch_to_default_content()

    def find_ads(self):
        '''
        Primary convenience function to use all ad identification mechanisms
        '''
        self.check_href()
        self.check_src()
        self.check_iframe()

    def visit_url(self,url):
        driver = self.driver
        try:
            driver.get(url)
            self.logger.debug("Visited: {}".format(url))
            return True
        except:
            self.logger.error("Error Visiting: {}".format(url))
            return False


    def collect_ads(self,url, reloads=1, delay=0, file_name=None):
        '''
        Visits a specified url and runs ad collection functions
        Result: 
        '''
        print("collecting ads on: {}".format(url))
        if file_name == None:
            file_name = self.log_file

        # number of reloads on site to capture all ads
        for r in range(reloads):
            time.sleep(delay)

            # if a successful visit
            if self.visit_url(url):
                # collect ads
                self.find_ads()
