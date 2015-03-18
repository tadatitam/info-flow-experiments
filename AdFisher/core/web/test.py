import time, re														# time.sleep, re.split
import sys															# some prints
from selenium import webdriver										# for running the driver on websites
from datetime import datetime										# for tagging log with datetime
from selenium.webdriver.common.keys import Keys						# to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains	# to move mouse over

# Google ad settings page class declarations

GENDER_DIV = "EA yP"
AGE_DIV = "EA mP"
LANGUAGES_DIV = "EA EP"
INTERESTS_DIV = "EA rQ"

OPTIN_DIV = "hl Dh uP"
OPTOUT_DIV = "hl LC Dh"
EDIT_DIV = "hl Dh c-Ha-qd c-Ha-Md"
RADIO_DIV = "a-u FA mQ"
SUBMIT_DIV = "c-T-S a-b a-b-A js"
ATTR_SPAN = "mk"

LANG_DROPDOWN = "c-T-S c-g-f-b a-oa Cr"
LANG_DIV = "c-l"

PREF_INPUT = "tQ a-la CK"
PREF_INPUT_FIRST = "zK wK va"
PREF_TR = "BK yr pQ"
PREF_TD = "Yt qQ"
PREF_OK_DIV = "c-T-S a-b a-b-A GJ IC"

SIGNIN_A = "gb_70"


class BrowserUnit:

    def opt_in(self, treatment_id=-1):
        """Opt in to behavioral advertising on Google"""
	self.driver.set_page_load_timeout(60)
	self.driver.get("https://www.google.com/settings/ads")
	self.driver.find_element_by_xpath(".//div[@class ='"+OPTIN_DIV+"']").click()
	if(self.unit_id != -1):
		self.log("optedIn||"+str(treatment_id))
