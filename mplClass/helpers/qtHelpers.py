import os
import re
import sys
import traceback
from subprocess import Popen, PIPE, STDOUT
from PyQt4 import QtCore
from PyQt4 import QtGui

import os, webbrowser

from PyQt4.QtGui import (QAction, QStyle, QWidget, QIcon, QApplication, QLabel,
                         QVBoxLayout, QHBoxLayout, QLineEdit, QKeyEvent, QMenu,
                         QKeySequence, QToolButton, QClipboard, QFileDialog, 
                         QListWidgetItem, QMessageBox)
from PyQt4.QtCore import (SIGNAL, QVariant, QObject, Qt, QLocale, QTranslator,
                          QLibraryInfo)

LOGGER = None


def batchRun(fileList, commandPath, options = None, logOutput = False, logName = None):
    '''
    Accepts a valid commandPath which is the program to run
    The options argument is the text (string) parameters used for the command line argument
    *****DUE NOT FORGET THE SPACES FOR THE OPTIONS ARGUMENT******
    logName is the filename for the log file
    '''
    
    if os.path.isfile(commandPath):
        if logName is None:
            logFileName = 'logFile.txt'
        else:
            logFileName = logName
            
        coreDir = os.path.dirname(fileList[0])
        logFileName = os.path.join(coreDir, logFileName)
        
        for i,f in enumerate(fileList):
            if i == 0:
                logFile = open(logFileName, 'w')
            else:
                logFile = open(logFileName, 'a')
            
            queueStr = "File #%s of %s: %s\n"%(i+1, len(fileList), f)
            print queueStr
            print ""
            outInfo = runCmd(f, commandPath, options)
            logFile.write(queueStr)
            logFile.write(outInfo)	
            logFile.close()
    else:
        print "%s is not a valid file Path"%commandPath

def runCmd(cmd, options = None):
    '''
    Pretty standard, open subprocess using Popen, return results and then pass them to calling function
    for more examples see:
    
    from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
    http://www.saltycrane.com/blog/2007/12/pyqt-example-how-to-run-command-and/
    
    '''
    try:
        cmd = cmd
        if options != None:
            cmd+=options
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        stdout, stderr = p.communicate()
        retVal = p.poll()
        return retVal, stdout, stderr
    except:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)
        errorMsg = "Sorry: %s\n\n:%s\n%s\n"%(exceptionType, exceptionValue, exceptionTraceback)
        #return QtGui.QMessageBox.warning(self, "Save Preferences Error", errorMsg)
        print errorMsg	

def parseDir(dirName, fileType, fullDive = False, debug = False):
    '''
    Currently this drills all the way down but it may be necessary to limit to a single directory
    '''
    filePaths = []
    if os.path.isdir(dirName):    
        if fullDive:
            for root, dirs, files in os.walk(dirName):
                for i,file in enumerate(files):
                    if re.search(r'\%s$'%fileType, file, re.IGNORECASE):
                        ffpn=os.path.abspath(os.path.join(root, file))#file full path name
                        filePaths.append(ffpn)
        
            return filePaths
        else:
            for file in os.listdir(dirName):
                if re.search(r'\%s$'%fileType, file, re.IGNORECASE):
                    ffpn=os.path.abspath(os.path.join(dirName, file))#file full path name
                    filePaths.append(ffpn)                       
            return filePaths
    
    else:
        print "%s is not a valid directory"%dirName
        return None

def log(output, quiet=True, doraise=False):
    if not LOGGER: return
    LOGGER.log(output)
    if quiet: return
    LOGGER.show()
    if not doraise: return
    raise_logger()

def raise_logger():
    LOGGER.raise_()

def input(msg, title=None):
    if title is None:
        title = msg
    parent = QtGui.qApp.activeWindow()
    result = QtGui.QInputDialog.getText(parent, msg, title)
    return (unicode(result[0]), result[1])

def close_log_window():
    LOGGER.hide()
    LOGGER.done(0)

def show_output(output, **kwargs):
    if not output: return
    log(output, quiet=False)

def toggle_log_window():
    if not LOGGER: return
    if LOGGER.isVisible():
        LOGGER.hide()
    else:
        LOGGER.show()
        LOGGER.raise_()

def create_listwidget_item(text, filename):
    icon = QIcon(filename)
    item = QListWidgetItem()
    item.setIcon(icon)
    item.setText(text)
    return item

def information(title, message=None):
    """Launches a QMessageBox information with the
    provided title and message."""
    if message is None:
        message = title
    QMessageBox.information(QtGui.qApp.activeWindow(), title, message)

