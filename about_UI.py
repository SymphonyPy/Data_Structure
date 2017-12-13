from PyQt5 import QtWidgets, QtCore, QtGui
from img import *
from Original_Model import about_GUI


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
