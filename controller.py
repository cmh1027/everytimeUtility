from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Slot(QObject):
    searchMineEndSignal = pyqtSignal()
    searchOthersEndSignal = pyqtSignal()
    deleteEndSignal = pyqtSignal()
    plasterEndSignal = pyqtSignal()
    addProgressSignal = pyqtSignal(str)

    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.searchMineEndSignal.connect(self.searchMineEnd)
        self.searchOthersEndSignal.connect(self.searchOthersEnd)
        self.deleteEndSignal.connect(self.deleteEnd)
        self.plasterEndSignal.connect(self.plasterEnd)
        self.addProgressSignal.connect(self.addProgress)
    
    @pyqtSlot(str)
    def addProgress(self, string):
        self.MainWindow.Render.addTextEdit(string)
    
    @pyqtSlot()
    def eraseProgress(self):
        self.MainWindow.Render.eraseTextEdit()

    @pyqtSlot()
    def login(self):
        _id = self.MainWindow.findChild(QtWidgets.QLineEdit, "idLineEdit").text()
        password = self.MainWindow.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text()
        response = self.MainWindow.RequestHandle.login(_id, password)
        if response:
            self.MainWindow.Render.home(response)
            self.MainWindow.boards = self.MainWindow.RequestHandle.extractBoards(response)
        else:
            self.MainWindow.Render.messageDialog("failed", "아이디나 비밀번호를 바르게 입력해주세요")

    @pyqtSlot()
    def logout(self):
        self.MainWindow.RequestHandle.logout()
        self.MainWindow.initialize()
        self.MainWindow.Render.login()
           
    @pyqtSlot()
    def deleteMenu(self):
        self.MainWindow.currentMenu = "delete"
        if self.MainWindow.mine is None: # Not updated
            if self.MainWindow.searchingMine:
                self.MainWindow.Render.loading()
            else:
                self.MainWindow.Render.loading()
                self.MainWindow.searchingMine = True
                self.MainWindow.Render.addTextEdit("[System] 작성 글 및 댓글 검색을 시작합니다")
                self.MainWindow.RequestHandle.getMine()
        else: # updated
            self.MainWindow.Render.delete()
    
    @pyqtSlot()
    def searchMineEnd(self):
        self.MainWindow.Render.addTextEdit("[System] 검색 완료")
        self.MainWindow.searchingMine = False
        self.MainWindow.Render.delete()

    @pyqtSlot()
    def deleteEnd(self):
        self.MainWindow.Render.addTextEdit("[System] 삭제 완료")
        self.MainWindow.deleting = False
        if self.MainWindow.currentMenu == "delete":
            btn = self.MainWindow.findChild(QtWidgets.QPushButton, "deleteButton")
            self.MainWindow.Render.enableButton(btn, "삭제")
            self.mineRefresh()

    @pyqtSlot()
    def mineRefresh(self):
        self.MainWindow.mine = None
        self.deleteMenu()

    @pyqtSlot()
    def plasterMenu(self):
        self.MainWindow.currentMenu = "plaster"
        self.MainWindow.Render.plaster()

    @pyqtSlot()
    def searchMenu(self):
        self.MainWindow.currentMenu = "search"
        self.MainWindow.Render.search()

    @pyqtSlot()
    def configMenu(self):
        self.MainWindow.currentMenu = "config"
        self.MainWindow.Render.config()
    
    @pyqtSlot()
    def configSave(self):
        threadCount = int(self.MainWindow.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").text())
        if threadCount == 0:
            self.MainWindow.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").setText("1")
            threadCount = 1
        self.MainWindow.threadCount = threadCount
        self.MainWindow.printIdFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "printidCheckBox").isChecked()
        self.MainWindow.printTextFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "printtextCheckBox").isChecked()
        self.MainWindow.printOriginFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "printoriginCheckBox").isChecked()
        self.MainWindow.printBoardSearchEndFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "printboardsearchendCheckBox").isChecked()
        plasterInterval = int(self.MainWindow.findChild(QtWidgets.QLineEdit, "plasterintervalLineEdit").text())
        if plasterInterval == 0:
            self.MainWindow.Render.messageDialog("failed", "도배 간격은 0초가 될 수 없습니다")
            return
        else:
            self.MainWindow.plasterInterval = plasterInterval
        self.MainWindow.printPlasterFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "printplasterCheckBox").isChecked()
        self.MainWindow.Render.messageDialog("save", "저장되었습니다")

    @pyqtSlot()
    def startDelete(self):
        articleFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "articleCheckBox").isChecked()
        commentFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "commentCheckBox").isChecked()
        minlikeFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "minlikeCheckBox").isChecked()
        mincommentFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "mincommentCheckBox").isChecked()
        scope = self.MainWindow.findChild(QtWidgets.QComboBox, "dateComboBox").currentText()
        minlike = self.MainWindow.findChild(QtWidgets.QLineEdit, "minlikeLineEdit").text()
        mincomment = self.MainWindow.findChild(QtWidgets.QLineEdit, "mincommentLineEdit").text()
        if not articleFlag and not commentFlag:
            self.MainWindow.Render.messageDialog("error", "글 혹은 댓글 삭제 중 적어도 하나를 체크해주세요")
            return
        if minlikeFlag and minlike == "":
            self.MainWindow.Render.messageDialog("error", "공감 제한 개수를 입력해주세요")
            return
        if mincommentFlag and mincomment == "":
            self.MainWindow.Render.messageDialog("error", "댓글 제한 개수를 입력해주세요")
            return
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "deleteButton")
        self.MainWindow.Render.disableButton(btn, "삭제중")
        option = {}
        option["articleFlag"] = articleFlag
        option["commentFlag"] = commentFlag
        option["minlikeFlag"] = minlikeFlag
        option["mincommentFlag"] = mincommentFlag
        option["scope"] = scope
        option["minlike"] = minlike
        option["mincomment"] = mincomment
        option["excludeWord"] = self.MainWindow.excludeWord
        option["excludeArticleFlag"] = self.MainWindow.excludeArticleFlag
        option["excludeCommentFlag"] = self.MainWindow.excludeCommentFlag
        self.MainWindow.deleting = True
        self.MainWindow.Render.addTextEdit("[System] 삭제를 시작합니다")
        self.MainWindow.RequestHandle.deleteMine(option)

    @pyqtSlot()
    def abortDelete(self):
        if self.MainWindow.deleting:
            self.MainWindow.RequestHandle.abortDelete()
            self.MainWindow.deleting = False
            self.MainWindow.Render.addTextEdit("[System] 삭제가 중지되었습니다")
            self.mineRefresh()

    @pyqtSlot()
    def excludeWord(self):
        self.MainWindow.Render.excludeWord()
    
    @pyqtSlot()
    def saveExcludeWord(self, dialog):
        self.MainWindow.excludeWord = dialog.findChild(QtWidgets.QTextEdit, "excludewordTextEdit").toPlainText().split("\n")
        self.MainWindow.excludeArticleFlag = dialog.findChild(QtWidgets.QCheckBox, "excludearticleCheckBox").isChecked()
        self.MainWindow.excludeCommentFlag = dialog.findChild(QtWidgets.QCheckBox, "excludecommentCheckBox").isChecked()
        dialog.deleteLater()

    @pyqtSlot()
    def cancelDialog(self, dialog):
        dialog.deleteLater()

    @pyqtSlot()
    def selectBoard(self):
        self.MainWindow.Render.selectBoard()
    
    @pyqtSlot()
    def saveSelectBoard(self, dialog):
        checkboxes = dialog.findChildren(QtWidgets.QCheckBox)
        checkboxes = list(filter(lambda checkbox:checkbox.isChecked(), checkboxes))
        if self.MainWindow.currentMenu == "search":
            self.MainWindow.selectedBoards.clear()
            for checkbox in checkboxes:
                self.MainWindow.selectedBoards[checkbox.text()] = self.MainWindow.boards[checkbox.text()]
        elif self.MainWindow.currentMenu == "plaster":
            self.MainWindow.plasterBoards.clear()
            for checkbox in checkboxes:
                self.MainWindow.plasterBoards[checkbox.text()] = self.MainWindow.boards[checkbox.text()]

    @pyqtSlot()
    def startSearch(self):
        searchPage = int(self.MainWindow.findChild(QtWidgets.QLineEdit, "searchpageLineEdit").text())
        searchEndPage = int(self.MainWindow.findChild(QtWidgets.QLineEdit, "searchpageEndLineEdit").text())
        searchNickname = self.MainWindow.findChild(QtWidgets.QLineEdit, "nicknameLineEdit").text()
        articleCheckFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "articleCheckBox").isChecked()
        commentCheckFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "commentCheckBox").isChecked()
        searchAllFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "allCheckBox").isChecked()
        articleKeyword = self.MainWindow.findChild(QtWidgets.QLineEdit, "articlekeywordLineEdit").text()
        commentKeyword = self.MainWindow.findChild(QtWidgets.QLineEdit, "commentkeywordLineEdit").text()
        articleKeywordFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "articlekeywordCheckBox").isChecked()
        commentKeywordFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "commentkeywordCheckBox").isChecked()
        if not articleCheckFlag and not commentCheckFlag:
            self.MainWindow.Render.messageDialog("error", "글 혹은 댓글 검색 중 적어도 하나를 체크해주세요")
            return
        if len(self.MainWindow.selectedBoards) == 0:
            self.MainWindow.Render.messageDialog("error", "적어도 하나의 게시판을 체크해주세요")
            return
        if searchPage == 0:
            self.MainWindow.Render.messageDialog("error", "시작 페이지는 1페이지 이상이어야 합니다")
            return
        if searchPage > searchEndPage:
            self.MainWindow.Render.messageDialog("error", "페이지 설정이 잘못되었습니다")
            return
        if searchNickname == "" and not searchAllFlag:
            self.MainWindow.Render.messageDialog("error", "닉네임을 입력해주세요")
            return
        if articleKeyword == "" and articleKeywordFlag:
            self.MainWindow.Render.messageDialog("error", "글 키워드를 입력해주세요")
            return
        if commentKeyword == "" and commentKeywordFlag:
            self.MainWindow.Render.messageDialog("error", "댓글 키워드를 입력해주세요")
            return            
        self.MainWindow.searchPage = searchPage
        self.MainWindow.searchEndPage = searchEndPage
        self.MainWindow.searchNickname = searchNickname
        self.MainWindow.articleCheckFlag = articleCheckFlag
        self.MainWindow.commentCheckFlag = commentCheckFlag
        self.MainWindow.searchAllFlag = searchAllFlag
        self.MainWindow.others = {}
        self.MainWindow.articleKeyword = articleKeyword
        self.MainWindow.commentKeyword = commentKeyword
        self.MainWindow.articleKeywordFlag = articleKeywordFlag
        self.MainWindow.commentKeywordFlag = commentKeywordFlag
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "searchButton")
        self.MainWindow.Render.disableButton(btn, "검색중")
        self.MainWindow.searchingOthers = True
        self.MainWindow.Render.addTextEdit("[System] 검색을 시작합니다")
        option = {}
        option["boards"] = self.MainWindow.selectedBoards
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
        self.MainWindow.RequestHandle.searchOthers(option)

    @pyqtSlot()
    def abortSearch(self):
        if self.MainWindow.searchingOthers:
            self.MainWindow.RequestHandle.abortSearch()
            self.MainWindow.searchingOthers = False
            btn = self.MainWindow.findChild(QtWidgets.QPushButton, "searchButton")
            self.MainWindow.Render.enableButton(btn, "검색")
            self.MainWindow.Render.addTextEdit("[System] 검색이 중지되었습니다")

    @pyqtSlot()
    def searchedDetail(self):
        self.MainWindow.Render.searchedDetail()

    @pyqtSlot()
    def mineDetail(self):
        self.MainWindow.Render.mineDetail()

    @pyqtSlot()
    def saveComment(self):
        if "comment" in self.MainWindow.others:
            comments = list(map(lambda comment:comment["comment"]["text"], self.MainWindow.others["comment"]))
            self.MainWindow.plasterWord = list(reversed(comments))
            self.MainWindow.Render.messageDialog("ok", "저장되었습니다")
        else:
            self.MainWindow.Render.messageDialog("error", "댓글을 먼저 검색해주세요")

    @pyqtSlot()
    def searchOthersEnd(self):
        self.MainWindow.Render.addTextEdit("[System] 검색 완료")
        self.MainWindow.searchingOthers = False
        if self.MainWindow.currentMenu == "search":
            self.MainWindow.Render.searchOthersEnd()
        elif self.MainWindow.currentMenu == "plaster":
            self.MainWindow.Render.searchOthersEndPlaster()

    @pyqtSlot()
    def plasterWord(self):
        self.MainWindow.Render.plasterWord()

    @pyqtSlot()
    def savePlasterWord(self, dialog):
        plasterWord = dialog.findChild(QtWidgets.QTextEdit, "plasterwordTextEdit").toPlainText().split("\n")
        plasterWord = list(map(lambda word:word.strip(), list(filter(lambda word:word!='', plasterWord))))
        self.MainWindow.plasterWord = plasterWord
        dialog.deleteLater()
    
    @pyqtSlot()
    def startPlaster(self):
        articlePlasterFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").isChecked()
        commentPlasterFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").isChecked()       
        promptRemoveFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "promptremoveCheckBox").isChecked()  
        isAnonymFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "isanonymFlag").isChecked()
        plasterIteration = int(self.MainWindow.findChild(QtWidgets.QLineEdit, "iterationLineEdit").text())
        plasterRetry = int(self.MainWindow.findChild(QtWidgets.QLineEdit, "retryLineEdit").text())
        articleCycleFlag = self.MainWindow.findChild(QtWidgets.QRadioButton, "articleRadioButton").isChecked()
        if not articlePlasterFlag and not commentPlasterFlag:
            self.MainWindow.Render.messageDialog("error", "글 혹은 댓글 도배 중 적어도 하나를 체크해주세요")
            return
        if len(self.MainWindow.plasterBoards) == 0:
            self.MainWindow.Render.messageDialog("error", "적어도 하나의 게시판을 체크해주세요")
            return
        if len(self.MainWindow.plasterWord) == 0:
            self.MainWindow.Render.messageDialog("error", "도배에 사용할 문자열을 적어주세요")
            return
        if plasterIteration == 0:
            self.MainWindow.Render.messageDialog("error", "반복 횟수는 1 이상이어야 합니다")
            return
        option = {}
        option["articleFlag"] = articlePlasterFlag
        option["commentFlag"] = commentPlasterFlag
        option["delete"] = promptRemoveFlag
        option["anonym"] = isAnonymFlag
        option["iteration"] = plasterIteration
        option["plasterWord"] = list(self.MainWindow.plasterWord)
        option["retry"] = plasterRetry
        option["interval"] = self.MainWindow.plasterInterval
        option["articleCycle"] = articleCycleFlag
        if "article" in self.MainWindow.others:
            option["article"] = list(filter(lambda article:article["board"] in \
            self.MainWindow.plasterBoards.values(), self.MainWindow.others["article"]))
            if len(option["article"]) == 0:
                self.MainWindow.Render.messageDialog("error", "검색된 글이 없습니다")
                return
        if "comment" in self.MainWindow.others:
            option["comment"] = list(filter(lambda comment:comment["board"] in \
            self.MainWindow.plasterBoards.values(), self.MainWindow.others["comment"]))
            if len(option["comment"]) == 0:
                self.MainWindow.Render.messageDialog("error", "검색된 댓글이 없습니다")
                return
        self.MainWindow.plastering = True
        self.MainWindow.articlePlasterFlag = articlePlasterFlag
        self.MainWindow.commentPlasterFlag = commentPlasterFlag
        self.MainWindow.promptRemoveFlag = promptRemoveFlag
        self.MainWindow.isAnonymFlag = isAnonymFlag
        self.MainWindow.plasterIteration = plasterIteration
        self.MainWindow.articleCycleFlag = articleCycleFlag
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "startplatsterButton")
        self.MainWindow.Render.disableButton(btn, "도배중")
        self.MainWindow.Render.addTextEdit("[System] 도배를 시작합니다")
        self.MainWindow.RequestHandle.plaster(option)


    @pyqtSlot()
    def abortPlaster(self):
        if self.MainWindow.plastering:
            self.MainWindow.RequestHandle.abortPlaster()
            self.MainWindow.plastering = False
            btn = self.MainWindow.findChild(QtWidgets.QPushButton, "startplatsterButton")
            self.MainWindow.Render.enableButton(btn, "Go!")
            self.MainWindow.Render.addTextEdit("[System] 도배를 중지합니다")

    @pyqtSlot()
    def plasterEnd(self):
        self.MainWindow.Render.addTextEdit("[System] 도배 완료")
        self.MainWindow.plastering = False
        if self.MainWindow.currentMenu == "search":
            self.MainWindow.Render.plasterEndSearch()
        elif self.MainWindow.currentMenu == "plaster":
            self.MainWindow.Render.plasterEnd()

