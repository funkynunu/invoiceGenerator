import re
import pickle

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QComboBox, \
    QTreeWidgetItem

from PyQt5.QtPrintSupport import QAbstractPrintDialog, QPrintDialog, QPrinter
from PyQt5.QtCore import QUrl, QObject, pyqtSlot


# from iGHtmlController import HtmlController
from iGModel import Model
#from iGUi import Ui_MainWindow
from mainDialog import Ui_MainWindow

from preferencesDialog import Ui_Dialog
#from preferencesDialog import Ui_Dialog
from storeDialog import Ui_StoreDialog
from clientDialog import Ui_ClientDialog
from lineItemsDialog import Ui_LineItemsDialog
from companyDialog import Ui_CompanyDialog

import os, sys

class Controller(QMainWindow):
    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.ui = Ui_MainWindow()

# http://stackoverflow.com/questions/4934806/python-how-to-find-scripts-directory
        self.baseUrl = QUrl.fromLocalFile(__file__)

        self.ui.setupUi(self)

        self.model = Model()

        #self.htmlController = HtmlController(self.model, self.ui, self)

        self.initializeMainWindow()

        # need to pass it the same values passed to preview and a
        # expose self.htmlController
        # 1st variable is the name that will be used in the js to reference the 2nd variable
        # i.e. whenever the js calls self.controller is will use the variable name 'controller'
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

    def initializeMainWindow(self):
        print("controller.initializeMainWindow")

        # populate MainWindow with data
        self.setInvoiceTreeList( \
             self.model.getInvoiceTreeList(self.model.getSortByOptions()[0]))

        self.ui.sortByCb.clear()
        self.ui.sortByCb.addItems(self.model.getSortByOptions())

        self.ui.clientsCb.clear()
        self.ui.clientsCb.addItems(self.model.getClientNames())

        self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

        self.ui.currInvNo.setText(self.model.getCurrentInvoiceNo())

        self.setCurrentView()

    def setPreview(self):
        print("controller.setPreview")
        self.ui.webView.setHtml(self.model.getCurrentInvoice(), self.baseUrl)

    def configurePreferences(self):
        print("controller.configurePreferences")
