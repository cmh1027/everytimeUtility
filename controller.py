from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Slot(QObject):
    searchMineEndSignal = pyqtSignal()
    searchOthersEndSignal = pyqtSignal()
    deleteEndSignal = pyqtSignal()
    addProgressSignal = pyqtSignal(str)

    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.searchMineEndSignal.connect(self.searchMineEnd)
        self.searchOthersEndSignal.connect(self.searchOthersEnd)
        self.deleteEndSignal.connect(self.deleteEnd)
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
        _id = "sodlqnf123"
        password = "sodlqnf12"
        response = self.MainWindow.RequestHandle.login(_id, password)
        if response:
            self.MainWindow.Render.home(response)
            self.MainWindow.boards = self.MainWindow.RequestHandle.extractBoards(response)
        else:
            self.MainWindow.Render.messageDialog("failed", "아이디나 비밀번호를 바르게 입력해주세요")
           
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
    def cancelDelete(self):
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
        for checkbox in checkboxes:
            self.MainWindow.selectedBoards[checkbox.text()] = self.MainWindow.boards[checkbox.text()]

    @pyqtSlot()
    def startSearch(self):
        self.MainWindow.searchPage = int(self.MainWindow.findChild(QtWidgets.QLineEdit, "searchpageLineEdit").text())
        self.MainWindow.nickname = self.MainWindow.findChild(QtWidgets.QLineEdit, "nicknameLineEdit").text()
        self.MainWindow.articleCheckFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "articleCheckBox").isChecked()
        self.MainWindow.commentCheckFlag = self.MainWindow.findChild(QtWidgets.QCheckBox, "commentCheckBox").isChecked()
        if not self.MainWindow.articleCheckFlag and not self.MainWindow.commentCheckFlag:
            self.MainWindow.Render.messageDialog("error", "글 혹은 댓글 검색 중 적어도 하나를 체크해주세요")
            return
        if len(self.MainWindow.selectedBoards) == 0:
            self.MainWindow.Render.messageDialog("error", "적어도 하나의 게시판을 체크해주세요")
            return            
        self.MainWindow.others = {}
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "searchButton")
        self.MainWindow.Render.disableButton(btn, "검색중")
        self.MainWindow.searchingOthers = True
        self.MainWindow.Render.addTextEdit("[System] 검색을 시작합니다")
        option = {}
        option["boards"] = self.MainWindow.selectedBoards
        option["page"] = self.MainWindow.searchPage
        option["nickname"] = self.MainWindow.nickname
        option["articleFlag"] = self.MainWindow.articleCheckFlag
        option["commentFlag"] = self.MainWindow.commentCheckFlag
        self.MainWindow.RequestHandle.searchOthers(option)

    @pyqtSlot()
    def cancelSearch(self):
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
    def searchOthersEnd(self):
        self.MainWindow.Render.addTextEdit("[System] 검색 완료")
        self.MainWindow.searchingOthers = False
        if self.MainWindow.currentMenu == "search":
            self.MainWindow.Render.searchOthersEnd()

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
        self.MainWindow.findChild(QtWidgets.QToolButton, "plasterButton").clicked.connect(self.MainWindow.Slot.plasterMenu)
        self.MainWindow.findChild(QtWidgets.QToolButton, "searchButton").clicked.connect(self.MainWindow.Slot.searchMenu)
        self.MainWindow.findChild(QtWidgets.QToolButton, "configButton").clicked.connect(self.MainWindow.Slot.configMenu)
        self.MainWindow.findChild(QtWidgets.QPushButton, "eraseButton").clicked.connect(self.MainWindow.Slot.eraseProgress)
    
    def deleteMenu(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "deleteButton").clicked.connect(self.MainWindow.Slot.startDelete)
        self.MainWindow.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(self.MainWindow.Slot.cancelDelete)
        self.MainWindow.findChild(QtWidgets.QPushButton, "refreshButton").clicked.connect(self.MainWindow.Slot.mineRefresh)
        self.MainWindow.findChild(QtWidgets.QPushButton, "detailButton").clicked.connect(self.MainWindow.Slot.mineDetail)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "minlikeLineEdit").setValidator(QtGui.QIntValidator(0, 1000))
        self.MainWindow.findChild(QtWidgets.QLineEdit, "mincommentLineEdit").setValidator(QtGui.QIntValidator(0, 1000))
        self.MainWindow.findChild(QtWidgets.QPushButton, "excludeWordButton").clicked.connect(self.MainWindow.Slot.excludeWord)

    def plasterMenu(self):
        pass

    def searchMenu(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "selectboardButton").clicked.connect(self.MainWindow.Slot.selectBoard)
        self.MainWindow.findChild(QtWidgets.QPushButton, "searchButton").clicked.connect(self.MainWindow.Slot.startSearch)
        self.MainWindow.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(self.MainWindow.Slot.cancelSearch)
        self.MainWindow.findChild(QtWidgets.QPushButton, "detailButton").clicked.connect(self.MainWindow.Slot.searchedDetail)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "searchpageLineEdit").setValidator(QtGui.QIntValidator(0, 9999))

    def configMenu(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "saveButton").clicked.connect(self.MainWindow.Slot.configSave)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").setValidator(QtGui.QIntValidator(1, 100))

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