import logging
import datetime
import os
import urllib

# imports to use selenium
import selenium
from selenium import webdriver
from xvfbwrapper import Xvfb    # artificial display for headless experiments

# imports to parse easylist
from adblockparser import AdblockRules
from adblockparser import AdblockRule

# imports to parse url
from urlparse import urlparse, parse_qs

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

        # setup selenium webdriver
        self.driver = webdriver.Firefox()
        self.session = self.driver.session_id
        print("Running session: {}".format(self.session))

        # setup session specific logging directory
        self.log_dir = os.path.join(os.getcwd(),"log_"+self.session)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        logging.basicConfig(filename=os.path.join(self.log_dir,'log.adbtest_unit.txt'),level=logging.INFO)
        
        # load easy list
        if easyList:
            self.rules = AdblockRules(self._load_easy_list())
            self.all_options = {opt:True for opt in AdblockRule.BINARY_OPTIONS}
        else:
            logging.info("skipping easy list")

        # data structure a dictionary with the following format
        # key: url (as extracted from the page using find_href_ads and find_src_ads
        # value: [(site,link_text,location,{url_paramters})]
        self.data = {}


    def visit_url(self,url):
        '''
        Visits a specificed url
        Result: following this self.driver can be used to query the page for ads
        '''
        driver = self.driver
        driver.get(url)
        logging.info("Visited: {}".format(url))
    

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
        
        # store to internal datastructure
        self.data[url] = row

        # store log line
        logging.info("Ad:Data:{}".format(element_data))

        # try enhanced collection beyond just url and link text
        try:
            if tag == "img":
                size = element.size
                if size['width']>=100 and size['height']>100:
                        urllib.urlretrieve(url, os.path.join(self.log_dir,"image_"+str(element.id)))
            elif tag == "a":
                a_img =  element.get_attribute("img")
                if a_img != None:
                    urllib.urlretrieve(url, os.path.join(self.log_dir,"a_image_"+str(element.id)))
        except:
            logging.error("Collecting enhanced contents:{}:{}:{}".format(self.session,element.id,tag))


    def check_elements(self, elements, source, options=None):
        '''
        Input: Given an element in the currently active page and an attribute to quer on
        Result: Queries the given attribute (source) and checks the url against the 
        filterlist. Logs any identified elements and returns the count.
        '''
        count = 0
        for e in elements:
            try:
                url = e.get_attribute(source)
                logging.info("Checking:{}:{}".format(source, url))
               
                # actually check the url against the filter list
                if self.rules.should_block(url, options):
                    self.log_element(e,source)

                    count+=1

            # occurs with stale elements that no longer exist in the DOM
            except selenium.common.exceptions.StaleElementReferenceException as e:
                logging.error(e)
        return count


    def find_href_ads(self):
        '''
        Identifies and captures ads based on HTML hyperlink tags.
        These are considered "text" ads.
        '''
        driver = self.driver
        elements = driver.find_elements_by_xpath("//*[@href]")
        count = self.check_elements(elements,"href", self.all_options)
        print "href search found: {}".format(count)
    

    def find_src_ads(self):
        '''
        Indetifies and captures ads based on tags with a 'src' attribute
        These are considered "media" ads and are often img, iframe,script
        tags
        '''
        driver = self.driver
        elements = driver.find_elements_by_xpath("//*[@src]")
        count = self.check_elements(elements, "src", self.all_options)
        print "src search found: {}".format(count)


    def check_iframes(self,parents=()):
        '''
        Functionality to check within nested iframes for ad related resources.
        Invariants: expects webdriver to enter at the level defined by parents
        resets webdriver to top level contents prior to leaving
        Input: a tuple describing the iframe name atrribute of parent levels
        '''

        driver = self.driver
        children = driver.find_elements_by_tag_name('iframe')
        for child in children:
            try:
                child_name = child.get_attribute('name').encode('utf-8')
            except selenium.common.exceptions.StaleElementReferenceException as e:
                logging.error(e)
                break

            driver.switch_to.frame(child)

            # check in the iframe for ads
            self.find_href_ads()
            self.find_src_ads()

            # set parent for children we check
            nesting = parents + (child,)
            self.check_iframes(parents=nesting)

            # return to correct level of nesting
            driver.switch_to_default_content()
            for p in parents:
                try:
                    driver.switch_to.frame(p)
                except selenium.common.exceptions.NoSuchElementException as e:
                    # this should not occur becasue above we correctly bail on iframes
                    # we can't navigate by "name", but just in case, preserve invaraint
                    # of function leaving at top level
                    logging.error("resetting level in iframe recursion")
                    driver.switch_to_default_content()


        # always reset to top level content prior to exiting
        driver.switch_to_default_content()
        #print "exiting"

    def find_ads(self):
        '''
        Primary convenience function to use all ad identification mechanisms
        '''
        self.find_href_ads()
        self.find_src_ads()
        self.check_iframes()

# element_data = (url,tag,link_text,link_location,query_args)
    def query_data(self,search=None):
        for k,v in self.data.iteritems():
             title=v[0][2]
             if search != None:
                 if title==search:
                     print k[:80]
                     print "#"*20
                     for iid, instance in enumerate(v):
                         print "-"*10
                         print "iid: ",iid
                         print "link text: ",instance[1]
                         for vk,vv in instance[2].iteritems():
                             print "\t",vk,vv
             else:
                 print title
