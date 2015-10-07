import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import ad_unit
#from xvfbwrapper import Xvfb    # artificial display for headless experiments



class PythonOrgSearch(unittest.TestCase):
    ''' Sample selenium test case to ensure all dependencies are met for running 
    headless tests'''

    def setUp(self):
        print "python org search"
        self.browser =  ad_unit.AdUnit()
        self.driver = self.browser.driver

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


class BrowseSites(unittest.TestCase):
    ''' Test browsing to sites using ad_unit driver '''

    def setUp(self):
        self.browser =  ad_unit.AdUnit()
        self.driver = self.browser.driver

    def test_browse_yahoo_news(self):
        self.browser.visit_url("http://news.yahoo.com/")
        assert self.driver.page_source != None

    def test_browse_fox_news(self):
        self.browser.visit_url("http://www.foxnews.com/")
        assert self.driver.page_source != None

    def test_browse_cnn_news(self):
        self.browser.visit_url("http://www.cnn.com/")
        assert self.driver.page_source != None

    def tearDown(self):
        self.driver.close()

class GetAds(unittest.TestCase):
    ''' Test collecting ads from sites using ad_unit driver '''

    def setUp(self):
        self.browser =  ad_unit.AdUnit(easyList=True)
        self.driver = self.browser.driver

    def test_browse_yahoo_news(self):
        self.browser.visit_url("http://news.yahoo.com/")
        self.browser.find_ads()
        self.browser.check_tag("script")
        self.browser.check_tag("img")
        assert self.driver.page_source != None

    def test_browse_fox_news(self):
        self.browser.visit_url("http://www.foxnews.com/")
        self.browser.find_ads()
        self.browser.check_tag("script")
        self.browser.check_tag("img")
        assert self.driver.page_source != None

    def test_browse_cnn_news(self):
        self.browser.visit_url("http://www.cnn.com/")
        self.browser.find_ads()
        self.browser.check_tag("script")
        self.browser.check_tag("img")
        assert self.driver.page_source != None
    
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
#    unittest.main()

    #suite = unittest.TestLoader().loadTestsFromTestCase(PythonOrgSearch)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    #suite = unittest.TestLoader().loadTestsFromTestCase(BrowseSites)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(GetAds)
    unittest.TextTestRunner(verbosity=2).run(suite)

