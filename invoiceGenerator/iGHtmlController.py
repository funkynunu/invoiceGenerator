from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QInputDialog, QDialog

from storeDialog import Ui_StoreDialog
from clientDialog import Ui_ClientDialog
from lineItemsDialog import Ui_LineItemsDialog
from companyDialog import Ui_CompanyDialog

# should receive a pointer to the same class that is used to populate the preview
class HtmlController(QDialog):
    def __init__(self, aModel, aView, parent=None):
# to do:
# initialise values in dialogs
# set ok, cancel events for buttons
        super(HtmlController, self).__init__(parent)

        self.model = aModel
        self.view = aView

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
        store1Dialog = QDialog(self)
        store1Ui = Ui_StoreDialog()
        store1Ui.setupUi(store1Dialog)

        # set values in dialog
        store1Ui.name.setText(self.model.getCurrentInvoice().getStore1().getName())
        store1Ui.manager.setText(self.model.getCurrentInvoice().getStore1().getManager())
        store1Ui.address1.setText(self.model.getCurrentInvoice().getStore1().getAddress1())
        store1Ui.address2.setText(self.model.getCurrentInvoice().getStore1().getAddress2())
        store1Ui.telNo.setText(self.model.getCurrentInvoice().getStore1().getTelNo())

        # if dialog is displayed
        if store1Dialog.exec_():
            #extract values from dialog
            self.model.getCurrentInvoice().getStore1().setName(store1Ui.name.text())
            self.model.getCurrentInvoice().getStore1().setManager(store1Ui.manager.text())
            self.model.getCurrentInvoice().getStore1().setAddress1(store1Ui.address1.text())
            self.model.getCurrentInvoice().getStore1().setAddress2(store1Ui.address2.text())
            self.model.getCurrentInvoice().getStore1().setTelNo(store1Ui.telNo.text())
            #self.model.getCurrentInvoice().getStore1().timestamp
            self.view.webView.setHtml(self.model.getPreviewCurrentInvoice())
            self.view.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self)

    @pyqtSlot()
    def displayStore2Dialog(self):
        # if 'ok' then update current invoice
        # and webview
        store2Dialog = QDialog(self)
        store2Ui = Ui_StoreDialog()
        store2Ui.setupUi(store2Dialog)

        # set values in dialog
        store2Ui.name.setText(self.model.getCurrentInvoice().getStore2().getName())
        store2Ui.manager.setText(self.model.getCurrentInvoice().getStore2().getManager())
        store2Ui.address1.setText(self.model.getCurrentInvoice().getStore2().getAddress1())
        store2Ui.address2.setText(self.model.getCurrentInvoice().getStore2().getAddress2())
        store2Ui.telNo.setText(self.model.getCurrentInvoice().getStore2().getTelNo())

        # if dialog is displayed
        if store2Dialog.exec_():
            #extract values from dialog
            self.model.getCurrentInvoice().getStore2().setName(store2Ui.name.text())
            self.model.getCurrentInvoice().getStore2().setManager(store2Ui.manager.text())
            self.model.getCurrentInvoice().getStore2().setAddress1(store2Ui.address1.text())
            self.model.getCurrentInvoice().getStore2().setAddress2(store2Ui.address2.text())
            self.model.getCurrentInvoice().getStore2().setTelNo(store2Ui.telNo.text())

            self.view.webView.setHtml(self.model.getPreviewCurrentInvoice())
            self.view.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self)

    @pyqtSlot()
    def displayClientDialog(self):
        clientDialog = QDialog(self)
        clientUi = Ui_ClientDialog()
        clientUi.setupUi(clientDialog)

        # set values in dialog
        clientUi.businessName.setText(self.model.getCurrentInvoice().getClient().getBusinessName())
        clientUi.contactName.setText(self.model.getCurrentInvoice().getClient().getContactName())
        clientUi.address1.setText(self.model.getCurrentInvoice().getClient().getAddress1())
        clientUi.address2.setText(self.model.getCurrentInvoice().getClient().getAddress2())

        # if dialog is displayed
        if clientDialog.exec_():
            #extract values from dialog
            self.model.getCurrentInvoice().getClient().setBusinessName(clientUi.businessName.text())
            self.model.getCurrentInvoice().getClient().setContactName(clientUi.contactName.text())
            self.model.getCurrentInvoice().getClient().setAddress1(clientUi.address1.text())
            self.model.getCurrentInvoice().getClient().setAddress2(clientUi.address2.text())

            self.view.webView.setHtml(self.model.getPreviewCurrentInvoice())
            self.view.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self)

    @pyqtSlot()
    def displayLineItemsDialog(self):
        lineItemsDialog = QDialog(self)
        lineItemsUi = Ui_LineItemsDialog()
        lineItemsUi.setupUi(lineItemsDialog)

        # set values in dialog
        lineItemsUi.note.setPlainText(self.model.getCurrentInvoice().getNote())
        lineNo = 0

        # todo: find a better way to do this
        for li in self.model.getCurrentInvoice().lineItems:
            lineNo += 1
            if lineNo == 1:
                lineItemsUi.quantity1.setText(str(li.getQuantity()))
                lineItemsUi.description1.setText(li.getDescription())
                lineItemsUi.price1.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory1.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory1.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat1.setText(str(li.getVatAmount()))
                # total after tax
                lineItemsUi.total1.setText(str(li.getPriceAfterVat()))

            elif lineNo == 2:
                lineItemsUi.quantity2.setText(str(li.getQuantity()))
                lineItemsUi.description2.setText(li.getDescription())
                lineItemsUi.price2.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory2.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory2.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat2.setText(str(li.getVatAmount()))

                lineItemsUi.total2.setText(str(li.getPriceAfterVat()))

            elif lineNo == 3:
                lineItemsUi.quantity3.setText(str(li.getQuantity()))
                lineItemsUi.description3.setText(li.getDescription())
                lineItemsUi.price3.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory3.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory3.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat3.setText(str(li.getVatAmount()))

                lineItemsUi.total3.setText(str(li.getPriceAfterVat()))
            elif lineNo == 4:
                lineItemsUi.quantity4.setText(str(li.getQuantity()))
                lineItemsUi.description4.setText(li.getDescription())
                lineItemsUi.price4.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory4.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory4.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat4.setText(str(li.getVatAmount()))

                lineItemsUi.total4.setText(str(li.getPriceAfterVat()))
            elif lineNo == 5:
                lineItemsUi.quantity5.setText(str(li.getQuantity()))
                lineItemsUi.description5.setText(li.getDescription())
                lineItemsUi.price5.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory5.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory5.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat5.setText(str(li.getVatAmount()))

                lineItemsUi.total5.setText(str(li.getPriceAfterVat()))
            elif lineNo == 6:
                lineItemsUi.quantity6.setText(str(li.getQuantity()))
                lineItemsUi.description6.setText(li.getDescription())
                lineItemsUi.price6.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory6.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory6.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat6.setText(str(li.getVatAmount()))

                lineItemsUi.total6.setText(str(li.getPriceAfterVat()))
            elif lineNo == 7:
                lineItemsUi.quantity7.setText(str(li.getQuantity()))
                lineItemsUi.description7.setText(li.getDescription())
                lineItemsUi.price7.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory7.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory7.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat7.setText(str(li.getVatAmount()))

                lineItemsUi.total7.setText(str(li.getPriceAfterVat()))
            elif lineNo == 8:
                lineItemsUi.quantity8.setText(str(li.getQuantity()))
                lineItemsUi.description8.setText(li.getDescription())
                lineItemsUi.price8.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory8.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory8.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat8.setText(str(li.getVatAmount()))

                lineItemsUi.total8.setTextstr(str(li.getPriceAfterVat()))
            elif lineNo == 9:
                lineItemsUi.quantity9.setText(str(li.getQuantity()))
                lineItemsUi.description9.setText(li.getDescription())
                lineItemsUi.price9.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory9.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory9.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat9.setText(str(li.getVatAmount()))

                lineItemsUi.total9.setText(str(li.getPriceAfterVat()))
            elif lineNo == 10:
                lineItemsUi.quantity10.setText(str(li.getQuantity()))
                lineItemsUi.description10.setText(li.getDescription())
                lineItemsUi.price10.setText(str(li.getPriceBeforeVat()))

                # set combo box based on tax category
                if li.getVatCategory() == '7':
                    lineItemsUi.vatCategory10.setCurrentIndex(0)
                elif li.getVatCategory() == '19':
                    lineItemsUi.vatCategory10.setCurrentIndex(1)

                # vat total
                lineItemsUi.vat10.setText(str(li.getVatAmount()))

                lineItemsUi.total10.setText(str(li.getPriceAfterVat()))

        # if dialog is displayed
        if lineItemsDialog.exec_():
            #extract values from dialog
            #lineItemsUi.note.setPlainText(self.model.getCurrentInvoice().getNote())
            self.model.getCurrentInvoice().setNote(lineItemsUi.note.document().toPlainText())

            # line items
            # e.g. [['111/13', 1, 1, '12x', 'Roses', 10.0, '7', 0.7, 10.7],
            #       ['111/13', 1, 2, '1x', 'Pot', 50.0, '7', 3.5, 53.5],
            #       ['111/13', 1, 3, '6x', 'Sausages', 10.0, '19', 1.9, 11.9]]
            lineItems = []

            #version = int(self.model.getCurrentInvoice().getLineItems()[0].getVersion())
            version = int(self.model.getCurrentInvoice().getVersion())

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

            self.model.getCurrentInvoice().setLineItems(lineItems)

            self.view.webView.setHtml(self.model.getPreviewCurrentInvoice())
            self.view.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self)

    @pyqtSlot()
    def displayCompanyDialog(self):
        companyDialog = QDialog(self)
        companyUi = Ui_CompanyDialog()
        companyUi.setupUi(companyDialog)

        # set values in dialog
        companyUi.bankName.setText(self.model.getCurrentInvoice().getCompany().getBankName())
        companyUi.branchCode.setText(self.model.getCurrentInvoice().getCompany().getBranchCode())
        companyUi.taxNo.setText(self.model.getCurrentInvoice().getCompany().getTaxNo())
        companyUi.customerNo.setText(self.model.getCurrentInvoice().getCompany().getCustomerNo())

        # if dialog is displayed
        if companyDialog.exec_():
            #extract values from dialog and change current invoice
            self.model.getCurrentInvoice().getCompany().setBankName(companyUi.bankName.text())
            self.model.getCurrentInvoice().getCompany().setBranchCode(companyUi.branchCode.text())
            self.model.getCurrentInvoice().getCompany().setTaxNo(companyUi.taxNo.text())
            self.model.getCurrentInvoice().getCompany().setCustomerNo(companyUi.customerNo.text())
        
            self.view.webView.setHtml(self.model.getPreviewCurrentInvoice())
            self.view.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self)
