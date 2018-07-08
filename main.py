from PyQt5 import QtWidgets
import model.widget as widget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = widget.Window()
    MainWindow.Render.login()
    MainWindow.show()
    sys.exit(app.exec_())