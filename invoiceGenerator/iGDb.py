    # https://pythonadventures.wordpress.com/2014/05/12/an-sqlite-example/
# data types - http://www.tutorialspoint.com/sqlite/sqlite_data_types.htm
# timestamp - http://www.sqlite.org/lang_datefunc.html
# autoincrement - http://www.sqlite.org/autoinc.html
#!/usr/bin/env python

# the primary key of invoices should not autoincremented
# not sure if all the tables need a timestamp

"""
Sqlite database handler.
"""
 
import os
import sqlite3
import atexit
import termcolor
import sys
#import random
#from iGInvoice import Invoice
 
PATH = os.path.dirname(os.path.abspath(__file__))
# Note: invoice number cannot be autoincremented as the format is
# number/year and should be determined by the program before insertion

# Research: should the be a table between invoice + store ????
# atm invoice references only 1 store.... must change!!!

# Note: Invoice should reference other tables so that previous invoice
# can accurately be recreated

# Note: sqlite-manager does not support tables without ROWID column.
# https://code.google.com/p/sqlite-manager/issues/detail?id=840

# Note: in invoice_line_items, price_after_vat is included because
# price_before_vat + vat might not add up

SCHEMA2 = """
CREATE TABLE IF NOT EXISTS company
(
  "company_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "company_name" TEXT NOT NULL,
  "bank_name" TEXT,
  "branch_code" TEXT,
  "tax_no" TEXT,
  "customer_no" TEXT,
  "timestamp" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clients
(
  "client_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "client_name" TEXT NOT NULL,
  "business_name" TEXT,
  "address_line1" TEXT NOT NULL,
  "address_line2" TEXT,
  "timestamp" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS invoices
(
  "invoice_id" TEXT PRIMARY KEY NOT NULL,
  "version" INTEGER NOT NULL,
  "invoice_date" DATE NOT NULL,
  "invoice_note" TEXT,
  "company_id" INTEGER NOT NULL,
  "client_id" INTEGER NOT NULL,
  "store1_id" INTEGER NOT NULL,
  "store2_id" INTEGER NOT NULL,
  "timestamp" TEXT NOT NULL,
  FOREIGN KEY(client_id) REFERENCES clients(client_id),
  FOREIGN KEY(company_id) REFERENCES company(company_id),
  FOREIGN KEY(store1_id) REFERENCES stores(store_id),
  FOREIGN KEY(store2_id) REFERENCES stores(store_id)
);

CREATE TABLE IF NOT EXISTS stores
(
  "store_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "store_name" TEXT NOT NULL,
  "store_manager" TEXT,
  "store_tel_no" TEXT,
  "address_line1" TEXT NOT NULL,
  "address_line2" TEXT,
  "timestamp" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS invoice_line_items
(
  "invoice_id" INTEGER NOT NULL,
  "version" INTEGER NOT NULL,
  "line_item_id" INTEGER NOT NULL,
  "quantity" INTEGER,
  "description" TEXT,
  "price_before_vat" REAL,
  "vat_catagory" TEXT,
  "vat" REAL,
  "price_after_vat" REAL,
  "timestamp" TEXT NOT NULL,
  PRIMARY KEY("invoice_id","line_item_id"),
  FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id)
);
"""

SCHEMA = """
CREATE TABLE addresses
(
  "address_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "address_line1" TEXT NOT NULL,
  "address_line2" TEXT,
  "timestamp" TEXT
);
  
CREATE TABLE clients
(
  "client_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "client_name" TEXT,
  "business_name" TEXT,
  "address_id" INTEGER,
  "timestamp" TEXT,
  FOREIGN KEY(address_id) REFERENCES addresses(address_id)
);

CREATE TABLE company
(
  "company_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "company_name" TEXT,
  "bank_name" TEXT,
  "branch_name" TEXT,
  "tax_no" TEXT,
  "customer_no" TEXT,
  "timestamp" TEXT
);

CREATE TABLE stores
(
  "store_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "store_name" TEXT NOT NULL,
  "store_manager" TEXT,
  "store_tel_no" TEXT,
  "address_id" INTEGER,
  "company_id" INTEGER,
  "timestamp" TEXT,
  FOREIGN KEY(address_id) REFERENCES addresses(address_id),
  FOREIGN KEY(company_id) REFERENCES company(company_id)
);

CREATE TABLE invoices
(
  "invoice_id" TEXT PRIMARY KEY NOT NULL,
  "invoice_date" TEXT NOT NULL,
  "invoice_note" TEXT,
  "company_id" INTEGER,
  "client_id" INTEGER,
  "timestamp" TEXT,
  FOREIGN KEY(client_id) REFERENCES clients(client_id),
  FOREIGN KEY(company_id) REFERENCES company(company_id)
);

CREATE TABLE invoice_line_items
(
  "invoice_id" INTEGER NOT NULL,
  "line_item_id" INTEGER NOT NULL,
  "quantity" INTEGER,
  "item_description" TEXT,
  "price_ex_vat" REAL,
  "price_in_vat" REAL,
  "vat" REAL,
  "vat_catagory" TEXT,
  "timestamp" TEXT,
  PRIMARY KEY("invoice_id","line_item_id"),
  FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id)
);
"""
SQLITE_DB = PATH + '/db.sqlite'

