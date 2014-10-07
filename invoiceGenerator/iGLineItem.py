class LineItem(object):
    def __init__(self, version, quantity, description, priceBeforeVat, \
            vatCategory, vat, priceAfterVat, timestamp):
        self.version = version
        self.quantity = quantity
        self.description = description
        self.priceBeforeVat = priceBeforeVat
        self.priceAfterVat = priceAfterVat
        self.vat = vat
        self.vatCategory = vatCategory
        self.timestamp = timestamp

    # def setVersion(self, version):
    #     self.version = version
    #
    # def setQuantity(self, quantity):
    #     self.quantity = quantity
    #
    # def setDescription(self, description):
    #     self.description = description
    #
    # def setPriceBeforeVat(self, price):
    #     self.priceBeforeVat = price
    #
    # def setPriceAfterVat(self, price):
    #     self.priceAfterVat = price
    #
    # def setVat(self, vat):
    #     self.vat = vat
    #
    # def setVatCatagory(self, category):
    #     self.vatCategory = category
    #
    # def setTimestamp(self, timestamp):
    #     self.timestamp = timestamp
    #
    # def getVersion(self):
    #     return self.version
    #
    # def getQuantity(self):
    #     return self.quantity
    #
    # def getDescription(self):
    #     return self.description
        
    def getPriceBeforeVat(self):
        return format(self.priceBeforeVat, '0.2f')
        
    def getPriceAfterVat(self):
        return format(self.priceAfterVat, '0.2f')
        
    def getVat(self):
        return format(self.vat, '0.2f')
        
    # def getVatCategory(self):
    #     return self.vatCategory
    #
    # def getTimestamp(self):
    #     return self.timestamp
