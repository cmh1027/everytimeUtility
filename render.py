from PyQt5 import QtWidgets, QtCore
from glob import glob
from os.path import splitext, basename
from importlib import import_module
from bs4 import BeautifulSoup
import model.widget as widget

for module in glob('view/*'):
    name, ext = splitext(module)
    name = basename(name)
    if ext == '.py':
        globals()[name] = import_module("view.{}".format(name))

def window_clear(function):
    def wrapper(*args):
        args[0].clear() # self.clear()
        return function(*args)
    return wrapper

def content_clear(function):
    def wrapper(*args):
        args[0].clearContent() # self.clearContent()
        function(*args)
        for child in args[0].MainWindow.findChild(QtWidgets.QWidget, "Form").findChildren(QtWidgets.QWidget):
            child.show()
    return wrapper

class Render:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow

    # Never change the name of centralwidget!
    def clear(self):
        centralwidget = self.MainWindow.findChild(QtWidgets.QWidget, "centralwidget")
        if centralwidget is not None:
            centralwidget.deleteLater()

    def clearContent(self):
        contents = self.MainWindow.findChild(QtWidgets.QWidget, "Form").findChildren(QtWidgets.QWidget)
        for content in contents:
            content.setParent(None)

    def messageDialog(self, title, content):
        widget.MessageDialog(self.MainWindow, title, content)

    def eraseTextEdit(self):
        progressTextEdit = self.MainWindow.findChild(QtWidgets.QTextEdit, "progressTextEdit")
        progressTextEdit.setText("")

    def addTextEdit(self, string):
        progressTextEdit = self.MainWindow.findChild(QtWidgets.QTextEdit, "progressTextEdit")
        text = progressTextEdit.toPlainText()
        progressTextEdit.setText(text+string+"\n")
    
    def disableButton(self, button, text=None):
        if button is None:
            return
        button.setEnabled(False)
        if text is not None:
            button.setText(text)

    def enableButton(self, button, text=None):
        if button is None:
            return
        button.setEnabled(True)
        if text is not None:
            button.setText(text)

    @window_clear
    def login(self):
        ui = loginScreen.Ui_MainWindow()
        ui.setupUi(self.MainWindow)
        self.MainWindow.Signal.bind("login")
    
    @window_clear
    def home(self, response):
        ui = mainScreen.Ui_MainWindow()
        ui.setupUi(self.MainWindow)
        soup = BeautifulSoup(response, 'html.parser')
        self.MainWindow.findChild(QtWidgets.QLabel, "univLabel").setText(soup.find("span", {"class":"subname"}).getText())
        self.MainWindow.findChild(QtWidgets.QLabel, "nicknameLabel").setText(soup.find("p", {"class":"nickname"}).getText())
        self.MainWindow.findChild(QtWidgets.QLabel, "nameLabel").setText(soup.find("p", {"class":"school"}).getText())
        self.MainWindow.Signal.bind("home")

    @content_clear
    def delete(self):
        ui = delete.Ui_Form()
        Form = self.MainWindow.findChild(QtWidgets.QWidget, "Form")
        ui.setupUi(Form)
        if "article" in self.MainWindow.mine and "comment" in self.MainWindow.mine:
            self.MainWindow.findChild(QtWidgets.QLabel, "writeLabel").setText("글 {}개 / 덧글 {}개".format(len(self.MainWindow.mine["article"]), len(self.MainWindow.mine["comment"])))
        else:
            self.MainWindow.findChild(QtWidgets.QLabel, "writeLabel").setText("오류 발생")
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "deleteButton")
        if self.MainWindow.deleting:
            self.disableButton(btn)
        self.MainWindow.Signal.bind("deleteMenu")


    @content_clear
    def config(self):
        ui = configuration.Ui_Form()
        Form = self.MainWindow.findChild(QtWidgets.QWidget, "Form")
        ui.setupUi(Form)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").setText(str(self.MainWindow.threadCount))
        self.MainWindow.findChild(QtWidgets.QCheckBox, "printidCheckBox").setChecked(self.MainWindow.printIdFlag)
        self.MainWindow.findChild(QtWidgets.QCheckBox, "printtextCheckBox").setChecked(self.MainWindow.printTextFlag)
        self.MainWindow.findChild(QtWidgets.QCheckBox, "printoriginCheckBox").setChecked(self.MainWindow.printOriginFlag)
        self.MainWindow.findChild(QtWidgets.QCheckBox, "printboardsearchendCheckBox").setChecked(self.MainWindow.printBoardSearchEndFlag)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "plasterintervalLineEdit").setText(str(self.MainWindow.plasterInterval))
        self.MainWindow.findChild(QtWidgets.QCheckBox, "printplasterCheckBox").setChecked(self.MainWindow.printPlasterFlag)
        self.MainWindow.Signal.bind("configMenu")

    @content_clear
    def loading(self):
        ui = loading.Ui_Form()
        Form = self.MainWindow.findChild(QtWidgets.QWidget, "Form")
        ui.setupUi(Form)

    @content_clear
    def search(self):
        ui = search.Ui_Form()
        Form = self.MainWindow.findChild(QtWidgets.QWidget, "Form")
        ui.setupUi(Form)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "searchpageLineEdit").setText(str(self.MainWindow.searchPage))
        self.MainWindow.findChild(QtWidgets.QLineEdit, "nicknameLineEdit").setText(self.MainWindow.searchNickname)
        self.MainWindow.findChild(QtWidgets.QCheckBox, "articleCheckBox").setChecked(self.MainWindow.articleCheckFlag)
        self.MainWindow.findChild(QtWidgets.QCheckBox, "commentCheckBox").setChecked(self.MainWindow.commentCheckFlag)
        if not self.MainWindow.searchingOthers:
            if "article" in self.MainWindow.others and "comment" in self.MainWindow.others:
                self.MainWindow.findChild(QtWidgets.QLabel, "infoLabel").setText("글 {}개 / 댓글 {}개".format(len(self.MainWindow.others["article"]), len(self.MainWindow.others["comment"])))
            elif "article" in self.MainWindow.others and "comment" not in self.MainWindow.others:
                self.MainWindow.findChild(QtWidgets.QLabel, "infoLabel").setText("글 {}개".format(len(self.MainWindow.others["article"])))
            elif "article" not in self.MainWindow.others and "comment" in self.MainWindow.others:
                self.MainWindow.findChild(QtWidgets.QLabel, "infoLabel").setText("댓글 {}개".format(len(self.MainWindow.others["comment"])))
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "searchButton")
        if self.MainWindow.searchingOthers:
            self.disableButton(btn, "검색중")
        if self.MainWindow.plastering:
            self.disableButton(btn, "도배중")
        self.MainWindow.Signal.bind("searchMenu")

    def excludeWord(self):
        Dialog = QtWidgets.QDialog(self.MainWindow)
        ui = excludeWordDialog.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.findChild(QtWidgets.QTextEdit, "excludewordTextEdit").setText('\n'.join(self.MainWindow.excludeWord))
        Dialog.findChild(QtWidgets.QCheckBox, "excludearticleCheckBox").setChecked(self.MainWindow.excludeArticleFlag)
        Dialog.findChild(QtWidgets.QCheckBox, "excludecommentCheckBox").setChecked(self.MainWindow.excludeCommentFlag)
        self.MainWindow.Signal.bind("excludeWord", Dialog)

    def selectBoard(self):
        Dialog = QtWidgets.QDialog(self.MainWindow)
        ui = selectBoardDialog.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        layout = Dialog.findChild(QtWidgets.QGridLayout, "boardLayout")
        x = 0
        y = 0
        for board in self.MainWindow.boards.keys():
            checkbox = QtWidgets.QCheckBox()
            checkbox.setText(board)
            layout.addWidget(checkbox, x, y)
            if self.MainWindow.currentMenu == "search":
                if board in self.MainWindow.selectedBoards:
                    checkbox.setChecked(True)
            elif self.MainWindow.currentMenu == "plaster":
                if board in self.MainWindow.plasterBoards:
                    checkbox.setChecked(True)                
            if y == 1:
                x = x + 1
            y = (y+1) % 2
        self.MainWindow.Signal.bind("selectBoard", Dialog)
    
    def searchOthersEnd(self):
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "searchButton")
        self.enableButton(btn, "검색")
        if "article" in self.MainWindow.others and "comment" in self.MainWindow.others:
            self.MainWindow.findChild(QtWidgets.QLabel, "infoLabel").setText("글 {}개 / 댓글 {}개".format(len(self.MainWindow.others["article"]), len(self.MainWindow.others["comment"])))
        elif "article" in self.MainWindow.others and "comment" not in self.MainWindow.others:
            self.MainWindow.findChild(QtWidgets.QLabel, "infoLabel").setText("글 {}개".format(len(self.MainWindow.others["article"])))
        elif "article" not in self.MainWindow.others and "comment" in self.MainWindow.others:
            self.MainWindow.findChild(QtWidgets.QLabel, "infoLabel").setText("댓글 {}개".format(len(self.MainWindow.others["comment"])))

    def searchOthersEndPlaster(self):
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "startplatsterButton")
        self.enableButton(btn, "Go!")
        self.MainWindow.findChild(QtWidgets.QLabel, "searchednicknameLabel").setText(self.MainWindow.searchNickname)
        if "article" not in self.MainWindow.others:
            self.MainWindow.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setChecked(False)
            self.MainWindow.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setEnabled(False)
        else:
            self.MainWindow.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setChecked(True)
            self.MainWindow.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setEnabled(True)            
        if "comment" not in self.MainWindow.others:
            self.MainWindow.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setChecked(False)
            self.MainWindow.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setEnabled(False)
        else:
            self.MainWindow.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setChecked(True)
            self.MainWindow.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setEnabled(True)            

    def searchedDetail(self):
        Dialog = QtWidgets.QDialog(self.MainWindow)
        ui = wrapDetail.OthersDetail()
        ui.setupUi(Dialog, self.MainWindow.others, self.MainWindow.boards)
        Dialog.show()
        self.MainWindow.Signal.bind("searchedDetail", Dialog)
    
    def mineDetail(self):
        Dialog = QtWidgets.QDialog(self.MainWindow)
        ui = wrapDetail.MineDetail()
        ui.setupUi(Dialog, self.MainWindow.mine, self.MainWindow.boards)
        Dialog.show()
        self.MainWindow.Signal.bind("searchedDetail", Dialog)
    
    @content_clear
    def plaster(self):
        ui = plaster.Ui_Form()
        Form = self.MainWindow.findChild(QtWidgets.QWidget, "Form")
        ui.setupUi(Form)
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "startplatsterButton")
        self.MainWindow.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setChecked(self.MainWindow.articlePlasterFlag)
        self.MainWindow.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setChecked(self.MainWindow.commentPlasterFlag)
        self.MainWindow.findChild(QtWidgets.QCheckBox, "promptremoveCheckBox").setChecked(self.MainWindow.promptRemoveFlag)
        self.MainWindow.findChild(QtWidgets.QCheckBox, "isanonymFlag").setChecked(self.MainWindow.isAnonymFlag)
        self.MainWindow.findChild(QtWidgets.QLineEdit, "iterationLineEdit").setText(str(self.MainWindow.plasterIteration))
        self.MainWindow.findChild(QtWidgets.QLineEdit, "retryLineEdit").setText(str(self.MainWindow.plasterRetry))
        if self.MainWindow.searchNickname == "":
            self.MainWindow.findChild(QtWidgets.QLabel, "searchednicknameLabel").setText("검색되지 않음")
            self.disableButton(btn, "Go!")
        else:
            self.MainWindow.findChild(QtWidgets.QLabel, "searchednicknameLabel").setText(self.MainWindow.searchNickname)
        if self.MainWindow.searchingOthers:
            self.disableButton(btn, "검색중")
        if self.MainWindow.plastering:
            self.disableButton(btn, "도배중")
        if "article" not in self.MainWindow.others:
            self.MainWindow.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setChecked(False)
            self.MainWindow.findChild(QtWidgets.QCheckBox, "articleplasterCheckBox").setEnabled(False)
        if "comment" not in self.MainWindow.others:
            self.MainWindow.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setChecked(False)
            self.MainWindow.findChild(QtWidgets.QCheckBox, "commentplasterCheckBox").setEnabled(False)
        self.MainWindow.Signal.bind("plasterMenu")

    def plasterWord(self):
        Dialog = QtWidgets.QDialog(self.MainWindow)
        ui = plasterWordDialog.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.findChild(QtWidgets.QTextEdit, "plasterwordTextEdit").setText('\n'.join(self.MainWindow.plasterWord))
        self.MainWindow.Signal.bind("plasterWord", Dialog)
    
    def plasterEndSearch(self):
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "searchButton")
        self.enableButton(btn, "검색")
    
    def plasterEnd(self):
        btn = self.MainWindow.findChild(QtWidgets.QPushButton, "startplatsterButton")
        self.enableButton(btn, "Go!")
