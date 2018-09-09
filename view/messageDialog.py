from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
class MessageDialog(QtWidgets.QMessageBox):
    def __init__(self, parent, title, content):
        super().__init__(parent)
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle(title)
        self.setText(content)
        self.setIcon(QMessageBox.Critical)
        self.setStyleSheet("QPushButton{background-color: white;}")
        self.show()
