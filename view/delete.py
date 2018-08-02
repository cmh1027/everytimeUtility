import view.ui.delete as delete
from view.excludeWordDialog import ExcludeWordDialog
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from data import Data
from config import Config
import view.detail as Detail

class Delete(QtWidgets.QWidget):
    searchMineEndSignal = pyqtSignal()
    deleteEndSignal = pyqtSignal()
    def __init__(self, window):
        super().__init__()
        self.MainWindow = window
        ui = delete.Ui_Form()
        ui.setupUi(self)
        self.findChild(QtWidgets.QPushButton, "deleteButton").clicked.connect(self.startDelete)
        self.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(self.abortDelete)
        self.findChild(QtWidgets.QPushButton, "refreshButton").clicked.connect(self.mineRefresh)
        self.findChild(QtWidgets.QPushButton, "detailButton").clicked.connect(self.mineDetail)
        self.findChild(QtWidgets.QPushButton, "excludeWordButton").clicked.connect(self.excludeWord)
        self.findChild(QtWidgets.QLineEdit, "minlikeLineEdit").setValidator(QtGui.QIntValidator(0, 10000))
        self.findChild(QtWidgets.QLineEdit, "mincommentLineEdit").setValidator(QtGui.QIntValidator(0, 10000))
        self.searchMineEndSignal.connect(self.searchMineEnd)
        self.deleteEndSignal.connect(self.deleteEnd)
    
    def update(self):
        if "article" in Data.mine and "comment" in Data.mine:
            self.findChild(QtWidgets.QLabel, "writeLabel").setText("글 {}개 / 덧글 {}개".format(len(Data.mine["article"]), len(Data.mine["comment"])))
        else:
            self.findChild(QtWidgets.QLabel, "writeLabel").setText("오류 발생")

    @pyqtSlot()
    def startDelete(self):
        articleFlag = self.findChild(QtWidgets.QCheckBox, "articleCheckBox").isChecked()
        commentFlag = self.findChild(QtWidgets.QCheckBox, "commentCheckBox").isChecked()
        minlikeFlag = self.findChild(QtWidgets.QCheckBox, "minlikeCheckBox").isChecked()
        mincommentFlag = self.findChild(QtWidgets.QCheckBox, "mincommentCheckBox").isChecked()
        scope = self.findChild(QtWidgets.QComboBox, "dateComboBox").currentText()
        minlike = self.findChild(QtWidgets.QLineEdit, "minlikeLineEdit").text()
        mincomment = self.findChild(QtWidgets.QLineEdit, "mincommentLineEdit").text()
        if not articleFlag and not commentFlag:
            self.MainWindow.messageDialog("error", "글 혹은 댓글 삭제 중 적어도 하나를 체크해주세요")
            return
        if minlikeFlag and minlike == "":
            self.MainWindow.messageDialog("error", "공감 제한 개수를 입력해주세요")
            return
        if mincommentFlag and mincomment == "":
            self.MainWindow.messageDialog("error", "댓글 제한 개수를 입력해주세요")
            return
        btn = self.findChild(QtWidgets.QPushButton, "deleteButton")
        btn.setEnabled(False)
        btn.setText("삭제중")
        option = {}
        option["articleFlag"] = articleFlag
        option["commentFlag"] = commentFlag
        option["minlikeFlag"] = minlikeFlag
        option["mincommentFlag"] = mincommentFlag
        option["scope"] = scope
        option["minlike"] = minlike
        option["mincomment"] = mincomment
        option["excludeWord"] = Config.Delete.excludeWord
        option["excludeArticleFlag"] = Config.Delete.excludeArticleFlag
        option["excludeCommentFlag"] = Config.Delete.excludeCommentFlag
        Config.Delete.deleting = True
        self.MainWindow.addProgressSignal.emit("[System] 삭제를 시작합니다")
        self.MainWindow.RequestHandle.deleteMine(option)

    @pyqtSlot()
    def abortDelete(self):
        if Config.Delete.deleting:
            self.MainWindow.RequestHandle.abortDelete()
            Config.Delete.deleting = False
            self.MainWindow.addProgressSignal.emit("[System] 삭제가 중지되었습니다")
            self.mineRefresh()
    
    @pyqtSlot()
    def mineRefresh(self):
        Data.mine = None
        self.MainWindow.deleteMenu()

    @pyqtSlot()
    def mineDetail(self):
        Detail.MineDetail(self.MainWindow)

    @pyqtSlot()
    def excludeWord(self):
        ExcludeWordDialog(self.MainWindow)

    @pyqtSlot()
    def deleteEnd(self):
        self.MainWindow.addProgressSignal.emit("[System] 삭제 완료")
        Config.Delete.deleting = False
        if self.MainWindow.currentMenu == "delete":
            btn = self.findChild(QtWidgets.QPushButton, "deleteButton")
            btn.setEnabled(True)
            btn.setText("삭제")
            self.mineRefresh()

    @pyqtSlot()
    def searchMineEnd(self):
        self.MainWindow.addProgressSignal.emit("[System] 검색 완료")
        Config.Search.searchingMine = False
        self.MainWindow.deleteScreen()