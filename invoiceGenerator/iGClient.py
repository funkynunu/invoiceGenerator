class Client(object):
    def __init__(self, clientId, name, businessName, address1, address2, timestamp):
        self.id = clientId
        self.name = name
        self.businessName = businessName
        self.address1 = address1
        self.address2 = address2
        self.timestamp = timestamp

    # def setId(self, clientId):
    #     self.clientId = clientId
    #
    # def setName(self, aName):
    #     self.name = aName
    #
    # def setBusinessName(self, aBusinessName):
    #     self.businessName = aBusinessName
    #
    # def setAddress1(self, address1):
    #     self.address1 = address1
    #
    # def setAddress2(self, address2):
    #     self.address2 = address2
    #
    # def getId(self):
    #     return self.clientId
    #
    # def getName(self):
    #     return self.name
    #
    # def getBusinessName(self):
    #     return self.businessName
    #
    # def getAddress1(self):
    #     return self.address1
    #
    # def getAddress2(self):
    #     return self.address2
    #
    # def getTimestamp(self):
    #     return self.timestamp
    #
