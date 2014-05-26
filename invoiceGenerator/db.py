# https://pythonadventures.wordpress.com/2014/05/12/an-sqlite-example/
# data types - http://www.tutorialspoint.com/sqlite/sqlite_data_types.htm
# timestamp - http://www.sqlite.org/lang_datefunc.html
# autoincrement - http://www.sqlite.org/autoinc.html
#!/usr/bin/env python

"""
Sqlite database handler.
"""
 
import os
import sqlite3
import atexit
import termcolor
#import random
 
PATH = os.path.dirname(os.path.abspath(__file__))
SCHEMA = """
CREATE TABLE addresses
(
  "address_id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  "address_line1" text NOT NULL,
  "address_line2" text,
  "timestamp" text
);
  
CREATE TABLE clients
(
  "client_id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  "client_name" text,
  "business_name" text,
  "address_id" integer,
  "timestamp" text,
  FOREIGN KEY(address_id) REFERENCES addresses(address_id)
);

CREATE TABLE company
(
  "company_id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  "company_name" text,
  "bank_name" text,
  "branch_name" text,
  "tax_no" text,
  "customer_no" text,
  "timestamp" text
);

CREATE TABLE stores
(
  "store_id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  "store_name" text NOT NULL,
  "store_manager" text,
  "store_tel_no" text,
  "address_id" integer,
  "company_id" integer,
  "timestamp" text,
  FOREIGN KEY(address_id) REFERENCES addresses(address_id),
  FOREIGN KEY(company_id) REFERENCES company(company_id)
);

CREATE TABLE invoices
(
  "invoice_id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  "invoice_date" date NOT NULL,
  "invoice_note" text,
  "company_id" integer,
  "client_id" integer,
  "timestamp" text,
  FOREIGN KEY(client_id) REFERENCES clients(client_id),
  FOREIGN KEY(company_id) REFERENCES company(company_id)
);

CREATE TABLE invoice_line_items
(
  "invoice_id" integer NOT NULL,
  "line_item_id" integer NOT NULL,
  "quantity" integer,
  "item_description" text,
  "price_ex_vat" real,
  "price_in_vat" real,
  "vat" real,
  "vat_catagory" text,
  "timestamp" text,
  PRIMARY KEY("invoice_id","line_item_id"),
  FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id)
);
"""
SQLITE_DB = PATH + '/db.sqlite'
 
conn = None
 
def get_symbols():
    query = "SELECT symbol FROM symbols"
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result
 
def add_symbol(symbol):
    try:
        query = "INSERT INTO symbols (symbol) VALUES (?)"
        conn.execute(query, (symbol))
    except sqlite3.IntegrityError:
        print termcolor.colored("# the image {0} is already in the DB...".format(url), "red")
  
def create_db():
    """
    Create the DB if not exists.
    """
    global conn
    conn = sqlite3.connect(SQLITE_DB)
    conn.executescript(SCHEMA)
 
def init(commit=True):
    """
    Initialize the DB.
    """
    global conn
    if commit:
        atexit.register(commit_and_close)
    else:
        atexit.register(close)
 
    if not os.path.exists(SQLITE_DB):
        create_db()
    if not conn:
        conn = sqlite3.connect(SQLITE_DB)
 
def commit():
    """
    Commit.
    """
    if conn:
        conn.commit()
 
def close():
    """
    Close.
    """
    if conn:
        conn.close()
 
def commit_and_close():
    """
    Commit and close DB connection.
 
    As I noticed, commit() must be called, otherwise changes
    are not committed automatically when the program terminates.
    """
    if conn:
        conn.commit()
        conn.close()
 
####################
 
if __name__ == "__main__":
    init()
