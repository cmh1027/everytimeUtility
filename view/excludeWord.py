# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'excludeWord.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(232, 225)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 157);")
        Dialog.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 190, 131, 32))
        self.buttonBox.setStyleSheet("background-color: rgb(191, 191, 191);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 21))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 150, 211, 22))
        self.layoutWidget.setObjectName("layoutWidget")
        self.excludearticleLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.excludearticleLayout.setContentsMargins(0, 0, 0, 0)
        self.excludearticleLayout.setObjectName("excludearticleLayout")
        self.excludearticleCheckBox = QtWidgets.QCheckBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.excludearticleCheckBox.sizePolicy().hasHeightForWidth())
        self.excludearticleCheckBox.setSizePolicy(sizePolicy)
        self.excludearticleCheckBox.setText("")
        self.excludearticleCheckBox.setObjectName("excludearticleCheckBox")
        self.excludearticleLayout.addWidget(self.excludearticleCheckBox)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.excludearticleLayout.addWidget(self.label_2)
        self.layoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 170, 201, 22))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.excludecommentLayout = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.excludecommentLayout.setContentsMargins(0, 0, 0, 0)
        self.excludecommentLayout.setObjectName("excludecommentLayout")
        self.excludecommentCheckBox = QtWidgets.QCheckBox(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.excludecommentCheckBox.sizePolicy().hasHeightForWidth())
        self.excludecommentCheckBox.setSizePolicy(sizePolicy)
        self.excludecommentCheckBox.setText("")
        self.excludecommentCheckBox.setObjectName("excludecommentCheckBox")
        self.excludecommentLayout.addWidget(self.excludecommentCheckBox)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.excludecommentLayout.addWidget(self.label_3)
        self.excludewordTextEdit = QtWidgets.QTextEdit(Dialog)
        self.excludewordTextEdit.setGeometry(QtCore.QRect(10, 30, 211, 121))
        self.excludewordTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.excludewordTextEdit.setObjectName("excludewordTextEdit")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "exclude"))
        self.label.setText(_translate("Dialog", "각 단어는 엔터로 구분"))
        self.label_2.setText(_translate("Dialog", "해당 단어가 포함된 게시글을 제외"))
        self.label_3.setText(_translate("Dialog", "해당 단어가 포함된 댓글을 제외"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

