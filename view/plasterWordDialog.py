from PyQt5 import QtWidgets
import view.ui.plasterWordDialog as plasterWordDialog
from config import Config
from data import Data
from PyQt5.QtCore import pyqtSlot

class PlasterWordDialog(QtWidgets.QDialog):
    def __init__(self, window):
        super().__init__(window)
        ui = plasterWordDialog.Ui_Dialog()
        ui.setupUi(self)
        self.show()
        textEdit = self.findChild(QtWidgets.QTextEdit, "plasterwordTextEdit")
        textEdit.setText('\n'.join(Config.Plaster.plasterWord))
        button = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        button.accepted.connect(self.savePlasterWord)
        button.rejected.connect(self.cancelDialog)

    @pyqtSlot()
    def savePlasterWord(self):
        plasterWord = self.findChild(QtWidgets.QTextEdit, "plasterwordTextEdit").toPlainText().split("\n")
        plasterWord = list(map(lambda word:word.strip(), list(filter(lambda word:word!='', plasterWord))))
        Config.Plaster.plasterWord = plasterWord
        self.deleteLater()

    @pyqtSlot()
    def cancelDialog(self):
        self.deleteLater()