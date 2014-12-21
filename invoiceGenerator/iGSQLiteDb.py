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
#import termcolor
import sys
import datetime
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

# Note: in line_items, price_after_vat is included because
# price_before_vat + vat might not add up

# timestamp are calculated when an invoice record is inserted into
# the Invoice table. Whenever there is a change to an Invoice whether
# it is client, company or item details, the updated Invoice record
# a new timestamp. The only timestamp field is in the Invoice table
SCHEMA = """
CREATE TABLE IF NOT EXISTS company
(
  "company_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "bank_name" TEXT,
  "branch_code" TEXT,
  "tax_no" TEXT,
  "customer_no" TEXT
);

CREATE TABLE IF NOT EXISTS store
(
  "store_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "company_id" INTEGER NOT NULL,
  "store_name" TEXT NOT NULL,
  "store_manager" TEXT,
  "address_line1" TEXT NOT NULL,
  "address_line2" TEXT,
  "store_tel_no" TEXT,
  FOREIGN KEY(company_id) REFERENCES company(company_id)
);

CREATE TABLE IF NOT EXISTS client
(
  "client_id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "contact_name" TEXT NOT NULL,
  "business_name" TEXT,
  "address_line1" TEXT NOT NULL,
  "address_line2" TEXT
);

CREATE TABLE IF NOT EXISTS invoice
(
  "invoice_id" TEXT NOT NULL,
  "version" INTEGER NOT NULL,
  "invoice_date" TEXT NOT NULL,
  "invoice_note" TEXT,
  "company_id" INTEGER NOT NULL,
  "client_id" INTEGER NOT NULL,
  "timestamp" TEXT NOT NULL,
  PRIMARY KEY("invoice_id","version"),
  FOREIGN KEY(client_id) REFERENCES client(client_id),
  FOREIGN KEY(company_id) REFERENCES company(company_id)
);

CREATE UNIQUE INDEX unique_timestamp ON invoice(timestamp);

CREATE TABLE IF NOT EXISTS line_item
(
  "invoice_id" TEXT NOT NULL,
  "version" INTEGER NOT NULL,
  "line_item_id" INTEGER NOT NULL,
  "quantity" INTEGER,
  "description" TEXT,
  "price_before_vat" REAL,
  "vat_category" TEXT,
  "vat_amount" REAL,
  "price_after_vat" REAL,
  PRIMARY KEY("invoice_id","version","line_item_id"),
  FOREIGN KEY(invoice_id,version) REFERENCES invoice(invoice_id,version)
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
        if not os.path.exists(SQLITE_DB):
            try:
                self.createDb()
                self.insert_test_data_invoices()
                self.insert_test_data_stores()
                self.insert_test_data_company()
                self.insert_test_data_clients()
                self.insert_test_data_line_items()
            except sqlite3.Error as e:
                out = "Error %s:" % e.args[0]
                print(out)
                sys.exit(1)
            finally:
                if conn:
                    conn.close()

        # initialise variables
    #     self.dbClients = self.getDbClients()
    #     self.dbInvoices = self.getDbInvoices()
    #     self.dbLineItems = self.getDbLineItems()
    #     self.dbCompany = self.getDbCompany()
    #     self.dbStores = self.getDbStores()


        self.initialiseDbVariables()

#
    def createDb(self):
        print("    SQLiteDB.createDb")
        """
        Create the DB if not exists.
        """
        global conn
        conn = sqlite3.connect(SQLITE_DB)
        conn.executescript(SCHEMA)

    def initialiseDbVariables(self):
        print("    SQLiteDB.initialiseDbVariables")
        try:
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
        print("    SQLiteDB.insert_test_data_invoices")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO invoice (invoice_id, version, invoice_date, invoice_note, company_id, client_id, timestamp) " \
                    + "VALUES (?,?,?,?,?,?,?)"
            #cur.execute(query, (invoice_id,invoice_date,invoice_note,company_id,client_id,timestamp))
            cur.execute(query, ("111/13", "1", "25/06/2013", "To be paid asap", 1, 1, "2013-06-04 17:31"))
            cur.execute(query, ("1/14", "1", "21/01/2014", "To be paid now", 1, 2, "2014-01-21 11:31"))
            cur.execute(query, ("2/14", "1", "22/02/2014", "To be paid now", 1, 3, "2014-02-22 11:31"))
            cur.execute(query, ("2/14", "2", "24/02/2014", "To be paid now", 1, 3, "2014-02-24 11:31"))
            cur.execute(query, ("3/14", "1", "22/03/2014", "To be paid now", 1, 4, "2014-03-22 11:31"))
            cur.execute(query, ("4/14", "1", "22/04/2014", "To be paid now", 2, 2, "2014-04-22 11:31"))
            cur.execute(query, ("5/14", "1", "22/05/2014", "To be paid now", 2, 3, "2014-05-22 11:31"))
            cur.execute(query, ("5/14", "2", "24/05/2014", "To be paid now", 2, 3, "2014-05-24 11:31"))
            cur.execute(query, ("5/14", "3", "26/05/2014", "To be paid now", 3, 3, "2014-05-26 11:31"))
            cur.execute(query, ("6/14", "1", "22/06/2014", "To be paid now", 3, 4, "2014-06-22 11:31"))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the invoice {0} is already in the DB...")

    def insert_test_data_clients(self):
        print("    SQLiteDB.insert_test_data_clients")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO client (client_id, contact_name, business_name, address_line1, address_line2) "\
                    + "VALUES (?,?,?,?,?)"
            cur.execute(query, (1,"Ola La","Ola La Ltd", "Pfaffendorfer Straße 29", "04105, Leipzig"))
            cur.execute(query, (2,"Diana Clausznitzer","Sugar Me Timbers Ltd", "Zellescher Weg 18", "01069, Dresden"))
            cur.execute(query, (3,"Bob Newhart","Acompany Ltd", "Borsbergstrasse 1","01309, Dresden"))
            cur.execute(query, (4,"Jaime Campus","easy-soft GmbH", "Fetscherstraße 32", "01307, Dresden"))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the client {0} is already in the DB...")

    def insert_test_data_company(self):
        print("    SQLiteDB.insert_test_data_company")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO company (bank_name, branch_code, tax_no, customer_no)" \
                    + "VALUES (?,?,?,?)"
            cur.execute(query, ("KSK Bautzen", "11111111","111/111/11111","1111111111"))
            cur.execute(query, ("Volksbank Bautzen", "22222222","222/222/22222","2222222222"))
            cur.execute(query, ("Volksbank Bautzen", "22222222","222/222/22222","2222222222"))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the company {0} is already in the DB...")

    def insert_test_data_stores(self):
        print("    SQLiteDB.insert_test_data_stores")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO store (store_name, company_id, store_manager, store_tel_no, address_line1, address_line2)" \
                    + "VALUES (?,?,?,?,?,?)"
            cur.execute(query, ("Garten Roland Richter", 1, "Inh. A. Claussnitzer","035936/30434","Oppacher Strasse 22","02689 Sohland OT Wehrsdorf"))
            cur.execute(query, ("Blumeneck Roland Richter", 1, "Inh. A. Claussnitzer","03592/33045","Dresdner Strasse 5","02681 Wilthen"))
            cur.execute(query, ("Garten Roland Richter", 2, "Inh. A. Claussnitzer","11111/11111","Oppacher Strasse 22","02689 Sohland OT Wehrsdorf"))
            cur.execute(query, ("Blumeneck Roland Richter", 2, "Inh. A. Claussnitzer","22222/22222","Dresdner Strasse 5","02681 Wilthen"))
            cur.execute(query, ("Garten Roland Richter", 3, "Inh. A. Claussnitzer","11111/11111","Oppacher Strasse 22","11111 Sohland OT Wehrsdorf"))
            cur.execute(query, ("Blumeneck Roland Richter", 3, "Inh. A. Claussnitzer","22222/22222","Dresdner Strasse 5","22222 Wilthen"))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the store {0} is already in the DB...")

    def insert_test_data_line_items(self):
        print("    SQLiteDB.insert_test_data_line_items")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO line_item (invoice_id, version, line_item_id, quantity, description, price_before_vat, vat_category, vat_amount, price_after_vat)" \
                    + "VALUES (?,?,?,?,?,?,?,?,?)"
            cur.execute(query, ("111/13","1","1","12","Roses","10.00","7","0.70","10.70"))
            cur.execute(query, ("111/13","1","2","1","Pot","50.00","7","3.50","53.50"))
            cur.execute(query, ("111/13","1","3","6","Sausages","10.00","19","1.90","11.90"))
            cur.execute(query, ("1/14","1","1","3","version 1 line 1","3.00","19","0.57","3.57"))
            cur.execute(query, ("2/14","1","1","3","version 1 line 1","3.00","19","0.57","3.57"))
            cur.execute(query, ("2/14","2","1","3","version 2 line 1","3.00","19","0.57","3.57"))
            cur.execute(query, ("2/14","2","2","3","version 2 line 2","3.00","19","0.57","3.57"))
            cur.execute(query, ("3/14","1","1","3","version 1 line 1","3.00","19","0.57","3.57"))
            cur.execute(query, ("4/14","1","1","3","version 1 line 1","3.00","19","0.57","3.57"))
            cur.execute(query, ("5/14","1","1","3","version 1 line 1","3.00","19","0.57","3.57"))
            cur.execute(query, ("5/14","2","1","3","version 2 line 1","3.00","19","0.57","3.57"))
            cur.execute(query, ("5/14","2","2","3","version 2 line 2","3.00","19","0.57","3.57"))
            cur.execute(query, ("5/14","3","1","3","version 3 line 1","3.00","19","0.57","3.57"))
            cur.execute(query, ("5/14","3","2","3","version 3 line 2","3.00","19","0.57","3.57"))
            cur.execute(query, ("5/14","3","3","3","version 3 line 3","3.00","19","0.57","3.57"))
            cur.execute(query, ("6/14","1","1","3","version 1 line 1","3.00","19","0.57","3.57"))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the line item {0} is already in the DB...")

# end of insertion ###################################################
# get data from database - initialise
    def getDbInvoices(self):
        print("    SQLiteDB.getDbInvoices")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            query = "SELECT * FROM invoice"
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
        print("    SQLiteDB.getDbClients")
        try:
            query = "SELECT * FROM client"
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
        print("    SQLiteDB.getDbCompany")
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
        print("    SQLiteDB.getDbStores")
        try:
            query = "SELECT * FROM store"
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
        print("    SQLiteDB.getDbLineItems")
        try:
            query = "SELECT * FROM line_item"
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
        print("    SQLiteDB.getInvoices")
        return self.dbInvoices

    def getClients(self):
        print("    SQLiteDB.getClients")
        return self.dbClients
    
    def getCompany(self):
        print("    SQLiteDB.getCompany")
        return self.dbCompany
    
    def getStores(self):
        print("    SQLiteDB.getStores")
        return self.dbStores

    def getLineItems(self):
        print("    SQLiteDB.getLineItems")
        return self.dbLineItems
# end of get functions

    def commit(self):
        print("    SQLiteDB.commit")
        """
        Commit.
        """
        if conn:
            conn.commit()
     
    def close(self):
        print("    SQLiteDB.close")
        """
        Close.
        """
        if conn:
            conn.close()
     
    def commit_and_close(self):
        print("    SQLiteDB.commit_and_close")
        """
        Commit and close DB connection.
     
        As I noticed, commit() must be called, otherwise changes
        are not committed automatically when the program terminates.
        """
        if conn:
            conn.commit()
            conn.close()

# insert records in database
    def insertInvoice(self, invoiceNo, version, invoiceDate, invoiceNote, companyId, clientId, timestamp):
        print("    SQLiteDB.insertInvoice")

        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO invoice (invoice_id, version, invoice_date, invoice_note, company_id, client_id, timestamp) "\
                    + "VALUES (?,?,?,?,?,?,?)"
            cur.execute(query, (invoiceNo, version, invoiceDate, invoiceNote, companyId, clientId, timestamp))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the invoice {0} is already in the DB...")

    def insertClient(self, clientId, contactName, businessName, addressLine1, addressLine2):
        print("    SQLiteDB.insertClient")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO client (client_id, contact_name, business_name, address_line1, address_line2) "\
                    + "VALUES (?,?,?,?,?)"
            cur.execute(query, (clientId, contactName, businessName, addressLine1, addressLine2))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the client {0} is already in the DB...")

    def insertCompany(self, companyId, bankName, branchCode, taxNo, customerNo):
        print("    SQLiteDB.insertCompany")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO company (company_id, bank_name, branch_code, tax_no, customer_no)" \
                    + "VALUES (?,?,?,?,?)"
            cur.execute(query, (companyId, bankName, branchCode, taxNo, customerNo))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the company {0} is already in the DB...")

    def insertStore(self, storeId, companyId, storeName, storeManager, addressLine1, addressLine2, storeTelNo):
        " Inserts a new record into sqlite store table"
        print("    SQLiteDB.insertStore")
        # when updating or insert a new store, two new store records must be created as well as
        # a new company record relative to the new stores
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO store (store_id, company_id, store_name, store_manager, address_line1, address_line2, store_tel_no)" \
                    + "VALUES (?,?,?,?,?,?,?)"
            cur.execute(query, (storeId, companyId, storeName, storeManager, addressLine1, addressLine2, storeTelNo))
            conn.commit()
        except sqlite3.IntegrityError:
            print(storeId, companyId, storeName, storeManager, addressLine1, addressLine2, storeTelNo)
            print("# the store {0} is already in the DB...")

# one line item at a time
    def insertLineItems(self, invoiceNo, version, lineItemId, quantity, description, \
                        priceBeforeVat, vatCategory, vatAmount, priceAfterVat):
        print("    SQLiteDB.insertLineItems")
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            query = "INSERT INTO line_item (invoice_id, version, line_item_id, quantity, description, price_before_vat, vat_category, vat_amount, price_after_vat)" \
                    + "VALUES (?,?,?,?,?,?,?,?,?)"
            cur.execute(query, (invoiceNo, version, lineItemId, quantity, description, priceBeforeVat, vatCategory, vatAmount, priceAfterVat))
            conn.commit()
        except sqlite3.IntegrityError:
            print("# the line item {0} is already in the DB...")

    def saveInvoice(self, invoice):
        print("    SQLiteDB.saveInvoice")
        self.insert_invoice(invoice)
        self.insert_store(invoice)
        self.insert_store(invoice)
        self.insert_client(invoice)
        self.insert_line_items(invoice)
        self.insert_client(invoice)
        self.insert_company(invoice)
####################

    # a timestamp is only retrieved when at the point an entry is made to the db
    def getTimestamp(self):
        print("    SQLiteDB.getTimestamp")
        now = datetime.datetime.now()
        return datetime.datetime.now().strftime("%d/%m/%Y %H:%M")


 
if __name__ == "__main__":
    db = SQLiteDb()
    print("    SQLiteDB.Invoices: ", db.getInvoices())
    print("    SQLiteDB.LineItems: ", db.getLineItems())
    print("    SQLiteDB.Company: ", db.getCompany())
    print("    SQLiteDB.Clients: ", db.getClients())
    print("    SQLiteDB.Stores: ", db.getStores())
    
