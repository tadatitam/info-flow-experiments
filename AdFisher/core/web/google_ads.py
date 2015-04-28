import time, re                                                     # time.sleep, re.split
import sys                                                          # some prints
from selenium import webdriver                                      # for running the driver on websites
from datetime import datetime                                       # for tagging log with datetime
from selenium.webdriver.common.keys import Keys                     # to press keys on a webpage
from selenium.webdriver.common.action_chains import ActionChains    # to move mouse over
# import browser_unit
import google_search

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
CROSS_TD = "Zt"
PREF_OK_DIV = "c-T-S a-b a-b-A GJ IC"

SIGNIN_A = "gb_70"

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

class GoogleAdsUnit(google_search.GoogleSearchUnit):

    def __init__(self, browser, log_file, unit_id, treatment_id, headless=False, proxy=None):
        google_search.GoogleSearchUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
#         browser_unit.BrowserUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)
        
    def opt_in(self):
        """Opt in to behavioral advertising on Google"""
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("https://www.google.com/settings/ads")
            self.driver.find_element_by_xpath(".//div[@class ='"+OPTIN_DIV+"']").click()
    #       if(self.unit_id != -1):
            self.log('treatment', 'optin', 'True')
        except:
            self.log('error', 'opting in', 'True')
        
    def opt_out(self):
        """Opt out of behavioral advertising on Google"""
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("https://www.google.com/settings/ads")
            self.driver.find_element_by_xpath(".//div[@class ='"+OPTOUT_DIV+"']").click()
            time.sleep(2)
            self.driver.execute_script("document.getElementsByName('ok')[1].click();")  
    #       if(self.unit_id != -1):
            self.log('treatment', 'optout', 'True')
        except:
            self.log('error', 'opting out', 'True')
    
    def login(self, username, password):
        """Login to Google with username and password"""
        try:
            self.driver.set_page_load_timeout(60)
            self.driver.get("https://www.google.com")
            self.driver.find_element_by_xpath(".//a[@id='"+SIGNIN_A+"']").click()
            self.driver.find_element_by_id("Email").send_keys(username)
            self.driver.find_element_by_id("Passwd").send_keys(password)
            self.driver.find_element_by_id("signIn").click()
            self.log('treatment', 'login', username)
        except:
            self.log('error', 'logging in', username)
    
    def set_gender(self, gender):
        """Set gender on Google Ad Settings page"""
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            gdiv = self.driver.find_element_by_xpath(".//div[@class='"+GENDER_DIV+"']")
            gdiv.find_element_by_xpath(".//div[@class='"+EDIT_DIV+"']").click()
            if(gender == 'm'):
                box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='1']/span")        # MALE          
            elif(gender == 'f'):
                box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='2']/span")            # FEMALE
            box.click()
            gdiv.find_element_by_xpath(".//div[@class='"+SUBMIT_DIV+"']").click()
#           self.log("setGender="+gender+"||"+str(self.treatment_id))
            self.log('treatment', 'gender', gender)
        except:
            print "Could not set gender. Did you opt in?"
            self.log('error', 'setting gender', gender)
        
    def set_age(self, age):
        """Set age on Google Ad Settings page"""
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            gdiv = self.driver.find_element_by_xpath(".//div[@class='"+AGE_DIV+"']")
            gdiv.find_element_by_xpath(".//div[@class='"+EDIT_DIV+"']").click()
            time.sleep(3)
            if(age>=18 and age<=24):
                box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='1']/span")
            elif(age>=25 and age<=34):  
                box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='2']/span")
            elif(age>=35 and age<=44):  
                box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='3']/span")
            elif(age>=45 and age<=54):  
                box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='4']/span")
            elif(age>=55 and age<=64):
                box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='5']/span")
            elif(age>=65):
                box = gdiv.find_element_by_xpath(".//div[@class='"+RADIO_DIV+"'][@data-value='6']/span")
            box.click()
            gdiv.find_element_by_xpath(".//div[@class='"+SUBMIT_DIV+"']").click()
            self.log('treatment', 'age', age)
#           self.log("setAge="+str(age)+"||"+str(treatment_id))
        except:
            print "Could not set age. Did you opt in?"
            self.log('error', 'setting age', age)

    def set_language(self, language):   
        """Set language on Google Ad Settings page"""
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            gdiv = self.driver.find_element_by_xpath(".//div[@class='"+LANGUAGES_DIV+"']")
            gdiv.find_element_by_xpath(".//div[@class='"+EDIT_DIV+"']").click()
            gdiv.find_element_by_xpath(".//div[@class='"+LANG_DROPDOWN+"']").click()
            time.sleep(3)
            gdiv.find_element_by_xpath(".//div[@class='"+LANG_DIV+"'][contains(.,'"+language+"')]").click()
            gdiv.find_element_by_xpath(".//div[@class='"+SUBMIT_DIV+"']").click()
