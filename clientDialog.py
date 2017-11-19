# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clientDialog.ui'
#
# Created: Fri Nov 14 11:14:42 2014
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ClientDialog(object):
    def setupUi(self, ClientDialog):
        ClientDialog.setObjectName("ClientDialog")
        ClientDialog.resize(300, 145)
        self.gridLayout = QtWidgets.QGridLayout(ClientDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.contactName = QtWidgets.QLineEdit(ClientDialog)
        self.contactName.setObjectName("contactName")
        self.gridLayout.addWidget(self.contactName, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(ClientDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.address2 = QtWidgets.QLineEdit(ClientDialog)
        self.address2.setObjectName("address2")
        self.gridLayout.addWidget(self.address2, 3, 1, 1, 1)
        self.address1 = QtWidgets.QLineEdit(ClientDialog)
        self.address1.setObjectName("address1")
        self.gridLayout.addWidget(self.address1, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(ClientDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ClientDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.businessName = QtWidgets.QLineEdit(ClientDialog)
        self.businessName.setObjectName("businessName")
        self.gridLayout.addWidget(self.businessName, 0, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ClientDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)
        self.label.setBuddy(self.businessName)
        self.label_3.setBuddy(self.address1)
        self.label_2.setBuddy(self.contactName)

        self.retranslateUi(ClientDialog)
        self.buttonBox.accepted.connect(ClientDialog.accept)
        self.buttonBox.rejected.connect(ClientDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientDialog)
        ClientDialog.setTabOrder(self.businessName, self.contactName)
        ClientDialog.setTabOrder(self.contactName, self.address1)
        ClientDialog.setTabOrder(self.address1, self.address2)
        ClientDialog.setTabOrder(self.address2, self.buttonBox)

    def retranslateUi(self, ClientDialog):
        _translate = QtCore.QCoreApplication.translate
        ClientDialog.setWindowTitle(_translate("ClientDialog", "Client Details"))
        self.label.setText(_translate("ClientDialog", "Firmenname"))
        self.label_3.setText(_translate("ClientDialog", "Adresse"))
        self.label_2.setText(_translate("ClientDialog", "Kontaktname"))

