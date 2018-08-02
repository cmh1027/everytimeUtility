from PyQt5 import QtCore, QtWidgets
import view.ui.detail as detail
from model.data import Data
from PyQt5.QtCore import pyqtSlot

class OthersDetail(QtWidgets.QDialog):
    def __init__(self, window):
        super(window)
        self.setupUi()
        self.show()
        button = self.findChild(QtWidgets.QPushButton, "cancelButton")
        button.clicked.connect(self.cancelDialog)

    def setupUi(self):
        ui = detail.Ui_Dialog()
        ui.setupUi(self)
        articleTableWidget = self.findChild(QtWidgets.QTableWidget, "articleTable")
        articleTableWidget.setColumnWidth(0, 248)
        articleTableWidget.setColumnWidth(1, 30)
        articleTableWidget.setColumnWidth(2, 30)
        articleTableWidget.setColumnWidth(3, 70)
        articleTableWidget.setColumnWidth(4, 80)
        articleTableWidget.setColumnWidth(5, 240)
        commentTableWidget = self.findChild(QtWidgets.QTableWidget, "commentTable")
        commentTableWidget.setColumnWidth(0, 181)
        commentTableWidget.setColumnWidth(1, 145)
        commentTableWidget.setColumnWidth(2, 70)
        commentTableWidget.setColumnWidth(3, 80)
        commentTableWidget.setColumnWidth(4, 240)
        if "article" in Data.others:
            for row, article in enumerate(Data.others["article"]):
                articleTableWidget.insertRow(row)
                if article["article"]["title"] == "":
                    item = QtWidgets.QTableWidgetItem(article["article"]["text"].replace("<br />", " ").replace("&lt;", "<"))
                else:
                    item = QtWidgets.QTableWidgetItem(article["article"]["title"].replace("&lt;", "<"))
                articleTableWidget.setItem(row, 0, item)
                item = QtWidgets.QTableWidgetItem(article["article"]["comment"])
                articleTableWidget.setItem(row, 1, item)
                item = QtWidgets.QTableWidgetItem(article["article"]["posvote"])
                articleTableWidget.setItem(row, 2, item)
                item = QtWidgets.QTableWidgetItem(article["article"]["created_at"])
                articleTableWidget.setItem(row, 3, item)
                for board, boardId in Data.boards.items():
                    if boardId == article["board"]:
                        item = QtWidgets.QTableWidgetItem(board)
                        break
                articleTableWidget.setItem(row, 4, item)
                item = QtWidgets.QTableWidgetItem("https://www.everytime.kr/{}/v/{}".format(boardId, article["article"]["id"]))
                articleTableWidget.setItem(row, 5, item)
        if "comment" in Data.others:
            for row, comment in enumerate(Data.others["comment"]):
                commentTableWidget.insertRow(row)
                item = QtWidgets.QTableWidgetItem(comment["comment"]["text"].replace("&lt;", "<"))
                commentTableWidget.setItem(row, 0, item)
                if comment["article"]["title"] == "":
                    item = QtWidgets.QTableWidgetItem(comment["article"]["text"].replace("<br />", " ").replace("&lt;", "<"))
                else:
                    item = QtWidgets.QTableWidgetItem(comment["article"]["title"].replace("&lt;", "<"))
                commentTableWidget.setItem(row, 1, item)
                item = QtWidgets.QTableWidgetItem(comment["comment"]["created_at"])
                commentTableWidget.setItem(row, 2, item)
                for board, boardId in Data.boards.items():
                    if boardId == comment["board"]:
                        item = QtWidgets.QTableWidgetItem(board)
                        break
                commentTableWidget.setItem(row, 3, item)
                item = QtWidgets.QTableWidgetItem("https://www.everytime.kr/{}/v/{}".format(boardId, comment["article"]["id"]))
                commentTableWidget.setItem(row, 4, item)
    
    @pyqtSlot()
    def cancelDialog(self):
        self.deleteLater()

class MineDetail(QtWidgets.QDialog):
    def __init__(self, window):
        super(window)
        self.setupUi()
        self.show()
        button = self.findChild(QtWidgets.QPushButton, "cancelButton")
        button.clicked.connect(self.cancelDialog)

    def setupUi(self):
        ui = detail.Ui_Dialog()
        ui.setupUi(self)
        articleTableWidget = self.findChild(QtWidgets.QTableWidget, "articleTable")
        articleTableWidget.setColumnWidth(0, 260)
        articleTableWidget.setColumnWidth(1, 30)
        articleTableWidget.setColumnWidth(2, 30)
        articleTableWidget.setColumnWidth(3, 70)
        articleTableWidget.setColumnWidth(4, 80)
        articleTableWidget.setColumnWidth(5, 253)
        commentTableWidget = self.findChild(QtWidgets.QTableWidget, "commentTable")
        commentTableWidget.setColumnWidth(0, 193)
        commentTableWidget.setColumnWidth(1, 145)
        commentTableWidget.setColumnWidth(2, 70)
        commentTableWidget.setColumnWidth(3, 80)
        commentTableWidget.setColumnWidth(4, 253)
        if "article" in Data.mine:
            for row, article in enumerate(Data.mine["article"]):
                articleTableWidget.insertRow(row)
                if article["title"] == "":
                    item = QtWidgets.QTableWidgetItem(article["text"].replace("<br />", " "))
                else:
                    item = QtWidgets.QTableWidgetItem(article["title"])
                articleTableWidget.setItem(row, 0, item)
                item = QtWidgets.QTableWidgetItem(article["comment"])
                articleTableWidget.setItem(row, 1, item)
                item = QtWidgets.QTableWidgetItem(article["posvote"])
                articleTableWidget.setItem(row, 2, item)
                item = QtWidgets.QTableWidgetItem(article["created_at"])
                articleTableWidget.setItem(row, 3, item)
                for board, boardId in Data.boards.items():
                    if boardId == article["board_id"]:
                        item = QtWidgets.QTableWidgetItem(board)
                        break
                articleTableWidget.setItem(row, 4, item)
                item = QtWidgets.QTableWidgetItem("https://www.everytime.kr/{}/v/{}".format(boardId, article["id"]))
                articleTableWidget.setItem(row, 5, item)
        if "comment" in Data.mine:
            for row, comment in enumerate(Data.mine["comment"]):
                commentTableWidget.insertRow(row)
                item = QtWidgets.QTableWidgetItem(comment["comment"]["text"])
                commentTableWidget.setItem(row, 0, item)
                if comment["article"]["title"] == "":
                    item = QtWidgets.QTableWidgetItem(comment["article"]["text"].replace("<br />", " "))
                else:
                    item = QtWidgets.QTableWidgetItem(comment["article"]["title"])
                commentTableWidget.setItem(row, 1, item)
                item = QtWidgets.QTableWidgetItem(comment["comment"]["created_at"])
                commentTableWidget.setItem(row, 2, item)
                for board, boardId in Data.boards.items():
                    if boardId == comment["article"]["board_id"]:
                        item = QtWidgets.QTableWidgetItem(board)
                        break
                commentTableWidget.setItem(row, 3, item)
                item = QtWidgets.QTableWidgetItem("https://www.everytime.kr/{}/v/{}".format(boardId, comment["article"]["id"]))
                commentTableWidget.setItem(row, 4, item)

    @pyqtSlot()
    def cancelDialog(self):
        self.deleteLater()