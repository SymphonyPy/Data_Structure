from PyQt5 import QtWidgets, QtCore
from img import *
from Original_Model import progressbar_GUI


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
