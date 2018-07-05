import view.loginScreen as loginScreen
import view.loginfailedScreen as loginfailedScreen
import model.widget as widget
from PyQt5 import QtWidgets
from glob import glob
from os.path import splitext
for module in glob('/view/*'):
    name, ext = splitext(module)
    if ext == '.py':
        globals()[name] = __import__("view."+name)
class Render:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
    
    # Never change the name of centralwidget!
    def clear(self):
        self.MainWindow.findChild(QtWidgets.QWidget, "centralwidget").deleteLater()
    
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
    
    def home(self, response):
        pass
