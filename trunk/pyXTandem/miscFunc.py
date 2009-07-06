#!/usr/bin/env python

from __future__ import division
from __future__ import with_statement

import base64
import os
import re
import sys

from PyQt4.QtCore import (PYQT_VERSION_STR, QByteArray, QDir, QEvent,
        QFile, QFileInfo, QIODevice, QPoint, QProcess, QRegExp,
        QSettings, QString, QT_VERSION_STR, QTextStream, QThread,
        QTimer, QUrl, QVariant, Qt, SIGNAL)
from PyQt4.QtGui import (QAction, QApplication, QButtonGroup, QCheckBox,
        QColor, QColorDialog, QComboBox, QCursor, QDesktopServices,
        QDialog, QDialogButtonBox, QFileDialog, QFont, QFontComboBox,
        QFontMetrics, QGridLayout, QHBoxLayout, QIcon, QInputDialog,
        QKeySequence, QLabel, QLineEdit, QListWidget, QMainWindow,
        QMessageBox, QPixmap, QPushButton, QRadioButton,
        QRegExpValidator, QShortcut, QSpinBox, QSplitter,
        QSyntaxHighlighter, QTabWidget, QTextBrowser, QTextCharFormat,
        QTextCursor, QTextDocument, QTextEdit, QToolTip, QVBoxLayout,
        QWidget)


__version__ = "1.0.0"

KEYWORDS = ["and", "as", "assert", "break", "class", "continue", "def",
        "del", "elif", "else", "except", "exec", "finally", "for", "from",
        "global", "if", "import", "in", "is", "lambda", "not", "or",
        "pass", "print", "raise", "return", "try", "while", "with",
        "yield"]

BUILTINS = ["abs", "all", "any", "basestring", "bool", "callable", "chr",
        "classmethod", "cmp", "compile", "complex", "delattr", "dict",
        "dir", "divmod", "enumerate", "eval", "execfile", "exit", "file",
        "filter", "float", "frozenset", "getattr", "globals", "hasattr",
        "hex", "id", "int", "isinstance", "issubclass", "iter", "len",
        "list", "locals", "long", "map", "max", "min", "object", "oct",
        "open", "ord", "pow", "property", "range", "reduce", "repr",
        "reversed", "round", "set", "setattr", "slice", "sorted",
        "staticmethod", "str", "sum", "super", "tuple", "type", "unichr",
        "unicode", "vars", "xrange", "zip"]

CONSTANTS = ["False", "True", "None", "NotImplemented", "Ellipsis"]

TIMEOUT = 5000
ICONS = {}
PIXMAPS = {}
Config = {}
CAT = {} # Completions And Tooltips
MIN_COMPLETION_LEN = 3
MAX_TOOLTIP_LEN = 1000
FROM_IMPORT_RE = re.compile(r"from\s+([\w.]+)\s+import\s+(.*)")
WORDS = set()
WORD_RE = re.compile(r"[\W+.]")
MIN_WORD_LEN = 3
MAX_WORD_LEN = 64
CATABLE_LINE_RE = QRegExp(r"\b(?:import|def|class)\s+")
CLASS_OR_DEF_RE = re.compile(r"(class|def) ([^\W(:]+)[:(]")

settings = QSettings()
for name, color, bold, italic in (
        ("normal", "#000000", False, False),
        ("keyword", "#000080", True, False),
        ("builtin", "#0000A0", False, False),
        ("constant", "#0000C0", False, False),
        ("decorator", "#0000E0", False, False),
        ("comment", "#007F00", False, True),
        ("string", "#808000", False, False),
        ("number", "#924900", False, False),
        ("error", "#FF0000", False, False),
        ("pyqt", "#50621A", False, False)):
    Config["%sfontcolor" % name] = settings.value(
            "%sfontcolor" % name, QVariant(color)).toString()
    Config["%sfontbold" % name] = settings.value(
            "%sfontbold" % name, QVariant(bold)).toBool()
    Config["%sfontitalic" % name] = settings.value(
            "%sfontitalic" % name, QVariant(italic)).toBool()


Config["findcasesensitive"] = settings.value("findcasesensitive",
        QVariant(False)).toBool()
Config["findwholewords"] = settings.value("findwholewords",
        QVariant(False)).toBool()
Config["tabwidth"] = settings.value("tabwidth",
        QVariant(4)).toInt()[0]
Config["fontfamily"] = settings.value("fontfamily",
        QVariant("Bitstream Vera Sans Mono")).toString()
Config["fontsize"] = settings.value("fontsize",
        QVariant(10)).toInt()[0]



