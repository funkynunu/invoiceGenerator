from iGLineItem import LineItem
from iGCompany import Company
from iGClient import Client
from iGStore import Store

from decimal import *

getcontext().prec = 2

# this class should set the line items when created
class Invoice(object):
# invLineItems is a list
    def __init__(self, invoiceNo, version, invoiceDate, invoiceNote, \
            # store1
            store1Id, store1Name, store1Manager, \
            store1Address1, store1Address2, store1TelNo, \
            # store2
            store2Id, store2Name, store2Manager, \
            store2Address1, store2Address2, store2TelNo, \
            # client
            clientId, clientName, clientBusinessName, \
            clientAddress1, clientAddress2, \
            # line item list
            lineItems,
            # company details
            companyId, bankName, branchCode, taxNo, customerNo, \
            timestamp):

        self.invoiceNo = invoiceNo
        self.version = version
        self.date = invoiceDate
        self.note = invoiceNote

        self.client = Client(clientId, clientName, clientBusinessName, \
            clientAddress1, clientAddress2, timestamp)

        self.store1 = Store(store1Id, store1Name, store1Manager, \
            store1Address1, store1Address2, store1TelNo, timestamp)

        self.store2 = Store(store2Id, store2Name, store2Manager, \
            store2Address1, store2Address2, store2TelNo, timestamp)

        self.lineItems = []
        
        # todo - sum all totals while looping creating line item obj
        self.total = 0
        self.total7Vat = 0
        self.total19Vat = 0
        self.totalExVat = 0
        
        for i in lineItems:
            print(i)
            self.total += i[8]
            if i[5] == "7":
                self.total7Vat += i[7]
            else:
                self.total19Vat += i[7]
            self.totalExVat += i[5]
            self.lineItems.append(LineItem(i[2], i[3], i[4], i[5], i[6], i[7], i[8], timestamp))

        self.company = Company(companyId, bankName, branchCode, taxNo, \
            customerNo, timestamp)

        self.timestamp = timestamp

    # def getInvoiceNo(self):
    #     return self.invoiceNo
    #
    # def getDate(self):
    #     return self.date
    #
    # def getNote(self):
    #     return self.note
    #
    # def getCompany(self):
    #     return self.company
    #
    # def getClient(self):
    #     return self.client
    #
    # def getStore1(self):
    #     return self.store1
    #
    # def getStore2(self):
    #     return self.store2
    #
    # def getLineItems(self):
    #     return self.lineItems

    def getTotal(self):
        return format(self.total, '0.2f')
    
    def getTotal7Vat(self):
        return format(self.total7Vat, '0.2f')
    
    def getTotal19Vat(self):
        return format(self.total19Vat, '0.2f')
    
    def getTotalExVat(self):
        return format(self.totalExVat, '0.2f')

    # def getTimestamp(self):
    #     return self.timestamp
    #
    # def setId(self, invId):
    #     self.invId = invId
    #
    # def setDate(self, date):
    #     self.date = date
    #
    # def setNote(self, note):
    #     self.note = note
    #
    # def setCompany(self, company):
    #     self.company = company
    #
    # def setClient(self, client):
    #     self.client = client
    #
    # # stores must be a list
    # def setStores(self, stores):
    #     self.stores = stores

    # lineItems must be a dict of LineItem objects - {1:lineItem obj, 2:....}
    def setLineItems(self, lineItems):
        self.lineItems = []
        for i in lineItems:
            self.lineItems.append(LineItem(i[2], i[3], i[4], i[5], i[6], i[7], timestamp))
        self.timestamp = timestamp

    # def setTimestamp(self, timestamp):
    #     self.timestamp = timestamp
