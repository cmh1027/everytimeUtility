import view.ui.excludeWordDialog as excludeWordDialog
from PyQt5 import QtWidgets
from model.config import Config
from PyQt5.QtCore import pyqtSlot

class ExcludeWordDialog(QtWidgets.QDialog):
    def __init__(self, window):
        super(window)
        ui = excludeWordDialog.Ui_Dialog()
        ui.setupUi(self)
        self.show()
        self.findChild(QtWidgets.QTextEdit, "excludewordTextEdit").setText('\n'.join(Config.Delete.excludeWord))
        self.findChild(QtWidgets.QCheckBox, "excludearticleCheckBox").setChecked(Config.Delete.excludeArticleFlag)
        self.findChild(QtWidgets.QCheckBox, "excludecommentCheckBox").setChecked(Config.Delete.excludeCommentFlag)
        button = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        button.accepted.connect(self.saveExcludeWord)
        button.rejected.connect(self.cancelDialog)
    
    @pyqtSlot()
    def saveExcludeWord(self):
        Config.Delete.excludeWord = self.findChild(QtWidgets.QTextEdit, "excludewordTextEdit").toPlainText().split("\n")
        Config.Delete.excludeArticleFlag = self.findChild(QtWidgets.QCheckBox, "excludearticleCheckBox").isChecked()
        Config.Delete.excludeCommentFlag = self.findChild(QtWidgets.QCheckBox, "excludecommentCheckBox").isChecked()
        self.deleteLater()

    @pyqtSlot()
    def cancelDialog(self):
        self.deleteLater()