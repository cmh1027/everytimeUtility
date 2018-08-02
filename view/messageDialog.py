from PyQt5 import QtWidgets
import view.ui.messageDialog as messageDialog
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