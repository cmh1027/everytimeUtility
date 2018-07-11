# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainScreen.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(371, 376)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(371, 376))
        MainWindow.setMaximumSize(QtCore.QSize(371, 377))
        MainWindow.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0))")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.progressTextEdit.setGeometry(QtCore.QRect(0, 247, 371, 129))
        self.progressTextEdit.setMaximumSize(QtCore.QSize(16777205, 16777215))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(7)
        self.progressTextEdit.setFont(font)
        self.progressTextEdit.setStyleSheet("background-color: white;\n"
"padding:5px")
        self.progressTextEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.progressTextEdit.setReadOnly(True)
        self.progressTextEdit.setObjectName("progressTextEdit")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 141, 101))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.verticalLayoutWidget.setFont(font)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.infoLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setSpacing(0)
        self.infoLayout.setObjectName("infoLayout")
        self.titleLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setMinimumSize(QtCore.QSize(0, 27))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("background-color:rgb(255, 85, 0)")
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.infoLayout.addWidget(self.titleLabel)
        self.univLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.univLabel.sizePolicy().hasHeightForWidth())
        self.univLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.univLabel.setFont(font)
        self.univLabel.setStyleSheet("background-color: rgb(255, 233, 65);\n"
"border: 2px solid rgb(126, 182, 255);\n"
"color:rgb(8, 53, 255)")
        self.univLabel.setText("")
        self.univLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.univLabel.setObjectName("univLabel")
        self.infoLayout.addWidget(self.univLabel)
        self.nicknameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nicknameLabel.setFont(font)
        self.nicknameLabel.setStyleSheet("background-color: rgb(255, 233, 65);\n"
"border: 2px solid rgb(126, 182, 255);\n"
"color:rgb(8, 53, 255)")
        self.nicknameLabel.setText("")
        self.nicknameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nicknameLabel.setObjectName("nicknameLabel")
        self.infoLayout.addWidget(self.nicknameLabel)
        self.nameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.nameLabel.setStyleSheet("background-color: rgb(255, 233, 65);\n"
"border: 2px solid rgb(126, 182, 255);\n"
"color:rgb(8, 53, 255)")
        self.nameLabel.setText("")
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.infoLayout.addWidget(self.nameLabel)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 101, 141, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.menuLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.menuLayout.setContentsMargins(0, 0, 0, 0)
        self.menuLayout.setSpacing(0)
        self.menuLayout.setObjectName("menuLayout")
        self.deleteButton = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("양재소슬체S")
        font.setPointSize(11)
        self.deleteButton.setFont(font)
        self.deleteButton.setStyleSheet("\n"
"background-color:rgb(156, 226, 255)")
        self.deleteButton.setObjectName("deleteButton")
        self.menuLayout.addWidget(self.deleteButton)
        self.searchButton = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("양재소슬체S")
        font.setPointSize(11)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("\n"
"background-color:rgb(156, 226, 255)")
        self.searchButton.setObjectName("searchButton")
        self.menuLayout.addWidget(self.searchButton)
        self.plasterButton = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plasterButton.sizePolicy().hasHeightForWidth())
        self.plasterButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("양재소슬체S")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.plasterButton.setFont(font)
        self.plasterButton.setStyleSheet("\n"
"background-color:rgb(156, 226, 255)")
        self.plasterButton.setObjectName("plasterButton")
        self.menuLayout.addWidget(self.plasterButton)
        self.configButton = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configButton.sizePolicy().hasHeightForWidth())
        self.configButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("양재소슬체S")
        font.setPointSize(11)
        self.configButton.setFont(font)
        self.configButton.setStyleSheet("\n"
"background-color:rgb(156, 226, 255)")
        self.configButton.setObjectName("configButton")
        self.menuLayout.addWidget(self.configButton)
        self.Form = QtWidgets.QWidget(self.centralwidget)
        self.Form.setGeometry(QtCore.QRect(140, 0, 231, 223))
        self.Form.setStyleSheet("background-color:rgb(208, 206, 255)")
        self.Form.setObjectName("Form")
        self.eraseButton = QtWidgets.QPushButton(self.centralwidget)
        self.eraseButton.setGeometry(QtCore.QRect(300, 223, 75, 24))
        self.eraseButton.setStyleSheet("background-color: rgb(182, 182, 182);")
        self.eraseButton.setObjectName("eraseButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Util"))
        self.progressTextEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:7pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Welcome to everytime utility!</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.titleLabel.setText(_translate("MainWindow", "Everytime Utility v.beta"))
        self.deleteButton.setText(_translate("MainWindow", "글/댓글 삭제"))
        self.searchButton.setText(_translate("MainWindow", "고정닉 검색"))
        self.plasterButton.setText(_translate("MainWindow", "도배"))
        self.configButton.setText(_translate("MainWindow", "설정"))
        self.eraseButton.setText(_translate("MainWindow", "지우기"))

