from database import *

class WebProductData:
    def __init__(self, webDomain):
        self.domain = webDomain 

    def getFeatureInfo(self, condition, feature):
        condition["Key"] = self.domain
        return Database.getFeatureInfo(condition, feature)
        
    def getProductList(self):
        condition = {}
        condition["Key"] = self.domain
        return Database.getProductList(condition)

    def getFeatureList(self, condition):
        condition["Key"] = self.domain
        return Database.getFeatureList(condition)
    
    def getProductDetails(self, condition):
        condition["Key"] = self.domain
        return Database.getProductDetails(condition)


#wpd = WebProductData("amazon.com")
#wpd.getProductList()
#wpd.getFeatureInfo({"product_list.product": "shoes" }, 'color');
#wpd.getFeatureList({"product_list.product": "shoes" })