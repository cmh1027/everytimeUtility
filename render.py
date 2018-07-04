import view.loginScreen as loginScreen
import view.loginfailedScreen as loginfailedScreen
import model.widget as widget
from controller import Signal
from PyQt5 import QtWidgets
class Render:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow

    def login(self):
        ui = loginScreen.Ui_MainWindow()
        ui.setupUi(self.MainWindow)
        self.MainWindow.Signal.bind("login")
    
    def loginfailed(self):
        Dialog = QtWidgets.QDialog(self.MainWindow)
        Dialog.setModal(True)
        ui = loginfailedScreen.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.setObjectName("loginfailedDialog")
        Dialog.show()
        self.MainWindow.Signal.bind("loginfailed")