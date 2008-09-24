#!/usr/bin/env python
# Copyright (c) 2007 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version. It is provided for educational purposes
# and is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.

import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


__version__ = "1.0.0"


class PythonHighlighter(QSyntaxHighlighter):

    Rules = []
    Formats = {}

    KEYWORDS = ["and", "as", "assert", "break", "class", "continue",
            "def", "del", "elif", "else", "except", "exec", "finally",
            "for", "from", "global", "if", "import", "in", "is", "lambda",
            "not", "or", "pass", "print", "raise", "return", "try",
            "while", "with", "yield", "show", "plot", "figure", "axes", "self"]

    BUILTINS = ["abs", "all", "any", "basestring", "bool", "callable",
            "chr", "classmethod", "cmp", "compile", "complex", "delattr",
            "dict", "dir", "divmod", "enumerate", "eval", "execfile",
            "exit", "file", "filter", "float", "frozenset", "getattr",
            "globals", "hasattr", "hex", "id", "int", "isinstance",
            "issubclass", "iter", "len", "list", "locals", "long", "map",
            "max", "min", "object", "oct", "open", "ord", "pow",
            "property", "range", "reduce", "repr", "reversed", "round",
            "set", "setattr", "slice", "sorted", "staticmethod", "str",
            "sum", "super", "tuple", "type", "unichr", "unicode", "vars",
            "xrange", "zip"] 

    CONSTANTS = ["False", "True", "None", "NotImplemented", "Ellipsis"]


    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % keyword \
                for keyword in PythonHighlighter.KEYWORDS])),
                "keyword"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % builtin \
                for builtin in PythonHighlighter.BUILTINS])),
                "builtin"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % constant \
                for constant in PythonHighlighter.CONSTANTS])),
                "constant"))
        PythonHighlighter.Rules.append((QRegExp(
                r"\b[+-]?[0-9]+[lL]?\b"
                r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
                r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),
                "number"))
        PythonHighlighter.Rules.append((QRegExp(
                r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt"))
        PythonHighlighter.Rules.append((QRegExp(r"\b@\w+\b"), "decorator"))
        PythonHighlighter.Rules.append((QRegExp(r"#.*"), "comment"))       
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')


    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        baseFormat.setFontFamily("Arial")
        baseFormat.setFontPointSize(10)
        for name, color, bold, italic in (
                ("normal", "#000000", False, False),
                ("keyword", "#FF0000", True, False),#000080
                ("builtin", "#0000A0", False, False),
                ("constant", "#0000C0", False, False),
                ("decorator", "#0000E0", False, False),
                ("comment", "#007F00", False, True),
                ("string", "#808000", False, False),
                ("number", "#924900", False, False),
                ("error", "#FF0000", False, False),
                ("pyqt", "#50621A", False, False)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(QColor(color))
            if bold:
                format.setFontWeight(QFont.Bold)
            format.setFontItalic(italic)
            PythonHighlighter.Formats[name] = format


    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)

        textLength = text.length()
        prevState = self.previousBlockState()

        self.setFormat(0, textLength,
                       PythonHighlighter.Formats["normal"])

        if text.startsWith("Traceback") or text.startsWith("Error: "):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return
        if prevState == ERROR and \
           not (text.startsWith(sys.ps1) or text.startsWith("#")):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return

        for regex, format in PythonHighlighter.Rules:
            i = text.indexOf(regex)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length,
                               PythonHighlighter.Formats[format])
                i = text.indexOf(regex, i + length)

        self.setCurrentBlockState(NORMAL)

        if text.indexOf(self.stringRe) != -1:
            return
        # This is fooled by triple quotes inside single quoted strings
        for i, state in ((text.indexOf(self.tripleSingleRe),
                          TRIPLESINGLE),
                         (text.indexOf(self.tripleDoubleRe),
                          TRIPLEDOUBLE)):
            if self.previousBlockState() == state:
                if i == -1:
                    i = text.length()
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3,     
                               PythonHighlighter.Formats["string"])
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, text.length(),
                               PythonHighlighter.Formats["string"])


    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()


class TextEdit(QTextEdit):

    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.wordList = ['alpha', 'alpaca', 'omega', 'omicron',  'zeta',  'zetta', 'my', 'mom',  'told',  'you'] 
        self.completer = QCompleter(self.wordList,  self)
        self.completer.setWrapAround(False)
        self.setCompleter(self.completer)
        
    
    def setCompleter(self,  completer):
#        if self.completer:
#            #self.completer.disconnect(SIGNAL("activated(QString)"))
#            QObject.disconnect(self.completer)#,  self.insertCompletion)
        
        self.completer = completer
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        QObject.connect(self.completer,  SIGNAL("activated(QString)"), self.insertCompletion)
            
    
    def insertCompletion(self,  completion):
        tc = self.textCursor()
        extra = completion.length() - self.completer.completionPrefix().length()
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion.right(extra))
        self.setTextCursor(tc)
    
    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()
        
    def focusInEvent(self,  event):
        if self.completer:
            self.completer.setWidget(self)
        return QTextEdit.focusInEvent(self, event)
        
    
    def keyPressEvent(self, event):
        if self.completer:
            
            completionPrefix = self.textUnderCursor()
            
            if self.completer.popup().isVisible():
                key = event.key()
                #print key
                if key == Qt.Key_Space:
                    self.completer.popup().hide()
                elif key == Qt.Key_Enter:
                    print "Enter"
                    self.insertCompletion(self.completer.currentCompletion())
                    #event.ignore()
                elif key == Qt.Key_Return:
                    event.ignore()
                elif key == Qt.Key_Escape:
                    event.ignore()
                elif key == Qt.Key_Tab:
                    event.ignore()
                elif key == Qt.Key_Backtab:
                    event.ignore()
                else:
                    return QTextEdit.keyPressEvent(self, event)#return 0
                #return 0
            
#            print event.modifiers()
#            print type(event.modifiers())
            if event.modifiers() is Qt.ControlModifier:
                print "CTRL"
            #isShortcut = ((event.modifiers()  and event.key() == Qt.Key_E))
            
            
            
            eow = QString("~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=")
            if event.text().isEmpty() or completionPrefix.length()<3 or eow.contains(event.text().right(1)):
                if self.completer.popup().isVisible():
                    self.completer.popup().hide()
                return QTextEdit.keyPressEvent(self, event)
                #return 0
            

            
            if completionPrefix != self.completer.completionPrefix() and completionPrefix.length()>3:
                if self.completer.popup().isVisible():
                    print "hide"
                    self.completer.popup().hide()
                return QTextEdit.keyPressEvent(self, event)
            
            
            if completionPrefix != self.completer.completionPrefix():
                self.completer.setCompletionPrefix(completionPrefix)
            
            cr = self.cursorRect()
            cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
            return QTextEdit.keyPressEvent(self, event)
            


    def event(self, event):
        if event.type() == QEvent.KeyPress and \
           event.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText("    ")
            return True
#        elif event.type() == QEvent.KeyPress and \
#           event.key() == Qt.Key_Period:
#            cursor = self.textCursor()
#            cursor.insertText("period")
        return QTextEdit.event(self, event)
    
##        self.editor = TextEdit()
##        self.editor.setFont(font)
##        self.highlighter = PythonHighlighter(self.editor.document())
##        self.setCentralWidget(self.editor)

