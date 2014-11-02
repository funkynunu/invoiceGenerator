from iGDb import SQLiteDb
from iGObjects import Invoice, LineItem, Company, Client, Store

#from any_other_files import other_classes
import datetime
    
HTMLTOP = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>
      A title
    </title>
  </head>

  <body style="width: 1000px; height: 1414px; border: solid; margin-left:10px; margin-right: 10px; margin-bottom: 10px;margin-top: 10px; font-family: Gill Sans, sans-serif; font-size: 11pt;">

    <div style="width:1000px; height: 220px; position:absolute; float: left; font-family: Gill Sans, sans-serif; font-size: 11pt;">

      <div style="position:relative; width:210px; left: 582px; top: 25px; padding-bottom: 25px;">
        <img src="logo.png" width="200px">
      </div>

      <div style="width: 667px; height: 220px; position: relative; float: left;">
        <br>
      </div>

      <div style="width:333px; height: 220px; top: 15px; position: relative;float: left;">
          <div onclick="controller.displayStore1Dialog()">
            <!-- Store 1 details-->
            {0}<br>
            {1}<br>
            {2}<br>
            {3}<br>
            Tel. {4}
          </div>
          <div onclick="controller.displayStore2Dialog()">
            <p>
              <!-- Store 2 details-->
              {5}<br>
              {6}<br>
	          {7}<br>
              {8}<br>
              Tel. {9}
            </p>
          </div>
      </div>
    </div>

    <div onclick="controller.displayClientDialog()" style="width:577px;position:absolute; top: 260px; left: 90px;">
      <table>
        <tr>
          <td width="100%">

          </td><!-- Customer details-->
        </tr>
        <tr>
          <td>
            <br>
            {10}<br>
            {11}<br>
            {12}<br>
            {13}
          </td>
        </tr>
      </table>
    </div>

    <div style="width:850px; position:absolute; top: 450px; left: 90px;">
      <table style="width:800px;">
      <!-- Invoice details-->
      <tr>
        <td width="587px">
          <span style="font-weight: bold; font-size: 16pt">Invoice {14}</span>
        </td>
        <td>
          Invoice date: {15}
        </td>

      </tr>
      </table>
    </div>
    <div onclick="controller.displayLineItemsDialog()" style="width:850px; position:absolute; top: 475px; left: 90px;">
      <table width="100%">
        <! -- Item headers-->
        <tr>
          <td colspan="6">
            <hr>
          </td>
        </tr>
        <tr>
          <td colspan="6">
            I delivered to you on date {16}:
          </td>
        </tr>
        <tr>
          <td>
            Quantity
          </td>
          <td>
            Description
          </td>
          <td>
            Price
          </td>
          <td>
          Tax
          </td>
          <td>
            Tax Rate
          </td>
          <td>
            Total
          </td>
        </tr>
        <! -- Item details-- loops until all line items displayed>"""

HTMLMIDDLE ="""
        <tr>
          <td>
            {0}
          </td>
          <td>
            {1}
          </td>
          <td>
            {2}
          </td>
          <td>
            {3}%
          </td>
          <td>
            {4}
          </td>
          <td align="right">
            {5}
          </td>
        </tr>"""

HTMLBOTTOM = """
        <! -- Total-->
        <tr>
          <td align="right" colspan="5"></td>
          <td>
            <hr>
          </td>
        </tr>
        <tr>
          <td align="right" colspan="5">
            Total:
          </td>
          <td align="right">
            {0}
          </td>
        </tr>
        <tr>
          <td align="right" colspan="5"></td>
          <td>
            <hr>
          </td>
        </tr>
        <tr>
          <td align="right" colspan="5">
            Tax at 7%:<br>
            Tax at 19%:<br>
            Items without tax:<br>
          </td>
          <td align="right">
            {1}<br>
            {2}<br>
            {3}
          </td>
        </tr>
      </table>
    </div>
    <div onclick="controller.displayCompanyDialog()" style="width:850px;position:absolute; top: 1300px; left: 90px;">
      <table width="100%">
        <! -- Company bank details-->
        <tr>
          <td colspan="2">
            <hr>
          </td>
        </tr>
        <tr>
          <td>
            Bank name: {4}<br>
            Braunch code: {5}<br>
          </td>
          <td>
            Customer number: {6}<br>
            Tax number: {7}<br>
          </td>
        </tr>
      </table>
    </div>
  </body>
