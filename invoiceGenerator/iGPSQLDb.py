#!/usr/bin/python
# -*- coding: utf-8 -*-

# passwords....
# http://code.activestate.com/recipes/578443-storing-a-single-username-and-encrypted-password-t/

# installed driver from
# http://www.stickpeople.com/projects/python/win-psycopg/
# file: psycopg2-2.5.3.win32-py3.4-pg9.3.4-release.exe

# http://www.tutorialspoint.com/postgresql/postgresql_python.htm
import psycopg2
import sys

class PostgreSQLDb(object):
    def __init__(self, host, database, user, pw):
        self.host = host
        self.dbName = database
        self.dbUser = user
        self.password = pw

    def getStores(self):
        print("PSQLDb.getStores")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()

            query = "SELECT * FROM invoices.store"
            cur.execute(query)
            result = cur.fetchall()

        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)

        finally:
            if con:
                con.close()
        return result

    def getClients(self):
        print("PSQLDb.getClients")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()

            query = "SELECT * FROM invoices.client"
            cur.execute(query)
            result = cur.fetchall()
            con.close()
        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)
        finally:
            if con:
                con.close()
        return result

    def getCompany(self):
        print("PSQLDb.getCompany")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()

            query = "SELECT * FROM invoices.company"
            cur.execute(query)
            result = cur.fetchall()

        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)

        finally:
            if con:
                con.close()
        return result

    def getLineItems(self):
        print("PSQLDb.getLineItems")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()

            query = "SELECT * FROM invoices.line_item"
            cur.execute(query)

            result = cur.fetchall()

        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)
            sys.exit(1)

        finally:
            if con:
                con.close()

        return result


    def getInvoices(self):
        print("PSQLDb.getInvoices")
        con = None

        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()

            # invoices
            query = "SELECT * FROM invoices.invoice"
            cur.execute(query)

            result = cur.fetchall()

        except psycopg2.DatabaseError:
            if con:
                con.rollback()

            print('Error - DatabaseError')
            sys.exit(1)

        except IOError:
            if con:
                con.rollback()

            print('Error - IOError')
            sys.exit(1)

        finally:
            if con:
                con.close()

        return result

    def insertClient(self, clientId, contactName, businessName, addressLine1, addressLine2):
        print("PSQLDb.insertClient")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()
            prequery = "INSERT INTO invoices.client (client_id, contact_name, business_name, address_line1, address_line2)"\
                    + " VALUES ({0},'{1}','{2}','{3}','{4}')"
            query = prequery.format(clientId, contactName, businessName, addressLine1, addressLine2)
            cur.execute(query)
            con.commit()
            print("Client inserted")
        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)

    def insertStore(self, storeId, companyId, storeName, storeManager, addressLine1, addressLine2, storeTelNo):
        print("PSQLDb.insertStore")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()
            prequery = "INSERT INTO invoices.store (store_id, company_id, store_name, store_manager, address_line1, address_line2, store_tel_no)" \
                    + " VALUES ({0},'{1}','{2}','{3}','{4}','{5}', '{6}')"
            query = prequery.format(storeId, companyId, storeName, storeManager, addressLine1, addressLine2, storeTelNo)
            cur.execute(query)
            con.commit()
            con.close()
            print("Store inserted")
        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)

    def insertCompany(self, companyId, bankName, branchCode, taxNo, customerNo):
        print("PSQLDb.insertCompany")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()
            prequery = "INSERT INTO invoices.company (company_id, bank_name, branch_code, tax_no, customer_no)" \
                    + " VALUES ({0},'{1}','{2}','{3}','{4}')"
            query = prequery.format(companyId, bankName, branchCode, taxNo, customerNo)
            cur.execute(query)
            con.commit()
            con.close()
            print("Company inserted")
        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)

    def insertInvoice(self, invoiceNo, version, invoiceDate, invoiceNote, companyId, clientId, timestamp):
        print("PSQLDb.insertInvoice")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()
            prequery = "INSERT INTO invoices.invoice (invoice_id, version, invoice_date, invoice_note, company_id, client_id, timestamp)"\
                    + " VALUES ('{0}',{1},'{2}','{3}',{4},{5},'{6}')"
            query = prequery.format(invoiceNo, version, invoiceDate, invoiceNote, companyId, clientId, timestamp)
            cur.execute(query)
            con.commit()
            print("Invoice inserted")
        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)

    def insertLineItems(self, invoiceNo, version, lineItemId, quantity, description, \
                        priceBeforeVat, vatCategory, vatAmount, priceAfterVat):
        print("PSQLDb.insertLineItems")
        try:
            con = psycopg2.connect(host=self.host, dbname=self.dbName, user=self.dbUser, password=self.password)
            cur = con.cursor()
            prequery = "INSERT INTO invoices.line_item (invoice_id, version, line_item_id, quantity, description, price_before_vat, vat_category, vat_amount, price_after_vat)" \
                    + " VALUES ('{0}',{1},{2},{3},'{4}',{5},'{6}',{7},{8})"
            query = prequery.format(invoiceNo, version, lineItemId, quantity, description, priceBeforeVat, vatCategory, vatAmount, priceAfterVat)
            cur.execute(query)
            con.commit()
            con.close()
            print("Line item inserted")
        except psycopg2.Error as e:
            out = "Error: %s" % e.args[0]
            print(out)


# add host value to psycopg2.connect()
database_name = 'Roland Richter'
user_name = 'rolandrichter'
userpw = 'mamamia'
host = '127.0.0.1'

if __name__ == "__main__":
    postgreSQLDb = PostgreSQLDb(database_name, user_name, userpw, host)
    postgreSQLDb.getInvoices()