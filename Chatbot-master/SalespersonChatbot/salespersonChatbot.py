import sys

from webProductData import *
from featureEngine import *
from featureDetection import FeatureDetection
from json import dumps
import json


class SalespersonChatbot:

    def __init__(self, domain): 
        self.webProductData = WebProductData(domain)
        self.domain = domain
        self.product = False
        
        self.productList = self.webProductData.getProductList()
        self.featureDetect = FeatureDetection()

    def getProductList(self):
        self.product = True
        prod = {}
        prod["Text"] = "Product List"
        prod["Button"] = self.productList
        prod['Template'] = []
        prod['Error'] = ""
        prod['Input_status'] = ""
        return dumps(prod)

    def createFeatureInstance(self,product):
        self.product = False
        if product not in self.productList:
            print "Website does not sell " + product
            return -1

        self.featureInstance = []
        self.featureList = self.webProductData.getFeatureList({"product_list.product": product })

        for feature in self.featureList:
            self.featureInstance.append(FeatureEngine(feature, product, self.domain))

    def output(self, intent, result):  
      
        for featureObject in self.featureInstance:
                if featureObject.isSlothasValue() == False:
                    self.featureDetect.setcontext(featureObject.feature)
                    r = json.loads(featureObject.getQuestion())
                    r["Input_status"] = intent + " " + result
                    r["template"] = []
                    r["Error"] = ""
                    return dumps(r)        
        
        return self.createFinalResponse()

    def input(self, statement):
        feature = self.featureDetect.getFeature(statement)
        for fObject in self.featureInstance:
            if fObject.feature == feature:
                intent, value = fObject.getIntentAndValue(statement)
                return (intent, value)

    def processInput(self,statement):
        intent, result = self.input(statement)
        return self.output(intent, result)

    def createFinalResponse(self):
        res = {}
        res["Button"] = []
        feature = {}
        for featureObject in self.featureInstance:
            if "NO#Choice" not in featureObject.slot:
                print featureObject.feature + ":"+featureObject.slot
                feature["product_list."+featureObject.feature] = featureObject.slot
                res["Button"].append(featureObject.slot)

        print res["Button"]
        res["Text"] = "Selected Items"
        print feature
        res['Template'] = self.webProductData.getProductDetails(feature)
        res['Error'] = ""
        res['Input_status'] = ""
    
        print dumps(res)
        return dumps(res)
                
                    