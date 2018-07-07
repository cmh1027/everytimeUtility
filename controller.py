from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import model.widget as widget

class Slot(QObject):
    searchEndSignal = pyqtSignal()

    def __init__(self, Mainwindow):
        super().__init__()
        self.MainWindow = Mainwindow
        self.searchEndSignal.connect(self.deleteUpdate)
    
    def searchEnd(self):
        self.searchEndSignal.emit()

    @pyqtSlot()
    def login(self):
        _id = self.MainWindow.findChild(QtWidgets.QLineEdit, "idLineEdit").text()
        password = self.MainWindow.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text()
        _id = "sodlqnf123"
        password = "sodlqnf12"
        response = self.MainWindow.RequestHandle.login(_id, password)
        if response:
            self.MainWindow.Render.home(response)
        else:
            self.MainWindow.Render.loginfailed()
    
    @pyqtSlot(QtWidgets.QDialog)
    def loginfailed(self, dialog):
        dialog.deleteLater()
    
    @pyqtSlot()
    def home_delete(self):
        if self.MainWindow.mine is None: # Not updated
            if self.MainWindow.searching:
                self.MainWindow.Render.loading()
            else:
                self.MainWindow.Render.loading()
                self.MainWindow.searching = True
                progressTextEdit = self.MainWindow.findChild(QtWidgets.QTextEdit, "progressTextEdit")
                text = progressTextEdit.toPlainText()
                progressTextEdit.setText(text+"\n작성 글 및 댓글 검색을 시작합니다")
                self.MainWindow.RequestHandle.getMine()
        else: # updated
            self.MainWindow.Slot.deleteUpdate()
    
    @pyqtSlot()
    def deleteUpdate(self):
        self.MainWindow.searching = False
        self.MainWindow.Render.delete()

    @pyqtSlot()
    def home_plaster(self):
        pass

    @pyqtSlot()
    def home_search(self):
        pass

    @pyqtSlot()
    def home_config(self):
        self.MainWindow.Render.config()
    
    @pyqtSlot()
    def config_save(self):
        self.MainWindow.threadCount = int(self.MainWindow.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").text())
    
    @pyqtSlot()
    def startdelete(self):
        print("hello world")
    
    @pyqtSlot()
    def canceldelete(self):
        print("hello world")

class Signal:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
    
    def bind(self, function, *argv):
        # Every functions must be written in small case letters
        getattr(self, function.lower())(*argv)
        
    def login(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "loginButton").clicked.connect(self.MainWindow.Slot.login)
    
    def loginfailed(self):
        dialog = self.MainWindow.findChild(QtWidgets.QDialog, "loginfailedDialog")
        dialog.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(lambda: self.MainWindow.Slot.loginfailed(dialog))
    
    def home(self):
        self.MainWindow.findChild(QtWidgets.QToolButton, "deleteButton").clicked.connect(self.MainWindow.Slot.home_delete)
        self.MainWindow.findChild(QtWidgets.QToolButton, "plasterButton").clicked.connect(self.MainWindow.Slot.home_plaster)
        self.MainWindow.findChild(QtWidgets.QToolButton, "searchButton").clicked.connect(self.MainWindow.Slot.home_search)
        self.MainWindow.findChild(QtWidgets.QToolButton, "configButton").clicked.connect(self.MainWindow.Slot.home_config)

    def home_delete(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "deleteButton").clicked.connect(self.MainWindow.Slot.startdelete)
        self.MainWindow.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(self.MainWindow.Slot.canceldelete)
    
    def home_plaster(self):
        pass

    def home_search(self):
        pass

    def home_config(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "saveButton").clicked.connect(self.MainWindow.Slot.config_save)