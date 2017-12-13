from main_UI import *
from SplashScreen import *
import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = SplashScreen()
    splash.effect()
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
