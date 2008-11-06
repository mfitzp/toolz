import tables as T
import numpy  as N
import time

try:
    import psyco
    psyco.full()
except:
    print "Pysco not installed, try easy_install psyco at your command prompt"
  
t1 = time.clock()
hdf = T.openFile('test.h5', mode = "w", title = '')


atom = T.Int32Atom()
rows = 400
columns = 50000
arr = N.random.random(rows)*100
shape = (rows, columns)#(rows, columns)
filters = T.Filters(complevel=5, complib='zlib')

ea = hdf.createEArray(hdf.root, "EArrayRows", atom, (0, rows),  filters = filters,  expectedrows = columns)
ea2 = hdf.createEArray(hdf.root, "EArrayColumns", atom, (rows, 0),  filters = filters,  expectedrows = rows)

for i in xrange(columns):
    arr = N.random.random(rows)*100
    ea.append(arr[N.newaxis,:])
    ea2.append(arr[:, N.newaxis])
    ea.flush()
    ea2.flush()
    if i%10000 == 0:
        print i

rowTime = time.clock()
print ea[1]
print 'Row Time', time.clock()-rowTime
colTime = time.clock()
print ea[:, 1]
print 'Col Time',  time.clock()-colTime

hdf.close()
print "Done"
t2 = time.clock()
print t2-t1

