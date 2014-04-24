import os

SITE_FILE = "shopping.vehicles.autos.txt"
ALEXA_SITE = "http://www.alexa.com/topsites/category/Top/Health/Mental_Health/Disorders"
INT_SITE_FILE = "int_"+SITE_FILE
SHORT_COLLECT_PY = "collector/short/collect.py"
LOG_FILE = "log.txt"
RUN_COLLECT_PY = "collector/collect/collect.py"


fo = open(LOG_FILE, "w")
fo.close()

#os.system("python collector/short/alexa.py %s %s" % (SITE_FILE, ALEXA_SITE))
# os.system("python collector/short/shortlist.py %s %s %s " % (SITE_FILE, INT_SITE_FILE, SHORT_COLLECT_PY))
os.system("python collector/collect/run.py %s %s %s" % (LOG_FILE, SITE_FILE, RUN_COLLECT_PY))
# os.system("python tester/pilot.py %s > outb" % (LOG_FILE))
# os.system("python tester/test.py %s > outc" % (LOG_FILE))
