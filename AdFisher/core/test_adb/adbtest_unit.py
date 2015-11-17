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

# imports to save screen shots
from PIL import Image
import StringIO
import base64

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
        # key: url (as extracted from the page using  find_href_ads and find_src_ads"
        # value: [(site,link_text,location,{url_paramters})]
        self.data = {}


    def visit_url(self,url):
        '''
        Visits a specificed url and stores screen shot in memory.
        Result: following this self.driver can be used to query the page for ads
        '''
        driver = self.driver
        driver.get(url)
        logging.info("Visited: {}".format(url))
        self.screenshot = self.screenshot_page()
    
    def screenshot_page(self):
        '''
        Captures a screenshot of the fullpage in memory.
        The screenshot includes everything even if it is not scrolled into view
        '''
        # uses PIL library to open image in memory
        driver = self.driver
        b64_shot = driver.get_screenshot_as_base64()
        decode  = base64.decodestring(b64_shot)
        s = StringIO.StringIO(decode)
        img = Image.open(s)
        return img

    def log_element(self,element,source):
        '''
        Input: An element that has been identified as an ad and how it was identified
        Result: Inserts appropriate information into the log
        If nessecary saves images and screenshots
        '''
        url = element.get_attribute(source)
        html = element.get_attribute('outerHTML').encode('utf-8')
        tag = element.tag_name
        link_text = element.text
        link_location = element.location
        url_query = urlparse(url).query
        query_args = parse_qs(url_query)
        #logging.info("Ad:Contents:{}:{}:{}".format(self.session, element.id, html))
        
        
        element_data = (url,tag,link_text,link_location,query_args)
        if url in self.data:
            row = self.data[url]
            row.append(element_data)
        else:
            row = [element_data,]

        logging.info("Ad:Data:{}".format(element_data))

        try:
            if tag == "img":
                urllib.urlretrieve(url, os.path.join(self.log_dir,"image_"+str(element.id)))
            elif tag == "a":
                a_img =  element.get_attribute("img")
                if a_img != None:
                    urllib.urlretrieve(url, os.path.join(self.log_dir,"a_image_"+str(element.id)))
            elif tag == "iframe":
                self.screen_shot_element(element)
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

    def find_ads(self):
        '''
        Convenience function to use all ad identification mechanisms
        '''
        self.find_href_ads()
        self.find_src_ads()

    def screen_shot_element(self, element):
        '''
        Input: a specific element on the page
        Result: saves a clipped image from the full page screenshot
        '''
        location = element.location
        size = element.size
        
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']


        # must have a visible size. top level container iframes will often fail this.
        if left == 0 or top == 0 or right == 0 or bottom == 0  or size['width'] == 0 or size['height'] ==0:
            logging.error("screen_shot_element:{}:{}:({},{} by {},{})".format(self.session,element.id,left,top,right,bottom))
            return
        
        try:
            img = img.crop((left, top, right, bottom)) # defines crop points
            img.save(os.path.join(self.log_dir,'iframe_'+str(element.id)+'.png')) # saves new cropped image
        except:
            logging.error("clipping screenshot:{}:{}".format(self.session,element.id))


    def check_iframes(self,parents=()):
        '''
        expect to enter at the level defined by parents
        collect subframes and loop
            enter subframe
            return to level defined by parents
        returns to top level
        '''

        driver = self.driver
        children = driver.find_elements_by_tag_name('iframe')

        for child in children:
            try:
                child_name = child.get_attribute('name').encode('utf-8')
            except selenium.common.exceptions.StaleElementReferenceException as e:
                logging.error(e)
                break

            xpath = '//iframe[@name="{}"]'.format(child_name)
            try:
                c_elem = driver.find_element_by_xpath(xpath)
                driver.switch_to.frame(c_elem)

                # check in the iframe for ads
                #self.find_href_ads()
                self.find_ads()
                
                # set parent for children we check
                nesting = parents + (child_name,)
                self.check_iframes(parents=nesting)
            except selenium.common.exceptions.NoSuchElementException as e:
                # if selenium was unable to `find_element_by_xpath` than we just skip it
                # we rely on `find_element_by_xpath` to naviagate between nested levels
                continue

            # return to correct level of nesting
            driver.switch_to_default_content()
            for p in parents:
                parent_xpath = '//iframe[@name="{}"]'.format(p)
                try:
                    p_elem = driver.find_element_by_xpath(parent_xpath)
                    driver.switch_to.frame(p_elem)
                except selenium.common.exceptions.NoSuchElementException as e:
                    # this should not occur becasue above we correctly bail on iframes
                    # we can't navigate by "name", but just in case, preserve invaraint
                    # of function leaving at top level
                    logging.error("resetting level in iframe recursion")
                    driver.switch_to_default_content()


        driver.switch_to_default_content()


