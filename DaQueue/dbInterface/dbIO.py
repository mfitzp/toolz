#! /usr/bin/python2.6

import httplib, simplejson  # http://cheeseshop.python.org/pypi/simplejson
                            # Here only used for prettyprinting
import couchdb as CDB

def prettyPrint(s):
    """Prettyprints the json response of an HTTPResponse object"""

    # HTTPResponse instance -> Python object -> str
    print simplejson.dumps(simplejson.loads(s.read()), sort_keys=True, indent=4)

class Couch:
    """Basic wrapper class for operations on a couchDB"""

    def __init__(self, host, port=5984, options=None):
        self.host = host
        self.port = port

    def connect(self):
        return httplib.HTTPConnection(self.host, self.port) # No close()

    # Database operations

    def createDb(self, dbName):
        """Creates a new database on the server"""

        r = self.put(''.join(['/',dbName,'/']), "")
        prettyPrint(r)

    def deleteDb(self, dbName):
        """Deletes the database on the server"""

        r = self.delete(''.join(['/',dbName,'/']))
        prettyPrint(r)

    def listDb(self):
        """List the databases on the server"""

        prettyPrint(self.get('/_all_dbs'))

    def infoDb(self, dbName):
        """Returns info about the couchDB"""
        r = self.get(''.join(['/', dbName, '/']))
        prettyPrint(r)

    # Document operations

    def listDoc(self, dbName):
        """List all documents in a given database"""

        r = self.get(''.join(['/', dbName, '/', '_all_docs']))
        prettyPrint(r)

    def openDoc(self, dbName, docId):
        """Open a document in a given database"""
        r = self.get(''.join(['/', dbName, '/', docId,]))
        prettyPrint(r)

    def saveDoc(self, dbName, body, docId=None):
        """Save/create a document to/in a given database"""
        if docId:
            r = self.put(''.join(['/', dbName, '/', docId]), body)
        else:
            r = self.post(''.join(['/', dbName, '/']), body)
        prettyPrint(r)

    def deleteDoc(self, dbName, docId):
        # XXX Crashed if resource is non-existent; not so for DELETE on db. Bug?
        # XXX Does not work any more, on has to specify an revid
        #     Either do html head to get the recten revid or provide it as parameter
        r = self.delete(''.join(['/', dbName, '/', docId]))
        prettyPrint(r)

    # Basic http methods

    def get(self, uri):
        c = self.connect()
        headers = {"Accept": "application/json"}
        c.request("GET", uri, None, headers)
        return c.getresponse()

    def post(self, uri, body):
        c = self.connect()
        headers = {"Content-type": "application/json"}
        c.request('POST', uri, body, headers)
        return c.getresponse()

    def put(self, uri, body):
        c = self.connect()
        if len(body) > 0:
            headers = {"Content-type": "application/json"}
            c.request("PUT", uri, body, headers)
        else:
            c.request("PUT", uri, body)
        return c.getresponse()

    def delete(self, uri):
        c = self.connect()
        c.request("DELETE", uri)
        return c.getresponse()

def test():
    foo = Couch('127.0.0.1', '5984')

    print "\nCreate database 'mydb':"
    foo.createDb('mydb')

    print "\nList databases on server:"
    foo.listDb()

    print "\nCreate a document 'mydoc' in database 'mydb':"
    doc = """
    {
        "value":
        {
            "Subject":"I like Planktion",
            "Author":"Rusty",
            "PostedDate":"2006-08-15T17:30:12-04:00",
            "Tags":["plankton", "baseball", "decisions"],
            "Body":"I decided today that I don't like baseball. I like plankton."
        }
    }
    """
    foo.saveDoc('mydb', doc, 'mydoc')

    print "\nCreate a document, using an assigned docId:"
    foo.saveDoc('mydb', doc)

    print "\nList all documents in database 'mydb'"
    foo.listDoc('mydb')

    print "\nRetrieve document 'mydoc' in database 'mydb':"
    foo.openDoc('mydb', 'mydoc')

    print "\nDelete document 'mydoc' in database 'mydb':"
    foo.deleteDoc('mydb', 'mydoc')

    print "\nList all documents in database 'mydb'"
    foo.listDoc('mydb')

    print "\nList info about database 'mydb':"
    foo.infoDb('mydb')

    print "\nDelete database 'mydb':"
    foo.deleteDb('mydb')

    print "\nList databases on server:"
    foo.listDb()

    foo.listDoc('dummyqueue')
    foo.infoDb('dummyqueue')
    print "Done"

    testKey = ['Data Path', 'Input File', 'Output Path', 'Task Status', 'Task Type', 'Job Queue']
    testItem = ['/home/clowers/Sandbox/text.xml','/home/clowers/input.xml', '/home/clowers', 'Processing', 'File Conversion', '23']
    docNames = xrange(5)
    testDict = {}
    for i, key in enumerate(testKey):
        testDict[key] = testItem[i]

