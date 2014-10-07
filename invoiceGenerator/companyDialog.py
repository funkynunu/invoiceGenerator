# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'companyDialog.ui'
#
# Created: Tue Jul 22 10:11:28 2014
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CompanyDialog(object):
    def setupUi(self, CompanyDialog):
        CompanyDialog.setObjectName("CompanyDialog")
        CompanyDialog.resize(242, 145)
        self.gridLayout = QtWidgets.QGridLayout(CompanyDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(CompanyDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.bankName = QtWidgets.QLineEdit(CompanyDialog)
        self.bankName.setObjectName("bankName")
        self.gridLayout.addWidget(self.bankName, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(CompanyDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.branchCode = QtWidgets.QLineEdit(CompanyDialog)
        self.branchCode.setObjectName("branchCode")
        self.gridLayout.addWidget(self.branchCode, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(CompanyDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.customerNo = QtWidgets.QLineEdit(CompanyDialog)
        self.customerNo.setObjectName("customerNo")
        self.gridLayout.addWidget(self.customerNo, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(CompanyDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.taxNo = QtWidgets.QLineEdit(CompanyDialog)
        self.taxNo.setObjectName("taxNo")
        self.gridLayout.addWidget(self.taxNo, 3, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(CompanyDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.label.setBuddy(self.bankName)
        self.label_2.setBuddy(self.branchCode)
        self.label_3.setBuddy(self.customerNo)
        self.label_4.setBuddy(self.taxNo)

        self.retranslateUi(CompanyDialog)
        self.buttonBox.accepted.connect(CompanyDialog.accept)
        self.buttonBox.rejected.connect(CompanyDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CompanyDialog)

    def retranslateUi(self, CompanyDialog):
        _translate = QtCore.QCoreApplication.translate
        CompanyDialog.setWindowTitle(_translate("CompanyDialog", "Company Details"))
        self.label.setText(_translate("CompanyDialog", "Bank name"))
        self.label_2.setText(_translate("CompanyDialog", "Branch code"))
        self.label_3.setText(_translate("CompanyDialog", "Customer number"))
        self.label_4.setText(_translate("CompanyDialog", "Tax number"))

