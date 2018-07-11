# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(231, 223)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 221, 169))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.selectboardButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectboardButton.sizePolicy().hasHeightForWidth())
        self.selectboardButton.setSizePolicy(sizePolicy)
        self.selectboardButton.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.selectboardButton.setFont(font)
        self.selectboardButton.setStyleSheet("background-color: rgb(200, 200, 200)")
        self.selectboardButton.setFlat(False)
        self.selectboardButton.setObjectName("selectboardButton")
        self.verticalLayout.addWidget(self.selectboardButton)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.searchpageLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.searchpageLineEdit.setMinimumSize(QtCore.QSize(35, 0))
        self.searchpageLineEdit.setMaximumSize(QtCore.QSize(35, 16777215))
        self.searchpageLineEdit.setText("")
        self.searchpageLineEdit.setMaxLength(14)
        self.searchpageLineEdit.setObjectName("searchpageLineEdit")
        self.horizontalLayout_4.addWidget(self.searchpageLineEdit)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 12, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.nicknameLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.nicknameLineEdit.setText("")
        self.nicknameLineEdit.setMaxLength(14)
        self.nicknameLineEdit.setObjectName("nicknameLineEdit")
        self.horizontalLayout.addWidget(self.nicknameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, 13, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.articleCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.articleCheckBox.sizePolicy().hasHeightForWidth())
        self.articleCheckBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("굴림")
        self.articleCheckBox.setFont(font)
        self.articleCheckBox.setObjectName("articleCheckBox")
        self.horizontalLayout_2.addWidget(self.articleCheckBox, 0, QtCore.Qt.AlignLeft)
        self.commentCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentCheckBox.sizePolicy().hasHeightForWidth())
        self.commentCheckBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("굴림")
        self.commentCheckBox.setFont(font)
        self.commentCheckBox.setObjectName("commentCheckBox")
        self.horizontalLayout_2.addWidget(self.commentCheckBox, 0, QtCore.Qt.AlignLeft)
        self.searchButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("background-color: rgb(200, 200, 200)")
        self.searchButton.setFlat(False)
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout_2.addWidget(self.searchButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, -1, 13, -1)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.cancelButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.cancelButton.setFont(font)
        self.cancelButton.setStyleSheet("background-color: rgb(200, 200, 200)")
        self.cancelButton.setFlat(False)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_5.addWidget(self.cancelButton, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(16)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.infoLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoLabel.sizePolicy().hasHeightForWidth())
        self.infoLabel.setSizePolicy(sizePolicy)
        self.infoLabel.setMinimumSize(QtCore.QSize(115, 0))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.infoLabel.setFont(font)
        self.infoLabel.setText("")
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.horizontalLayout_3.addWidget(self.infoLabel)
        self.detailButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detailButton.sizePolicy().hasHeightForWidth())
        self.detailButton.setSizePolicy(sizePolicy)
        self.detailButton.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.detailButton.setFont(font)
        self.detailButton.setStyleSheet("background-color: rgb(200, 200, 200)")
        self.detailButton.setFlat(False)
        self.detailButton.setObjectName("detailButton")
        self.horizontalLayout_3.addWidget(self.detailButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.selectboardButton.setText(_translate("Form", "게시판 선택"))
        self.label_3.setText(_translate("Form", "탐색 페이지 수"))
        self.label_4.setText(_translate("Form", "페이지"))
        self.label.setText(_translate("Form", "닉네임"))
        self.articleCheckBox.setText(_translate("Form", "게시글"))
        self.commentCheckBox.setText(_translate("Form", "댓글"))
        self.searchButton.setText(_translate("Form", "검색"))
        self.cancelButton.setText(_translate("Form", "중지"))
        self.detailButton.setText(_translate("Form", "자세히"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

