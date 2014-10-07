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
    # create instance of sync class
    syncDbs = Sync()

    # create thread instance and pass it the sync class
    t = Thread(target = syncDbs.doSync, args=(10,), daemon=True)
    t.start()

    import sys

    #create frontend instance
    app = QApplication(sys.argv)

    invoiceGenerator = Controller()
    invoiceGenerator.show()

    sys.exit(app.exec_())