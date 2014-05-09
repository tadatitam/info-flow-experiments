import unittest, time								# unittest starts of the testing environment for browsers, time.sleep
import os, platform									# for running  os, platform specific function calls
import sys											# sys.argv
import re											# to parse treatments

from selenium import webdriver						# for running the driver on websites
from selenium.webdriver.common.proxy import *		# for proxy settings

from xvfbwrapper import Xvfb						# for creating artificial display buffers to run experiments				
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
			fo.write("Xvfbfailure||"+str(TREATMENTID)+"||"+str(ID)+"\n")
			fo.close()
			sys.exit(0)
		if(BROWSER=='firefox'):
			if (platform.system()=='Darwin'):
				self.driver = webdriver.Firefox()
			elif (platform.system()=='Linux'):
				self.driver = webdriver.Firefox(proxy=proxy)
			else:
				print "Unidentified Platform"
				sys.exit(0)
		elif(BROWSER=='chrome'):
			print "WARNING: Expecting chromedriver at specified location !!"
			if (platform.system()=='Darwin'):
				chromedriver = "chromedriver/chromedriver_mac"
				os.environ["webdriver.chrome.driver"] = chromedriver
				self.driver = webdriver.Chrome(executable_path=chromedriver)
			elif (platform.system() == 'Linux'):
				chromedriver = "chromedriver/chromedriver_linux"
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
		self.driver.set_page_load_timeout(40)
		self.accept_next_alert = True
	
	def test_webdriver(self):
		driver = self.driver
		cole.setLogFile(LOG_FILE)
		cole.log("browserStarted||"+str(TREATMENTID), ID)
		cole.optIn(driver)							# Enable behavioral ads
		cole.log("optedIn||"+str(TREATMENTID), ID)
		run = 0
		while (run < RUNS):
			cole.applyTreatment(driver, TREATMENTS[TREATMENTID], ID, TREATMENTID)
			cole.wait_for_others(SAMPLES, ID, ROUND)
			pref = cole.get_ad_pref(2, driver)
			cole.log("pref"+"||"+str(TREATMENTID)+"||"+", ".join(pref), ID)
			cole.collect_ads(RELOADS, DELAY, LOG_FILE, driver, ID, TREATMENTID, 'toi')
			run = run+1

    
	def tearDown(self):
		self.driver.quit()
		self.vdisplay.stop()
		self.assertEqual([], self.verificationErrors)


def run_script(id, samples, treatment, runs, reloads, delay, browser, logfile, round, treatments, timeout=2000):
	global ID, SAMPLES, TREATMENTID, RUNS, RELOADS, DELAY, BROWSER, ROUND, LOG_FILE, SITE_FILE, TREATMENTS
	ID = id
	SAMPLES = samples
	TREATMENTID = treatment
	RUNS = runs
	RELOADS = reloads
	DELAY = delay
	BROWSER = browser
	LOG_FILE = logfile
	ROUND = round
	TREATMENTS = treatments
	if (ID > SAMPLES):
		sys.exit("ERROR: id must be less than total instances")
		
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(timeout)   # 2000 seconds
	try:
		suite = unittest.TestLoader().loadTestsFromTestCase(Webdriver)
		unittest.TextTestRunner(verbosity=2).run(suite)
	except Exception, msg:
		print "Timed out!"
		fo = open(LOG_FILE, "a")
		fo.write("LaunchFailure||"+str(TREATMENTID)+"||"+str(ID)+"\n")
		fo.close()
		sys.exit(0)


# if __name__ == "__main__":
# 	global ID, SAMPLES, TREATMENT, RUNS, RELOADS, DELAY, BROWSER, ROUND, LOG_FILE, SITE_FILE, STR_TREAT
# 	ID = int(sys.argv[1])
# 	SAMPLES = int(sys.argv[2])
# 	TREATMENT = int(sys.argv[3])
# 	RUNS = int(sys.argv[4])
# 	RELOADS = int(sys.argv[5])
# 	DELAY = int(sys.argv[6])
# 	BROWSER = sys.argv[7]
# 	LOG_FILE = sys.argv[8]
# 	ROUND = sys.argv[9]
# 	STR_TREAT = sys.arg[10]
# 	if (ID > SAMPLES):
# 		sys.exit("ERROR: id must be less than total instances")
# 	
# 	del sys.argv[1:]
# 	
# 	signal.signal(signal.SIGALRM, signal_handler)
# 	signal.alarm(2000)   # Ten seconds
# 	try:
# 		unittest.main()
# 	except Exception, msg:
# 		print "Timed out!"
# 		fo = open(LOG_FILE, "a")
# 		fo.write("LaunchFailure||"+str(TREATMENT)+"||"+str(ID)+"\n")
# 		fo.close()
# 		sys.exit(0)
