import main_GUI
import file_GUI
import item_GUI
import freq_GUI
import search_GUI
import create_file_GUI
import File
import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class search_UI(QtWidgets.QDialog, search_GUI.Ui_Dialog):
    def __init__(self, item_ui):
        super(search_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init()
        self.ob = item_ui

    def init(self):
        self.pushButton.clicked.connect(self.next_word)
        self.pushButton_2.clicked.connect(self.count)
        self.pushButton_3.clicked.connect(self.substitute)
        self.pushButton_4.clicked.connect(self.substitute_all)

    def next_word(self):
        keyword = self.lineEdit.text()
        if keyword:
            self.ob.highlight(keyword)

    def count(self):
        self.next_word()
        keyword = self.lineEdit.text()
        import KMP
        result = KMP.count(self.ob.file.get_content(), keyword)
        _translate = QtCore.QCoreApplication.translate
        self.label_3.setText(_translate("Dialog", str(result)))

    def substitute(self):
        pass

    def substitute_all(self):
        keyword = self.lineEdit.text()
        substitute_to = self.lineEdit_2.text()
        text_ = self.ob.textEdit.toPlainText().replace(keyword, substitute_to)
        self.ob.textEdit.setText(text_)
        self.ob.file.set_content(text_)
        self.ob.highlight(substitute_to)


class freq_UI(QtWidgets.QDialog, freq_GUI.Ui_Dialog):
    def __init__(self, freqs):
        super(freq_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init(freqs)

    def init(self, freqs):
        if freqs:
            order = 1
            for i in freqs:
                string = str(order) + ". " + i["word"]
                string = string + "\t\t\t\t" + str(i["num"]) + "次"
                self.listWidget.addItem(string)
                order += 1


class create_file_UI(QtWidgets.QDialog, create_file_GUI.Ui_dialog):
    def __init__(self):
        super(create_file_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def file_pos(self):
        return self.lineEdit.text()


class item_UI(QtWidgets.QDialog, item_GUI.Ui_Dialog):
    def __init__(self, file_pos, keyword=None):
        super(item_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.file = File.File(file_pos)
        self.init(keyword)

    def init(self, keyword):
        self.pushButton.clicked.connect(self.encode)
        self.pushButton_2.clicked.connect(self.decode)
        # self.pushButton_3.clicked.connect(self.buttonClicked)
        self.pushButton_4.clicked.connect(self.edit)
        self.toolButton.setShortcut('Ctrl+F')
        self.toolButton.clicked.connect(self.search_substitute)
        self.highlight(keyword)
        self.textEdit.setReadOnly(True)

    def highlight(self, pattern, color="red"):
        self.textEdit.setText(self.file.get_content())
        if pattern:
            cursor = self.textEdit.textCursor()
            # Setup the desired format for matches
            format = QtGui.QTextCharFormat()
            format.setBackground(QtGui.QBrush(QtGui.QColor(color)))
            # Setup the regex engine
            regex = QtCore.QRegExp(pattern)
            # Process the displayed document
            pos = 0
            index = regex.indexIn(self.textEdit.toPlainText(), pos)
            while index != -1:
                # Select the matched text and apply the desired format
                cursor.setPosition(index)
                for i in range(len(pattern)):
                    cursor.movePosition(QtGui.QTextCursor.Right, 1)
                cursor.mergeCharFormat(format)
                # Move to the next match
                pos = index + regex.matchedLength()
                index = regex.indexIn(self.textEdit.toPlainText(), pos)

    def encode(self):
        self.textEdit.setText(self.file.get_encodeStr())

    def decode(self):
        self.textEdit.setText(self.file.get_decodeStr(self.file.get_encodeStr()))

    def edit(self):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_4.setText(_translate("Dialog", "保存"))
        self.pushButton_4.clicked.connect(self.save)
        self.textEdit.setReadOnly(False)

    def save(self):
        _translate = QtCore.QCoreApplication.translate
        self.file.set_content(self.textEdit.toPlainText())
        # f = open(self.file.pos, "w+")
        # f.write(self.textEdit.toPlainText())
        self.file.chars_freqs = None
        self.file.Huffman_codes = None
        self.textEdit.setReadOnly(True)
        self.pushButton_4.setText(_translate("Dialog", "编辑"))
        self.pushButton_4.clicked.connect(self.edit)

    def search_substitute(self):
        search_ui = search_UI(self)
        search_ui.show()
        search_ui.exec_()


class UI(QtWidgets.QMainWindow, main_GUI.Ui_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init()
        self.search_status = None

    def init(self):
        self.statusBar().showMessage("欢迎~~~")
        self.pushButton.clicked.connect(self.search)
        self.pushButton_3.clicked.connect(self.create_file)
        self.pushButton_4.clicked.connect(self.cal_words_freq)
        self.pushButton_5.clicked.connect(self.buttonClicked)
        self.action.triggered.connect(self.add_files)
        self.action_3.triggered.connect(self.clear_list)
        self.listWidget.itemDoubleClicked.connect(self.itemClicked)

    def add_files(self):
        ui_file = file_GUI.Ui_FileDialog()
        self.creat_listWidget(ui_file.openFileNamesDialog())

    def create_file(self):
        dialog = create_file_UI()
        file_pos = ""
        if dialog.exec_():
            file_pos = (QtGui.QStandardItem(dialog.file_pos())).text()
            # dialog.destroy()
        if file_pos and "\\" not in file_pos:
            import os
            if os.path.isabs(file_pos):
                pass
            else:
                file_pos = os.getcwd() + "\\" + file_pos
            file = open(file_pos, "w")
            file.close()
            self.creat_listWidget([file_pos])

    def cal_words_freq(self):
        files = [self.listWidget.item(i).text().split("\t")[0] for i in range(self.listWidget.count())]
        freqs = File.cal_words_freq(files=files, reverse=True)
        freq_ui = freq_UI(freqs)
        freq_ui.show()
        freq_ui.exec_()

    def clear_list(self):
        self.listWidget.clear()

    def get_research_content(self):
        return self.lineEdit.text()

    def creat_listWidget(self, files):
        if files:
            for file in files:
                self.listWidget.addItem(file)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "真退出？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def search(self):
        self.search_status = self.get_research_content()
        self.statusBar().showMessage(self.get_research_content() + " 的检索结果")
        files = [self.listWidget.item(i).text().split("\t")[0] for i in range(self.listWidget.count())]
        result = File.search(files, self.get_research_content())
        self.listWidget.clear()
        for i in result:
            string = i["file"] + "\t\t\t" + str(i["num"]) + "次"
            self.listWidget.addItem(string)

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(str(sender) + ' was pressed')

    def itemClicked(self, index):
        self.statusBar().showMessage(str(index.text()).split("\t")[0])
        item_ui = item_UI(index.text().split("\t")[0], self.search_status)
        item_ui.show()
        item_ui.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
