import sys,re
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent,QRegExp)
from PySide2.QtGui import (QBrush, QColor, QSyntaxHighlighter,QConicalGradient,QTextCharFormat, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from ui_pytexteditor import Ui_MainWindow

class main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('PyEditor')
        highlighter = MyHighlighter(self.ui.textEdit.document())
        self.show()
class MyHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        self.highlight_regex = {
            'HighlightCode' : re.compile(u'=|if|elif|else|for|while|return|def|print'),

            'HighlightQuote': re.compile(u'".+?"'), # > This is a quote

            'HighlightNumbers': re.compile(u'[0-9]+|True|False|None')
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
        self.highlightCode(text,0)
        self.highlightquate(text,0)
        self.highlightnumbers(text,0)
    def highlightCode(self,text,strt):
        found = False
        for mo in re.finditer(self.highlight_regex['HighlightCode'],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.highlight_format['HighlightCode'])
            found = True
        return found
    def highlightquate(self,text,strt):
        found = False
        for mo in re.finditer(self.highlight_regex['HighlightQuote'],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.highlight_format['HighlightQuote'])
            found = True
        return found
    def highlightnumbers(self,text,strt):
        found = False
        for mo in re.finditer(self.highlight_regex['HighlightNumbers'],text):
            self.setFormat(mo.start()+strt, mo.end() - mo.start(), self.highlight_format['HighlightNumbers'])
            found = True
        return found
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main()
    sys.exit(app.exec_())
