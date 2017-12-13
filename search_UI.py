from PyQt5 import QtWidgets, QtCore
from img import *
from Original_Model import search_GUI


class search_UI(QtWidgets.QDialog, search_GUI.Ui_Dialog):
    def __init__(self, item_ui):
        super(search_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init()
        self.ob = item_ui
        self.word = ""
        self.index = None
        self.pos = None

    def init(self):
        self.pushButton.clicked.connect(self.next_word)
        self.pushButton_2.clicked.connect(self.count)
        self.pushButton_3.clicked.connect(self.substitute)
        self.pushButton_4.clicked.connect(self.substitute_all)

    def prepare(self):
        def positions(content, pattern):
            result = []
            regex = QtCore.QRegExp(pattern)
            pos = 0
            index = regex.indexIn(content, pos)
            while index != -1:
                result.append(index)
                pos = index + regex.matchedLength()
                index = regex.indexIn(content, pos)
            return result

        keyword = self.lineEdit.text()
        if self.word != keyword:
            self.word = keyword
            self.index = -1
        self.pos = [(i, i + len(keyword)) for i in positions(self.ob.textEdit.toPlainText(), keyword)]

    def next_word(self):
        self.prepare()
        keyword = self.lineEdit.text()
        if keyword:
            self.index = (self.index + 1) % len(self.pos)
            self.ob.highlight(keyword)
            self.ob.highlight_specific(self.pos[self.index])

    def count(self):
        self.prepare()
        keyword = self.lineEdit.text()
        self.ob.highlight(keyword)
        if keyword:
            result = len(self.pos)
            _translate = QtCore.QCoreApplication.translate
            self.label_3.setText(_translate("Dialog", str(result)))

    def substitute(self):
        self.prepare()
        keyword = self.lineEdit.text()
        if keyword and self.pos:
            self.index = self.index % len(self.pos)
            substitute_to = self.lineEdit_2.text()
            text_1 = self.ob.textEdit.toPlainText()[:self.pos[self.index][0]]
            text_2 = self.ob.textEdit.toPlainText()[self.pos[self.index][1]:]
            text_ = text_1 + substitute_to + text_2
            self.ob.edit()
            self.ob.textEdit.setText(text_)
            self.ob.file.set_content(text_)
            pos = (len(text_1), len(text_1) + len(substitute_to))
            self.prepare()
            self.ob.highlight(keyword)
            self.ob.highlight_specific(pos, color="grey")

    def substitute_all(self):
        keyword = self.lineEdit.text()
        if keyword:
            substitute_to = self.lineEdit_2.text()
            text_ = self.ob.textEdit.toPlainText().replace(keyword, substitute_to)
            self.ob.textEdit.setText(text_)
            self.ob.file.set_content(text_)
            self.ob.highlight(substitute_to)
