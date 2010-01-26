import types
import threading
import win32file
import win32con
import os

class WatchDirectory(object):
   """
   This method was adapted from example by Tim Golden:
   http://tgolden.sc.sabren.com/python/win32_how_do_i/watch_directory_for_changes.html

   Watches for changes to any file/dir inside specified directory.
   Instantiating this class spawns the watcher function in a separate thread.
   self.changeList accumulates changes until client requests list using the check() method.
   Calling that method returns the changeList then empties it.

   The watching thread will self-terminate when the WatchDirectory instance is destroyed
   or falls out-of-scope.

   Usage Examples:
      watcher = WatchDirectory(r'D:\myStuff')
      # Typically you'd have a main loop here somewhere, inside of which you'd make occasional
      # calls to watcher.check, like so:
      while (not doneWithLoop):
         changes = watcher.check()
         for c in changes:
            # do something to each modified file, etc...
            print "file: %s, change: %s" % c

   See self.ACTIONS below for a list of possible change strings.

   Also, the "onlyExtensions" keyword arg can be used to only watch certain filetypes:
      watcher = WatchDirectory(r'D:\myStuff', onlyExtensions=('.jpg', '.xml') 

   NOTES:
   ChangeList returned is chronological, oldest to newest.  A file that's modified early in the list
   could show up as deleted later.  Your client code is responsible for verifying files still
   exist, etc.

   The win32 method used here seems very reliable.  I did notice that it fails to report
   deleted files if they were inside a subdir that was deleted in its entirety, however.
   Seems like a border case, however, so I'm inclined to leave it as-is for now.
   Also, deleted subdirs still sometimes show up as a change with watchSubdirs=False.

   TODO:
   - Maybe add option to not multithread, making it a blocking call.
 
   Adam Pletcher
   adam@volition-inc.com
   Volition, Inc./THQ
   """
   def __init__(self, dirToWatch, bufferSize=1024, watchSubdirs=True, onlyExtensions=None):
      self.dirToWatch = dirToWatch
      self.changeList = []
      self.bufferSize = bufferSize
      self.watchSubdirs = watchSubdirs
      if (type(onlyExtensions) == types.StringType):
         onlyExtensions = onlyExtensions.split(',')
      self.onlyExtensions = onlyExtensions
      # Constants for making win32file stuff readable
      self.ACTIONS = {
         1 : "Created",
         2 : "Deleted",
         3 : "Modified",
         4 : 'Renamed to something',
         5 : 'Renamed from "%s"'
      }
      # Start watching in a separate thread
      self.thread = threading.Thread(target=self._checkInThread).start()

   def _checkInThread(self):
      """
      Watch for changes in specified directory.  Designed to be run in a
      separate thread, since ReadDirectoryChangesW is a blocking call.
      Don't call this directly.
      """
      while (1):
         FILE_LIST_DIRECTORY = 0x0001
         hDir = win32file.CreateFile (
            self.dirToWatch,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
         )
         # The following is a blocking call.  Which is why we run this in its own thread.
         newChanges = win32file.ReadDirectoryChangesW (
            hDir,                # Previous handle to directory
            self.bufferSize,     # Buffer to hold results
            self.watchSubdirs,   # Watch subdirs?
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |   # What to watch for
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
         )
         # Changes found, process them
         finalChanges = []
         oldFilename = None
         for change in newChanges:
            if (change[0] == 4):   # renamed to something
               oldFilename = os.path.split(change[1])[1]
               pass
            else:
               file = os.path.join(self.dirToWatch, change[1])
               skip = False
               # Verify a few things first
               if (not self.watchSubdirs) and (os.path.isdir(file)):
                  skip = True
               elif (self.onlyExtensions) and (not os.path.splitext(file)[1] in self.onlyExtensions):
                  skip = True
               if (not skip):  # passed checks, so use it
                  action = self.ACTIONS.get (change[0], "Unknown")
                  if (change[0] == 5): # renamed from something
                     # Insert old filename, prior to being renamed
                     action = action % (oldFilename)
                     oldFilename = None
                  # Add change tuple to list
                  finalChanges.append((file, action, change[0]))
         # Add processed changes to running list
         self.changeList += finalChanges

   def check(self):
      """
      Fetches list of changes our watcher thread has accumulated.
      """
      changes = self.changeList
      self.changeList = []  # clear changeList
      return changes
 
### MAIN ###
if (__name__ == '__main__'):
	import time
	import sys
	watchDir = r'C:\ChemBio\Data'
	print "Watching: %s"%watchDir
	watcher = WatchDirectory(watchDir)
	try:
		while (True):
			changes = watcher.check()
			for c in changes:
				print "file: %s, change: %s, type: %d" % c
			
			time.sleep(5)  # wait 5 seconds before checking again
	except KeyboardInterrupt:
		sys.exit()
        