def loadConfig():
    def setDefaultString(name, default):
        value = settings.value(name).toString()
        if value.isEmpty():
            value = default
        Config[name] = value

    settings = QSettings()
    for name in ("window", "shell"):
        Config["%swidth" % name] = settings.value("%swidth" % name,
                QVariant(QApplication.desktop()
                         .availableGeometry().width() / 2)).toInt()[0]
        Config["%sheight" % name] = settings.value("%sheight" % name,
                QVariant(QApplication.desktop()
                         .availableGeometry().height() / 2)).toInt()[0]
        Config["%sy" % name] = settings.value("%sy" % name,
                QVariant(0)).toInt()[0]
    Config["toolbars"] = settings.value("toolbars").toByteArray()
    Config["splitter"] = settings.value("splitter").toByteArray()
    Config["shellx"] = settings.value("shellx",
                                      QVariant(0)).toInt()[0]
    Config["windowx"] = settings.value("windowx",
            QVariant(QApplication.desktop()
                            .availableGeometry().width() / 2)).toInt()[0]
    Config["remembergeometry"] = settings.value("remembergeometry",
            QVariant(True)).toBool()
    Config["startwithshell"] = settings.value("startwithshell",
            QVariant(True)).toBool()
    Config["showwindowinfo"] = settings.value("showwindowinfo",
            QVariant(True)).toBool()
    setDefaultString("shellstartup", """\
from __future__ import division
import codecs
import sys
sys.stdin = codecs.getreader("UTF8")(sys.stdin)
sys.stdout = codecs.getwriter("UTF8")(sys.stdout)""")
    setDefaultString("newfile", """\
#!/usr/bin/env python

from __future__ import division

import sys
""")
    Config["backupsuffix"] = settings.value("backupsuffix",
            QVariant(".bak")).toString()
    setDefaultString("beforeinput", "#>>>")
    setDefaultString("beforeoutput", "#---")
    Config["cwd"] = settings.value("cwd", QVariant(".")).toString()
    Config["tooltipsize"] = settings.value("tooltipsize",
            QVariant(150)).toInt()[0]
    Config["maxlinestoscan"] = settings.value("maxlinestoscan",
            QVariant(5000)).toInt()[0]
    Config["pythondocpath"] = settings.value("pythondocpath",
            QVariant("http://docs.python.org")).toString()
    Config["autohidefinddialog"] = settings.value("autohidefinddialog",
            QVariant(True)).toBool()
    Config["findcasesensitive"] = settings.value("findcasesensitive",
            QVariant(False)).toBool()
    Config["findwholewords"] = settings.value("findwholewords",
            QVariant(False)).toBool()
    Config["tabwidth"] = settings.value("tabwidth",
            QVariant(4)).toInt()[0]
    Config["fontfamily"] = settings.value("fontfamily",
            QVariant("Bitstream Vera Sans Mono")).toString()
    Config["fontsize"] = settings.value("fontsize",
            QVariant(10)).toInt()[0]
    for name, color, bold, italic in (
            ("normal", "#000000", False, False),
            ("keyword", "#000080", True, False),
            ("builtin", "#0000A0", False, False),
            ("constant", "#0000C0", False, False),
            ("decorator", "#0000E0", False, False),
            ("comment", "#007F00", False, True),
            ("string", "#808000", False, False),
            ("number", "#924900", False, False),
            ("error", "#FF0000", False, False),
            ("pyqt", "#50621A", False, False)):
        Config["%sfontcolor" % name] = settings.value(
                "%sfontcolor" % name, QVariant(color)).toString()
        Config["%sfontbold" % name] = settings.value(
                "%sfontbold" % name, QVariant(bold)).toBool()
        Config["%sfontitalic" % name] = settings.value(
                "%sfontitalic" % name, QVariant(italic)).toBool()

def saveConfig():
    settings = QSettings()
    for key, value in Config.items():
        settings.setValue(key, QVariant(value))

class PythonHighlighter(QSyntaxHighlighter):

    Rules = []
    Formats = {}
    #loadConfig()

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])),
                "keyword"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])),
                "builtin"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % constant
                for constant in CONSTANTS])), "constant"))
        PythonHighlighter.Rules.append((QRegExp(
                r"\b[+-]?[0-9]+[lL]?\b"
                r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
                r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),
                "number"))
        PythonHighlighter.Rules.append((QRegExp(
                r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt"))
        PythonHighlighter.Rules.append((QRegExp(r"\b@\w+\b"),
                "decorator"))
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
        baseFormat.setFontFamily(Config["fontfamily"])
        baseFormat.setFontPointSize(Config["fontsize"])
        for name in ("normal", "keyword", "builtin", "constant",
                "decorator", "comment", "string", "number", "error",
                "pyqt"):
            format = QTextCharFormat(baseFormat)
            format.setForeground(
                            QColor(Config["%sfontcolor" % name]))
            if Config["%sfontbold" % name]:
                format.setFontWeight(QFont.Bold)
            format.setFontItalic(Config["%sfontitalic" % name])
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
        if (prevState == ERROR and
            not (text.startsWith(sys.ps1) or text.startsWith("#"))):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return

        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length,
                               PythonHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)

        # Slow but good quality highlighting for comments. For more
        # speed, comment this out and add the following to __init__:
        # PythonHighlighter.Rules.append((QRegExp(r"#.*"), "comment"))
        if text.isEmpty():
            pass
        elif text[0] == "#":
            self.setFormat(0, text.length(),
                           PythonHighlighter.Formats["comment"])
        else:
            stack = []
            for i, c in enumerate(text):
                if c in ('"', "'"):
                    if stack and stack[-1] == c:
                        stack.pop()
                    else:
                        stack.append(c)
                elif c == "#" and len(stack) == 0:
                    self.setFormat(i, text.length(),
                                   PythonHighlighter.Formats["comment"])
                    break

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
        QApplication.setOverrideCursor(QCursor(
                                                    Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()
