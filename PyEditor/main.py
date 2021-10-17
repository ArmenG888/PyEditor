import sys,re
from subprocess import run
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent,QRegExp)
from PySide2.QtGui import (QBrush, QColor, QSyntaxHighlighter,QConicalGradient,QTextCharFormat, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from ui_pytexteditor import Ui_MainWindow

class main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.filename = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        self.setWindowTitle('PyEditor')
        self.setup_menus()
        highlighter = MyHighlighter(self.ui.textEdit.document())
        self.show()
    def setup_menus(self):
        self.ui.actionOpen_File.triggered.connect(self.open)
        self.ui.actionOpen_File.setShortcut("Ctrl+O")
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave.setShortcut("Ctrl+S")
        self.ui.actionSave_As.triggered.connect(self.save_as)
        self.ui.actionSave_As.setShortcut("Ctrl+Shift+S")
        self.ui.actionRun.triggered.connect(self.run_file)
        self.ui.actionRun.setShortcut("Ctrl+B")
    def save(self):
        if self.filename == []:
            self.save_as()
        print(self.ui.textEdit.toPlainText())
        with open(self.filename[0], "w") as w:
            w.write(self.ui.textEdit.toPlainText())
        return
    def save_as(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_():
            self.filename = dialog.selectedFiles()
        with open(self.filename[0], "w") as w:
            w.write(self.ui.textEdit.toPlainText())
    def open(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec_():
            self.filename = dialog.selectedFiles()
            print(self.filename)
        with open(self.filename[0], "r") as r:
            file_content = r.read()
        self.ui.textEdit.setText(file_content)
    def run_file(self):
        run([sys.executable, self.filename[0]])
class MyHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        self.highlight_regex = {
            'HighlightCode' : re.compile(u'=|if|elif|else|for|while|return|def|print'),

            'HighlightQuote': re.compile(u'".+?"'), 

            'HighlightNumbers': re.compile(u'[0-9]+|True|False|None|from|import|self'),
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
