from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from bs4 import BeautifulSoup
import view.loginScreen as loginScreen
import view.mainScreen as mainScreen
from view.configuration import Configuration
from view.delete import Delete
from view.search import Search
from view.plaster import Plaster
from view.loading import Loading
from view.messageDialog import MessageDialog
from model.data import Data
from model.config import Config
from module.requesthandle import RequestHandle

class Window(QtWidgets.QMainWindow):
    addProgressSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.RequestHandle = RequestHandle(self)
        self.addProgressSignal.connect(self.addProgress)
        self.initialize()
        self.loginScreen()
        
    def initialize(self):
        Data.initialize()
        Config.initialize()
        self.Delete = None
        self.Search = None
        self.Plaster = None
        self.Config = None
        self.currentMenu = None

    
    def clear(self):
        centralWidget = self.findChild(QtWidgets.QWidget, "centralwidget")
        if centralWidget is not None: 
            centralWidget.deleteLater()

    def loginScreen(self):
        self.clear()
        ui = loginScreen.Ui_MainWindow()
        ui.setupUi(self)
        self.findChild(QtWidgets.QPushButton, "loginButton").clicked.connect(self.login)

    @pyqtSlot()
    def login(self):
        _id = self.findChild(QtWidgets.QLineEdit, "idLineEdit").text()
        password = self.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text()
        response = self.RequestHandle.login(_id, password)
        if response:
            self.mainScreen(response)
            Data.boards = self.RequestHandle.extractBoards(response)
        else:
            self.messageDialog("failed", "아이디나 비밀번호를 바르게 입력해주세요")

    def mainScreen(self, response):
        self.clear()
        ui = mainScreen.Ui_MainWindow()
        ui.setupUi(self)
        soup = BeautifulSoup(response, 'html.parser')
        self.findChild(QtWidgets.QLabel, "univLabel").setText(soup.find("span", {"class":"subname"}).getText())
        self.findChild(QtWidgets.QLabel, "nicknameLabel").setText(soup.find("p", {"class":"nickname"}).getText())
        self.findChild(QtWidgets.QLabel, "nameLabel").setText(soup.find("p", {"class":"school"}).getText())

        self.findChild(QtWidgets.QToolButton, "deleteButton").clicked.connect(self.deleteMenu)
        self.findChild(QtWidgets.QToolButton, "searchButton").clicked.connect(self.searchMenu)
        self.findChild(QtWidgets.QToolButton, "plasterButton").clicked.connect(self.plasterMenu)
        self.findChild(QtWidgets.QToolButton, "configButton").clicked.connect(self.configMenu)
        self.findChild(QtWidgets.QToolButton, "logoutButton").clicked.connect(self.logout)
        self.findChild(QtWidgets.QPushButton, "eraseButton").clicked.connect(self.eraseProgress)

        #
        stackedWidget = self.findChild(QtWidgets.QStackedWidget, "Form")
        self.Delete = Delete(self)
        stackedWidget.addWidget(self.Delete)
        self.Search = Search(self)
        stackedWidget.addWidget(self.Search)
        self.Plaster = Plaster(self)
        stackedWidget.addWidget(self.Plaster)
        self.Configuration = Configuration(self)
        stackedWidget.addWidget(self.Configuration)
        stackedWidget.addWidget(Loading())
        self.deleteMenu()

    def messageDialog(self, title, content):
        MessageDialog(self, title, content)

    @pyqtSlot()
    def deleteMenu(self):
        self.currentMenu = "delete"
        if Data.mine is None: # Not updated
            if Config.Search.searchingMine:
                self.loading()
            else:
                self.loading()
                Config.Search.searchingMine = True
                self.addProgressSignal.emit("[System] 작성 글 및 댓글 검색을 시작합니다")
                self.RequestHandle.getMine()
        else: # updated
            self.deleteScreen()
    
    def deleteScreen(self):
        self.Delete.update()
        self.findChild(QtWidgets.QStackedWidget, "Form").setCurrentIndex(0)

    @pyqtSlot()
    def searchMenu(self):
        self.currentMenu = "search"
        self.searchScreen()

    def searchScreen(self):
        self.Search.update()
        self.findChild(QtWidgets.QStackedWidget, "Form").setCurrentIndex(1)

    @pyqtSlot()
    def plasterMenu(self):
        self.currentMenu = "plaster"
        self.plasterScreen()

    def plasterScreen(self):
        self.Plaster.update()
        self.findChild(QtWidgets.QStackedWidget, "Form").setCurrentIndex(2)

    @pyqtSlot()
    def configMenu(self):
        self.currentMenu = "config"
        self.configScreen()

    def configScreen(self):
        self.findChild(QtWidgets.QStackedWidget, "Form").setCurrentIndex(3)
    
    def loading(self):
        self.findChild(QtWidgets.QStackedWidget, "Form").setCurrentIndex(4)

    @pyqtSlot()
    def logout(self):
        self.RequestHandle.abortDelete()
        self.RequestHandle.abortSearch()
        self.RequestHandle.abortPlaster()
        self.RequestHandle.logout()
        self.initialize()
        self.loginScreen()

    @pyqtSlot()
    def eraseProgress(self):
        progressTextEdit = self.findChild(QtWidgets.QTextEdit, "progressTextEdit")
        progressTextEdit.setText("")
    
    @pyqtSlot(str)
    def addProgress(self, string):
        progressTextEdit = self.findChild(QtWidgets.QTextEdit, "progressTextEdit")
        text = progressTextEdit.toPlainText()
        progressTextEdit.setText(text+string+"\n")