#           log("setLanguage="+str(language)+"||"+str(self.treatment_id), id, LOG_FILE)
            self.log('treatment', 'language', language)
        except:
            print "Could not set language"
            self.log('error', 'setting language', language)

    def remove_interest(self, pref):
        """Remove interests containing pref on the Google Ad Settings page"""
        try:
            prefs = self.get_interests(text="interests prior to removal")
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            self.driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
            rem = []
            while(1):
                trs = self.driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
                flag=0
                for tr in trs:
                    td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']")
                    div = tr.find_element_by_xpath(".//td[@class='"+CROSS_TD+"']/div")
                    int = td.get_attribute('innerHTML')
                    if pref.lower() in div.get_attribute('aria-label').lower():
                        flag=1
                        hover = ActionChains(self.driver).move_to_element(td)
                        hover.perform()
                        time.sleep(1)
                        td.click()
                        div.click()
                        rem.append(int)
                        time.sleep(2)
                        break
                if(flag == 0):
                    break
            self.driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
            self.log('treatment', 'remove interest ('+pref+')', "@|".join(rem))
        except:
            print "No interests matched '%s'. Skipping." %(pref)
            self.log('error', 'removing interest', pref)

    def add_interest(self, pref):                                   # check the logging
        """Set an ad pref"""
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            self.driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
    
            self.driver.find_element_by_xpath(".//input[@class='"+PREF_INPUT+"']").send_keys(pref)
            self.driver.find_element_by_xpath(".//div[@class='"+PREF_INPUT_FIRST+"']").click()
            time.sleep(1)
            trs = self.driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']")
            for tr in trs:
                td = tr.find_element_by_xpath(".//td[@class='"+PREF_TD+"']").get_attribute('innerHTML')
    #               print td
                self.log('treatment', 'add interest ('+pref+')', td)
            time.sleep(2)
            self.driver.find_element_by_xpath(".//div[@class='"+PREF_OK_DIV+"']").click()
            time.sleep(5)
        except:
            print "Error setting interests containing '%s'. Maybe no interests match this keyword." %(pref)
            self.log('error', 'adding interest', pref)


    def get_gender(self):
        """Read gender from Google Ad Settings"""
        inn = "Error reading"
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            gdiv = self.driver.find_element_by_xpath(".//div[@class='"+GENDER_DIV+"']")
            inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
            self.log('measurement', 'gender', inn)
        except:
            print "Could not get gender. Did you opt in?"
            self.log('error', 'getting gender', inn)
        return inn
    
    def get_age(self):
        """Read age from Google Ad Settings"""
        inn = "Error reading"
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            gdiv = self.driver.find_element_by_xpath(".//div[@class='"+AGE_DIV+"']")
            inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
            self.log('measurement', 'age', inn)
        except:
            print "Could not get age. Did you opt in?"
            self.log('error', 'getting age', inn)
        return inn
    
    def get_language(self): 
        """Read language from Google Ad Settings"""
        inn = "Error reading"
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            gdiv = self.driver.find_element_by_xpath(".//div[@class='"+LANGUAGES_DIV+"']")
            inn = gdiv.find_element_by_xpath(".//span[@class='"+ATTR_SPAN+"']").get_attribute('innerHTML')
            self.log('measurement', 'language', inn)
        except:
            print "Could not get language. Did you opt in?"
            self.log('error', 'getting language', inn)
#       self.log("language"+"||"+str(self.treatment_id)+"||"+inn)
        return inn
        
    def get_interests(self, text="interests"):                                  
        """Returns list of Ad preferences"""
        pref = []
        try:
            self.driver.set_page_load_timeout(40)
            self.driver.get("https://www.google.com/settings/ads")
            self.driver.find_elements_by_xpath(".//div[@class='"+EDIT_DIV+"']")[3].click()
            ints = self.driver.find_elements_by_xpath(".//tr[@class='"+PREF_TR+"']/td[@class='"+PREF_TD+"']")
            for interest in ints:
                pref.append(str(interest.get_attribute('innerHTML')))
            self.log('measurement', text, "@|".join(pref))
        except:
            print "Error collecting ad preferences. Skipping." %(pref)
            self.log('error', 'getting '+text, "@|".join(pref))
#       self.log("pref"+"||"+str(self.treatment_id)+"||"+"@|".join(pref))
        return pref 

    def collect_ads(self, reloads, delay, site, file_name=None):
        if file_name == None:
            file_name = self.log_file
        rel = 0
        while (rel < reloads):  # number of reloads on sites to capture all ads
            time.sleep(delay)
#           try:
            for i in range(0,1):
                s = datetime.now()
                if(site == 'toi'):
                    save_ads_toi(file_name)
                elif(site == 'bbc'):
                    self.save_ads_bbc(file_name)
                elif(site == 'guardian'):
                    save_ads_guardian(file_name)
                elif(site == 'reuters'):
                    save_ads_reuters(file_name)
                elif(site == 'bloomberg'):
                    save_ads_bloomberg(file_name)
                else:
                    raw_input("No such site found: %s!" % site)
                e = datetime.now()
                self.log('measurement', 'loadtime', str(e-s))
