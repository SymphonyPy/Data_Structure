import main_GUI
import file_GUI
import item_GUI
import search_GUI
import create_file_GUI
import progressbar_GUI
import huffman_GUI
import about_GUI
import File
import sys
import time
from PyQt5 import QtWidgets, QtCore, QtGui
from img import *


class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__(QtGui.QPixmap(":start_page.png"))

    def effect(self):
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() + 0.1
            if newOpacity > 1:
                break

            self.setWindowOpacity(newOpacity)
            self.show()
            t -= 1
            time.sleep(0.04)

        time.sleep(1)
        t = 0
        while t <= 500:
            newOpacity = self.windowOpacity() - 0.1
            if newOpacity < 0:
                break

            self.setWindowOpacity(newOpacity)
            t += 1
            time.sleep(0.04)


class about_UI(QtWidgets.QDialog, about_GUI.Ui_dialog):
    def __init__(self):
        super(about_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init()

    def init(self):
        self.pushButton.clicked.connect(self.close)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.label.setPixmap(QtGui.QPixmap(":icon.png"))


class huffman_UI(QtWidgets.QDialog, huffman_GUI.Ui_Dialog):
    def __init__(self, form):
        super(huffman_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init(form)

    def init(self, form):
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(form))
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setHorizontalHeaderLabels(['字符', "出现次数", '编码'])
        row = 0
        for item in form:
            newItem = QtWidgets.QTableWidgetItem(item[0])
            self.tableWidget.setItem(row, 0, newItem)
            newItem = QtWidgets.QTableWidgetItem(str(item[1]))
            self.tableWidget.setItem(row, 1, newItem)
            newItem = QtWidgets.QTableWidgetItem(item[2])
            self.tableWidget.setItem(row, 2, newItem)
            row += 1
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)


class progressbar_UI(QtWidgets.QDialog, progressbar_GUI.Ui_Dialog):
    def __init__(self, value=0, text="123"):
        super(progressbar_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init()
        self.setValue(value)
        self.setText(text)

    def init(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def setValue(self, value):
        self.progressBar.setProperty("value", value)
        if value >= 100:
            import time
            for i in range(3):
                self.setText("创建完成！..." + str(3 - i))
                QtWidgets.QApplication.processEvents()
                time.sleep(1)

    def setText(self, file_pos):
        if len(file_pos) > 35:
            string = file_pos.split("/")[0] + "/" + file_pos.split("/")[1] + "/.../" + file_pos.split("/")[-1]
        else:
            string = file_pos
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", string))


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


class freq_UI(QtWidgets.QDialog, huffman_GUI.Ui_Dialog):
    def __init__(self, freqs):
        super(freq_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init(freqs)

    def init(self, freqs):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "词频统计"))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(freqs))
        self.tableWidget.setHorizontalHeaderLabels(['字符', "出现次数"])
        row = 0
        for item in freqs:
            newItem = QtWidgets.QTableWidgetItem(item["word"])
            self.tableWidget.setItem(row, 0, newItem)
            newItem = QtWidgets.QTableWidgetItem(str(item["num"]))
            self.tableWidget.setItem(row, 1, newItem)
            row += 1
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)


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
        self.init(keyword, file_pos.split("/")[-1])

    def init(self, keyword, filename):
        self.pushButton.clicked.connect(self.encode)
        self.pushButton_2.clicked.connect(self.decode)
        self.pushButton_3.clicked.connect(self.huffman_codes)
        self.pushButton_4.clicked.connect(self.edit)
        self.toolButton.setShortcut('Ctrl+F')
        self.toolButton.clicked.connect(self.search_substitute)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+T"), self)
        self.shortcut.activated.connect(self.translate)
        self.highlight(keyword)
        self.textEdit.setReadOnly(True)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", filename))
        self.label.setText(_translate("Dialog", "选中内容后，按Ctrl+T翻译"))
        self.current_selected_string = None

    def highlight(self, pattern, color="yellow"):
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

    def highlight_specific(self, pos=(0, 0), color="grey"):
        cursor = self.textEdit.textCursor()
        # Setup the desired format for matches
        format = QtGui.QTextCharFormat()
        format.setBackground(QtGui.QBrush(QtGui.QColor(color)))
        cursor.setPosition(pos[0])
        for i in range(pos[1] - pos[0]):
            cursor.movePosition(QtGui.QTextCursor.Right, 1)
        cursor.mergeCharFormat(format)

    def encode(self):
        self.textEdit.setText(self.file.get_encodeStr())

    def decode(self):
        self.textEdit.setText(self.file.get_decodeStr(self.file.get_encodeStr()))

    def huffman_codes(self):
        huffman_codes = self.file.get_huffman_codes()
        form = []
        for item in huffman_codes:
            for tuple in self.file.chars_freqs:
                if item[0] == tuple[0]:
                    form.append((item[0], tuple[1], item[1]))
        huffman_ui = huffman_UI(form)
        huffman_ui.show()
        huffman_ui.exec_()

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

    def translate(self):
        import requests
        def t(string):
            import bs4
            rooturl = 'http://www.youdao.com/w/'
            finurl = rooturl + string
            res = {}
            res['word'] = string
            try:
                response = requests.get(finurl)
                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                tran = soup.select('.trans-container > ul > li')[0].get_text()
                res['翻译'] = tran
            except IndexError:
                res['翻译'] = "好像没找到这个词..."
            return res

        internet = requests.get("http://www.baidu.com").status_code
        if internet == 200:
            string = self.textEdit.textCursor().selectedText()
            if " " in string:
                _translate = QtCore.QCoreApplication.translate
                self.label.setText(_translate("Dialog", "只能查单词哟~~"))
                return True
            result = t(string)
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("Dialog", result["翻译"]))
        else:
            _translate = QtCore.QCoreApplication.translate
            self.label.setText(_translate("Dialog", "似乎没有联网..."))


