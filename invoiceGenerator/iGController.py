import re
import pickle

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QComboBox, \
    QTreeWidgetItem
from PyQt5.QtPrintSupport import QAbstractPrintDialog, QPrintDialog, QPrinter
from iGHtmlController import HtmlController
from iGModel import Model
from iGUi import Ui_MainWindow
from preferencesDialog import Ui_PreferencesDialog

class Controller(QMainWindow):
    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = Model()

        self.htmlController = HtmlController(self.model, self.ui, self)

        self.initializeMainWindow()

        # need to pass it the same values passed to preview and a
        # expose self.htmlController
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self.htmlController)

    def initializeMainWindow(self):
        print("controller.initializeMainWindow")

        # populate MainWindow with data
        self.setInvoiceTreeList( \
             self.model.getInvoiceTreeList(self.model.getSortByOptions()[0]))

        self.ui.sortByCb.clear()
        self.ui.sortByCb.addItems(self.model.getSortByOptions())

        self.ui.clientsCb.clear()
        self.ui.clientsCb.addItems(self.model.getClientNames())

        self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice())
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self.htmlController)

        self.ui.currInvNo.setText(self.model.getCurrentInvoiceNo())

        self.setCurrentView()

    def setPreview(self):
        self.ui.webView.setHtml(self.model.getCurrentInvoice())

    def configurePreferences(self):
        print("controller.configurePreferences")
#        preferenceDialog = Preferences(self)
#        preferenceDialog.show()
        preferencesDialog = QDialog(self)
        preferencesUi = Ui_PreferencesDialog()
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

    def treeListSelected(self):
        print("controller.treeListSelected")
        # https://docs.python.org/3/library/re.html
        # is clicked item an invoice?
        if re.search(r"[0-9]+\/[0-9]+",self.ui.invList.currentItem().text(0)):
            # make sure selection is not a date
            if not re.search(r"[0-9]+\/[0-9]+\/[0-9]+",self.ui.invList.currentItem().text(0)):
                self.ui.webView.setHtml \
                    (self.model.getPreviewPreviousInvoice \
                    (self.ui.invList.currentItem().text(0)))

            # previous does not get popups to change data!!!
            #self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self.htmlController)

                self.model.setDisplayedInvoiceNo \
                    (self.ui.invList.currentItem().text(0))
                self.setPreviousView()

    def reset(self):
        print("controller.reset")
        self.ui.webView.setHtml(self.model.getInitialPreview())
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self.htmlController)
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
        print(self.model.getCurrentInvoice().note)
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
        self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice())
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self.htmlController)

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
        self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice())
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self.htmlController)
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

        self.ui.webView.setHtml(self.model.getPreviewCurrentInvoice())
        self.ui.webView.page().mainFrame().addToJavaScriptWindowObject("htmlController", self.htmlController)

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

    def setPreviousView(self):
        print("controller.setPreviousView")
        # greys out options that are not available when viewing previous invoices
        self.ui.resetBtn.setEnabled(False)
        self.ui.saveBtn.setEnabled(False)
        self.ui.clientsCb.setEnabled(False)
        self.ui.viewCurrentBtn.setEnabled(True)
        self.ui.setCurrentBtn.setEnabled(True)
        
    def setCurrentView(self):
        print("controller.setCurrentView")
        # enables options that are were not available when viewing previous invoices
        self.ui.resetBtn.setEnabled(True)
        self.ui.saveBtn.setEnabled(True)
        self.ui.clientsCb.setEnabled(True)
        self.ui.viewCurrentBtn.setEnabled(False)
        self.ui.setCurrentBtn.setEnabled(False)
        #self.htmlController.updateDialogs(self.model.getCurrentInvoice())
