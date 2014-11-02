from decimal import *

getcontext().prec = 2

# this class should set the line items when created
class Invoice(object):
# invLineItems is a list
    def __init__(self, invoiceNo, version, invoiceDate, invoiceNote, \
            client, lineItems, company, store1, store2):

        self.invoiceNo = invoiceNo
        self.version = version
        self.date = invoiceDate
        self.note = invoiceNote

        self.client = client

        self.lineItems = []

        # todo - sum all totals while looping creating line item obj - total can b calculated on the fly
        #self.total, self.total7Vat, self.total19Vat, self.totalExVat = self.calculateTotals(lineItems)

        for i in lineItems:
            self.lineItems.append(LineItem(i[2], i[3], i[4], i[5], i[6], i[7], i[8]))

        self.company = company

        self.store1 = store1
        self.store2 = store2

    def getTotal(self):
        total = 0
        for i in self.lineItems:
            total += float(i.getPriceAfterVat())
        return format(total, '0.2f')

    def getTotal7Vat(self):
        total7Vat = 0
        for i in self.lineItems:
            if i.vatCategory == "7":
                total7Vat += float(i.getVatAmount())
        return format(total7Vat, '0.2f')

    def getTotal19Vat(self):
        total19Vat = 0
        for i in self.lineItems:
            if i.vatCategory == "19":
                total19Vat += float(i.getVatAmount())
        return format(total19Vat, '0.2f')

    def getTotalExVat(self):
        totalExVat = 0
        for i in self.lineItems:
            totalExVat += float(i.getPriceBeforeVat())
        return format(totalExVat, '0.2f')

    # lineItems must be a list of value from which lineItem objects can be created
    # e.g. [['111/13', 1, 1, '12x', 'Roses', 10.0, '7', 0.7, 10.7],
    #       ['111/13', 1, 2, '1x', 'Pot', 50.0, '7', 3.5, 53.5],
    #       ['111/13', 1, 3, '6x', 'Sausages', 10.0, '19', 1.9, 11.9]]
    def setLineItems(self, lineItems):
        self.lineItems = []

        for i in lineItems:
            self.lineItems.append(LineItem(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

class LineItem(object):
    def __init__(self, version, quantity, description, priceBeforeVat, \
            vatCategory, vatAmount, priceAfterVat):
        self.version = version
        self.quantity = quantity
        self.description = description
        self.priceBeforeVat = priceBeforeVat
        self.vatCategory = vatCategory
        self.vatAmount = vatAmount
        self.priceAfterVat = priceAfterVat

    def getPriceBeforeVat(self):
        return format(float(self.priceBeforeVat), '0.2f')

    def getPriceAfterVat(self):
        return format(float(self.priceAfterVat), '0.2f')

    def getVatAmount(self):
        return format(float(self.vatAmount), '0.2f')

class Client(object):
    def __init__(self, clientId, contactName, businessName, address1, address2):#, timestamp):
        self.clientId = clientId
        self.contactName = contactName
        self.businessName = businessName
        self.address1 = address1
        self.address2 = address2

class Company(object):
    def __init__(self, companyId, bankName, branchCode, taxNo, customerNo):

        self.companyId = companyId
        self.bankName = bankName
        self.branchCode = branchCode
        self.taxNo = taxNo
        self.customerNo = customerNo

class Store(object):
    def __init__(self, storeId, companyId, name, manager, address1, address2, telNo):
        self.storeId = storeId
        self.companyId = companyId
        self.name = name
        self.manager = manager
        self.address1 = address1
        self.address2 = address2
        self.telNo = telNo
