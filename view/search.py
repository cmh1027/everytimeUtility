import view.ui.search as search
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from model.data import Data
from model.config import Config
from view.selectBoardDialog import SelectBoardDialog
import view.detail as Detail

class Search(QtWidgets.QWidget):
    searchOthersEndSignal = pyqtSignal()
    plasterEndSignal = pyqtSignal()
    def __init__(self, window):
        super().__init__()
        self.MainWindow = window
        ui = search.Ui_Form()
        ui.setupUi(self)
        checkbox = self.findChild(QtWidgets.QCheckBox, "allCheckBox")
        nickname = self.findChild(QtWidgets.QLineEdit, "nicknameLineEdit")
        checkbox.stateChanged.connect(lambda: nickname.setEnabled(not checkbox.isChecked()))
        checkbox2 = self.findChild(QtWidgets.QCheckBox, "articlekeywordCheckBox")
        articleKeyword = self.findChild(QtWidgets.QLineEdit, "articlekeywordLineEdit")
        checkbox2.stateChanged.connect(lambda: articleKeyword.setEnabled(checkbox2.isChecked()))
        checkbox3 = self.findChild(QtWidgets.QCheckBox, "commentkeywordCheckBox")
        commentKeyword = self.findChild(QtWidgets.QLineEdit, "commentkeywordLineEdit")
        checkbox3.stateChanged.connect(lambda: commentKeyword.setEnabled(checkbox3.isChecked()))
        self.findChild(QtWidgets.QPushButton, "selectboardButton").clicked.connect(self.selectBoard)
        self.findChild(QtWidgets.QPushButton, "searchButton").clicked.connect(self.startSearch)
        self.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(self.abortSearch)
        self.findChild(QtWidgets.QPushButton, "detailButton").clicked.connect(self.searchedDetail)
        self.findChild(QtWidgets.QPushButton, "savecommentButton").clicked.connect(self.saveComment)
        self.findChild(QtWidgets.QLineEdit, "searchpageLineEdit").setValidator(QtGui.QIntValidator(0, 100000))
        self.findChild(QtWidgets.QLineEdit, "searchpageEndLineEdit").setValidator(QtGui.QIntValidator(0, 100000))
        self.searchOthersEndSignal.connect(self.searchOthersEnd)
        self.plasterEndSignal.connect(self.plasterEnd)
    
    def update(self):
        if not Config.Search.searchingOthers:
            if "article" in Data.others and "comment" in Data.others:
                self.findChild(QtWidgets.QLabel, "infoLabel").setText("글 {}개 / 댓글 {}개".format(len(Data.others["article"]), len(Data.others["comment"])))
            elif "article" in Data.others and "comment" not in Data.others:
                self.findChild(QtWidgets.QLabel, "infoLabel").setText("글 {}개".format(len(Data.others["article"])))
            elif "article" not in Data.others and "comment" in Data.others:
                self.findChild(QtWidgets.QLabel, "infoLabel").setText("댓글 {}개".format(len(Data.others["comment"])))
        btn = self.findChild(QtWidgets.QPushButton, "searchButton")
        if Config.Search.searchingOthers:
            btn.setEnabled(False)
            btn.setText("검색중")
        if Config.Plaster.plastering:
            btn.setEnabled(False)
            btn.setText("도배중")
        

    @pyqtSlot()
    def selectBoard(self):
        SelectBoardDialog(self.MainWindow)

    @pyqtSlot()
    def startSearch(self):
        searchPage = int(self.findChild(QtWidgets.QLineEdit, "searchpageLineEdit").text())
        searchEndPage = int(self.findChild(QtWidgets.QLineEdit, "searchpageEndLineEdit").text())
        searchNickname = self.findChild(QtWidgets.QLineEdit, "nicknameLineEdit").text()
        articleCheckFlag = self.findChild(QtWidgets.QCheckBox, "articleCheckBox").isChecked()
        commentCheckFlag = self.findChild(QtWidgets.QCheckBox, "commentCheckBox").isChecked()
        searchAllFlag = self.findChild(QtWidgets.QCheckBox, "allCheckBox").isChecked()
        articleKeyword = self.findChild(QtWidgets.QLineEdit, "articlekeywordLineEdit").text()
        commentKeyword = self.findChild(QtWidgets.QLineEdit, "commentkeywordLineEdit").text()
        articleKeywordFlag = self.findChild(QtWidgets.QCheckBox, "articlekeywordCheckBox").isChecked()
        commentKeywordFlag = self.findChild(QtWidgets.QCheckBox, "commentkeywordCheckBox").isChecked()
        if not articleCheckFlag and not commentCheckFlag:
            self.MainWindow.messageDialog("error", "글 혹은 댓글 검색 중 적어도 하나를 체크해주세요")
            return
        if len(Config.Search.selectedBoards) == 0:
            self.MainWindow.messageDialog("error", "적어도 하나의 게시판을 체크해주세요")
            return
        if searchPage == 0:
            self.MainWindow.messageDialog("error", "시작 페이지는 1페이지 이상이어야 합니다")
            return
        if searchPage > searchEndPage:
            self.MainWindow.messageDialog("error", "페이지 설정이 잘못되었습니다")
            return
        if searchNickname == "" and not searchAllFlag:
            self.MainWindow.messageDialog("error", "닉네임을 입력해주세요")
            return
        if articleKeyword == "" and articleKeywordFlag:
            self.MainWindow.messageDialog("error", "글 키워드를 입력해주세요")
            return
        if commentKeyword == "" and commentKeywordFlag:
            self.MainWindow.messageDialog("error", "댓글 키워드를 입력해주세요")
            return            
        Data.others = {}
        btn = self.findChild(QtWidgets.QPushButton, "searchButton")
        btn.setEnabled(False)
        btn.setText("검색중")
        Config.Search.searchingOthers = True
        self.MainWindow.addProgressSignal.emit("[System] 검색을 시작합니다")
        option = {}
        option["boards"] = Config.Search.selectedBoards
        option["page"] = searchPage
        option["pageEnd"] = searchEndPage
        option["nickname"] = searchNickname
        option["articleFlag"] = articleCheckFlag
        option["commentFlag"] = commentCheckFlag
        option["all"] = searchAllFlag
        option["articleKeyword"] = articleKeyword
        option["commentKeyword"] = commentKeyword
        option["articleKeywordFlag"] = articleKeywordFlag
        option["commentKeywordFlag"] = commentKeywordFlag
        Config.Search.searchAllFlag = searchAllFlag
        Config.Search.searchNickname = searchNickname
        self.MainWindow.RequestHandle.searchOthers(option)

    @pyqtSlot()
    def abortSearch(self):
        if Config.Search.searchingOthers:
            self.MainWindow.RequestHandle.abortSearch()
            Config.Search.searchingOthers = False
            btn = self.findChild(QtWidgets.QPushButton, "searchButton")
            btn.setEnabled(True)
            btn.setText("검색")
            self.MainWindow.addProgressSignal.emit("[System] 검색이 중지되었습니다")

    @pyqtSlot()
    def searchedDetail(self):
        Detail.OthersDetail(self.MainWindow)

    @pyqtSlot()
    def saveComment(self):
        if "comment" in Data.others:
            comments = list(map(lambda comment:comment["comment"]["text"], Data.others["comment"]))
            Config.Plaster.plasterWord = list(reversed(comments))
            self.MainWindow.messageDialog("ok", "저장되었습니다")
        else:
            self.MainWindow.messageDialog("error", "댓글을 먼저 검색해주세요")

    @pyqtSlot()
    def searchOthersEnd(self):
        self.MainWindow.addProgressSignal.emit("[System] 검색 완료")
        Config.Search.searchingOthers = False
        if self.MainWindow.currentMenu == "search":
            btn = self.findChild(QtWidgets.QPushButton, "searchButton")
            btn.setEnabled(True)
            btn.setText("검색")
            if "article" in Data.others and "comment" in Data.others:
                self.findChild(QtWidgets.QLabel, "infoLabel").setText("글 {}개 / 댓글 {}개".format(len(Data.others["article"]), len(Data.others["comment"])))
            elif "article" in Data.others and "comment" not in Data.others:
                self.findChild(QtWidgets.QLabel, "infoLabel").setText("글 {}개".format(len(Data.others["article"])))
            elif "article" not in Data.others and "comment" in Data.others:
                self.findChild(QtWidgets.QLabel, "infoLabel").setText("댓글 {}개".format(len(Data.others["comment"])))
        elif self.MainWindow.currentMenu == "plaster":
            self.MainWindow.Plaster.searchOthersEndSignal.emit()
    
    @pyqtSlot()
    def plasterEnd(self):
        btn = self.findChild(QtWidgets.QPushButton, "searchButton")
        btn.setEnabled(True)
        btn.setText("검색")
