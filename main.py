from PyQt5 import QtWidgets
import model.widget as widget
from render import Render
from controller import Signal, Slot

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = widget.Window()
    MainWindow.init(Render(MainWindow), Signal(MainWindow), Slot(MainWindow))
    MainWindow.Render.login()
    MainWindow.show()
    sys.exit(app.exec_())