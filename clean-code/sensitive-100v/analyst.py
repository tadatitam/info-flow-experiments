import os

SITE_FILES = [	"mental.disorder.txt",
				"adult.txt",
				"disabled.txt",
				"lgb.txt",
				"substance.txt",
				"infertility.txt"
				]
ALEXA_SITES = [	"http://www.alexa.com/topsites/category/Top/Health/Mental_Health/Disorders",
				"http://www.alexa.com/topsites/category/Top/Adult",
				"http://www.alexa.com/topsites/category/Top/Society/Disabled",
				"http://www.alexa.com/topsites/category/Top/Society/Gay,_Lesbian,_and_Bisexual",
				"http://www.alexa.com/topsites/category/Top/Health/Addictions/Substance_Abuse",
				"http://www.alexa.com/topsites/category/Top/Health/Reproductive_Health/Infertility"
				]
# INT_SITE_FILE = "int_"+SITE_FILE
SHORT_COLLECT_PY = "collector/short/collect.py"
# LOG_FILE = "log.txt"
RUN_COLLECT_PY = "collector/collect/collect.py"



fo = open(LOG_FILE, "w")
fo.close()

if(len(SITE_FILES) != len(ALEXA_SITES)):
	raw_input("sites and files not matching!")

for i in range(0, len(SITE_FILES)):
# 	os.system("python collector/short/alexa.py %s %s" % (SITE_FILES[i], ALEXA_SITES[i]))
# 	os.system("python collector/short/shortlist.py %s %s %s " % (SITE_FILES[i], "int_"+SITE_FILES[i], SHORT_COLLECT_PY))
	os.system("python collector/collect/run.py %s %s %s" % ("log."+SITE_FILE[i], SITE_FILE[i], RUN_COLLECT_PY))
	os.system("python tester/pilot.py %s > outb" % (LOG_FILE))
	os.system("python tester/test.py %s > outc" % (LOG_FILE))