conn = None

class SQLiteDb(object):
    def __init__(self):
        # need to populate dictionary with the following structure
        # {invoiceNo: client_details,...., [invoice_details,....]}
        """
        Initialize the DB.
        """
        global conn
        #if commit:
        #    atexit.register(commit_and_close)
        #else:
        #    atexit.register(close)
        if not os.path.exists(SQLITE_DB):
            print("creating database...")
            self.createDb()
            print("inserting test data...")
            self.insert_test_data_invoices()
            self.insert_test_data_stores()
            self.insert_test_data_company()
            self.insert_test_data_clients()
            self.insert_test_data_line_items()
            self.close()

        # initialise variables
        self.dbClients = ""
        self.dbInvoices = ""
        self.dbLineItems = ""
        self.dbCompany = ""
        self.dbStores = ""

        self.initialiseDbVariables()
        
#
    def createDb(self):
        """
        Create the DB if not exists.
        """
        global conn
        conn = sqlite3.connect(SQLITE_DB)
        conn.executescript(SCHEMA2)

    def initialiseDbVariables(self):
        global conn
        if not conn:
            try:
                print("Initialising variables")
                self.dbClients = self.getDbClients()
                self.dbInvoices = self.getDbInvoices()
                self.dbLineItems = self.getDbLineItems()
                self.dbCompany = self.getDbCompany()
                self.dbStores = self.getDbStores()

            except sqlite3.Error as e:
                out = "Error %s:" % e.args[0]
                print(out)
                sys.exit(1)
        
# inserting test data ################################################
    def insert_test_data_invoices(self):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO invoices (invoice_id, version, invoice_date, invoice_note, company_id, client_id, store_id, store_id2, timestamp) " \
                    + "VALUES (?,?,?,?,?,?,?,?,?)"
            #conn.execute(query, (invoice_id,invoice_date,invoice_note,company_id,client_id,store_id,timestamp))
            conn.execute(query, ("111/13","1","25062013","To be paid asap",1,1,1,1,"2013-06-04 17:31"))
            conn.execute(query, ("112/14","1","21042014","To be paid now",1,2,1,2,"2014-04-24 11:31"))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the invoice {0} is already in the DB..."))
            
    def insert_test_data_clients(self):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO clients (client_id, client_name, business_name, address_line1, address_line2, timestamp) "\
                    + "VALUES (?,?,?,?,?,?)"
            conn.execute(query, (1,"Ola La","Ola La Ltd", "address1","address2","2014-04-24 11:31"))
            conn.execute(query, (2,"Ola La as Well","Ola La as Well Ltd", "address1 - 2","address2 - 2","2013-04-23 10:11"))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the client {0} is already in the DB..."))

    def insert_test_data_company(self):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO company (company_name, bank_name, branch_code, tax_no, customer_no, timestamp)" \
                    + "VALUES (?,?,?,?,?,?)"
            conn.execute(query, ("Garten Roland Richter","KSK Bautzen","85550000","204/299/03603","1000025086","2013-06-04 17:31"))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the company {0} is already in the DB..."))

    def insert_test_data_stores(self):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO stores (store_name, store_manager, address_line1, address_line2, store_tel_no, timestamp)" \
                    + "VALUES (?,?,?,?,?,?)"
            conn.execute(query, ("Garten Roland Richter","Inh. A. Claussnitzer","Oppacher Strasse 22","02689 Sohland OT Wehrsdorf","035936/30434","2013-06-04 17:31"))
            conn.execute(query, ("Blumeneck Roland Richter","Inh. A. Claussnitzer","Dresdner Strasse 5","02681 Wilthen","03592/33045","2013-06-05 13:31"))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the store {0} is already in the DB..."))

    def insert_test_data_line_items(self):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO invoice_line_items (invoice_id, version, line_item_id, quantity, description, price_before_vat, vat_catagory, vat, price_after_vat, timestamp)" \
                    + "VALUES (?,?,?,?,?,?,?,?,?,?)"
            conn.execute(query, ("111/13","1","1","12x","Roses","10.00","7","0.70","10.70","2013-06-05 13:31"))
            conn.execute(query, ("111/13","1","2","1x","Pot","50.00","7","3.50","53.50","2013-06-05 13:31"))
            conn.execute(query, ("111/13","1","3","6x","Sausages","10.00","19","1.90","11.90","2013-06-05 13:31"))
            conn.execute(query, ("112/14","1","1","3x","Birthday cards","3.00","19","0.57","3.57","2014-02-25 10:42"))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the line item {0} is already in the DB..."))

