from PyQt5 import QtWidgets
from Original_Model import huffman_GUI


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