class Signal:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
    
    def bind(self, function, *argv):
        getattr(self, function)(*argv)
        
    def login(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "loginButton").clicked.connect(self.MainWindow.Slot.login)
    
    def loginfailed(self, dialog):
        dialog.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(lambda: self.MainWindow.Slot.loginfailed(dialog))
    
    def home(self):
        self.MainWindow.findChild(QtWidgets.QToolButton, "deleteButton").clicked.connect(self.MainWindow.Slot.deleteMenu)
        self.MainWindow.findChild(QtWidgets.QToolButton, "searchButton").clicked.connect(self.MainWindow.Slot.searchMenu)
        self.MainWindow.findChild(QtWidgets.QToolButton, "plasterButton").clicked.connect(self.MainWindow.Slot.plasterMenu)
        self.MainWindow.findChild(QtWidgets.QToolButton, "configButton").clicked.connect(self.MainWindow.Slot.configMenu)
        self.MainWindow.findChild(QtWidgets.QToolButton, "logoutButton").clicked.connect(self.MainWindow.Slot.logout)
        self.MainWindow.findChild(QtWidgets.QPushButton, "eraseButton").clicked.connect(self.MainWindow.Slot.eraseProgress)
    
    def deleteMenu(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "deleteButton").clicked.connect(self.MainWindow.Slot.startDelete)
        self.MainWindow.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(self.MainWindow.Slot.abortDelete)
        self.MainWindow.findChild(QtWidgets.QPushButton, "refreshButton").clicked.connect(self.MainWindow.Slot.mineRefresh)
        self.MainWindow.findChild(QtWidgets.QPushButton, "detailButton").clicked.connect(self.MainWindow.Slot.mineDetail)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "minlikeLineEdit").setValidator(QtGui.QIntValidator(0, 10000))
        self.MainWindow.findChild(QtWidgets.QLineEdit, "mincommentLineEdit").setValidator(QtGui.QIntValidator(0, 10000))
        self.MainWindow.findChild(QtWidgets.QPushButton, "excludeWordButton").clicked.connect(self.MainWindow.Slot.excludeWord)

    def plasterMenu(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "selectboardButton").clicked.connect(self.MainWindow.Slot.selectBoard)
        self.MainWindow.findChild(QtWidgets.QPushButton, "plasterWordButton").clicked.connect(self.MainWindow.Slot.plasterWord)
        self.MainWindow.findChild(QtWidgets.QPushButton, "startplatsterButton").clicked.connect(self.MainWindow.Slot.startPlaster)
        self.MainWindow.findChild(QtWidgets.QPushButton, "cancelplasterButton").clicked.connect(self.MainWindow.Slot.abortPlaster)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "iterationLineEdit").setValidator(QtGui.QIntValidator(0, 10000))
        self.MainWindow.findChild(QtWidgets.QLineEdit, "retryLineEdit").setValidator(QtGui.QIntValidator(0, 100))

    def searchMenu(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "selectboardButton").clicked.connect(self.MainWindow.Slot.selectBoard)
        self.MainWindow.findChild(QtWidgets.QPushButton, "searchButton").clicked.connect(self.MainWindow.Slot.startSearch)
        self.MainWindow.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(self.MainWindow.Slot.abortSearch)
        self.MainWindow.findChild(QtWidgets.QPushButton, "detailButton").clicked.connect(self.MainWindow.Slot.searchedDetail)
        self.MainWindow.findChild(QtWidgets.QPushButton, "savecommentButton").clicked.connect(self.MainWindow.Slot.saveComment)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "searchpageLineEdit").setValidator(QtGui.QIntValidator(0, 100000))
        self.MainWindow.findChild(QtWidgets.QLineEdit, "searchpageEndLineEdit").setValidator(QtGui.QIntValidator(0, 100000))

    def configMenu(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "saveButton").clicked.connect(self.MainWindow.Slot.configSave)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").setValidator(QtGui.QIntValidator(1, 100))
        self.MainWindow.findChild(QtWidgets.QLineEdit, "plasterintervalLineEdit").setValidator(QtGui.QDoubleValidator(1, 100, 3))
    
    def excludeWord(self, dialog):
        button = dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        button.accepted.connect(lambda: self.MainWindow.Slot.saveExcludeWord(dialog))
        button.rejected.connect(lambda: self.MainWindow.Slot.cancelDialog(dialog))
    
    def selectBoard(self, dialog):
        button = dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        button.accepted.connect(lambda: self.MainWindow.Slot.saveSelectBoard(dialog))
        button.rejected.connect(lambda: self.MainWindow.Slot.cancelDialog(dialog))
    
    def searchedDetail(self, dialog):
        button = dialog.findChild(QtWidgets.QPushButton, "cancelButton")
        button.clicked.connect(lambda: self.MainWindow.Slot.cancelDialog(dialog))
    
    def plasterWord(self, dialog):
        button = dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        button.accepted.connect(lambda: self.MainWindow.Slot.savePlasterWord(dialog))
        button.rejected.connect(lambda: self.MainWindow.Slot.cancelDialog(dialog))
