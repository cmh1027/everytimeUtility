from PyQt5 import QtWidgets
import view.ui.selectBoardDialog as selectBoardDialog
from model.config import Config
from model.data import Data
from PyQt5.QtCore import pyqtSlot

class SelectBoardDialog(QtWidgets.QDialog):
    def __init__(self, window):
        super().__init__(window)
        ui = selectBoardDialog.Ui_Dialog()
        ui.setupUi(self)
        self.show()
        layout = self.findChild(QtWidgets.QGridLayout, "boardLayout")
        x = 0
        y = 0
        for board in Data.boards.keys():
            checkbox = QtWidgets.QCheckBox()
            checkbox.setText(board)
            layout.addWidget(checkbox, x, y)
            if window.currentMenu == "search":
                if board in Config.Search.selectedBoards:
                    checkbox.setChecked(True)
            elif window.currentMenu == "plaster":
                if board in Config.Plaster.plasterBoards:
                    checkbox.setChecked(True)                
            if y == 1:
                x = x + 1
            y = (y+1) % 2
        button = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        button.accepted.connect(self.saveSelectBoard)
        button.rejected.connect(self.close)
        self.MainWindow = window

    @pyqtSlot()
    def saveSelectBoard(self):
        checkboxes = self.findChildren(QtWidgets.QCheckBox)
        checkboxes = list(filter(lambda checkbox:checkbox.isChecked(), checkboxes))
        if self.MainWindow.currentMenu == "search":
            Config.Search.selectedBoards.clear()
            for checkbox in checkboxes:
                Config.Search.selectedBoards[checkbox.text()] = Data.boards[checkbox.text()]
        elif self.MainWindow.currentMenu == "plaster":
            Config.Plaster.plasterBoards.clear()
            for checkbox in checkboxes:
                Config.Plaster.plasterBoards[checkbox.text()] = Data.boards[checkbox.text()]

    def close(self):
        self.deleteLater()