#        preferenceDialog = Preferences(self)
#        preferenceDialog.show()
        preferencesDialog = QDialog(self)
        preferencesUi = Ui_Dialog()
        preferencesUi.setupUi(preferencesDialog)

        # read preferences and set values in dialog
        try:
            with open('preferences.pickle', 'rb') as f:
                preferences = pickle.load(f)

                preferencesUi.dbIp.setText(preferences['host'])
                preferencesUi.dbUsername.setText(preferences['username'])
                preferencesUi.dbPassword.setText(preferences['password'])
        except:
            print('Preferences not found')
            preferencesUi.dbIp.setText("")
            preferencesUi.dbUsername.setText("")
            preferencesUi.dbPassword.setText("")

        # if dialog is displayed
        if preferencesDialog.exec_():
            #extract values from dialog
            preferences = {}
            preferences['host'] = preferencesUi.dbIp.text()
            preferences['username'] = preferencesUi.dbUsername.text()
            preferences['password'] = preferencesUi.dbPassword.text()
            preferences['database'] = 'Roland Richter'

            with open('preferences.pickle', 'wb') as f:
                preferences = pickle.dump(preferences, f)

    def invoiceNoChanged(self):
        " check if text entered is old invoice no "
        # if yes, get invoice and display, set view to previous
        # of no, initialise invoice via reset
        print("controller.invoiceNoChanged")
        if self.model.previousInvoice(self.ui.currInvNo.text()) != None:
            self.ui.webView.setHtml \
                (self.model.getPreviewPreviousInvoice(self.ui.currInvNo.text()), self.baseUrl)
            self.setPreviousView()
        else:
        # trying something
        # initialize initial current invoice with invoice number
            self.model.initializeCurrentInvoice()
            self.model.currentInvoice.invoiceNo = self.ui.currInvNo.text()
        # display current invoice
            self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(),self.baseUrl)
            self.setCurrentView()


            #self.reset()


    def treeListSelected(self):
        print("controller.treeListSelected")
        # https://docs.python.org/3/library/re.html
        # is clicked item an invoice?
        if re.search(r"[0-9]+\/[0-9]+",self.ui.invList.currentItem().text(0)):
            # make sure selection is not a date
            if not re.search(r"[0-9]+\/[0-9]+\/[0-9]+",self.ui.invList.currentItem().text(0)):
                self.ui.webView.setHtml \
                    (self.model.getPreviewPreviousInvoice \
                    (self.ui.invList.currentItem().text(0)), self.baseUrl)

            # previous does not get popups to change data!!!
            #self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

                self.model.setDisplayedInvoiceNo \
                    (self.ui.invList.currentItem().text(0))
                self.setPreviousView()

    def reset(self):
        print("controller.reset")
        self.ui.webView.setHtml(self.model.getInitialPreview(), self.baseUrl)
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)
        self.setCurrentView()
        self.ui.currInvNo.setText(self.model.getCurrentInvoiceNo())


    def save(self):
        print("controller.save")
        self.model.saveCurrentInvoice()

        # reinitialize model object by creating new model object
        self.model = Model()

        self.initializeMainWindow()

    def print(self):
        print("controller.print")
        editor = self.ui.webView
        printer = QPrinter()

        #print(printer, self)
        dialog = QPrintDialog(printer, self)
        dialog.setWindowTitle("Print Document")

        if dialog.exec_() != QDialog.Accepted:
            return

        editor.print_(printer)

    def companyAccept(self):
        print("controller.Company Accept")

    def setAsCurrent(self):
        print("controller.setAsCurrent")
        invoice = self.model.getPreviousInvoice(self.ui.invList.currentItem().text(0))

        self.model.setCurrentInvoice \
            (self.model.getPreviousInvoice \
            (self.ui.invList.currentItem().text(0)))

        # view calls
        self.ui.currInvNo.setText(self.ui.invList.currentItem().text(0))
        self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

