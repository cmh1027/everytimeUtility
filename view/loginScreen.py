# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginScreen.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(221, 145)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(221, 145))
        MainWindow.setMaximumSize(QtCore.QSize(221, 145))
        MainWindow.setStyleSheet("background-color:rgb(250, 255, 151)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(0, 0, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("background-color:rgb(211, 232, 117)")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 60, 221, 101))
        self.layoutWidget.setObjectName("layoutWidget")
        self.loginLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.loginLayout.setContentsMargins(5, 5, 5, 5)
        self.loginLayout.setObjectName("loginLayout")
        self.passwordLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.passwordLabel.setIndent(0)
        self.passwordLabel.setObjectName("passwordLabel")
        self.loginLayout.addWidget(self.passwordLabel, 1, 0, 1, 1)
        self.passwordLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.passwordLineEdit.setMaxLength(16)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.loginLayout.addWidget(self.passwordLineEdit, 1, 1, 1, 1)
        self.idLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.idLabel.setFont(font)
        self.idLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.idLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.idLabel.setIndent(0)
        self.idLabel.setObjectName("idLabel")
        self.loginLayout.addWidget(self.idLabel, 0, 0, 1, 1)
        self.idLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.idLineEdit.setText("")
        self.idLineEdit.setMaxLength(16)
        self.idLineEdit.setObjectName("idLineEdit")
        self.loginLayout.addWidget(self.idLineEdit, 0, 1, 1, 1)
        self.loginButtonLayout = QtWidgets.QVBoxLayout()
        self.loginButtonLayout.setContentsMargins(60, 0, 60, 15)
        self.loginButtonLayout.setObjectName("loginButtonLayout")
        self.loginButton = QtWidgets.QPushButton(self.layoutWidget)
        self.loginButton.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.loginButton.setObjectName("loginButton")
        self.loginButtonLayout.addWidget(self.loginButton)
        self.loginLayout.addLayout(self.loginButtonLayout, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.titleLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ff5500;\">Everytime Utility</span></p></body></html>"))
        self.passwordLabel.setText(_translate("MainWindow", "Password"))
        self.idLabel.setText(_translate("MainWindow", "ID"))
        self.loginButton.setText(_translate("MainWindow", "Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

