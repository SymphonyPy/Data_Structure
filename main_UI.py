import os
import KMP
import File
import file_UI
from PyQt5 import QtWidgets, QtGui
from Original_Model import main_GUI
from create_file_UI import *
from item_UI import *
from freq_UI import *
from about_UI import *
from progressbar_UI import *
import six.moves.cPickle as pickle


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
        ui_file = file_UI.Ui_FileDialog()
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
        ui_file = file_UI.Ui_FileDialog()
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
