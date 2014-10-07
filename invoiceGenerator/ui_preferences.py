# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_preferences.ui'
#
# Created: Wed Jul 16 14:30:08 2014
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName("Preferences")
        Preferences.resize(300, 119)
        self.gridLayout = QtWidgets.QGridLayout(Preferences)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Preferences)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dbUsername = QtWidgets.QLineEdit(Preferences)
        self.dbUsername.setObjectName("dbUsername")
        self.gridLayout.addWidget(self.dbUsername, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Preferences)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.dbPassword = QtWidgets.QLineEdit(Preferences)
        self.dbPassword.setObjectName("dbPassword")
        self.gridLayout.addWidget(self.dbPassword, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Preferences)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.dbIp = QtWidgets.QLineEdit(Preferences)
        self.dbIp.setEchoMode(QtWidgets.QLineEdit.Password)
        self.dbIp.setObjectName("dbIp")
        self.gridLayout.addWidget(self.dbIp, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Preferences)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(Preferences)
        self.buttonBox.accepted.connect(Preferences.accept)
        self.buttonBox.rejected.connect(Preferences.reject)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        _translate = QtCore.QCoreApplication.translate
        Preferences.setWindowTitle(_translate("Preferences", "Preferences"))
        self.label.setText(_translate("Preferences", "Database username"))
        self.label_2.setText(_translate("Preferences", "Database password"))
        self.label_3.setText(_translate("Preferences", "Database IP address"))

