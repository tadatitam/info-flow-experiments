import unittest, time, re
import os, platform
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *

from xvfbwrapper import Xvfb

import matplotlib
from datetime import datetime

import collectHelper as cole

LOG_FILE = "log"
myProxy = "yogi.pdl.cmu.edu:3128"

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
		if(BROWSER=='ff'):
			if (platform.system()=='Darwin'):
				self.driver = webdriver.Firefox()
			elif (platform.system()=='Linux'):
				self.driver = webdriver.Firefox(proxy=proxy)
			else:
				print "Unidentified Platform"
				sys.exit(0)
		elif(BROWSER=='chr'):
			if (platform.system()=='Darwin'):
				chromedriver = "/Users/amitdatta/Desktop/chromedriver/chromedriver_mac"
				os.environ["webdriver.chrome.driver"] = chromedriver
				self.driver = webdriver.Chrome(executable_path=chromedriver)
			elif (platform.system() == 'Linux'):
				chromedriver = "root/Desktop/chromedriver/chromedriver_linux"
				os.environ["webdriver.chrome.driver"] = chromedriver
				chrome_option = webdriver.ChromeOptions()
				chrome_option.add_argument("--proxy-server=yogi.pdl.cmu.edu:3128" )
				self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_option)
			else:
				print "Unidentified Platform"
				sys.exit(0)
		else:
			print "Unknown Browser"
			sys.exit(0)
		self.driver.implicitly_wait(5)
		self.base_url = "https://www.google.com/"
		self.verificationErrors = []
		self.driver.set_page_load_timeout(10)
		self.accept_next_alert = True
	
	def test_webdriver(self):
		driver = self.driver
		cole.optIn(driver)
		driver.get(SITE)
		time.sleep(10)
		#raw_input("wait")
		pref = cole.get_ad_pref(2, driver)
		print SITE
		print 'pref=', pref
		if pref != []:
			fo = open(TARGET_FILE, "a")
			fo.write(SITE+"||"+", ".join(pref)+'\n')
			fo.close()

    
	def tearDown(self):
		self.driver.quit()
		self.vdisplay.stop()
		self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
# 	if len(sys.argv) != 8:
# 		sys.exit("SYNTAX: collector.py <id> <total-instances> <TREATMENT (a/b)> #runs #reloads #delay browser")
	global BROWSER, SITE, TARGET_FILE
	BROWSER = sys.argv[1]
	SITE = sys.argv[2]
	TARGET_FILE = sys.argv[3]
			
	del sys.argv[1:]
	unittest.main()
