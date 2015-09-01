import unittest, time                               # unittest starts of the testing environment for browsers, time.sleep
import os, platform, sys                                 # for running  os, platform specific function calls

def collect_sites(make_browser, output_file="out.txt", num_sites=5, 
                 alexa_link="http://www.alexa.com/topsites"):
    PATH="./"+output_file
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        response = raw_input("This will overwrite file %s... Continue? (Y/n)" % output_file)
        if response == 'n':
            sys.exit(0)
    fo = open(output_file, "w")
    fo.close()
    print "Beginning Collection"
    
    class Test(unittest.TestCase):
        def setUp(self):
            self.unit = make_browser(-1, -1)
        def runTest(self):
            self.unit.collect_sites_from_alexa(alexa_link, output_file, num_sites)
        def tearDown(self):
            self.unit.quit()
    test = Test()
    suite = unittest.TestSuite()
    suite.addTest(test)
    unittest.TextTestRunner(verbosity=1).run(suite)
        
    print "Collection Complete. Results stored in ", output_file
