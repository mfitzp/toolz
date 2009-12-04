#! /usr/bin/python


if __name__ == "__main__":
    import couchdb as C
    s = C.Server('http://127.0.0.1:5984/')



    testKey = ['Data Path', 'Input File', 'Output Path', 'Task Status', 'Task Type', 'Job Queue']
    testItem = ['/home/clowers/Sandbox/text.xml','/home/clowers/input.xml', '/home/clowers', 'Processing', 'File Conversion', '23']
    docNames = xrange(5)
    testDict = {'type':'Document','title':'testDoc'}
    for i, key in enumerate(testKey):
        testDict[key] = testItem[i]

    try:
        db = s['dummyqueue']
    except:
        db = s.create('dummyqueue')
#    print len(db)
#    for docId in db:
#        print docId
    for j in xrange(5):
        db.create(testDict)