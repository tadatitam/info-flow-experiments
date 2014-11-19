import unittest, time								# unittest starts of the testing environment for browsers, time.sleep
import os, platform									# for running  os, platform specific function calls
import sys											# sys.argv

from selenium import webdriver						# for running the driver on websites
from selenium.webdriver.common.proxy import *		# for proxy settings

from xvfbwrapper import Xvfb						# for creating artificial display to run experiments				
import helper as cole								# functions from collectHelper

LOG_FILE = "log"
myProxy = "proxy.pdl.cmu.edu:8080"

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': '' # set this value as desired
    })


class Webdriver(unittest.TestCase):
	def setUp(self):
		self.vdisplay = Xvfb(width=1280, height=720)
		self.vdisplay.start()
# 		if(not vdisplay.start()):
# 			fo = open(LOG_FILE, "a")
# 			fo.write("Xvfbfailure||"+str(TREATMENTID)+"||"+str(ID)+"\n")
# 			fo.close()
# 			sys.exit(0)
		if(BROWSER=='firefox'):
			if (platform.system()=='Darwin'):
				self.driver = webdriver.Firefox()
			elif (platform.system()=='Linux'):
				self.driver = webdriver.Firefox(proxy=proxy)
			else:
				print "Unidentified Platform"
				sys.exit(0)
		elif(BROWSER=='chrome'):
			if (platform.system()=='Darwin'):
				chromedriver = "./experiment/chromedriver/chromedriver_mac"
				os.environ["webdriver.chrome.driver"] = chromedriver
				self.driver = webdriver.Chrome(executable_path=chromedriver)
			elif (platform.system() == 'Linux'):
				chromedriver = "./experiment/chromedriver/chromedriver_linux"
				os.environ["webdriver.chrome.driver"] = chromedriver
				chrome_option = webdriver.ChromeOptions()
				chrome_option.add_argument("--proxy-server=yogi.pdl.cmu.edu:3128" )
				self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_option)
			else:
				print "Unidentified Platform"
				sys.exit(0)
		else:
			print "Unsupported Browser"
			sys.exit(0)
		self.driver.implicitly_wait(10)
		self.verificationErrors = []
		self.driver.set_page_load_timeout(40)
		self.accept_next_alert = True
	
	def test_webdriver(self):
		fo = open(SITE_FILE, "w")
		fo.close()
		driver = self.driver
 		driver.get("https://adwords.google.com/da/DisplayPlanner/Home?__c=9100554603&__u=1800375603&__o=cues#start")
		raw_input("wait")
		count = 0
		els = driver.find_elements_by_css_selector("tr td div div div a")
		print len(els)
		for el in els:
			t = el.get_attribute('innerHTML').lower()
			print t
			fo = open(SITE_FILE, "a")
			fo.write(t + '\n')
			fo.close()
			count += 1
		raw_input("done")
		
    
	def tearDown(self):
		self.vdisplay.stop()
		self.driver.quit()

def run_script(word, file, nsites, browser):
	global SITE_FILE, WORD, BROWSER, N
	BROWSER = browser
	SITE_FILE = file
	WORD = word
	N = nsites
	suite = unittest.TestLoader().loadTestsFromTestCase(Webdriver)
	unittest.TextTestRunner(verbosity=1).run(suite)
