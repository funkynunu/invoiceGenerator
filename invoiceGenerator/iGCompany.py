class Company(object):
    def __init__(self, companyId, bankName, branchCode, taxNo, customerNo, timestamp):
        self.companyId = companyId
        self.bankName = bankName
        self.branchCode = branchCode
        self.taxNo = taxNo
        self.customerNo = customerNo
        self.timestamp = timestamp

    # def setId(self, companyId):
    #     self.companyId = companyId
    #
    # def setBankName(self, bankName):
    #     self.bankName = bankName
    #
    # def setBranchCode(self, branchCode):
    #     self.branchCode = branchCode
    #
    # def setTaxNo(self, taxNo):
    #     self.taxNo = taxNo
    #
    # def setCustomerNo(self, customerNo):
    #     self.customerNo = customerNo
    #
    # def getId(self):
    #     return self.companyId
    #
    # def getBankName(self):
    #     return self.bankName
    
    def getBranchCode(self):
        return str(self.branchCode)
    
    # def getTaxNo(self):
    #     return self.taxNo
    #
    # def getCustomerNo(self):
    #     return self.customerNo
    #
    # def getTimestamp(self):
    #     return self.timestamp
    