#    print foo['dummyqueue']
#    print foo

#    for j in docNames:


#a = db['manifesto']
#>>> a['title']
#u'Personal Manifesto'
#>>> a['title'] = "Ehm. Lame title."
#>>> a
#<Document u'manifesto'@u'818144524' {u'txt': u'I strongly believe in something. I thi
#
#
#>>> db = s.create('docs')
#>>> len(db)
#0
#>>> db.create({'type':'Document','title':'Document One','txt':"This is some text."})
#u'fd179491f0d95268eb1761e0439cf3e2'
#>>> len(db)

class DB:
    def __init__(self, server, dbName, keys):
        self.server = server
        self.dbName = dbName
        self.keys = keys
        self.OK = False
        self.setup()

    def setup(self):
        try:
            self.db = self.server.server[self.dbName]
            self.OK = True
        except:
            self.db = None
            self.OK = False

    def updateDoc(self, docID, docKey, docVal):
        '''
        This is not working the way I want....
        '''
        doc = self.db.get(docID)
        doc[docKey] = docVal

    def addDocument(self, docDict):
        if self.OK:
            try:
                docId = self.db.create(docDict)
                return True, docId
            except:
                return False, ''

    def delDocument(self, jobID):
        if self.OK:
            try:
                self.db.__delitem__(jobID)
            except:
                print "Error deleting item. Double check deletion"


class CouchDBServer:
    def __init__(self, host, port=5984, options=None):
        self.host = host
        self.port = port
        self.timeout = 5
        self.server = None
        self.dbList = []
        self.OK = False
        self.version = None
        self.setup()

    def setup(self):
        serverAddress = 'http://%s:%s/'%(self.host,str(self.port))
        print "Server Address", serverAddress
        self.server = CDB.Server(serverAddress, timeout = self.timeout)
        self.getStatus()
#        self.getCurrentDB()

    def getStatus(self):
        '''
        Simple test to see if couchdb is connected
        '''
        try:
            self.version = self.server.version
            self.OK = True
        except:
            self.version = None
            self.OK = False
        return self.OK

    def getCurrentDB(self):
        if self.OK:
            for db in self.server:
#                print db, type(db)
                self.dbList.append(db)



if __name__ == "__main__":
#    test()
    import couchdb as CDB
    from time import strftime, localtime
    s = CDB.Server('http://127.0.0.1:5984/')


    dbName = 'labqueue'
    dbKeys = ['Task Type', 'Method File', 'Data Path', 'Output Path', 'State', 'User', 'Submit Time']
    testItem = ['File Conversion', '/home/clowers/Sandbox/text.xml','/home/clowers/input.xml', '/home/clowers', 'Queued', 'clowers']
    docNames = xrange(5)
#    testDict = {'type':'Document','title':'testDoc'}
    testDict = {}
    for i, key in enumerate(dbKeys):

        if key == "Submit Time":
            testDict[key] = strftime("%a, %d %b %Y %H:%M:%S", localtime())
        else:
            testDict[key] = testItem[i]

    try:
        db = s[dbName]
    except:
        try:
            s.delete(dbName)
        except:
            pass
        db = s.create(dbName)
#    print len(db)
#    for docId in db:
#        print docId
#    print db[docId], type(db[docId])
    for j in xrange(5):
        print db.create(testDict)

#    s.delete()



