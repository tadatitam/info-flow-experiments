import os

SITE_FILE = "mentaldisorder.txt"
ALEXA_SITE = "http://www.alexa.com/topsites/category/Top/Health/Mental_Health/Disorders"
INT_SITE_FILE = "int_mentaldisorder.txt"
SHORT_COLLECT_PY = "collector/short/collect.py"
AD_FILE = "ads.txt"
RUN_COLLECT_PY = "collector/collect/collect.py"

#os.system("python collector/short/alexa.py %s %s" % (SITE_FILE, ALEXA_SITE))
#os.system("python collector/short/shortlist.py %s %s %s " % (SITE_FILE, INT_SITE_FILE, SHORT_COLLECT_PY))
os.system("python collector/collect/run.py %s %s %s > outa" % (AD_FILE, SITE_FILE, RUN_COLLECT_PY))
os.system("python tester/pilot.py %s > outb" % (AD_FILE))
os.system("python tester/test.py %s > outc" % (AD_FILE))
