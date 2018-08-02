import view.ui.plaster as plaster
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from model.data import Data
from model.config import Config
from view.selectBoardDialog import SelectBoardDialog
from view.plasterWordDialog import PlasterWordDialog

class Plaster(QtWidgets.QWidget):
    searchOthersEndSignal = pyqtSignal()
    plasterEndSignal = pyqtSignal()
    def __init__(self, window):
        super().__init__()
        self.MainWindow = window
        ui = plaster.Ui_Form()
        ui.setupUi(self)
        self.searchOthersEndSignal.connect(self.searchOthersEnd)
        self.plasterEndSignal.connect(self.plasterEnd)
        self.findChild(QtWidgets.QPushButton, "selectboardButton").clicked.connect(self.selectBoard)
        self.findChild(QtWidgets.QPushButton, "plasterWordButton").clicked.connect(self.plasterWord)
        self.findChild(QtWidgets.QPushButton, "startplatsterButton").clicked.connect(self.startPlaster)
        self.findChild(QtWidgets.QPushButton, "cancelplasterButton").clicked.connect(self.abortPlaster)
        self.findChild(QtWidgets.QLineEdit, "iterationLineEdit").setValidator(QtGui.QIntValidator(0, 10000))
        self.findChild(QtWidgets.QLineEdit, "retryLineEdit").setValidator(QtGui.QIntValidator(0, 100))
    
    def update(self):
        btn = self.findChild(QtWidgets.QPushButton, "startplatsterButton")
        if Config.Search.searchAllFlag:
            self.findChild(QtWidgets.QLabel, "searchednicknameLabel").setText("모두")
        else:
            if Config.Search.searchNickname == "":
                self.findChild(QtWidgets.QLabel, "searchednicknameLabel").setText("검색되지 않음")
                btn.setEnabled(False)
                btn.setText("Go!")
            else:
                self.findChild(QtWidgets.QLabel, "searchednicknameLabel").setText(Config.Search.searchNickname)
        if Config.Search.searchingOthers:
            btn.setEnabled(False)
            btn.setText("검색중")
        if Config.Plaster.plastering:
            btn.setEnabled(False)
            btn.setText("도배중")
    
    def searchOthersEnd(self):
        btn = self.findChild(QtWidgets.QPushButton, "startplatsterButton")
        btn.setEnabled(True)
        btn.setText("Go!")
        self.findChild(QtWidgets.QLabel, "searchednicknameLabel").setText(Config.Search.searchNickname)
        if "article" not in Data.others:
            self.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setChecked(False)
            self.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setEnabled(False)
        else:
            self.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setChecked(True)
            self.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setEnabled(True)            
        if "comment" not in Data.others:
            self.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setChecked(False)
            self.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setEnabled(False)
        else:
            self.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setChecked(True)
            self.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setEnabled(True)      

    @pyqtSlot()
    def selectBoard(self):
        SelectBoardDialog(self.MainWindow)

    @pyqtSlot()
    def plasterWord(self):
        PlasterWordDialog(self.MainWindow)

    @pyqtSlot()
    def startPlaster(self):
        articlePlasterFlag = self.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").isChecked()
        commentPlasterFlag = self.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").isChecked()       
        promptRemoveFlag = self.findChild(QtWidgets.QCheckBox, "promptremoveCheckBox").isChecked()  
        isAnonymFlag = self.findChild(QtWidgets.QCheckBox, "isanonymFlag").isChecked()
        plasterIteration = int(self.findChild(QtWidgets.QLineEdit, "iterationLineEdit").text())
        plasterRetry = int(self.findChild(QtWidgets.QLineEdit, "retryLineEdit").text())
        articleCycleFlag = self.findChild(QtWidgets.QRadioButton, "articleRadioButton").isChecked()
        if not articlePlasterFlag and not commentPlasterFlag:
            self.MainWindow.messageDialog("error", "글 혹은 댓글 도배 중 적어도 하나를 체크해주세요")
            return
        if len(Config.Plaster.plasterBoards) == 0:
            self.MainWindow.messageDialog("error", "적어도 하나의 게시판을 체크해주세요")
            return
        if len(Config.Plaster.plasterWord) == 0:
            self.MainWindow.messageDialog("error", "도배에 사용할 문자열을 적어주세요")
            return
        if plasterIteration == 0:
            self.MainWindow.messageDialog("error", "반복 횟수는 1 이상이어야 합니다")
            return
        option = {}
        option["articleFlag"] = articlePlasterFlag
        option["commentFlag"] = commentPlasterFlag
        option["delete"] = promptRemoveFlag
        option["anonym"] = isAnonymFlag
        option["iteration"] = plasterIteration
        option["plasterWord"] = list(Config.Plaster.plasterWord)
        option["retry"] = plasterRetry
        option["interval"] = Config.Plaster.plasterInterval
        option["articleCycle"] = articleCycleFlag
        if "article" in Data.others:
            option["article"] = list(filter(lambda article:article["board"] in \
            Config.Plaster.plasterBoards.values(), Data.others["article"]))
            if len(option["article"]) == 0:
                self.MainWindow.messageDialog("error", "검색된 글이 없습니다")
                return
        if "comment" in Data.others:
            option["comment"] = list(filter(lambda comment:comment["board"] in \
            Config.Plaster.plasterBoards.values(), Data.others["comment"]))
            if len(option["comment"]) == 0:
                self.MainWindow.messageDialog("error", "검색된 댓글이 없습니다")
                return
        Config.Plaster.plastering = True
        btn = self.findChild(QtWidgets.QPushButton, "startplatsterButton")
        btn.setEnabled(False)
        btn.setText("도배중")
        self.MainWindow.addProgressSignal.emit("[System] 도배를 시작합니다")
        self.MainWindow.RequestHandle.plaster(option)

    @pyqtSlot()
    def abortPlaster(self):
        if Config.Plaster.plastering:
            self.MainWindow.RequestHandle.abortPlaster()
            Config.Plaster.plastering = False
            btn = self.findChild(QtWidgets.QPushButton, "startplatsterButton")
            btn.setEnabled(True)
            btn.setText("Go!")
            self.MainWindow.addProgressSignal.emit("[System] 도배를 중지합니다")

    @pyqtSlot()
    def plasterEnd(self):
        self.MainWindow.addProgressSignal.emit("[System] 도배 완료")
        Config.Plaster.plastering = False
        if self.MainWindow.currentMenu == "search":
            self.MainWindow.Search.plasterEndSignal.emit()
        elif self.MainWindow.currentMenu == "plaster":
            btn = self.findChild(QtWidgets.QPushButton, "startplatsterButton")
            btn.setEnabled(True)
            btn.setText("Go!")
            self.enableButton(btn, "Go!")

    
