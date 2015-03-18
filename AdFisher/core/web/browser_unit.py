import time, re 							# time.sleep, re.split
import sys 									# some prints
import os, platform 						# for running  os, platform specific function calls
from selenium import webdriver 				# for running the driver on websites
from datetime import datetime 				# for tagging log with datetime
from selenium.webdriver.common.proxy import *		# for proxy settings

class BrowserUnit:

	def __init__(self, browser, log_file, unit_id, treatment_id, proxy=None):
		if(proxy != None):
			sproxy = Proxy({
    			'proxyType': ProxyType.MANUAL,
    			'httpProxy': proxy,
    			'ftpProxy': proxy,
    			'sslProxy': proxy,
    			'noProxy': '' # set this value as desired
   			 	})
		else:
			sproxy = Proxy({
    			'proxyType': ProxyType.MANUAL
   			 	})
			
		if(browser=='firefox'):
			if (platform.system()=='Darwin'):
				self.driver = webdriver.Firefox(proxy=sproxy)
			elif (platform.system()=='Linux'):
				self.driver = webdriver.Firefox(proxy=sproxy)
			else:
				print "Unidentified Platform"
				sys.exit(0)
		elif(browser=='chrome'):
			print "WARNING: Expecting chromedriver at specified location !!"
			if (platform.system()=='Darwin'):
				chromedriver = "./chromedriver/chromedriver_mac"
			elif (platform.system() == 'Linux'):
				chromedriver = "./chromedriver/chromedriver_linux"
			else:
				print "Unidentified Platform"
				sys.exit(0)
			os.environ["webdriver.chrome.driver"] = chromedriver
			chrome_option = webdriver.ChromeOptions()
			chrome_option.add_argument("--proxy-server="+proxy)
			self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_option)
		else:
			print "Unsupported Browser"
			sys.exit(0)
		self.driver.implicitly_wait(10)
		self.base_url = "https://www.google.com/"
		self.verificationErrors = []
		self.driver.set_page_load_timeout(40)
		self.accept_next_alert = True
		self.log_file = log_file
		self.unit_id = unit_id
		self.treatment_id = treatment_id

	def quit(self):
		self.driver.quit()
	
	def log(self, linetype, linename, msg):		# linetype = ['treatment', 'measurement', 'event', 'error', 'meta']
		"""Maintains a log of visitations"""
		fo = open(self.log_file, "a")
		fo.write(str(datetime.now())+"||"+linetype+"||"+linename+"||"+msg+"||"+str(self.unit_id)+"||"+str(self.treatment_id) + '\n')
		fo.close()   	
	
	def interpret_log_line(self, line):
		"""Interprets a line of the log, and returns six components
			For lines containing meta-data, the unit_id and treatment_id is -1
		"""
		chunks = re.split("\|\|", line)
		tim = chunks[0]
		linetype = chunks[1]
		linename = chunks[2]
		value = chunks[3].strip()
		if(len(chunks)>5):
			unit_id = chunks[4]
			treatment_id = chunks[5].strip()
		else:
			unit_id = -1
			treatment_id = -1
		return tim, linetype, linename, value, unit_id, treatment_id
		
	def train_with_sites(self, file_name): 
		"""Visits all pages in file_name"""
		fo = open(file_name, "r")
		for line in fo:
			chunks = re.split("\|\|", line)
			site = "http://"+chunks[0].strip()
			try:
				self.driver.set_page_load_timeout(40)
				self.driver.get(site)
				time.sleep(5)
				self.log('treatment', 'visit website', site)
							# pref = get_ad_pref(self.driver)
							# self.log("pref"+"||"+str(treatment_id)+"||"+"@".join(pref), self.unit_id)
			except:
				self.log('error', 'website timeout', site)


	def wait_for_others(self):
		"""Makes instance with SELF.UNIT_ID wait while others train"""
		fo = open(self.log_file, "r")
		line = fo.readline()
		tim, linetype, linename, value, unit_id, treatment_id = self.interpret_log_line(line)
		instances = int(value)
	
		fo = open(self.log_file, "r")
		for line in fo:
			tim, linetype, linename, value, unit_id, treatment_id = self.interpret_log_line(line)
			if(linename == 'block_id'):
				round = int(value)
# 		print "round, instances: ", round, instances
		
		clear = False
		count = 0
		round = int(round)
		while(not clear):
			count += 1
			if(count > 500):
				self.log('event', 'wait_for_others timeout', 'breaking out')
				break
			c = [0]*instances
			curr_round = 0
			fo = open(self.log_file, "r")
			for line in fo:
				tim, linetype, linename, value, unit_id, treatment_id = self.interpret_log_line(line)
				if(linename == 'block_id'):
					curr_round = int(value)
				if(round == curr_round):
					if(value=='training-start'):
						c[int(unit_id)-1] += 1
					if(value=='training-end'):
						c[int(unit_id)-1] -= 1
			fo.close()
			time.sleep(5)
			clear = True
			for i in range(0, instances):
				if(c[i] == 0):
					clear = clear and True
				else:
					clear = False