class UI(QtWidgets.QMainWindow, main_GUI.Ui_MainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.init()
        self.search_status = None
        self.freqs = None

    def init(self):
        self.statusBar().showMessage("欢迎~~~")
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.load_package)
        self.pushButton_3.clicked.connect(self.create_file)
        self.pushButton_4.clicked.connect(self.cal_words_freq)
        self.pushButton_5.clicked.connect(self.packaging)
        self.action.triggered.connect(self.add_files)
        self.action_2.triggered.connect(self.about)
        self.action_3.triggered.connect(self.clear_list)
        self.tableWidget.itemDoubleClicked.connect(self.itemClicked)

    def add_files(self):
        self.freqs = None
        ui_file = file_GUI.Ui_FileDialog()
        files = ui_file.openFileNamesDialog()
        if files:
            self.creat_tableWidget(files)

    def about(self):
        about_ui = about_UI()
        about_ui.show()
        about_ui.exec_()

    def create_file(self):
        self.freqs = None
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
                file_pos = os.getcwd() + "\\" + file_pos + ".txt"
            file = open(file_pos, "w")
            file.close()
            self.creat_tableWidget([file_pos])

    def cal_words_freq(self):
        total_freq = []
        result = {}
        if not self.freqs:
            self.freqs = []
            files = self.get_files_from_table()
            proBar_ui = progressbar_UI()
            proBar_ui.show()
            for file in files:
                self.freqs.append((file, File.cal_words_positions(files=[file])))
                proBar_ui.setText(file)
                proBar_ui.setValue((files.index(file) + 1) * 100 / len(files))
                QtWidgets.QApplication.processEvents()
            proBar_ui.close()
        for word_tuple in self.freqs:
            for word_and_freq_dict in word_tuple[1]:
                if word_and_freq_dict["word"] not in result.keys():
                    result[word_and_freq_dict["word"]] = len(word_and_freq_dict["pos"])
                else:
                    result[word_and_freq_dict["word"]] += len(word_and_freq_dict["pos"])
        for key in result.keys():
            total_freq.append({"word": key, "num": result[key]})

        def num(result):
            return result["num"]

        total_freq.sort(key=num, reverse=True)
        freq_ui = freq_UI(total_freq)
        freq_ui.show()
        freq_ui.exec_()

    def load_package(self):
        import six.moves.cPickle as pickle
        ui_file = file_GUI.Ui_FileDialog()
        package_pos = ui_file.openFileNameDialog(file_type="PKL Files (*.pkl)")
        if package_pos:
            with open(package_pos, "rb") as package:
                self.freqs = pickle.load(package)
            files = [file[0] for file in self.freqs]
            self.creat_tableWidget(files)
            self.statusBar().showMessage(package_pos + '读取成功！')

    def packaging(self):
        import six.moves.cPickle as pickle
        dialog = create_file_UI()
        file_pos = ""
        if dialog.exec_():
            file_pos = (QtGui.QStandardItem(dialog.file_pos())).text()
        proBar_ui = progressbar_UI()
        proBar_ui.show()
        files = self.get_files_from_table()
        self.freqs = []
        for file in files:
            self.freqs.append((file, File.cal_words_positions(files=[file])))
            proBar_ui.setText(file)
            proBar_ui.setValue((files.index(file) + 1) * 100 / len(files))
            QtWidgets.QApplication.processEvents()
        proBar_ui.close()
        if file_pos and "\\" not in file_pos:
            import os
            if os.path.isabs(file_pos):
                pass
            else:
                file_pos = os.getcwd() + "\\" + file_pos + ".pkl"
            with open(file_pos, "wb") as file:
                pickle.dump(self.freqs, file)
            self.statusBar().showMessage(file_pos + '保存成功！')

    def clear_list(self):
        self.freqs = None
        self.tableWidget.clear()
        self.tableWidget.setHorizontalHeaderLabels(['文件', "词频"])
        self.tableWidget.setRowCount(0)

    def get_research_content(self):
        return self.lineEdit.text()

    def get_files_from_table(self):
        files = []
        row = self.tableWidget.rowCount()
        for i in range(row):
            files.append(self.tableWidget.item(i, 0).text())
        return files

    def creat_tableWidget(self, files, nums=[], poss=[]):
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(files))
        self.tableWidget.setColumnWidth(0, 640)
        self.tableWidget.setColumnWidth(1, 80)
        self.tableWidget.setHorizontalHeaderLabels(['文件', "词频", "位置"])
        if files:
            row = 0
            for file in files:
                newItem = QtWidgets.QTableWidgetItem(file)
                self.tableWidget.setItem(row, 0, newItem)
                row += 1
        if nums:
            row = 0
            for num in nums:
                newItem = QtWidgets.QTableWidgetItem(str(num))
                self.tableWidget.setItem(row, 1, newItem)
                row += 1
        if poss:
            row = 0
            for pos in poss:
                newItem = QtWidgets.QTableWidgetItem(str(pos)[1:-1])
                self.tableWidget.setItem(row, 2, newItem)
                row += 1

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "真退出？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def search(self):
        def word_result(freqs, word):
            result = []
            for word_tuple in freqs:
                temp = {"file": word_tuple[0], "num": 0, "pos": []}
                if " " not in word:
                    for word_and_freq_dict in word_tuple[1]:
                        if word_and_freq_dict["word"] == word:
                            temp["num"] = len(word_and_freq_dict["pos"])
                            temp["pos"] = word_and_freq_dict["pos"]
                else:
                    import KMP
                    pos = KMP.positions(File.File(word_tuple[0]).get_content(), word)
                    temp["num"] = len(pos)
                    temp["pos"] = pos
                result.append(temp)

            def num(result):
                return result["num"]

            result.sort(key=num, reverse=True)
            return result

        self.search_status = self.get_research_content()
        self.statusBar().showMessage(self.get_research_content() + " 的检索结果")
        files = self.get_files_from_table()
        if not self.freqs:
            self.freqs = [(file, File.cal_words_positions(files=[file], reverse=True)) for file in files]
        temp_result = []
        result = []
        for word in self.search_status.split(";"):
            temp_result.append(word_result(self.freqs, word))
        for file in files:
            temp = {"file": file, "num": "", "pos": []}
            for i in temp_result:
                for j in i:
                    if j["file"] == file:
                        temp["num"] += str(j["num"]) + "+"
                        temp["pos"].append(j["pos"])
            result.append(temp)

        def num(result):
            return eval(result["num"][:-1])

        result.sort(key=num, reverse=True)
        self.tableWidget.clear()
        files = []
        nums = []
        poss = []
        for i in result:
            files.append(i["file"])
            nums.append(i["num"][:-1])
            poss.append(i["pos"])
        self.creat_tableWidget(files, nums, poss)

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(str(sender) + ' was pressed')

    def itemClicked(self):
        row = self.tableWidget.currentColumn()
        file = self.tableWidget.item(row, 0).text()
        self.statusBar().showMessage(file)
        item_ui = item_UI(file, self.search_status)
        item_ui.show()
        item_ui.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.effect()
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
