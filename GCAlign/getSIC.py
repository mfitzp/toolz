import tables as T
f=T.openfile('C:/...h5', 'r')
mz = f.root.mzCube

def getmz(mzVal):
    sic = []
    t1 = time.clock()
    for row in mz.iterrows():
        sic.append(row[mzVal])
    t2 = time.clock()
    print t2-t1
    return sic