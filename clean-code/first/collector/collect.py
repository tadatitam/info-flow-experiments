import unittest, time								# unittest starts of the testing environment for browsers, time.sleep
import os, platform									# for running  os, platform specific function calls
import sys											# sys.argv

from selenium import webdriver						# for running the driver on websites
from selenium.webdriver.common.proxy import *		# for proxy settings

from xvfbwrapper import Xvfb						# for creating artificial display to run experiments				
import collectHelper as cole						# functions from collectHelper

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
			print "WARNING: Expecting chromedriver at specified location !!"
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
			print "Unsupported Browser"
			sys.exit(0)
		self.driver.implicitly_wait(10)
		self.base_url = "https://www.google.com/"
		self.verificationErrors = []
		self.driver.set_page_load_timeout(10)
		self.accept_next_alert = True
	
	def test_webdriver(self):
		driver = self.driver
		cole.optIn(driver)							# Enable behavioral ads
        
# 		cole.set_gender(TREATMENT, driver)
# 		time.sleep(3)
#		print(str(ID)+"-"+cole.get_gender(driver))

		run = 0
		while (run < RUNS):
			print(run)
			if(TREATMENT=='1'):
# 				#cole.train_with_queries(list, 11, ID, driver)
				cole.train_with_sites(SITE_FILE, driver, ID, TREATMENT)
				cole.wait_for_others(SAMPLES, ID, ROUND)
			else:
				time.sleep(5)
# 				cole.train_with_sites(LSITE_FILE, driver, ID)
				cole.wait_for_others(SAMPLES, ID, ROUND)
			cole.collect_ads(RELOADS, DELAY, LOG_FILE, driver, ID, TREATMENT)
			run = run+1

    
	def tearDown(self):
		self.driver.quit()
		self.vdisplay.stop()
		self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
	global ID, SAMPLES, TREATMENT, RUNS, RELOADS, DELAY, BROWSER, ROUND
	ID = int(sys.argv[1])
	SAMPLES = int(sys.argv[2])
	TREATMENT = sys.argv[3]
	RUNS = int(sys.argv[4])
	RELOADS = int(sys.argv[5])
	DELAY = int(sys.argv[6])
	BROWSER = sys.argv[7]
	ROUND = sys.argv[8]
	if (ID > SAMPLES):
		sys.exit("ERROR: id must be less than total instances")

# 	if(TREATMENT == '1'):
# 		HSITE_FILE = "american_football.txt"
# 	elif(TREATMENT == '2'):
# 		HSITE_FILE = "basketball.txt"
# 	elif(TREATMENT == '3'):
# 		HSITE_FILE = "baseball.txt"
# 	elif(TREATMENT == '4'):
# 		HSITE_FILE = "ice_hockey.txt"
# 	else:
# 		print "UNHANDLED TREATMENT"
# 		raw_input("Plan what to do! Then press enter to exit")
# 		sys.exit(0)
	
# 	LSITE_FILE="business.employment.txt"

	SITE_FILE = "collector/INT_SITES.txt"		
	del sys.argv[1:]
	unittest.main()
