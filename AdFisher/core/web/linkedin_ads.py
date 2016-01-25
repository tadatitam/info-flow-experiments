import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
import browser_unit
from selenium.common.exceptions import NoSuchElementException
import random

MALE_EMAIL = 'benkevinjohns@gmail.com'
MALE_PASSWORD = '65382$wtcv'

FEMALE_EMAIL = 'amjoyjohns@gmail.com'
FEMALE_PASSWORD = '874g*59&T'


SEPARATOR='@|'

MAX_COLLECTED = 5




# get login ids
def clean(s):
    toks = s.strip().split(' ')
    return toks

with open('site_files/linkedin_login_credentials_female.txt') as f:
    FEMALE_CREDENTIALS = map(clean, f.readlines())
    print FEMALE_CREDENTIALS

with open('site_files/linkedin_login_credentials_male.txt') as f:
    MALE_CREDENTIALS = map(clean, f.readlines())










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










class LinkedInAdsUnit(browser_unit.BrowserUnit):

  def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
    browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)

  def get_random_entry(self, array):
    index = random.randrange(1,len(array)-1)
    return array[index]

  def get_login_credentials(self, gender):
    '''returns (username, password)'''
    if (gender=='male'): #male
      return self.get_random_entry(MALE_CREDENTIALS)
    else: # female 
      return self.get_random_entry(FEMALE_CREDENTIALS)

      
  def create_user(self, gender, occupation):
    """user's gender is either male or female"""
    [user_email, user_password] = self.get_login_credentials(gender)

    #user_email = MALE_EMAIL if (gender=='male') else FEMALE_EMAIL
    #user_password = MALE_PASSWORD if (gender=='male') else FEMALE_PASSWORD

    self.driver.get("https://www.linkedin.com/")

    login_email = self.driver.find_element_by_id("login-email")
    login_email.send_keys(user_email)

    login_password = self.driver.find_element_by_id("login-password")
    login_password.send_keys(user_password)

    signin = self.driver.find_element_by_css_selector("input[name='submit']")
    signin.click()

    self.occupation = occupation

  def collect_ads(self, reloads, delay, file_name=None):
    if file_name == None:
      file_name = self.log_file
    rel = 0
    while (rel < reloads):  # number of reloads on sites to capture all ads
      time.sleep(delay)
      s = datetime.now()
      self.save_ads_linkedin(file_name)
      e = datetime.now()
      self.log('measurement', 'loadtime', str(e-s))
      rel = rel + 1
    
  def search_term(self):
    self.driver.get('https://www.linkedin.com/nhome')

    try:
      search_box = self.driver.find_element_by_id("main-search-box")
      search_box.send_keys(self.occupation)

      search_box_button = self.driver.find_element_by_css_selector(".search-button")
      search_box_button.click()
    except NoSuchElementException:
      pass

  def save_ads_linkedin(self, file_name=None):
    id = self.unit_id
    sys.stdout.write(".")
    sys.stdout.flush()
    self.driver.set_page_load_timeout(60)

    self.search_term()
    time = str(datetime.now())
    lis = self.driver.find_elements_by_css_selector('div#results-container ol.search-results li.mod.result.job')

    for li in lis:
      try:
        company_title = li.find_element_by_css_selector('div.description bdi a').get_attribute('innerHTML')
        location = li.find_element_by_css_selector('dl.demographic dd.separator bdi').get_attribute('innerHTML')
        ad = strip_tags(time+SEPARATOR+company_title+SEPARATOR+'URL'+SEPARATOR+location).encode("utf8")
        self.log('measurement', 'ad', ad)
      except NoSuchElementException:
        pass

  









