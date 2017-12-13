from PyQt5 import QtWidgets, QtCore
from img import *
from Original_Model import huffman_GUI


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
