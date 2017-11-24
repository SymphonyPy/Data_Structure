import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon


class Ui_FileDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '选择需要导入的TXT文档'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        # self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.openFileNameDialog()
        # self.openFileNamesDialog()
        # self.saveFileDialog()
        self.show()

    def openFileNameDialog(self, file_type="TXT Files (*.txt)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择要导入索引文件", "", file_type, options=options)
        if fileName:
            return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "选择要导入的文件", "", "TXT Files (*.txt)", options=options)
        if files:
            return files

    def saveFileDialog(self):
        pass
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
        #                                           "All Files (*);;Text Files (*.txt)", options=options)
        # if fileName:
        #     print(fileName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
