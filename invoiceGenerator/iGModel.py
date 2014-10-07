from iGDb import SQLiteDb
from iGInvoice import Invoice
from iGClient import Client

#from any_other_files import other_classes
from decimal import *
import datetime
    

HTMLTOP = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>
      A title
    </title>
    <script>
    function updateStore1() {{
        htmlControls.updateStore1();
    }}
    function updateStore2() {{
        var result = htmlControls.updateStore2();
    }}
    function updateClient() {{
        var result = htmlControls.updateClient();
    }}
    function updateLineItems() {{
        var result = htmlControls.updateLineItems();
    }}
    function updateCompany() {{
        var result = htmlControls.updateCompany();
    }}
    </script>
  </head>

  <body style="width: 1000px; height: 1414px; border: solid; margin-left:80px; margin-right: 80px; margin-bottom: 10px;margin-top: 20px; font-family: Gill Sans, sans-serif; font-size: 11pt;">

    <div style="width:1000px; height: 220px; position:absolute; float: left; font-family: Gill Sans, sans-serif; font-size: 11pt;">

      <div style="position:relative; width:210px; left: 582px; top: 25px; padding-bottom: 25px;">
        <img src="logo.png" width="200px">
      </div>

      <div style="width: 667px; height: 220px; position: relative; float: left;">
        <br>
      </div>

      <div style="width:333px; height: 220px; top: 15px; position: relative;float: left;">
          <div onclick="htmlControls.updateStore1()">
            <!-- Store 1 details-->
            {0}G&auml;rtnerei Roland Richter<br>
            {1}Inh. A. Clau&szlig;nitzer<br>
            {2}Oppacher Stra&szlig;e 22<br>
            {3}02689 Sohland OT Wehrsdorf<br>
            {4}Tel. 035936 / 30434
          </div>
          <div onclick="updateStore2()">
            <p>
              <!-- Store 2 details-->
              {5}Blumeneck Roland Richter<br>
              {6}Inh. A. Clau&szlig;nitzer<br>
	      {7}Dresdner Stra&szlig;e 5<br>
              {8}02681 Wilthen<br>
              {9}Tel. 03592 / 33045
            </p>
          </div>
      </div>
    </div>

    <div onclick="updateClient()" style="width:1000px;position:absolute; top: 260px; left: 160px;">
      <table>
        <tr>
          <td width="100%">

          </td><!-- Customer details-->
        </tr>
        <tr>
          <td>
            <br>
            {10}Client X<br>
            {11}Name Y<br>
            {12}Street Z<br><br>
            {13}Postcode Place
          </td>
        </tr>
      </table>
    </div>

    <div style="width:1000px; position:absolute; top: 450px; left: 160px;">
      <table style="width:800px;">
      <!-- Invoice details-->
      <tr>
        <td width="587px">
          <span style="font-weight: bold; font-size: 16pt"> {14}Invoice</span> 1/2014
        </td>
        <td>
          {15}Invoice date: dd/mm/yyyy
        </td>

      </tr>
      </table>
    </div>

    <div onclick="updateLineItems()" style="width:850px; position:absolute; top: 475px; left: 160px;">
      <table width="100%">
        <!-- Item headers-->
        <tr>
          <td colspan="6">
            <hr>
          </td>
        </tr>
        <tr>
          <td colspan="6">
            {16}I delivered to you on date dd/mm/yy:
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
        <!-- Item details-- loops until all line items displayed>"""

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
          <td align="right">
            {3}
          </td>
          <td>
            {4}
          </td>
          <td align="right">
            {5}
          </td>
        </tr>"""

