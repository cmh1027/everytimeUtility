from PyQt5 import QtWidgets
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import view.messageDialog as messageDialog
import urllib3
import requests

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        from render import Render
        from controller import Signal, Slot
        from requesthandle import RequestHandle
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        with requests.Session() as self.req:
            retry = Retry(connect=4, backoff_factor=0.3)
            adapter = HTTPAdapter(max_retries=retry)
            self.req.mount('https://www.everytime.kr', adapter)
        self.Render = Render(self)
        self.Signal = Signal(self)
        self.Slot = Slot(self)
        self.RequestHandle = RequestHandle(self)
        self.initialize()
    
    def initialize(self):
        self.currentMenu = None
        self.boards = None
        self.threadCount = 4

        self.mine = None # My articles and comments
        self.printIdFlag = True
        self.printTextFlag = True
        self.printOriginFlag = True
        self.excludeWord = []
        self.excludeArticleFlag = False
        self.excludeCommentFlag = False
        self.searchingMine = False
        self.deleting = False

        self.printBoardSearchEndFlag = True
        self.others = {} # Articles and comments of others
        self.selectedBoards = {}
        self.searchPage = 1
        self.searchEndPage = 1
        self.searchNickname = ""
        self.articleCheckFlag = False
        self.commentCheckFlag = False
        self.searchAllFlag = False
        self.searchingOthers = False
        self.articleKeyword = ""
        self.commentKeyword = ""
        self.articleKeywordFlag = False
        self.commentKeywordFlag = False

        self.plasterBoards = {}
        self.plasterWord = []
        self.plastering = False
        self.articlePlasterFlag = True
        self.commentPlasterFlag = True
        self.promptRemoveFlag = True
        self.isAnonymFlag = True
        self.printPlasterFlag = False
        self.plasterIteration = 1
        self.plasterRetry = 4
        self.plasterInterval = 4
        self.articleCycleFlag = True


class MessageDialog(QtWidgets.QDialog):
    def __init__(self, parent, title, content):
        super().__init__(parent)
        ui = messageDialog.Ui_Dialog()
        ui.setupUi(self)
        self.setWindowTitle(title)
        self.findChild(QtWidgets.QLabel, "messageLabel").setText(content)
        self.findChild(QtWidgets.QPushButton, "cancelButton").clicked.connect(self.close)
        layoutWidget = self.findChild(QtWidgets.QWidget, "verticalLayoutWidget")
        self.resize(len(content)*13, layoutWidget.height()+5)
        layoutWidget.setFixedWidth(self.width())
        self.show()

    def close(self):
        self.deleteLater()