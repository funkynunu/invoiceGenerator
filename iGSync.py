import time
from iGSQLiteDb import SQLiteDb
from iGPSQLDb import PostgreSQLDb
import pickle

class Sync:
    def __init__(self):
        print("iGSync")
        self.SQLiteDb = ""
        self.postgreSQLDb = ""

    def doSync(self, arg):
        while True:
            # load user settings
            try:
                with open('preferences.pickle', 'rb') as f:
                    preferences = pickle.load(f)
            except:
                print('Preferences not found')
                break

            # load local
            self.SQLiteDb = SQLiteDb()
            localInvoices = self.SQLiteDb.getInvoices()

            # load remote
            self.postgreSQLDb = PostgreSQLDb(preferences['host'],preferences['database'], \
                                             preferences['username'],preferences['password'])
            remoteInvoices = self.postgreSQLDb.getInvoices()

            # compare timestamp of invoice database
            # http://wtfbigdata.vickiboykis.com/2013/09/06/how-to-compare-two-lists-in-python/
            # http://www.saltycrane.com/blog/2008/01/how-to-find-intersection-and-union-of/
            missingFromLocal = list(set(remoteInvoices).difference(set(localInvoices)))

            missingFromRemote= list(set(localInvoices).difference(set(remoteInvoices)))

            # upload to local
            print("Uploading data to SQLite db")
            for invoice in missingFromLocal:
                # get and insert company
                for company in self.postgreSQLDb.getCompany():
                    if company[0] == invoice[4]:
                        # get and insert stores
                        for store in self.postgreSQLDb.getStores():
                            # should check if store already exists
                            self.SQLiteDb.insertStore(store[0],store[1],store[2],store[3],store[4],store[5],store[6])
                        print(company)

                        self.SQLiteDb.insertCompany(company[0],company[1],company[2],company[3],company[4])

                # get and insert client
                for client in self.postgreSQLDb.getClients():
                    if client[0] == invoice[5]:
                        self.SQLiteDb.insertClient(client[0],client[1],client[2],client[3],client[4])

                # insert invoice
                self.SQLiteDb.insertInvoice(invoice[0],invoice[1],invoice[2],invoice[3], \
                                                invoice[4],invoice[5],invoice[6])

                # get and insert line items
                for lineitem in self.postgreSQLDb.getLineItems():
                    if lineitem[0] == invoice[0] and lineitem[1] == invoice[1]:
                        #
                        self.SQLiteDb.insertLineItems(lineitem[0],lineitem[1],lineitem[2],lineitem[3], \
                                                          lineitem[4],lineitem[5],lineitem[6],lineitem[7],lineitem[8])

            # upload to remote
            print("Uploading data to PostgreSQL db")
            for invoice in missingFromRemote:
                # get and insert company and stores
                for company in self.SQLiteDb.getCompany():
                    if company[0] == invoice[4]:
                        self.postgreSQLDb.insertCompany(company[0],company[1],company[2],company[3],company[4])
                        # get and insert stores
                        for store in self.SQLiteDb.getStores():
                            # should check if store already exists
                            print("here: ", store)
                            self.postgreSQLDb.insertStore(store[0],store[1],store[2],store[3],store[4],store[5],store[6])



                # get and insert client
                for client in self.SQLiteDb.getClients():
                    if client[0] == invoice[5]:
                        self.postgreSQLDb.insertClient(client[0],client[1],client[2],client[3],client[4])

                # insert invoice
                self.postgreSQLDb.insertInvoice(invoice[0],invoice[1],invoice[2],invoice[3], \
                                                invoice[4],invoice[5],invoice[6])

                # get and insert line items
                for lineitem in self.SQLiteDb.getLineItems():
                    if lineitem[0] == invoice[0] and lineitem[1] == invoice[1]:
                        #
                        self.postgreSQLDb.insertLineItems(lineitem[0],lineitem[1],lineitem[2],lineitem[3], \
                                                          lineitem[4],lineitem[5],lineitem[6],lineitem[7],lineitem[8])

                #after each invoice inserted

            time.sleep(60)
        print(arg)
