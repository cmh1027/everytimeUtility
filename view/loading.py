import view.ui.loading as loading
from PyQt5 import QtWidgets
class Loading(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        ui = loading.Ui_Form()
        ui.setupUi(self)