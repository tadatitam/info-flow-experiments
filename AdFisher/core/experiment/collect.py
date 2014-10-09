import unittest, time								# unittest starts of the testing environment for browsers, time.sleep
import os, platform									# for running  os, platform specific function calls
import sys, re										# sys.argv, to parse treatments								# 
from datetime import datetime						# for tagging log with datetime
from selenium import webdriver						# for running the driver on websites
from selenium.webdriver.common.proxy import *		# for proxy settings

# from xvfbwrapper import Xvfb						# for creating artificial display buffers to run experiments				
import helper as cole								# functions from collectHelper

import signal										# for timing out external calls

myProxy = "yogi.pdl.cmu.edu:3128"

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': '' # set this value as desired
    })

class TimeoutException(Exception): 
    pass 
    
class Webdriver(unittest.TestCase):
	def setUp(self):
# 		self.vdisplay = Xvfb(width=1280, height=720)
# 		self.vdisplay.start()
# 		if(not vdisplay.start()):
# 			fo = open(LOG_FILE, "a")
# 			fo.write("Xvfbfailure||"+str(TREATMENTID)+"||"+str(ID)+"\n")
# 			fo.close()
# 			sys.exit(0)
		if(BROWSER=='firefox'):
			if (platform.system()=='Darwin'):
				self.driver = webdriver.Firefox()
			elif (platform.system()=='Linux'):
# 				self.driver = webdriver.Firefox(proxy=proxy)
				self.driver = webdriver.Firefox()
			else:
				print "Unidentified Platform"
				sys.exit(0)
		elif(BROWSER=='chrome'):
			print "WARNING: Expecting chromedriver at specified location !!"
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
		self.base_url = "https://www.google.com/"
		self.verificationErrors = []
		self.driver.set_page_load_timeout(40)
		self.accept_next_alert = True
	
	def test_webdriver(self):
		driver = self.driver
		cole.setLogFile(LOG_FILE)
		cole.log("browserStarted||"+str(TREATMENTID), ID)
		run = 0
		while (run < RUNS):
			cole.applyTreatment(driver, TREATMENTS[TREATMENTID], ID, TREATMENTID)
			cole.wait_for_others(AGENTS, ID, ROUND)
			time.sleep(20)
			cole.collectMeasurement(driver, MEASUREMENT, ID, TREATMENTID)
			run = run+1

	def tearDown(self):
# 		self.vdisplay.stop()
		self.driver.quit()

def run_script(id, agents, treatmentid, runs, browser, logfile, round, treatments, measurement, timeout=2000):
	global ID, AGENTS, TREATMENTID, RUNS, BROWSER, ROUND, LOG_FILE, SITE_FILE, TREATMENTS, MEASUREMENT
	ID = id
	AGENTS = agents
	TREATMENTID = treatmentid
	RUNS = runs
	BROWSER = browser
	LOG_FILE = logfile
	ROUND = round
	TREATMENTS = treatments
	MEASUREMENT = measurement
	if (ID > AGENTS):
		sys.exit("ERROR: id must be less than total instances")
		
	
	def signal_handler(signum, frame):
		print "Timeout!"
		fo = open(LOG_FILE, "a")
		fo.write(str(datetime.now())+"||TimedOut||"+str(TREATMENTID)+"||"+str(ID)+"\n")
		fo.close()
		raise TimeoutException("Timed out!")
		
# 	timeout = 10	
	
	old_handler = signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(timeout)   # 2000 seconds
	try:
		suite = unittest.TestLoader().loadTestsFromTestCase(Webdriver)
		unittest.TextTestRunner(verbosity=1).run(suite)
	except TimeoutException:
		return
	finally:
		print "Instance", ID, "exiting!"
		signal.signal(signal.SIGALRM, old_handler)
	
	signal.alarm(0)
