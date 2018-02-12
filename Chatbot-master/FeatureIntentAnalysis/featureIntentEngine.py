import sys
sys.path.append('../Data')
sys.path.append('../WebDataParser')
sys.path.append('../Utility')

import numpy as np
import tflearn
import tensorflow as tf
from featureIntentData import *
from tockenizeData import *
from Dataconverter import *
from webProductData import *
from json import dumps



class IntentAnalyzer:

    def __init__(self, Feature, product, domain):        
        self.webProductData = WebProductData(domain)
        self.featureValues = self.getFeatureValue(Feature, product)
        
        self.product = product
        self.Feature = Feature
        


    def getInputArray(self, var):        
        bagOfWords = IntentTrainingData.bagOfWords(self.Feature)
        listIntent = IntentTrainingData.listOfIntent(self.Feature)
        #filteredData = TockenizeData.getTockenizedDataWithStem(var)
        filteredData = TockenizeData.getTockenizedData(var)

        localTrainingSet = []
        for word in bagOfWords:        
            if word in filteredData:
                localTrainingSet.append(1)
            else:
                localTrainingSet.append(0)

        return localTrainingSet


    def getIntentAndValue(self, statement):
        #filteredData = TockenizeData.getTockenizedDataWithStem(statement)
        filteredData = TockenizeData.getTockenizedData(statement)

        Input = self.getInputArray(statement)        

        if len(filteredData) == 1:
            for f in self.featureValues:
                if filteredData[0] in f:
                    return "like", filteredData[0]

        var = Dataconverter.convertBinaryListToInt(IntentTrainingData.model[self.Feature].predict([Input]))

        filteredData = TockenizeData.getTockenizedData(statement)
        listIntent = IntentTrainingData.listOfIntent(self.Feature) 

        if var == -1:
            return "Error", "USER_ERROR"

        #if intent is question. process that question and return the reply in "Question", "Reply string" format                   
        
        intent = listIntent[var]
        featureValue = ""

        print filteredData
        print self.featureValues
        print intent
        for value in self.featureValues:
            if value in filteredData:
                featureValue = value
                return intent, featureValue
        
        return "Error", "SELECTION_NOT_AVAILABLE"
        
        

    def getFeatureValue(self,feature, product):
        return self.webProductData.getFeatureInfo({"product_list.product": product }, feature)

    def question(self):
        Button = self.featureValues
        if "Any" not in Button:
            Button.append("Any")
        return dumps({"Text": "Please select " + self.Feature, "Button" :Button})


if __name__ == "__main__":    
    IntentTrainingData.initialize()
    inAnaly = IntentAnalyzer("color","shoes","amazon.com")
    while(1):
        var = raw_input(">>")
        intent, featureValue = inAnaly.getIntentAndValue(var)
        print "you " + intent + " " + featureValue
    