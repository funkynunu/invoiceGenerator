# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferencesDialog.ui'
#
# Created: Fri Nov 14 11:14:49 2014
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 119)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dbUsername = QtWidgets.QLineEdit(Dialog)
        self.dbUsername.setObjectName("dbUsername")
        self.gridLayout.addWidget(self.dbUsername, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.dbPassword = QtWidgets.QLineEdit(Dialog)
        self.dbPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.dbPassword.setObjectName("dbPassword")
        self.gridLayout.addWidget(self.dbPassword, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.dbIp = QtWidgets.QLineEdit(Dialog)
        self.dbIp.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.dbIp.setObjectName("dbIp")
        self.gridLayout.addWidget(self.dbIp, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.label.setBuddy(self.dbUsername)
        self.label_2.setBuddy(self.dbPassword)
        self.label_3.setBuddy(self.dbIp)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Datenbank Benutzername"))
        self.label_2.setText(_translate("Dialog", "Datenbank Passwort"))
        self.label_3.setText(_translate("Dialog", "Datenbank IP Adresse"))

