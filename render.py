import model.widget as widget
from PyQt5 import QtWidgets
from glob import glob
from os.path import splitext, basename
from importlib import import_module
from bs4 import BeautifulSoup
for module in glob('view/*'):
    name, ext = splitext(module)
    name = basename(name)
    if ext == '.py':
        globals()[name] = import_module("view.{}".format(name))

def window_clear(function):
    def wrapper(*args):
        args[0].clear() # self.clear()
        return function(*args)
    return wrapper

def content_clear(function):
    def wrapper(*args):
        args[0].clearContent() # self.clearContent()
        function(*args)
        for child in args[0].MainWindow.findChild(QtWidgets.QWidget, "Form").findChildren(QtWidgets.QWidget):
            child.show()
    return wrapper

class Render:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow

    # Never change the name of centralwidget!
    def clear(self):
        centralwidget = self.MainWindow.findChild(QtWidgets.QWidget, "centralwidget")
        if centralwidget is not None:
            centralwidget.deleteLater()

    def clearContent(self):
        contents = self.MainWindow.findChild(QtWidgets.QWidget, "Form").findChildren(QtWidgets.QWidget)
        for content in contents:
            content.setParent(None)

    @window_clear
    def login(self):
        ui = loginScreen.Ui_MainWindow()
        ui.setupUi(self.MainWindow)
        self.MainWindow.Signal.bind("login")
    
    @window_clear
    def loginfailed(self):
        Dialog = QtWidgets.QDialog(self.MainWindow)
        Dialog.setModal(True)
        ui = loginfailedScreen.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.setObjectName("loginfailedDialog")
        Dialog.show()
        self.MainWindow.Signal.bind("loginfailed")
    
    @window_clear
    def home(self, response):
        ui = mainScreen.Ui_MainWindow()
        ui.setupUi(self.MainWindow)
        soup = BeautifulSoup(response, 'html.parser')
        self.MainWindow.findChild(QtWidgets.QLabel, "univLabel").setText(soup.find("span", {"class":"subname"}).getText())
        self.MainWindow.findChild(QtWidgets.QLabel, "nicknameLabel").setText(soup.find("p", {"class":"nickname"}).getText())
        self.MainWindow.findChild(QtWidgets.QLabel, "nameLabel").setText(soup.find("p", {"class":"school"}).getText())
        self.MainWindow.Signal.bind("home")

    @content_clear
    def delete(self):
        ui = delete.Ui_Form()
        Form = self.MainWindow.findChild(QtWidgets.QWidget, "Form")
        ui.setupUi(Form)
        self.MainWindow.findChild(QtWidgets.QLabel, "writeLabel").setText("글 {}개 / 덧글 {}개".format(len(self.MainWindow.mine["article"]), len(self.MainWindow.mine["comment"])))
        self.MainWindow.Signal.bind("home_delete")

    @content_clear
    def config(self):
        ui = configuration.Ui_Form()
        Form = self.MainWindow.findChild(QtWidgets.QWidget, "Form")
        ui.setupUi(Form)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").setText(str(self.MainWindow.threadCount))
        self.MainWindow.Signal.bind("home_config")

    @content_clear
    def loading(self):
        ui = loading.Ui_Form()
        Form = self.MainWindow.findChild(QtWidgets.QWidget, "Form")
        ui.setupUi(Form)