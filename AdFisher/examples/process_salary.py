
import sys
import numpy

t1 = {}
t2 = {}
l1 = []
l2 = []
for line in sys.stdin:
    try:
        toks = line.split('||')
        exp = int(toks[-1])
        info = toks[3]
        sals = info.split('@|')[1]
        sals = sals.split(' ')
        for sal in sals:
            if int(sal) > 10000:
                if exp:
                    if sal in t1:
                        t1[sal] += 1
                    else:
                        t1[sal] = 1
                    l1.append(sal)
                else:
                    if sal in t2:
                        t2[sal] += 1
                    else:
                        t2[sal] = 1
                    l2.append(sal)
    except:
        pass

print ""
print "Controlled Summary (0): "
print t1
print "Mean: " + str(numpy.mean(numpy.array(l1).astype(numpy.float)))
print "Standard Dev: " + str(numpy.std(numpy.array(l1).astype(numpy.float)))
print ""
print "Experimental Summary (1): "
print t2
print "Mean: " + str(numpy.mean(numpy.array(l2).astype(numpy.float)))
print "Standard Dev: " + str(numpy.std(numpy.array(l2).astype(numpy.float)))
print ""
