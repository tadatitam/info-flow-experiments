from subprocess import Popen
import glob, sys

if __name__ == "__main__":
	SITE_FILE = sys.argv[1]
	TARGET_FILE = sys.argv[2]
	COLLECT_PY = sys.argv[3]
	test = glob.glob(COLLECT_PY)[0]
	processes = []
	BROWSER = 'ff'			
	fo = open(TARGET_FILE, "w")
	fo.close()

	fo = open(SITE_FILE, 'r')
	for line in fo:
		site = line.strip()		
		print 'python %s %s %s %s' % (test, BROWSER, site, TARGET_FILE)
		processes.append(Popen('python %s %s %s %s' % (test, BROWSER, site, TARGET_FILE), shell=True))

		for process in processes:
			process.wait()