#        self.htmlController.setInvoice(self.model.getCurrentInvoice())

        self.setCurrentView()

        #self.updateDialogs(self.model.getCurrentInvoice())

    def about(self):
        print("controller.about")
        QMessageBox.about(self, "About Application",
                "The Invoice Generator - powering invoices everywhere!")

    def setInvoiceTreeList(self, treeList):
        print("controller.setInvoiceTreeList")

        self.ui.invList.clear()
        parentItem = self.ui.invList.invisibleRootItem()

        # first add key as parent then loop at value list
        for category in treeList.keys():
            rootChildItem = QTreeWidgetItem()
            rootChildItem.setText(0, str(category))
            # add children to rootChild
            for inv in treeList[category]:
                invNo = QTreeWidgetItem()
                invNo.setText(0, inv)
                rootChildItem.addChild(invNo)
            # add rootChild to invList
            parentItem.addChild(rootChildItem)

    def setViewToCurrentInvoice(self, event):
        print("controller.setViewToCurrentInvoice")
        self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)
        self.setCurrentView()

    """
    Offer to save an unsaved invoice and then exit app
    """
    def exitApp(self):
        print("controller.exitApp")
        QApplication.quit()

    """
    Updates invoice with selected client's data
    """
    def clientChanged(self):
        print("controller.clientChanged")
        self.model.setClient(self.model.getClientObject(self.ui.clientsCb.currentText()))

        self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

    """
    Updates tree list with sort prefer
    """
    def sortByOrderChanged(self):
        print("controller.sortByChanged")
        # self.setInvoiceTreeList(self.model.getInvoiceTreeList \
        #     (self.model.getSelectedSortByOptions \
        #     (self.ui.sortByCb.currentIndex())))
        self.setInvoiceTreeList(self.model.getInvoiceTreeList(self.ui.sortByCb.currentText()))
        self.setPreviousView()

    """
    Updates screen with the data from the previous selected invoice
    """
    def previousInvSelected(self):
        print("controller.previousInvSelected")
        print(self.getSelectedInv())

    """
    Updates invoice with current invoice data
    """
    # def currentInvoiceSelected(self):
    #     print("controller.currentInvoiceSelected")
    #     self.setCurrentView()

    """
    Cause I'm lazy
    """
    def displayInvoice(self, Invoice):
        print("controller.displayInvoice")

    """
    Turns required screen widgets on/off as needed when viewing a previous invoice
    """
    def setPreviousView(self):
        print("controller.setPreviousView")
        # greys out options that are not available when viewing previous invoices
        self.ui.resetBtn.setEnabled(False)
        self.ui.saveBtn.setEnabled(False)
        self.ui.clientsCb.setEnabled(False)
        self.ui.viewCurrentBtn.setEnabled(True)
        self.ui.setCurrentBtn.setEnabled(True)

    """
    Turns required screen widgets on/off as needed when editing an invoice
    """
    def setCurrentView(self):
        print("controller.setCurrentView")
        # enables options that are were not available when viewing previous invoices
        self.ui.resetBtn.setEnabled(True)
        self.ui.saveBtn.setEnabled(True)
        self.ui.clientsCb.setEnabled(True)
        self.ui.viewCurrentBtn.setEnabled(False)
        self.ui.setCurrentBtn.setEnabled(False)
        #self.htmlController.updateDialogs(self.model.getCurrentInvoice())

    def setDialogs(self, store1, store2, client, lineItems, company):
        self.uiStore1 = store1
        self.uiStore2 = store2
        self.uiClient = client
        self.uiLineItems = lineItems
        self.uiCompany = company

    @pyqtSlot()
    def displayStore1Dialog(self):
        # if 'ok' then update current invoice
        # and webview
        print("controller.displayStore1Dialog")
        store1Dialog = QDialog(self)
        store1Ui = Ui_StoreDialog()
        store1Ui.setupUi(store1Dialog)

        cInvoice = self.model.getCurrentInvoice()

        # set values in dialog
        store1Ui.name.setText(cInvoice.store1.name)
        store1Ui.manager.setText(cInvoice.store1.manager)
        store1Ui.address1.setText(cInvoice.store1.address1)
        store1Ui.address2.setText(cInvoice.store1.address2)
        store1Ui.telNo.setText(cInvoice.store1.telNo)

        # if dialog is displayed
        if store1Dialog.exec_():
            #extract values from dialog
            setattr(cInvoice.store1,"name",store1Ui.name.text())
            setattr(cInvoice.store1,"manager",store1Ui.manager.text())
            setattr(cInvoice.store1,"address1",store1Ui.address1.text())
            setattr(cInvoice.store1,"address2",store1Ui.address2.text())
            setattr(cInvoice.store1,"telNo",store1Ui.telNo.text())
            #self.model.getCurrentInvoice().store1.timestamp

            self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
            self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

    @pyqtSlot()
    def displayStore2Dialog(self):
        # if 'ok' then update current invoice
        # and webview
        print("controller.displayStore2Dialog")
        store2Dialog = QDialog(self)
        store2Ui = Ui_StoreDialog()
        store2Ui.setupUi(store2Dialog)

        cInvoice = self.model.getCurrentInvoice()

        # set values in dialog
        store2Ui.name.setText(cInvoice.store2.name)
        store2Ui.manager.setText(cInvoice.store2.manager)
        store2Ui.address1.setText(cInvoice.store2.address1)
        store2Ui.address2.setText(cInvoice.store2.address2)
        store2Ui.telNo.setText(cInvoice.store2.telNo)

        # if dialog is displayed
        if store2Dialog.exec_():
            #extract values from dialog
            setattr(cInvoice.store2,"name",store2Ui.name.text())
            setattr(cInvoice.store2,"manager",store2Ui.manager.text())
            setattr(cInvoice.store2,"address1",store2Ui.address1.text())
            setattr(cInvoice.store2,"address2",store2Ui.address2.text())
            setattr(cInvoice.store2,"telNo",store2Ui.telNo.text())

            self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
            self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

    @pyqtSlot()
    def displayClientDialog(self):
        print("controller.displayClientDialog")
        clientDialog = QDialog(self)
        clientUi = Ui_ClientDialog()
        clientUi.setupUi(clientDialog)

        cInvoice = self.model.getCurrentInvoice()

        # set values in dialog from current invoice
        clientUi.businessName.setText(cInvoice.client.businessName)
        clientUi.contactName.setText(cInvoice.client.contactName)
        clientUi.address1.setText(cInvoice.client.address1)
        clientUi.address2.setText(cInvoice.client.address2)

        # if dialog is displayed
        if clientDialog.exec_():
            #extract values from dialog
            setattr(cInvoice.client,"businessName",clientUi.businessName.text())
            setattr(cInvoice.client,"contactName",clientUi.contactName.text())
            setattr(cInvoice.client,"address1",clientUi.address1.text())
            setattr(cInvoice.client,"address2",clientUi.address2.text())

            self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
            self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

    @pyqtSlot()
    def displayLineItemsDialog(self):
        print("controller.displayLineItemsDialog")
        lineItemsDialog = QDialog(self)
        lineItemsUi = Ui_LineItemsDialog()
        lineItemsUi.setupUi(lineItemsDialog)

        cInvoice = self.model.getCurrentInvoice()

        # set values in dialog
        lineItemsUi.note.setPlainText(cInvoice.note)
        lineNo = 0

        # todo: find a better way to do this
        for li in self.model.getCurrentInvoice().lineItems:
            lineNo += 1
            if lineNo == 1:
                lineItemsUi.quantity1.setText(str(li.quantity))
                lineItemsUi.description1.setText(li.description)
                lineItemsUi.price1.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory1.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory1.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat1.setText(str(li.getVatAmount()))
                # total after tax
                lineItemsUi.total1.setText(str(li.getPriceAfterVat()))

            elif lineNo == 2:
                lineItemsUi.quantity2.setText(str(li.quantity))
                lineItemsUi.description2.setText(li.description)
                lineItemsUi.price2.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory2.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory2.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat2.setText(str(li.getVatAmount()))

                lineItemsUi.total2.setText(str(li.getPriceAfterVat()))

            elif lineNo == 3:
                lineItemsUi.quantity3.setText(str(li.quantity))
                lineItemsUi.description3.setText(li.description)
                lineItemsUi.price3.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory3.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory3.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat3.setText(str(li.getVatAmount()))

                lineItemsUi.total3.setText(str(li.getPriceAfterVat()))
            elif lineNo == 4:
                lineItemsUi.quantity4.setText(str(li.quantity))
                lineItemsUi.description4.setText(li.description)
                lineItemsUi.price4.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory4.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory4.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat4.setText(str(li.getVatAmount()))

                lineItemsUi.total4.setText(str(li.getPriceAfterVat()))
            elif lineNo == 5:
                lineItemsUi.quantity5.setText(str(li.quantity))
                lineItemsUi.description5.setText(li.description)
                lineItemsUi.price5.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory5.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory5.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat5.setText(str(li.getVatAmount()))

                lineItemsUi.total5.setText(str(li.getPriceAfterVat()))
            elif lineNo == 6:
                lineItemsUi.quantity6.setText(str(li.quantity))
                lineItemsUi.description6.setText(li.description)
                lineItemsUi.price6.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory6.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory6.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat6.setText(str(li.getVatAmount()))

                lineItemsUi.total6.setText(str(li.getPriceAfterVat()))
            elif lineNo == 7:
                lineItemsUi.quantity7.setText(str(li.quantity))
                lineItemsUi.description7.setText(li.description)
                lineItemsUi.price7.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory7.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory7.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat7.setText(str(li.getVatAmount()))

                lineItemsUi.total7.setText(str(li.getPriceAfterVat()))
            elif lineNo == 8:
                lineItemsUi.quantity8.setText(str(li.quantity))
                lineItemsUi.description8.setText(li.description)
                lineItemsUi.price8.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory8.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory8.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat8.setText(str(li.getVatAmount()))

                lineItemsUi.total8.setTextstr(str(li.getPriceAfterVat()))
            elif lineNo == 9:
                lineItemsUi.quantity9.setText(str(li.quantity))
                lineItemsUi.description9.setText(li.description)
                lineItemsUi.price9.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory9.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory9.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat9.setText(str(li.getVatAmount()))

                lineItemsUi.total9.setText(str(li.getPriceAfterVat()))
            elif lineNo == 10:
                lineItemsUi.quantity10.setText(str(li.quantity))
                lineItemsUi.description10.setText(li.description)
                lineItemsUi.price10.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.vatCategory == '7':
                    lineItemsUi.vatCategory10.setCurrentIndex(0)
                elif li.vatCategory == '19':
                    lineItemsUi.vatCategory10.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat10.setText(str(li.getVatAmount()))

                lineItemsUi.total10.setText(str(li.getPriceAfterVat()))

        # if dialog is displayed
        if lineItemsDialog.exec_():
            #extract values from dialog
            #lineItemsUi.note.setPlainText(cInvoice.getNote())
            setattr(cInvoice,"note",lineItemsUi.note.document().toPlainText())

            # line items
            # e.g. [['111/13', 1, 1, '12x', 'Roses', 10.0, '7', 0.7, 10.7],
            #       ['111/13', 1, 2, '1x', 'Pot', 50.0, '7', 3.5, 53.5],
            #       ['111/13', 1, 3, '6x', 'Sausages', 10.0, '19', 1.9, 11.9]]
            lineItems = []

            #version = int(cInvoice.getLineItems()[0].getVersion())
            version = int(cInvoice.version)

            # line 1
            # todo: seriously, find a better way to do this!!!
            if not lineItemsUi.quantity1.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity1.text()))
                lineItem.append(lineItemsUi.description1.text())
                lineItem.append(float(lineItemsUi.price1.text()))

                if lineItemsUi.vatCategory1.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory1.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory1.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat1.text()))
                lineItem.append(float(lineItemsUi.total1.text()))

                lineItems.append(lineItem)

            # line 2
            if not lineItemsUi.quantity2.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity2.text()))
                lineItem.append(lineItemsUi.description2.text())
                lineItem.append(float(lineItemsUi.price2.text()))

                if lineItemsUi.vatCategory2.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory2.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory2.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat2.text()))
                lineItem.append(float(lineItemsUi.total2.text()))

                lineItems.append(lineItem)

                # line 3.
            if not lineItemsUi.quantity3.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity3.text()))
                lineItem.append(lineItemsUi.description3.text())
                lineItem.append(float(lineItemsUi.price3.text()))

                if lineItemsUi.vatCategory3.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory3.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory3.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat3.text()))
                lineItem.append(float(lineItemsUi.total3.text()))

                lineItems.append(lineItem)

                # line 4.
            if not lineItemsUi.quantity4.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity4.text()))
                lineItem.append(lineItemsUi.description4.text())
                lineItem.append(float(lineItemsUi.price4.text()))

                if lineItemsUi.vatCategory4.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory4.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory4.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat4.text()))
                lineItem.append(float(lineItemsUi.total4.text()))

                lineItems.append(lineItem)

                # line 5.
            if not lineItemsUi.quantity5.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity5.text()))
                lineItem.append(lineItemsUi.description5.text())
                lineItem.append(float(lineItemsUi.price5.text()))

                if lineItemsUi.vatCategory5.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory5.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory5.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat5.text()))
                lineItem.append(float(lineItemsUi.total5.text()))

                lineItems.append(lineItem)

                # line 6.
            if not lineItemsUi.quantity6.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity6.text()))
                lineItem.append(lineItemsUi.description6.text())
                lineItem.append(float(lineItemsUi.price6.text()))

                if lineItemsUi.vatCategory6.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory6.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory6.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat6.text()))
                lineItem.append(float(lineItemsUi.total6.text()))

                lineItems.append(lineItem)

                # line 7.
            if not lineItemsUi.quantity7.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity7.text()))
                lineItem.append(lineItemsUi.description7.text())
                lineItem.append(float(lineItemsUi.price7.text()))

                if lineItemsUi.vatCategory7.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory7.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory7.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat7.text()))
                lineItem.append(float(lineItemsUi.total7.text()))

                lineItems.append(lineItem)

                # line 8.
            if not lineItemsUi.quantity8.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity8.text()))
                lineItem.append(lineItemsUi.description8.text())
                lineItem.append(float(lineItemsUi.price8.text()))

                if lineItemsUi.vatCategory8.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory8.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory8.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat8.text()))
                lineItem.append(float(lineItemsUi.total8.text()))

                lineItems.append(lineItem)

                # line 9.
            if not lineItemsUi.quantity9.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity9.text()))
                lineItem.append(lineItemsUi.description9.text())
                lineItem.append(float(lineItemsUi.price9.text()))

                if lineItemsUi.vatCategory9.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory9.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory9.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat9.text()))
                lineItem.append(float(lineItemsUi.total9.text()))

                lineItems.append(lineItem)

                # line 10.
            if not lineItemsUi.quantity10.text()=="":
                lineItem = []
                lineItem.append(version)
                lineItem.append(int(lineItemsUi.quantity10.text()))
                lineItem.append(lineItemsUi.description10.text())
                lineItem.append(float(lineItemsUi.price10.text()))

                if lineItemsUi.vatCategory10.currentText() == '0%':
                    lineItem.append('0')
                elif lineItemsUi.vatCategory10.currentText() == '7%':
                    lineItem.append('7')
                elif lineItemsUi.vatCategory10.currentText() == '19%':
                    lineItem.append('19')

                lineItem.append(float(lineItemsUi.vat10.text()))
                lineItem.append(float(lineItemsUi.total10.text()))

                lineItems.append(lineItem)

            #setattr(cInvoice, "lineItems", lineItems)
            cInvoice.setLineItems(lineItems)

            self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
            self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)

    @pyqtSlot()
    def displayCompanyDialog(self):
        print("controller.displayCompanyDialog")
        companyDialog = QDialog(self)
        companyUi = Ui_CompanyDialog()
        companyUi.setupUi(companyDialog)

        cInvoice = self.model.getCurrentInvoice()

        # set values in dialog
        companyUi.bankName.setText(cInvoice.company.bankName)
        companyUi.branchCode.setText(cInvoice.company.branchCode)
        companyUi.taxNo.setText(cInvoice.company.taxNo)
        companyUi.customerNo.setText(cInvoice.company.customerNo)

        # if dialog is displayed
        if companyDialog.exec_():
            #extract values from dialog and change current invoice
            self.model.getCurrentInvoice().company.bankName = companyUi.bankName.text()
            self.model.getCurrentInvoice().company.branchCode = companyUi.branchCode.text()
            self.model.getCurrentInvoice().company.taxNo = companyUi.taxNo.text()
            self.model.getCurrentInvoice().company.customerNo = companyUi.customerNo.text()

            self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice(), self.baseUrl)
            self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("controller", self)
