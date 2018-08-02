import view.ui.configuration as configuration
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from config import Config
class Configuration(QtWidgets.QWidget):
    def __init__(self, window):
        super().__init__()
        self.MainWindow = window
        ui = configuration.Ui_Form()
        ui.setupUi(self)
        self.findChild(QtWidgets.QPushButton, "saveButton").clicked.connect(self.configSave)
        self.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").setValidator(QtGui.QIntValidator(1, 100))
        self.findChild(QtWidgets.QLineEdit, "plasterintervalLineEdit").setValidator(QtGui.QDoubleValidator(1, 100, 3))

    @pyqtSlot()
    def configSave(self):
        threadCount = int(self.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").text())
        if threadCount == 0:
            self.findChild(QtWidgets.QLineEdit, "threadcountLineEdit").setText("1")
            threadCount = 1
        Config.All.threadCount = threadCount
        Config.Delete.printIdFlag = self.findChild(QtWidgets.QCheckBox, "printidCheckBox").isChecked()
        Config.Delete.printTextFlag = self.findChild(QtWidgets.QCheckBox, "printtextCheckBox").isChecked()
        Config.Delete.printOriginFlag = self.findChild(QtWidgets.QCheckBox, "printoriginCheckBox").isChecked()
        Config.Search.printBoardSearchEndFlag = self.findChild(QtWidgets.QCheckBox, "printboardsearchendCheckBox").isChecked()
        plasterInterval = int(self.findChild(QtWidgets.QLineEdit, "plasterintervalLineEdit").text())
        if plasterInterval == 0:
            self.MainWindow.messageDialog("failed", "도배 간격은 0초가 될 수 없습니다")
            return
        else:
            Config.Plaster.plasterInterval = plasterInterval
        Config.Plaster.printPlasterFlag = self.findChild(QtWidgets.QCheckBox, "printplasterCheckBox").isChecked()
        self.MainWindow.messageDialog("save", "저장되었습니다")