def get_selected_row(list_widget):
    """Returns a(row_number, is_selected) tuple for a QListWidget."""
    row = list_widget.currentRow()
    item = list_widget.item(row)
    selected = item is not None and item.isSelected()
    return(row, selected)

def get_selection_list(listwidget, items):
    """Returns an array of model items that correspond to
    the selected QListWidget indices."""
    selected = []
    itemcount = listwidget.count()
    widgetitems = [ listwidget.item(idx) for idx in range(itemcount) ]

    for item, widgetitem in zip(items, widgetitems):
        if widgetitem.isSelected():
            selected.append(item)
    return selected

def get_selected_item(list_widget, items):
    row, selected = get_selected_row(list_widget)
    if selected and row < len(items):
        return items[row]
    else:
        return None

def open_dialog(parent, title, filename=None):
    qstr = QFileDialog.getOpenFileName(parent, parent.tr(title), filename)
    return unicode(qstr)

def opendir_dialog(parent, title, directory):
    flags = QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks
    qstr = QFileDialog.getExistingDirectory(parent, directory,
                                            parent.tr(title),
                                            flags)
    return unicode(qstr)

def save_dialog(parent, title, filename=''):
    return unicode(QFileDialog.getSaveFileName(parent,
                                               parent.tr(title),
                                               filename))

def new_dir_dialog(parent, title, filename=''):
    return unicode(QFileDialog.getSaveFileName(parent,
                                               parent.tr(title),
                                               filename,
                                               os.getcwd(),
                                               parent.tr('New Directory ()')))

def dir_dialog(parent, title, directory):
    directory = QFileDialog.getExistingDirectory(parent, parent.tr(title), directory)
    return unicode(directory)


def question(parent, title, message, default=True):
    """Launches a QMessageBox question with the provided title and message.
    Passing "default=False" will make "No" the default choice."""
    yes = QMessageBox.Yes
    no = QMessageBox.No
    buttons = yes | no
    if default:
        default = yes
    else:
        default = no
    result = QMessageBox.question(parent, title, message, buttons, default)
    return result == QMessageBox.Yes

def set_clipboard(text):
    QtGui.qApp.clipboard().setText(text, QClipboard.Clipboard)
    QtGui.qApp.clipboard().setText(text, QClipboard.Selection)

def add_items(widget, items):
    for item in items: widget.addItem(item)

def set_items(widget, items):
    widget.clear()
    add_items(widget, items)

def tr(txt):
    return unicode(QtGui.qApp.translate('', txt))

def create_txt_item(txt):
    item = QListWidgetItem()
    item.setText(txt)
    return item

def update_listwidget(widget, items, staged=True,
            untracked=False, append=False):
    """Populate a QListWidget with custom icon items."""
    if not append: widget.clear()
    add_items(widget, [ create_item(i, staged, untracked) for i in items ])

def set_listwidget_strings(widget, items):
    widget.clear()
    add_items(widget, [ create_txt_item(i) for i in items ])


def translate(context, string):
    """Translation"""
    return QApplication.translate(context, string)


def add_actions(target, actions, insert_before=None):
    """Add actions to a menu"""
    previous_action = None
    target_actions = list(target.actions())
    if target_actions:
        previous_action = target_actions[-1]
        if previous_action.isSeparator():
            previous_action = None
    for action in actions:
        if (action is None) and (previous_action is not None):
            if insert_before is None:
                target.addSeparator()
            else:
                target.insertSeparator(insert_before)
        elif isinstance(action, QMenu):
            if insert_before is None:
                target.addMenu(action)
            else:
                target.insertMenu(insert_before, action)
        elif isinstance(action, QAction):
            if insert_before is None:
                target.addAction(action)
            else:
                target.insertAction(insert_before, action)
        previous_action = action
        
def create_action(parent, text, shortcut=None, icon=None, tip=None,
                  toggled=None, triggered=None, data=None,
                  context=Qt.WindowShortcut):
    """Create a QAction"""
    action = QAction(text, parent)
    if triggered is not None:
        parent.connect(action, SIGNAL("triggered()"), triggered)
    if toggled is not None:
        parent.connect(action, SIGNAL("toggled(bool)"), toggled)
        action.setCheckable(True)
    if icon is not None:
        if isinstance(icon, (str, unicode)):
            icon = get_icon(icon)
        action.setIcon( icon )
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if data is not None:
        action.setData(QVariant(data))
    #TODO: Hard-code all shortcuts and choose context=Qt.WidgetShortcut
    # (this will avoid calling shortcuts from another dockwidget
    #  since the context thing doesn't work quite well with these widgets)
    action.setShortcutContext(context)
    return action
