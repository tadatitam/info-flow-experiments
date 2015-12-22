import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
import browser_unit
from selenium.common.exceptions import NoSuchElementException

import string
import random

SEPARATOR='@|'

# Random gender name declarations
def clean(s):
    toks = s.strip().split(' ')
    return toks[1]

with open('female_names.txt') as f:
    FEMALE_NAMES = map(clean, f.readlines())

with open('male_names.txt') as f:
    MALE_NAMES = map(clean, f.readlines())

# Let's stick to 1 job for now
JOBS = ['software+engineer']
JOBS_SALARY = ['sales']

# Locations may vary
LOCATIONS = ['New+Milford%2C+CT', 'New+York%2C+NY', 'Seattle%2C+WA']

# strip html
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_random_string(N):
	return ''.join(random.choice(string.ascii_uppercase) for _ in range(N))

def random_female_first_name():
	index = random.randrange(1,len(FEMALE_NAMES)-1)
	return FEMALE_NAMES[index]

def random_male_first_name():
	index = random.randrange(1,len(MALE_NAMES)-1)
	return MALE_NAMES[index]

def random_user_email(firstName):
	num_chars_in_lastName = random.randrange(5,40)
	lastName = get_random_string(num_chars_in_lastName)
	return firstName+'@'+lastName+'.com'











class IndeedAdsUnit(browser_unit.BrowserUnit):

  def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
    browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)


  def create_user(self, gender, job_description):
  	self.driver.get('http://www.indeed.com/')

  	signin = self.driver.find_element_by_id("userOptionsLabel").click()

  	signin_but = self.driver.find_element_by_css_selector('.sign_up_prompt a')
  	signin_but.click()

  	# indeed next part
  	firstName = ''
  	if (gender=='male'):
  		firstName = random_male_first_name()
  	else:
  		firstName = random_female_first_name()
  	email_txt = random_user_email(firstName)

  	email = self.driver.find_element_by_id('register_email')
  	email.send_keys(email_txt)

  	retype_email = self.driver.find_element_by_id('register_retype_email')
  	retype_email.send_keys(email_txt)

  	password = self.driver.find_element_by_id('register_password')
  	password.send_keys('12345678910')

  	create_button = self.driver.find_element_by_css_selector('.input_submit.button.blueButton').click()

  	#start searching for jobs now
  	search_bar = self.driver.find_element_by_id('what')
  	search_bar.send_keys(job_description)

  	search_button = self.driver.find_element_by_css_selector('.input_submit')
  	search_button.click()


  # Collects Salary Statistics for separate analysis later
  def collect_salary(self):
      # Salary ranges 30,000 - 125,000 by 5k's
      salary_cutoffs = map(lambda x : str(x) + ',000', range(30, 125, 5))
      salaries = []
      for sal in salary_cutoffs:
          try:
            title = self.driver.find_element_by_partial_link_text(sal).get_attribute('title')
            salaries.append(title)
            self.log('measurement', 'salary', title)
          except:
            pass

  def get_salary_info(self, description):
    newstr = description.replace(",","")
    salary = []
    for i, ch in enumerate(newstr):
      money = ''
      if (ch=='$'):
        index = 1
        while (newstr[i+index].isdigit() and index < len(newstr)):
          money = money + newstr[i+index]
          index = index+1
      if (len(money)):
        salary.append(money)
    return salary

  def indeed_salary(self, fname, rel):
    driver = self.driver
    driver.set_page_load_timeout(60)
    # Varies the location per reload cycle
    exp_link = "http://www.indeed.com/jobs?q="
    exp_link += JOBS_SALARY[rel % len(JOBS_SALARY)]
    exp_link += "&l=" + LOCATIONS[rel % len(LOCATIONS)]
    driver.get(exp_link)
    time.sleep(5)
    driver.execute_script('window.stop()')
    # Get rid of initial advertisement overlay
    try:
      driver.find_element_by_id('prime-popover-close-button').click()
      time.sleep(1)
      driver.execute_script('window.stop()')
    except:
      pass
    ctime = str(datetime.now())
    # Find the advertisement listings using selenium
    sponsored_jobs = driver.find_element_by_css_selector('div[data-tn-section="sponsoredJobs"]')
    job_listings = sponsored_jobs.find_elements_by_css_selector('div[data-tn-component="sponsoredJob"]')
    for job in job_listings:
      description = job.find_element_by_class_name('sjcl').get_attribute('innerHTML').strip()
      salary = self.get_salary_info(description)
      if (len(salary) > 0):
        salary_str = ' '.join(salary)
        print salary_str
        ad = strip_tags(ctime+'@|'+salary_str+'@|'+'PLACEHOLDER'+'@|'+'PLACEHOLDER').encode("utf8")
        self.log('measurement', 'ad', ad)
      driver.switch_to.default_content()


  # Collects the top 3 "Sponsored" listings (ads)
  def indeed_ads(self, fname, rel, salary):
      driver = self.driver
      driver.set_page_load_timeout(60)
      # Varies the location per reload cycle
      exp_link = "http://www.indeed.com/jobs?q="
      exp_link += JOBS[rel % len(JOBS)]
      exp_link += "&l=" + LOCATIONS[rel % len(LOCATIONS)]
      driver.get(exp_link)
      time.sleep(5)
      driver.execute_script('window.stop()')
      # Get rid of initial advertisement overlay
      try:
        driver.find_element_by_id('prime-popover-close-button').click()
        time.sleep(1)
        driver.execute_script('window.stop()')
      except:
        pass
      ctime = str(datetime.now())
      # Find the advertisement listings using selenium
      sponsored_jobs = driver.find_element_by_css_selector('div[data-tn-section="sponsoredJobs"]')
      job_listings = sponsored_jobs.find_elements_by_css_selector('div[data-tn-component="sponsoredJob"]')
      div_id = 'sjcl'
      for i in xrange(1, 4):
        elem_id = 'sja' + str(i)
        title = sponsored_jobs.find_element_by_id(elem_id).get_attribute('title')
        raw_listing = job_listings[i-1]
        listing = raw_listing.find_element_by_class_name(div_id)
        location = listing.find_element_by_class_name('location').get_attribute('innerHTML')
        ad = strip_tags(ctime+SEPARATOR+title.strip()+SEPARATOR+'URL'+SEPARATOR+location).encode("utf8")
        self.log('measurement', 'ad', ad)
        # Optionally find the salary statistics as well
        #if salary:
            #self.collect_salary(driver)
        driver.switch_to.default_content()
   

  def collect_ads(self, reloads, delay, salary=None, file_name=None):
      if not file_name:
          file_name = self.log_file
      rel = 0
      while (rel < reloads):
        time.sleep(delay)
        s = datetime.now()
        if (salary):
          self.indeed_salary(file_name, rel)
        else:
          self.indeed_ads(file_name, rel, salary)
        e = datetime.now()
        self.log('measurement', 'loadtime', str(e-s))
        rel += 1

