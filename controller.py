from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from requesthandle import RequestHandle
import model.widget as widget

class Slot(QObject):
    def __init__(self, Mainwindow):
        super().__init__()
        self.MainWindow = Mainwindow
        self.req = self.MainWindow.req
    
    @pyqtSlot()
    def login(self):
        _id = self.MainWindow.findChild(QtWidgets.QLineEdit, "idLineEdit").text()
        password = self.MainWindow.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text()
        result = RequestHandle.login(self.req, _id, password)
        if result:
            print("로그인 성공")
        else:
            self.MainWindow.Render.loginfailed()
    
    @pyqtSlot(QtWidgets.QDialog)
    def loginfailed(self, dialog):
        dialog.deleteLater()

class Signal:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
    
    def bind(self, function):
        # Every functions must be written in small case letters
        getattr(self, function.lower())()
        
    def login(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "loginButton").clicked.connect(self.MainWindow.Slot.login)
    
    def loginfailed(self):
        dialog = self.MainWindow.findChild(QtWidgets.QDialog, "loginfailedDialog")
        dialog.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(lambda: self.MainWindow.Slot.loginfailed(dialog))