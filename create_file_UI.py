from PyQt5 import QtWidgets
from img import *
from Original_Model import create_file_GUI


class create_file_UI(QtWidgets.QDialog, create_file_GUI.Ui_dialog):
    def __init__(self):
        super(create_file_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def file_pos(self):
        return self.lineEdit.text()
