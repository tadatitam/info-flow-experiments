import unittest, time								# unittest starts of the testing environment for browsers, time.sleep
import os, platform									# for running  os, platform specific function calls
import sys											# sys.argv

from selenium import webdriver						# for running the driver on websites
from selenium.webdriver.common.proxy import *		# for proxy settings

from xvfbwrapper import Xvfb						# for creating artificial display to run experiments				
import collectHelper as cole						# functions from collectHelper

import signal										# for timing out external calls

def signal_handler(signum, frame):
    raise Exception("Timed out!")
    
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
		if(not self.vdisplay.start()):
			fo = open(LOG_FILE, "a")
			fo.write("Xvfbfailure||"+str(TREATMENT)+"||"+str(ID)+"\n")
			fo.close()
			sys.exit(0)
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
		cole.setLogFile(LOG_FILE)
		cole.log("browserStarted||"+str(TREATMENT), ID)
		cole.optIn(driver)							# Enable behavioral ads
		cole.log("optedIn||"+str(TREATMENT), ID)	
		run = 0
		while (run < RUNS):
			print(run)
			if(TREATMENT == '0'):
				cole.collect_ads(RELOADS, DELAY, LOG_FILE, driver, ID, TREATMENT, site='toi')
			elif(TREATMENT == '1'):
				cole.collect_ads(RELOADS, DELAY, LOG_FILE, driver, ID, TREATMENT, site='bbc')		
			elif(TREATMENT == '2'):
				cole.collect_ads(RELOADS, DELAY, LOG_FILE, driver, ID, TREATMENT, site='guardian')	
			elif(TREATMENT == '3'):
				cole.collect_ads(RELOADS, DELAY, LOG_FILE, driver, ID, TREATMENT, site='reuters')
			elif(TREATMENT == '4'):
				cole.collect_ads(RELOADS, DELAY, LOG_FILE, driver, ID, TREATMENT, site='bloomberg')	
			run = run+1

    
	def tearDown(self):
		self.driver.quit()
		self.vdisplay.stop()
		self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
	global ID, SAMPLES, TREATMENT, RUNS, RELOADS, DELAY, BROWSER, ROUND, LOG_FILE, SITE_FILE
	ID = int(sys.argv[1])
	SAMPLES = int(sys.argv[2])
	TREATMENT = sys.argv[3]
	RUNS = int(sys.argv[4])
	RELOADS = int(sys.argv[5])
	DELAY = int(sys.argv[6])
	BROWSER = sys.argv[7]
	LOG_FILE = sys.argv[8]
	SITE_FILE = sys.argv[9]
	ROUND = sys.argv[10]
	if (ID > SAMPLES):
		sys.exit("ERROR: id must be less than total instances")
	
	del sys.argv[1:]	
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(2000)   # Ten seconds
	try:
		unittest.main()
	except Exception, msg:
		print "Timed out!"
		fo = open(LOG_FILE, "a")
		fo.write("LaunchFailure||"+str(TREATMENT)+"||"+str(ID)+"\n")
		fo.close()
		sys.exit(0)
