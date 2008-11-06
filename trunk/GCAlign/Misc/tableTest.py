import tables as T
import numpy as N
import time


t1 = time.clock()
hdf = T.openFile('TableTest.h5', mode = "w")
group = hdf.createGroup("/", 'TestGroup', 'Table information')
rows = 300
columns = 5
arr = N.random.random(rows)*100
#ra = N.array([(3.14159,'some string',[1,2,3,4,5],N.arange(0,10,0.1))], dtype = "f8,S20,(5,)i4,(100,)f8")
#print ra


ra = N.rec.fromarrays(arr)
#ra = N.array(arr,  dtype = 'i4')
print ra
print type(ra)

#arr = N.array(arr, dtype = N.int32)
filters = T.Filters(complevel=5, complib='zlib')

t = hdf.createTable(group, 'test', arr)
t.flush()
#for i in xrange(columns):
#    arr = N.random.random(rows)*100
#    t.append(arr)
#    t.flush()
#    if i%10000 == 0:
#        print i

##rowTime = time.clock()
##print t[1]
##print 'Row Time', time.clock()-rowTime
##colTime = time.clock()
##print t[:, 1]
##print 'Col Time',  time.clock()-colTime

hdf.close()
print "Done"
t2 = time.clock()
print t2-t1
