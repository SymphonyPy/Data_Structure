# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_8.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(480, 360)
        dialog.setMinimumSize(QtCore.QSize(480, 360))
        dialog.setMaximumSize(QtCore.QSize(480, 360))
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(160, 20, 160, 160))
        self.label.setMinimumSize(QtCore.QSize(160, 160))
        self.label.setMaximumSize(QtCore.QSize(160, 160))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(dialog)
        self.pushButton.setGeometry(QtCore.QRect(360, 310, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(dialog)
        self.label_2.setGeometry(QtCore.QRect(41, 194, 401, 111))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dialog)
        self.label_3.setGeometry(QtCore.QRect(331, 340, 151, 20))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "关于"))
        self.label.setText(_translate("dialog", "TextLabel"))
        self.pushButton.setText(_translate("dialog", "确定"))
        self.label_2.setText(_translate("dialog",
                                        "<html><head/><body><p align=\"center\">作者：SymPy</p><p align=\"center\">GitHub：https://github.com/SymphonyPy</p><p align=\"center\">邮箱：568603742@qq.com</p><p align=\"center\">个人主页：http://www.sympy.xyz/</p></body></html>"))
        self.label_3.setText(_translate("dialog",
                                        "<html><head/><body><p><span style=\" font-size:6pt;\">点击“确定”承认作者是最帅的！</span></p></body></html>"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())