#           except:
#               self.log('error', 'collecting ads', 'Error')
            rel = rel + 1

    def save_ads_fox(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://www.foxnews.com/us/index.html")
        tim = str(datetime.now())
        frame1 = driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
        driver.switch_to_frame(frame1)
        frame2 = driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
        driver.switch_to_frame(frame2)
        lis = driver.find_elements_by_css_selector("div#ads ul li")
        print len(lis)
        for li in lis:
            t = li.find_element_by_css_selector("td.rh000c div a span").get_attribute('innerHTML')
            l = li.find_element_by_css_selector("td.rh010c div div a span").get_attribute('innerHTML')
            b = li.find_element_by_css_selector("td.rh0111c div span").get_attribute('innerHTML')
    #       f = (str(id)+"||"+time+"||"+t+"||"+l+"||"+b).encode("utf8")
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)
        driver.switch_to_default_content()
        driver.switch_to_default_content()
        
    def save_ads_bloomberg(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://www.bloomberg.com/") 
        tim = str(datetime.now())
        frame0 = driver.find_element_by_xpath(".//iframe[@src='/bcom/home/iframe/google-adwords']")
        driver.switch_to.frame(frame0)
        frame1 = driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
        driver.switch_to.frame(frame1)
        time.sleep(2)
        frame2 = driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
        driver.switch_to.frame(frame2)
        lis = driver.find_elements_by_css_selector("div#adunit div#ads ul li")
        for li in lis:
            t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
            l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
            b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)
        driver.switch_to.default_content()
        driver.switch_to.default_content()
        driver.switch_to.default_content()

    def save_ads_reuters(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://www.reuters.com/news/us")    
        tim = str(datetime.now())
        frame0 = driver.find_element_by_xpath(".//iframe[@id='pmad-rt-frame']")
        driver.switch_to.frame(frame0)
        frame1 = driver.find_element_by_xpath(".//iframe[@id='aswift_0']")
        driver.switch_to.frame(frame1)
        time.sleep(2)
        frame2 = driver.find_element_by_xpath(".//iframe[@id='google_ads_frame1']")
        driver.switch_to.frame(frame2)
        lis = driver.find_elements_by_css_selector("div#adunit div#ads ul li")
        for li in lis:
            t = li.find_element_by_css_selector("td.rh-titlec div a span").get_attribute('innerHTML')
            l = li.find_element_by_css_selector("td.rh-urlc div div a span").get_attribute('innerHTML')
            b = li.find_element_by_css_selector("td.rh-bodyc div span").get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)
        driver.switch_to.default_content()
        driver.switch_to.default_content()
        driver.switch_to.default_content()

    def save_ads_guardian(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://www.theguardian.com/us") 
        time = str(datetime.now())
        els = driver.find_elements_by_css_selector("div#google-ads-container div.bd ul li")
        for el in els:
            t = el.find_element_by_css_selector("p.t6 a").get_attribute('innerHTML')
            ps = el.find_elements_by_css_selector("p")
            b = ps[1].get_attribute('innerHTML')
            l = ps[2].find_element_by_css_selector("a").get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)

    def save_ads_toi(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://timesofindia.indiatimes.com/international-home")
        time.sleep(10)
        tim = str(datetime.now())
        frame = driver.find_element_by_xpath(".//iframe[@id='ad-left-timeswidget']")
    
        def scroll_element_into_view(driver, element):
            """Scroll element into view"""
            y = element.location['y']
            driver.execute_script('window.scrollTo(0, {0})'.format(y))
    
        scroll_element_into_view(driver, frame)
        print frame
        driver.switch_to.frame(frame)
        ads = driver.find_elements_by_css_selector("html body table tbody tr td table")
        for ad in ads:
            aa = ad.find_elements_by_xpath(".//tbody/tr/td/a")
            bb = ad.find_elements_by_xpath(".//tbody/tr/td/span")
            t = aa[0].get_attribute('innerHTML')
            l = aa[1].get_attribute('innerHTML')
            b = bb[0].get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)
        driver.switch_to.default_content()  

    def save_ads_bbc(self, file):
        driver = self.driver
        id = self.unit_id
        sys.stdout.write(".")
        sys.stdout.flush()
        driver.set_page_load_timeout(60)
        driver.get("http://www.bbc.com/news/")
        tim = str(datetime.now())
        els = driver.find_elements_by_css_selector("div.bbccom_adsense_container ul li")
        for el in els:
            t = el.find_element_by_css_selector("h4 a").get_attribute('innerHTML')
            ps = el.find_elements_by_css_selector("p")
            b = ps[0].get_attribute('innerHTML')
            l = ps[1].find_element_by_css_selector("a").get_attribute('innerHTML')
            ad = strip_tags(tim+"@|"+t+"@|"+l+"@|"+b).encode("utf8")
            self.log('measurement', 'ad', ad)
