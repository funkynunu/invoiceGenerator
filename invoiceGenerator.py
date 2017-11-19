#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Controller for invoiceGenerator
"""
from iGController import Controller
from iGSync import Sync
from threading import Thread

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    # temp commented out for testing
    # # create instance of sync class
    # syncDbs = Sync()
    #
    # # create thread instance and pass it the sync class
    # t = Thread(target = syncDbs.doSync, args=(10,), daemon=True)
    # t.start()

    import sys
    import time

    #create frontend instance after delay for database sync
    time.sleep(2) # should be enough for initial sync, find another solution
    app = QApplication(sys.argv)

    invoiceGenerator = Controller()
    invoiceGenerator.show()

    sys.exit(app.exec_())