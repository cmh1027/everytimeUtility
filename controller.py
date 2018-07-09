from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Slot(QObject):
    searchEndSignal = pyqtSignal()
    deleteEndSignal = pyqtSignal()
    addProgressSignal = pyqtSignal(str)

    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        self.searchEndSignal.connect(self.searchEnd)
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
        else:
            self.MainWindow.Render.messageDialog("failed", "아이디나 비밀번호를 바르게 입력해주세요")
           
    @pyqtSlot()
    def deleteMenu(self):
        if self.MainWindow.mine is None: # Not updated
            if self.MainWindow.searching:
                self.MainWindow.Render.loading()
            else:
                self.MainWindow.Render.loading()
                self.MainWindow.searching = True
                self.MainWindow.Render.addTextEdit("[System] 작성 글 및 댓글 검색을 시작합니다")
                self.MainWindow.RequestHandle.getMine()
        else: # updated
            self.MainWindow.Render.delete()
    
    @pyqtSlot()
    def searchEnd(self):
        self.MainWindow.Render.addTextEdit("[System] 검색 완료")
        self.MainWindow.searching = False
        self.MainWindow.Render.delete()

    @pyqtSlot()
    def deleteEnd(self):
        self.MainWindow.Render.addTextEdit("[System] 삭제 완료")
        self.MainWindow.deleting = False
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "deleteButton")
        self.MainWindow.Render.enableButton(btn)
        self.mineRefresh()

    @pyqtSlot()
    def mineRefresh(self):
        self.MainWindow.mine = None
        self.deleteMenu()

    @pyqtSlot()
    def plasterMenu(self):
        pass

    @pyqtSlot()
    def searchMenu(self):
        pass

    @pyqtSlot()
    def configMenu(self):
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
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "deleteButton")
        self.MainWindow.Render.disableButton(btn)
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
    def cancelExcludeWord(self, dialog):
        dialog.deleteLater()

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
        self.MainWindow.findChild(QtWidgets.QLineEdit, "minlikeLineEdit").setValidator(QtGui.QIntValidator(0, 1000))
        self.MainWindow.findChild(QtWidgets.QLineEdit, "mincommentLineEdit").setValidator(QtGui.QIntValidator(0, 1000))
        self.MainWindow.findChild(QtWidgets.QPushButton, "excludeWordButton").clicked.connect(self.MainWindow.Slot.excludeWord)

    def plasterMenu(self):
        pass

    def searchMenu(self):
        pass

    def configMenu(self):
        self.MainWindow.findChild(QtWidgets.QPushButton, "saveButton").clicked.connect(self.MainWindow.Slot.configSave)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").setValidator(QtGui.QIntValidator(1, 100))

    def excludeWord(self, dialog):
        buttons = dialog.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        buttons.accepted.connect(lambda: self.MainWindow.Slot.saveExcludeWord(dialog))
        buttons.rejected.connect(lambda: self.MainWindow.Slot.cancelExcludeWord(dialog))