# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'storeDialog.ui'
#
# Created: Sat Jul 26 12:42:59 2014
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StoreDialog(object):
    def setupUi(self, StoreDialog):
        StoreDialog.setObjectName("StoreDialog")
        StoreDialog.resize(300, 171)
        self.gridLayout = QtWidgets.QGridLayout(StoreDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(StoreDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.name = QtWidgets.QLineEdit(StoreDialog)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(StoreDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.manager = QtWidgets.QLineEdit(StoreDialog)
        self.manager.setObjectName("manager")
        self.gridLayout.addWidget(self.manager, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(StoreDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.address1 = QtWidgets.QLineEdit(StoreDialog)
        self.address1.setObjectName("address1")
        self.gridLayout.addWidget(self.address1, 2, 1, 1, 1)
        self.address2 = QtWidgets.QLineEdit(StoreDialog)
        self.address2.setObjectName("address2")
        self.gridLayout.addWidget(self.address2, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(StoreDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.telNo = QtWidgets.QLineEdit(StoreDialog)
        self.telNo.setObjectName("telNo")
        self.gridLayout.addWidget(self.telNo, 4, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(StoreDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.label.setBuddy(self.name)
        self.label_2.setBuddy(self.manager)
        self.label_3.setBuddy(self.address1)
        self.label_4.setBuddy(self.telNo)

        self.retranslateUi(StoreDialog)
        self.buttonBox.accepted.connect(StoreDialog.accept)
        self.buttonBox.rejected.connect(StoreDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StoreDialog)

    def retranslateUi(self, StoreDialog):
        _translate = QtCore.QCoreApplication.translate
        StoreDialog.setWindowTitle(_translate("StoreDialog", "Store details"))
        self.label.setText(_translate("StoreDialog", "Store name"))
        self.label_2.setText(_translate("StoreDialog", "Store manager"))
        self.label_3.setText(_translate("StoreDialog", "Address"))
        self.label_4.setText(_translate("StoreDialog", "Telephone"))