HTMLBOTTOM = """
        <!-- Total-->
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
    <div onclick="updateCompany()" style="width:850px;position:absolute; top: 1300px; left: 160px;">
      <table width="100%">
        <!-- Company bank details-->
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
        self.SQLiteDb = SQLiteDb()
        
        # initials variables from database - tuples
        # http://stackoverflow.com/questions/16296643/convert-tuple-to-list-and-back

        # initialise previous Invoices
        self.dbClients = self.getDbClients()
        self.dbInvoices = self.getDbInvoices()
        self.dbLineItems = self.getDbLineItems()
        self.dbCompany = self.getDbCompany()
        self.dbStores = self.getDbStores()

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
        
        
    def initializePreviousInvoices(self):
        # does not contain line item details. Line item details are keep
        # in line item dict
        invDict = {}
        
        for invoice in self.dbInvoices:
            company = self.getCompany(invoice[4])
            client = self.getClient(invoice[5])
            store1 = self.getStore(invoice[6])
            store2 = self.getStore(invoice[7])

            items = self.getLineItems(invoice[0],invoice[1])
            
            invDict[invoice[0]] = \
                Invoice(invoice[0], invoice[1], invoice[2], invoice[3], \
                    invoice[6], store1[1], store1[2], store1[4], store1[5], store1[3], \
                    invoice[7], store2[1], store2[2], store2[4], store2[5], store2[3],
                    invoice[5], client[1], client[2], client[3], client[4], \
                    items, company[2], company[3],
                    invoice[4], company[4], company[5], invoice[7])

        return invDict
    
    # use most recent invoice saved as template without line item details
    def initializeCurrentInvoice(self):
        # lastInvoice = .... look at self.previousInvoices and use data from there
        lastInv = self.previousInvoices[self.getLastInvoiceNoUsed()]
        return Invoice(self.getNextInvoiceNo(), \
            "1", \
            self.getDate(), \
            # note
            "", \
            lastInv.store1.storeId, \
            lastInv.store1.name, \
            lastInv.store1.manager, \
            lastInv.store1.address1, \
            lastInv.store1.address2, \
            lastInv.store1.telNo, \
            lastInv.store2.storeId, \
            lastInv.store2.name, \
            lastInv.store2.manager, \
            lastInv.store2.address1, \
            lastInv.store2.address2, \
            lastInv.store2.telNo, \
            # client details
            "","","","","", \
            # line items
            [], \
            #company details
            lastInv.company.companyId,
            lastInv.company.bankName, \
            lastInv.company.branchCode, \
            lastInv.company.taxNo, \
            lastInv.company.customerNo, \
            self.getTimestamp)

    def getNextInvoiceNo(self):
        splitResult = self.getLastInvoiceNoUsed().split("/")
        invSeqNo = int(splitResult[0]) + 1
        
        return (str(invSeqNo) + '/' + splitResult[1])

    def getLastInvoiceNoUsed(self):
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
        return self.previousInvoices

    def getTimestamp(self):
        now = datetime.datetime.now()
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def getDate(self):
        now = datetime.datetime.now()
        return datetime.datetime.now().strftime("%d/%m/%Y")

    # get client list from sqlite db and updates list of clients var
    def getDbInvoices(self):
        return self.SQLiteDb.getInvoices()

    def getDbLineItems(self):
        return self.SQLiteDb.getLineItems()

    # get company details from sqlite db and updates company var
    def getDbCompany(self):
        return self.SQLiteDb.getCompany()

    # gets stores' details from sqlite db and updates list of store vars
    def getDbStores(self):
        return self.SQLiteDb.getStores()

    # get client list from sqlite db and updates list of clients vars
    def getDbClients(self):
        return self.SQLiteDb.getClients()
    
# sortBy functionality
    def getSortByOptions(self):
        return ['Invoice No', 'Date', 'Client']

    def getSelectedSortByOptions(self, index):
        return self.sortByOptions[index]


################

    def getInvoices(self):
        return self.invoices

    def getLineItems(self, invNo, version):
        items = []
        for lineItem in self.dbLineItems:
            if invNo == lineItem[0] and version == lineItem[1]:
                items.append(list(lineItem))
        return items

    # get client list from sqlite db and updates list of clients var
    def getCompany(self, companyId):
        for company in self.dbCompany:
            if company[0] == companyId:
                return company
        return None
    # get client list from sqlite db and updates list of clients var
    def getStore(self, storeId):
        for store in self.dbStores:
            if store[0] == storeId:
                return store
        return None

    # get client list from sqlite db and updates list of clients var
    def getClient(self, clientId):
        store = []
        for client in self.dbClients:
            if client[0] == clientId:
                return list(client)
        return []
    
#################

    # return list of clients
    def getClients(self):
        return [list(i) for i in self.getDbClients()]
    
    # return list of clients names
    def getClientNames(self):
        clientNames = []
        for client in self.dbClients:
            clientNames.append(client[1])
        return clientNames

    def getSelectedClientsName(self, index):
        return self.clientNames[index]

    def getCurrentInvoiceNo(self):
        return self.currentInvoice.invoiceNo
        
    def add_stuff(self, no):
        self.total = self.total + no
    
    def increment(self, value):
        try:
            value = int(value) + 1
        except Exception:
            print("Ahhh, shit")
        return value

    def getTotal(self):
        return self.total
        
    def getCurrentInvoice(self):
        return self.currentInvoice
    
    def getPreviousInvoice(self, invNo):
        return self.previousInvoices[invNo]
        
# preview
    def getPreviewCurrentInvoice(self):
        return self.getPreviewHTML(self.currentInvoice)

    def getDisplayedInvoiceNo(self):
        return self.displayedInvoiceNo

    def setDisplayedInvoiceNo(self, invoiceNo):
        self.displayedInvoiceNo = invoiceNo

#
    def setCurrentInvoice(self, invoiceObject):
        self.currentInvoice = invoiceObject

#
    def getPreviewPreviousInvoice(self, invoice):
        return self.getPreviewHTML(self.previousInvoices[invoice])
        
    def getPreviewHTML(self, invoice):
    # name = "allen"
    # notName = "notAllen"
    # "{0} is my name and not {1} ".format(name, notName)
        top = ""
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
            invoice.client.name, \
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
                    i.getVat(), \
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

        return (top + middle + bottom)

    # e.g. {'test': ['1','2','3'],'test2': ['4','5','6']}
    def getInvoiceTreeList(self, sortBy):
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
        result = {}
        # Invoice number
        if sortBy == self.getSortByOptions()[0]:
            aList = []
            for key in self.previousInvoices.keys():
                result[key] = aList
        # Date
        elif sortBy == self.getSortByOptions()[1]:
            for key in self.previousInvoices:
                aList = []
                if self.previousInvoices[key].date in result:
                    tempList = result[key]
                    tempList.append(key)
                    result[self.previousInvoices[key].date] = tempList
                else:
                    result[self.previousInvoices[key].date] = [key]
        #Client
        elif sortBy == self.getSortByOptions()[2]:
            for key in self.previousInvoices:
                aList = []
                if self.previousInvoices[key].client.name in result:
                    tempList = result[key]
                    tempList.append(key)
                    result[self.previousInvoices[key].client.name] = tempList
                else:
                    result[self.previousInvoices[key].client.name] = [key]
        return result

# returns Client object
    def getClientObject(self, clientName):
        result = None
        for client in self.SQLiteDb.getClients():
            if client[1] == clientName:
                result = Client(client[0], client[1], client[2], client[3], \
                    client[4], client[5])
        return result
        
# takes a Client object and set it as the current invoice client
    def setClient(self, client):
        self.currentInvoice.client = client

    def getInitialPreview(self):
        self.setCurrentInvoice(self.initializeCurrentInvoice())
        return self.getPreviewCurrentInvoice()

    def saveCurrentInvoice(self):
        # # is current invoice already in db
        # current invoice should have version number correct already
        SQLiteDb.insertStore(self.currentInvoice.store1.storeId, \
                          self.currentInvoice.store1.name, \
                          self.currentInvoice.store1.manager, \
                          self.currentInvoice.store1.address1, \
                          self.currentInvoice.store1.address2, \
                          self.currentInvoice.store1.telNo, \
                          self.currentInvoice.store1.getTimestamp())

        SQLiteDb.insertStore(self.currentInvoice.store2.storeId, \
                          self.currentInvoice.store2.name, \
                          self.currentInvoice.store2.manager, \
                          self.currentInvoice.store2.address1, \
                          self.currentInvoice.store2.address2, \
                          self.currentInvoice.store2.telNo, \
                          self.currentInvoice.store2.getTimestamp())

# clientId, clientName, businessName, addressLine1, addressLine2, timestamp
        SQLiteDb.insertClient(self.currentInvoice.client.clientId, \
                              self.currentInvoice.client.name, \
                              self.currentInvoice.client.businessName, \
                              self.currentInvoice.client.address1, \
                              self.currentInvoice.client.address2, \
                              self.currentInvoice.client.getTimestamp())

# companyId, bankName, branchCode, taxNo, customerNo, timestamp
        SQLiteDb.insertCompany(self.currentInvoice.company.companyId, \
                               self.currentInvoice.company.bankName, \
                               self.currentInvoice.company.branchCode, \
                               self.currentInvoice.company.taxNo, \
                               self.currentInvoice.company.customerNo, \
                               self.currentInvoice.company.getTimestamp())

# invoiceId, version, invoiceDate, invoiceNote, companyId, clientId, store1Id, store2Id, timestamp
        SQLiteDb.insertInvoice(self.currentInvoice.invoiceNo, \
                               self.currentInvoice.version, \
                               self.currentInvoice.date, \
                               self.currentInvoice.note, \
                               self.currentInvoice.company.companyId, \
                               self.currentInvoice.client.clientId, \
                               self.currentInvoice.store.storeId, \
                               self.currentInvoice.store2.storeId, \
                               self.currentInvoice.getTimestamp())

# invoiceId, version, lineItemId, quantity, description, priceBeforeVat, vatCategory, vat, priceAfterVat, timestamp
        for line in self.currentInvoice.lineItems:
            SQLiteDb.insertLineItems(self.currentInvoice.invoiceNo, \
                                     line.version, \
                                     line.lineItemNo, \
                                     line.quantity, \
                                     line.description, \
                                     line.getPriceBeforeVat(), \
                                     line.getVatategory(), \
                                     line.getPriceAfterVat(), \
                                     line.getTimeStamp())


if __name__ == "__main__":
    aModel = Model()
    print('getClients: ', aModel.getClients())
    print('getPreviousInvoices: ', aModel.getPreviousInvoices())
