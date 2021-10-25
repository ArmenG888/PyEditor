import sys,re
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent,QRegExp)
from PySide2.QtGui import (QBrush, QColor, QSyntaxHighlighter,QConicalGradient,QTextCharFormat, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
import subprocess
from ui_pytexteditor import Ui_MainWindow
from ui_output import Ui_MainWindow as output_win
class main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.filename = "None"
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.setWindowTitle('PyEditor')
        self.font_size = 12
        self.setup_menus()
        self.show()
    def setup_menus(self):
        self.ui.actionOpen_File.triggered.connect(self.open)
        self.ui.actionOpen_File.setShortcut("Ctrl+O")
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave.setShortcut("Ctrl+S")
        self.ui.actionSave_As.triggered.connect(self.save_as)
        self.ui.actionSave_As.setShortcut("Ctrl+Shift+S")
        self.ui.actionRun.triggered.connect(self.run_file)
        self.ui.actionRun.setShortcut("Ctrl+Shift+B")
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionNew.setShortcut("Ctrl+N")
        self.ui.actionLicenses.triggered.connect(self.license)

    def save(self):
        if self.filename == "None":
            self.save_as()
        with open(self.filename, "w") as w:
            w.write(self.ui.textEdit.toPlainText())
        return
    def save_as(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_():
            self.filename = dialog.selectedFiles()
        with open(self.filename, "w") as w:
            w.write(self.ui.textEdit.toPlainText())
    def new(self):
        self.setWindowTitle("PyEditor Untitled")
        self.ui.textEdit.setText("")
    def license(self):
        with open("License","r") as r:
            r = r.read()
        self.ui.textEdit.setText(r)
    def open(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_():
            self.filename = dialog.selectedFiles()[0]
            print(self.filename)
        with open(self.filename, "r") as r:
            file_content = r.read()
        self.ui.textEdit.setText(file_content)
        self.setWindowTitle("PyEditor " + self.filename)
        if self.filename.endswith(".py") == True:
            Py_Highligther = py_highligther(self.ui.textEdit.document())
        elif self.filename.endswith(".html") == True:
            Html_Highlighter = html_highlighter(self.ui.textEdit.document())
    def run_file(self):
        QMessageBox.information(self, self.filename,exec(open(self.filename).read()))
class py_highligther(QSyntaxHighlighter):
    def highlightBlock(self, text):
        self.highlight_regex = {
            'HighlightCode' : re.compile(u'=|if|elif|else|for|while|return|def|print|class'),

            'HighlightQuote': re.compile(u"""'.+?'|".+?"|"""),
            'HighlightNumbers': re.compile(u'[0-9]+|True|False|None|from|import|self')
        }
        self.highlight_format = {}
        text_char_format = QTextCharFormat()
        text_char_format.setForeground(QBrush(QColor("#dc322f")))
        self.highlight_format['HighlightCode'] = text_char_format
        text_char_format = QTextCharFormat()
        text_char_format.setForeground(QBrush(QColor("#ffff66")))
        self.highlight_format['HighlightQuote'] = text_char_format
        text_char_format = QTextCharFormat()
        text_char_format.setForeground(QBrush(QColor("#bf75ff")))
        self.highlight_format['HighlightNumbers'] = text_char_format
        for i in self.highlight_format:
            self.highlightCode(text,0,i)
    def highlightCode(self,text,strt,x):
        found = False
        for mo in re.finditer(self.highlight_regex[x],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.highlight_format[x])
            found = True
        return found
class html_highlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        self.highlight_regex = {
            'HighlightCode' : re.compile(u'<.+?>|'),

            'HighlightQuote': re.compile(u"""'.+?'|".+?"|"""),

            'HighlightNumbers': re.compile(u'class|href|{.+?}')
        }
        self.highlight_format = {}
        text_char_format = QTextCharFormat()
        text_char_format.setForeground(QBrush(QColor("#dc322f")))
        self.highlight_format['HighlightCode'] = text_char_format
        text_char_format = QTextCharFormat()
        text_char_format.setForeground(QBrush(QColor("#ffff66")))
        self.highlight_format['HighlightQuote'] = text_char_format
        text_char_format = QTextCharFormat()
        text_char_format.setForeground(QBrush(QColor("#bf75ff")))
        self.highlight_format['HighlightNumbers'] = text_char_format
        for i in self.highlight_format:
            self.highlightCode(text,0,i)
    def highlightCode(self,text,strt,x):
        found = False
        for mo in re.finditer(self.highlight_regex[x],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.highlight_format[x])
            found = True
        return found
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    sys.exit(app.exec_())