</html>"""

# contains a dict with all previous invoice objects
# contains a Invoice obj that is not stored in database
class Model(object):
    def __init__(self):
        # initialise database data
        print("Model.__init__")
        self.SQLiteDb = SQLiteDb()
        
        # initials variables from database - tuples
        # http://stackoverflow.com/questions/16296643/convert-tuple-to-list-and-back

        # initialise variables from local database
        self.loadDbVariables()

        # initialise previous invoices
        # {invNo: Invoice()}
        self.previousInvoices = self.initializePreviousInvoices()
        
        # initialise current invoice
        self.currentInvoice = self.initializeCurrentInvoice()
        
        # invoice currently displayed by html
        self.displayedInvoiceNo = self.getNextInvoiceNo()

        # variables for initialisation of view...
        self.clientNames = self.getClientNames()
        self.sortByOptions = self.getSortByOptions()
        
        
    def loadDbVariables(self):
        self.dbClients = self.getDbClients()
        self.dbInvoices = self.getDbInvoices()
        self.dbLineItems = self.getDbLineItems()
        self.dbCompany = self.getDbCompany()
        self.dbStores = self.getDbStores()

    def initializePreviousInvoices(self):
        print("  model.initializePreviousInvoices")
        # does not contain line item details. Line item details are keep
        # in line item dict
        invDict = {}
        
        for invoice in self.dbInvoices:
            client = self.getClient(invoice[5])
            company = self.getCompany(invoice[4])
            # get list of stores with company id
            stores = self.getStores(invoice[4])
            store1 = stores[0]
            store2 = stores[1]
            items = self.getLineItems(invoice[0],invoice[1])

            invDict[invoice[0]] = \
                Invoice(invoice[0], invoice[1], invoice[2], invoice[3], client, items, company, store1, store2)

        return invDict
    
    # use most recent invoice saved as template without line item details
    def initializeCurrentInvoice(self):
        # lastInvoice = .... look at self.previousInvoices and use data from there
        print("  model.initializeCurrentInvoice")
        lastInv = self.previousInvoices[self.getLastInvoiceNoUsed()]

        return Invoice(self.getNextInvoiceNo(), \
            # version
            "1", \
            # today's date
            self.getDate(), \
            # note
            "", \
            # client details
            lastInv.client,
            # line items
            [], \
            # company
            lastInv.company,
            # stores
            lastInv.store1,
            lastInv.store2)

    def getNextInvoiceNo(self):
        print("  model.getNextInvoiceNo")
        splitResult = self.getLastInvoiceNoUsed().split("/")
        invSeqNo = int(splitResult[0]) + 1
        
        return (str(invSeqNo) + '/' + splitResult[1])

    def getLastInvoiceNoUsed(self):
        print("  model.getLastInvoiceNoUsed")
        invSeqNo = 0
        invYear = 0
        splitResult = []
        
        # find last invoice no used
        for key in self.previousInvoices.keys():
            splitResult = key.split("/")
            if int(splitResult[1]) > int(invYear):
                invYear = splitResult[1]
                invSeqNo = splitResult[0]
            elif int(splitResult[1]) == int(invYear):
                if int(splitResult[0]) > int(invSeqNo):
                    invSeqNo = splitResult[0]

        return (str(invSeqNo) + '/' + str(invYear))

    def getPreviousInvoices(self):
        print("  model.getPreviousInvoices")
        return self.previousInvoices

    def getDate(self):
        print("  model.getDate")
        now = datetime.datetime.now()
        return datetime.datetime.now().strftime("%d/%m/%Y")

    # get client list from sqlite db and updates list of clients var
    def getDbInvoices(self):
        print("  model.getDbInvoices")
        return self.SQLiteDb.getDbInvoices()

    def getDbLineItems(self):
        print("  model.getDbLineItems")
        return self.SQLiteDb.getDbLineItems()

    # get company details from sqlite db and updates company var
    def getDbCompany(self):
        print("  model.getDbCompany")
        return self.SQLiteDb.getDbCompany()

    # gets stores' details from sqlite db and updates list of store vars
    def getDbStores(self):
        print("  model.getDbStores")
        return self.SQLiteDb.getDbStores()

    # get client list from sqlite db and updates list of clients vars
    def getDbClients(self):
        print("  model.getDbClients")
        return self.SQLiteDb.getDbClients()
    
# sortBy functionality
    def getSortByOptions(self):
        print("  model.getSortByOptions")
        return ['Invoice No', 'Date', 'Client']

    def getSelectedSortByOptions(self, index):
        print("  model.getSelectedSortByOptions")
        return self.sortByOptions[index]


################

    def getInvoices(self):
        print("  model.getInvoices")
        return self.invoices

    def getLineItems(self, invNo, version):
        print("  model.getLineItems")
        items = []
        for lineItem in self.dbLineItems:
            if invNo == lineItem[0] and version == lineItem[1]:
                items.append(list(lineItem))
        return items

    # get client list from sqlite db and updates list of clients var
    def getCompany(self, companyId):
        print("  model.getCompany")
        for company in self.dbCompany:
            if company[0] == companyId:
                return Company(company[0], company[1],company[2],company[3],company[4])
        return None

    # get client list from sqlite db and updates list of clients var
    def getStore(self, storeId):
        print("  model.getStore")
        for store in self.dbStores:
            if store[0] == storeId:
                return Store(store[0],store[1],store[2],store[3],store[4],store[5],store[6])
        return None

    # returns a list of stores with specified company id
    def getStores(self, companyId):
        print("  model.getStores")
        stores = []
        for store in self.dbStores:
            if store[1] == companyId:
                stores.append(Store(store[0],store[1],store[2],store[3],store[4],store[5],store[6]))
        return stores

    # returns client object with a specified id or None
    def getClient(self, clientId):
        print("  model.getClient")
        for client in self.dbClients:
            if client[0] == clientId:
                return Client(client[0],client[1],client[2],client[3],client[4])
        return None
    
#################

    # return list of clients
    def getClients(self):
        print("  model.getClients")
        return [list(i) for i in self.getDbClients()]
    
    # return list of clients names
    def getClientNames(self):
        print("  model.getClientNames")
        clientNames = []
        for client in self.dbClients:
            clientNames.append(client[1])
        return clientNames

    def getSelectedClientsName(self, index):
        print("  model.getSelectedClientsName")
        return self.clientNames[index]

    def getCurrentInvoiceNo(self):
        print("  model.getCurrentInvoiceNo")
        return self.currentInvoice.invoiceNo
        
    def add_stuff(self, no):
        print("  model.add_stuff")
        self.total = self.total + no
    
    def increment(self, value):
        print("  model.increment")
        try:
            value = int(value) + 1
        except Exception:
            print("  model.Ahhh, shit")
        return value

    def getTotal(self):
        print("  model.getTotal")
        return self.total
        
    def getCurrentInvoice(self):
        print("  model.getCurrentInvoice")
        return self.currentInvoice
    
    def getPreviousInvoice(self, invNo):
        print("  model.getPreviousInvoice")
        return self.previousInvoices[invNo]
        
# preview
    def getPreviewCurrentInvoice(self):
        print("  model.getPreviewCurrentInvoice")
        return self.getPreviewHTML(self.currentInvoice)

    def getDisplayedInvoiceNo(self):
        print("  model.getDisplayedInvoiceNo")
        return self.displayedInvoiceNo

    def setDisplayedInvoiceNo(self, invoiceNo):
        print("  model.setDisplayedInvoiceNo")
        self.displayedInvoiceNo = invoiceNo

#
    def setCurrentInvoice(self, invoiceObject):
        print("  model.setCurrentInvoice")
        self.currentInvoice = invoiceObject

#
    def getPreviewPreviousInvoice(self, invoice):
        print("  model.getPreviewPreviousInvoice")
        return self.getPreviewHTML(self.previousInvoices[invoice])
        
    def getPreviewHTML(self, invoice):
        print("  model.getPreviewHTML")
    # name = "allen"
    # notName = "notAllen"
    # "{0} is my name and not {1} ".format(name, notName)
        top = HTMLTOP.format( \
            invoice.store1.name, \
            invoice.store1.manager, \
            invoice.store1.address1, \
            invoice.store1.address2, \
            invoice.store1.telNo, \
            invoice.store2.name, \
            invoice.store2.manager, \
            invoice.store2.address1, \
            invoice.store2.address2, \
            invoice.store2.telNo, \
            invoice.client.contactName, \
            invoice.client.businessName, \
            invoice.client.address1, \
            invoice.client.address2, \
            invoice.invoiceNo, \
            invoice.date, \
            invoice.note)

        middle = "" # do I need to initialise this???
        
        for i in invoice.lineItems:
            # quantity, itemDescription, priceExVat, priceInVat, vat, vatCatagory, timestamp
            middle = middle + \
                HTMLMIDDLE.format(i.quantity, \
                    i.description, \
                    i.getPriceBeforeVat(), \
                    i.vatCategory, \
                    i.getVatAmount(), \
                    i.getPriceAfterVat()
                    )

        # calculate totals
        bottom = HTMLBOTTOM.format( \
            invoice.getTotal(), \
            invoice.getTotal7Vat(), \
            invoice.getTotal19Vat(), \
            invoice.getTotalExVat(), \
            invoice.company.bankName, \
            invoice.company.branchCode, \
            invoice.company.taxNo, \
            invoice.company.customerNo)
        #print(top + middle + bottom)
        return top + middle + bottom

    # e.g. {'test': ['1','2','3'],'test2': ['4','5','6']}
    def getInvoiceTreeList(self, sortBy):
        print("  model.getInvoiceTreeList")
        # need to check what list is sorted by
        # if....
        #but for testing purposes we will use sort by date...
        # how to do it
        """ 1. make dict with sort condition as key and
               value as list of inv no
            2. create list with keys of new list
            3. sort list of key
            4. loop at list accessing dict, sort value list 
            5. return dict
        
        """
        # reload previousInvoices for new invoices
        # self.previousInvoices = self.initializePreviousInvoices()

        result = {}
        # Invoice number
        # {'114/14': [],'116/14': []}
        if sortBy == self.getSortByOptions()[0]:
            aList = []
            for key in self.previousInvoices:
                result[key] = aList

        # Date {'24/07/2014': ['114/14','116/14'],'25/07/2014': ['118/14','119/14']}
        elif sortBy == self.getSortByOptions()[1]:
            for key in self.previousInvoices:
                # if date is not in result dict, add it with value key
                if not self.previousInvoices[key].date in result:
                    result[self.previousInvoices[key].date] = [key]
                # if date is in result dict, add the key to the value list
                else:
                    invoiceList = result[self.previousInvoices[key].date]
                    invoiceList.append(key)
                    result[self.previousInvoices[key].date] = invoiceList

        #Client {'Bob': ['114/14','116/14'],'Joe': ['118/14','119/14']}
        elif sortBy == self.getSortByOptions()[2]:
            for key in self.previousInvoices:
                if not self.previousInvoices[key].client.contactName in result:
                    result[self.previousInvoices[key].client.contactName] = [key]
                else:
                    clientList = result[self.previousInvoices[key].client.contactName]
                    clientList.append(key)
                    result[self.previousInvoices[key].client.contactName] = clientList
        return result

# returns Client object
    def getClientObject(self, clientName):
        print("  model.getClientObject")
        result = None
        for client in self.dbClients:
            # there are instances where client is changed but no value is selected
            if clientName == "":
                result = Client(client[0], client[1], client[2], client[3], \
                    client[4])
                break
            if client[1] == clientName:
                result = Client(client[0], client[1], client[2], client[3], \
                    client[4])#, client[5])
        return result
        
# takes a Client object and set it as the current invoice client
    def setClient(self, client):
        print("  model.setClient")
        self.currentInvoice.client = client

    def getInitialPreview(self):
        print("  model.getInitialPreview")
        self.setCurrentInvoice(self.initializeCurrentInvoice())
        return self.getPreviewCurrentInvoice()

    def saveCurrentInvoice(self):
        print("  model.saveCurrentInvoice")
# http://www.tutorialspoint.com/python/python_loop_control.htm

        # check stores for updates
        # if there is a change to any of the stores then both stores need to be saved referencing a new company
        # store 1
        store1Id = None
        store2Id = None

        # check for store_id in store table
        for store in self.dbStores:
            # we check all columns except id
            if (store[1]==self.currentInvoice.store1.getCompanyId() and \
                    store[2]==self.currentInvoice.store1.getName() and \
                    store[3]==self.currentInvoice.store1.getManager() and \
                    store[4]==self.currentInvoice.store1.getAddress1() and \
                    store[5]==self.currentInvoice.store1.getAddress2() and \
                    store[6]==self.currentInvoice.store1.getTelNo()):
                print("Store1 found - not saved")
                # and we get the primary key!
                store1Id = store[0]

            if (store[1]==self.currentInvoice.store2.getCompanyId() and \
                    store[2]==self.currentInvoice.store2.getName() and \
                    store[3]==self.currentInvoice.store2.getManager() and \
                    store[4]==self.currentInvoice.store2.getAddress1() and \
                    store[5]==self.currentInvoice.store2.getAddress2() and \
                    store[6]==self.currentInvoice.store2.getTelNo()):
                print("Store2 found - not saved")
                # and we get the primary key!
                store2Id = store[0]

        # if we don't find the primary key we insert a record
        if store1Id is None or store2Id is None:
            companyId = len(self.dbCompany) + 1

            self.SQLiteDb.insertCompany(companyId, \
                                self.currentInvoice.company.getBankName(), \
                                self.currentInvoice.company.getBranchCode(), \
                                self.currentInvoice.company.getTaxNo(), \
                                self.currentInvoice.company.getCustomerNo())

            #if store1Id is None:
            store1Id = len(self.dbStores) + 1
            #else:
            #    store1Id = self.currentInvoice.store1.getStoreId()

            self.SQLiteDb.insertStore(store1Id, \
                                 companyId, \
                                 self.currentInvoice.store1.getName(), \
                                 self.currentInvoice.store1.getManager(), \
                                 self.currentInvoice.store1.getAddress1(), \
                                 self.currentInvoice.store1.getAddress2(), \
                                 self.currentInvoice.store1.getTelNo())

            # we need to refresh the dbStores list for store2
            self.dbStores = self.getDbStores()

        # store 2
            #if store2Id is None:
            store2Id = len(self.dbStores) + 1
            #else:
            #    store2Id = self.currentInvoice.store2.getStoreId()

            self.SQLiteDb.insertStore(store2Id, \
                                 companyId, \
                                 self.currentInvoice.store2.getName(), \
                                 self.currentInvoice.store2.getManager(), \
                                 self.currentInvoice.store2.getAddress1(), \
                                 self.currentInvoice.store2.getAddress2(), \
                                 self.currentInvoice.store2.getTelNo())

        # if both stores are found then check the company details for changes
        else:
            # company
            companyId = None

            for company in self.dbCompany:
                # if the exact record is not found then we consider
                # the current invoice contains a update to a previous company
                if ( company[1]==self.currentInvoice.company.getBankName() and \
                        company[2]==self.currentInvoice.company.getBranchCode() and \
                        company[3]==self.currentInvoice.company.getTaxNo() and \
                        company[4]==self.currentInvoice.company.getCustomerNo()):
                    # company found
                    companyId = company[0] # primary key
                    print("company found - not saved")
                    break

            if companyId is None: # not found then insert record into client table
                companyId = len(self.dbCompany) + 1
                self.SQLiteDb.insertCompany(companyId, \
                                    self.currentInvoice.company.getBankName(), \
                                    self.currentInvoice.company.getBranchCode(), \
                                    self.currentInvoice.company.getTaxNo(), \
                                    self.currentInvoice.company.getCustomerNo())


        # client
        # check client for updates
        clientId = None
        for client in self.dbClients:
            # check to see if client contact name exists
            # if the exact record is not found then we consider
            # the current invoice contains a update to a previous client or
            # a new client
            if (client[1]==self.currentInvoice.client.getContactName() and \
                    client[2]==self.currentInvoice.client.getBusinessName() and \
                    client[3]==self.currentInvoice.client.getAddress1() and \
                    client[4]==self.currentInvoice.client.getAddress2()):
                # client found
                # check rest of record, if different then create version 2 of client with different values
                clientId = client[0] # primary key
                print("client found - not saved")
                break

        if clientId is None: # not found then insert record into client table
            clientId = len(self.dbClients) + 1
            self.SQLiteDb.insertClient(clientId, \
                                 self.currentInvoice.client.getContactName(), \
                                 self.currentInvoice.client.getBusinessName(), \
                                 self.currentInvoice.client.getAddress1(), \
                                 self.currentInvoice.client.getAddress2())

        # invoice
        self.currentInvoice.setVersion(int(1))
        for inv in self.dbInvoices:
            # inv[0] all invoices no.
            if (self.currentInvoice.getInvoiceNo()==inv[0]):
                # increment version
                self.currentInvoice.setVersion(int(self.currentInvoice.getVersion()) + 1)
                print('invoice found - incrementing version')

        self.SQLiteDb.insertInvoice(self.currentInvoice.getInvoiceNo(), \
                               self.currentInvoice.getVersion(), \
                               self.currentInvoice.getDate(), \
                               self.currentInvoice.getNote(), \
                               companyId, \
                               clientId, \
                               self.getTimestamp())

        # line items
        lineItemNo = 0
        for li in self.currentInvoice.getLineItems():
            lineItemNo += 1
            self.SQLiteDb.insertLineItems(self.currentInvoice.getInvoiceNo(), \
                                          self.currentInvoice.getVersion(), \
                                          lineItemNo, li.getQuantity(), \
                                          li.getDescription(), li.getPriceBeforeVat(), \
                                          li.getVatCategory(), li.getVatAmount(), \
                                          li.getPriceAfterVat())

        print("Finished insert")

    def getTimestamp(self):
        print("  model.getTimestamp")
        now = datetime.datetime.now()
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

if __name__ == "__main__":
    aModel = Model()
    print('getClients: ', aModel.getClients())
    print('getPreviousInvoices: ', aModel.getPreviousInvoices())
