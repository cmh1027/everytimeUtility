# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plaster.ui'
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
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 231, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(5, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(11, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.searchednicknameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchednicknameLabel.sizePolicy().hasHeightForWidth())
        self.searchednicknameLabel.setSizePolicy(sizePolicy)
        self.searchednicknameLabel.setMinimumSize(QtCore.QSize(0, 28))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.searchednicknameLabel.setFont(font)
        self.searchednicknameLabel.setText("")
        self.searchednicknameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.searchednicknameLabel.setObjectName("searchednicknameLabel")
        self.verticalLayout_2.addWidget(self.searchednicknameLabel)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 2, 15, 2)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
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
        self.horizontalLayout.addWidget(self.selectboardButton)
        self.plasterWordButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plasterWordButton.sizePolicy().hasHeightForWidth())
        self.plasterWordButton.setSizePolicy(sizePolicy)
        self.plasterWordButton.setMinimumSize(QtCore.QSize(0, 0))
        self.plasterWordButton.setMaximumSize(QtCore.QSize(60, 16777215))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.plasterWordButton.setFont(font)
        self.plasterWordButton.setStyleSheet("background-color: rgb(200, 200, 200)")
        self.plasterWordButton.setFlat(False)
        self.plasterWordButton.setObjectName("plasterWordButton")
        self.horizontalLayout.addWidget(self.plasterWordButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(15, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.articleplasterCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.articleplasterCheckBox.sizePolicy().hasHeightForWidth())
        self.articleplasterCheckBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("굴림")
        self.articleplasterCheckBox.setFont(font)
        self.articleplasterCheckBox.setChecked(True)
        self.articleplasterCheckBox.setObjectName("articleplasterCheckBox")
        self.horizontalLayout_3.addWidget(self.articleplasterCheckBox)
        self.commentplasterCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentplasterCheckBox.sizePolicy().hasHeightForWidth())
        self.commentplasterCheckBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("굴림")
        self.commentplasterCheckBox.setFont(font)
        self.commentplasterCheckBox.setChecked(True)
        self.commentplasterCheckBox.setObjectName("commentplasterCheckBox")
        self.horizontalLayout_3.addWidget(self.commentplasterCheckBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(15, -1, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.promptremoveCheckBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.promptremoveCheckBox.sizePolicy().hasHeightForWidth())
        self.promptremoveCheckBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("굴림")
        self.promptremoveCheckBox.setFont(font)
        self.promptremoveCheckBox.setChecked(True)
        self.promptremoveCheckBox.setObjectName("promptremoveCheckBox")
        self.horizontalLayout_6.addWidget(self.promptremoveCheckBox)
        self.isanonymFlag = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.isanonymFlag.sizePolicy().hasHeightForWidth())
        self.isanonymFlag.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("굴림")
        self.isanonymFlag.setFont(font)
        self.isanonymFlag.setChecked(True)
        self.isanonymFlag.setObjectName("isanonymFlag")
        self.horizontalLayout_6.addWidget(self.isanonymFlag)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(5, -1, 0, -1)
        self.horizontalLayout_4.setSpacing(12)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.retryLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.retryLineEdit.setMinimumSize(QtCore.QSize(35, 0))
        self.retryLineEdit.setMaximumSize(QtCore.QSize(35, 16777215))
        self.retryLineEdit.setMaxLength(2)
        self.retryLineEdit.setObjectName("retryLineEdit")
        self.horizontalLayout_4.addWidget(self.retryLineEdit)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(5, -1, 0, -1)
        self.horizontalLayout_5.setSpacing(12)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.iterationLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.iterationLineEdit.setMinimumSize(QtCore.QSize(35, 0))
        self.iterationLineEdit.setMaximumSize(QtCore.QSize(35, 16777215))
        self.iterationLineEdit.setMaxLength(14)
        self.iterationLineEdit.setObjectName("iterationLineEdit")
        self.horizontalLayout_5.addWidget(self.iterationLineEdit)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(4, -1, -1, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.articleRadioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.articleRadioButton.sizePolicy().hasHeightForWidth())
        self.articleRadioButton.setSizePolicy(sizePolicy)
        self.articleRadioButton.setChecked(True)
        self.articleRadioButton.setObjectName("articleRadioButton")
        self.cycleGroup = QtWidgets.QButtonGroup(Form)
        self.cycleGroup.setObjectName("cycleGroup")
        self.cycleGroup.addButton(self.articleRadioButton)
        self.horizontalLayout_7.addWidget(self.articleRadioButton)
        self.stringRadioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.stringRadioButton.setObjectName("stringRadioButton")
        self.cycleGroup.addButton(self.stringRadioButton)
        self.horizontalLayout_7.addWidget(self.stringRadioButton)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startplatsterButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startplatsterButton.sizePolicy().hasHeightForWidth())
        self.startplatsterButton.setSizePolicy(sizePolicy)
        self.startplatsterButton.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.startplatsterButton.setFont(font)
        self.startplatsterButton.setStyleSheet("background-color: rgb(200, 200, 200)")
        self.startplatsterButton.setFlat(False)
        self.startplatsterButton.setObjectName("startplatsterButton")
        self.horizontalLayout_2.addWidget(self.startplatsterButton)
        self.cancelplasterButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelplasterButton.sizePolicy().hasHeightForWidth())
        self.cancelplasterButton.setSizePolicy(sizePolicy)
        self.cancelplasterButton.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.cancelplasterButton.setFont(font)
        self.cancelplasterButton.setStyleSheet("background-color: rgb(200, 200, 200)")
        self.cancelplasterButton.setFlat(False)
        self.cancelplasterButton.setObjectName("cancelplasterButton")
        self.horizontalLayout_2.addWidget(self.cancelplasterButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.selectboardButton.setText(_translate("Form", "게시판 선택"))
        self.plasterWordButton.setText(_translate("Form", "문자열"))
        self.articleplasterCheckBox.setText(_translate("Form", "게시글"))
        self.commentplasterCheckBox.setText(_translate("Form", "댓글"))
        self.promptremoveCheckBox.setText(_translate("Form", "즉시 삭제"))
        self.isanonymFlag.setText(_translate("Form", "익명"))
        self.label_3.setText(_translate("Form", "실패시 재시도 횟수"))
        self.retryLineEdit.setText(_translate("Form", "1"))
        self.label_4.setText(_translate("Form", "번"))
        self.label_5.setText(_translate("Form", "반복 횟수"))
        self.iterationLineEdit.setText(_translate("Form", "4"))
        self.label_6.setText(_translate("Form", "번"))
        self.articleRadioButton.setText(_translate("Form", "글 기준"))
        self.stringRadioButton.setText(_translate("Form", "문자열 기준"))
        self.startplatsterButton.setText(_translate("Form", "Go!"))
        self.cancelplasterButton.setText(_translate("Form", "중단"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