# end of insertion ###################################################
# get data from database - initialise
    def getDbInvoices(self):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            query = "SELECT * FROM invoices"
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)
        finally:
            if conn:
                conn.close()
        
        return result
    
    def getDbClients(self):
        try:
            query = "SELECT * FROM clients"
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)
        finally:
            if conn:
                conn.close()
        return result
    
    def getDbCompany(self):
        try:
            query = "SELECT * FROM company"
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)
        finally:
            if conn:
                conn.close()
        return result
    
    def getDbStores(self):
        try:
            query = "SELECT * FROM stores"
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)
        finally:
            if conn:
                conn.close()
        return result

    def getDbLineItems(self):
        try:
            query = "SELECT * FROM invoice_line_items"
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)
        finally:
            if conn:
                conn.close()
        return result
# end of initialise

# get functions
    def getInvoices(self):
        return self.dbInvoices
    
    def getClients(self):
        return self.dbClients
    
    def getCompany(self):
        return self.dbCompany
    
    def getStores(self):
        return self.dbStores

    def getLineItems(self):
        return self.dbLineItems
# end of get functions

    def commit(self):
        """
        Commit.
        """
        if conn:
            conn.commit()
     
    def close(self):
        """
        Close.
        """
        if conn:
            conn.close()
     
    def commit_and_close(self):
        """
        Commit and close DB connection.
     
        As I noticed, commit() must be called, otherwise changes
        are not committed automatically when the program terminates.
        """
        if conn:
            conn.commit()
            conn.close()

# insert records in database
    def insertInvoice(self, invoiceNo, version, invoiceDate, invoiceNote, companyId, clientId, store1Id, store2Id, timestamp):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO invoices (invoice_id, version, invoice_date, invoice_note, company_id, client_id, store1_id, store2_id, timestamp) "\
                    + "VALUES (?,?,?,?,?,?,?,?,?)"
            conn.execute(query, (invoiceNo, version, invoiceDate, invoiceNote, companyId, clientId, store1Id, store2Id, timestamp))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the invoice {0} is already in the DB..."))

    def insertClient(self, clientId, clientName, businessName, addressLine1, addressLine2, timestamp):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO clients (client_id, client_name, business_name, address_line1, address_line2, timestamp) "\
                    + "VALUES (?,?,?,?,?,?)"
            conn.execute(query, (clientId, clientName, businessName, addressLine1, addressLine2, timestamp))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the client {0} is already in the DB..."))

    def insertCompany(self, companyId, bankName, branchCode, taxNo, customerNo, timestamp):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO company (company_name, bank_name, branch_code, tax_no, customer_no, timestamp)" \
                    + "VALUES (?,?,?,?,?,?)"
            conn.execute(query, (companyId, bankName, branchCode, taxNo, customerNo, timestamp))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the company {0} is already in the DB..."))

    def insertStore(self, storeId, storeName, storeManager, addressLine1, addressLine2, storeTelNo, timestamp):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO stores (store_id, store_name, store_manager, address_line1, address_line2, store_tel_no, timestamp)" \
                    + "VALUES (?,?,?,?,?,?,?)"
            conn.execute(query, (storeId, storeName, storeManager, addressLine1, addressLine2, storeTelNo, timestamp))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the store {0} is already in the DB..."))

# one line item at a time
    def insertLineItems(self, invoiceNo, version, lineItemId, quantity, description, priceBeforeVat, vatCategory, vat, priceAfterVat, timestamp):
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO invoice_line_items (invoice_id, version, line_item_id, quantity, description, price_before_vat, vat_catagory, vat, price_in_vat, timestamp)" \
                    + "VALUES (?,?,?,?,?,?,?,?,?,?)"
            conn.execute(query, (invoiceNo, version, lineItemId, quantity, description, priceBeforeVat, vatCategory, vat, priceAfterVat, timestamp))
            conn.commit()
        except sqlite3.IntegrityError:
            print(termcolor.colored("# the line item {0} is already in the DB..."))

    def saveInvoice(self, invoice):
        self.insert_invoice(invoice)
        self.insert_store(invoice)
        self.insert_store(invoice)
        self.insert_client(invoice)
        self.insert_line_items(invoice)
        self.insert_client(invoice)
        self.insert_company(invoice)
####################
 
if __name__ == "__main__":
    db = SQLiteDb()
    print("Invoices: ", db.getInvoices())
    print("LineItems: ", db.getLineItems())
    print("Company: ", db.getCompany())
    print("Clients: ", db.getClients())
    print("Stores: ", db.getStores())
    
