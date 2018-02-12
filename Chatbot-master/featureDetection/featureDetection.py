import sys
sys.path.append('../Utility')

from tockenizeData import *
import random
import numpy as np
from Dataconverter import *
from featureTrainingDataFileReader import *
import tflearn
import tensorflow as tf


class FeatureDetectionEngine:    
    
    trainingData = None
    model = {}
    @staticmethod
    def initialize():
        FeatureDetectionEngine.trainingData = FeatureTrainingDataFileReader().getFeatureTrainingData()
        FeatureDetectionEngine.trainModel()

    @staticmethod
    def getFilteredTrainingData():
        FilteredTrainingSet = []

        for statement, feature in FeatureDetectionEngine.trainingData:
            #f = TockenizeData.getTockenizedDataWithStem(statement)
            f = TockenizeData.getTockenizedData(statement)
            FilteredTrainingSet.append((f, feature))

        return FilteredTrainingSet
    
    @staticmethod
    def bagOfWords():
        FilteredTrainingSet = FeatureDetectionEngine.getFilteredTrainingData()
        
        listElements = []
        for elements, feature in FilteredTrainingSet:
            for element in elements:
                listElements.append(element)
        print list(set(listElements))
        return list(set(listElements))

    @staticmethod
    def listOfFeature():
        FilteredTrainingSet = FeatureDetectionEngine.getFilteredTrainingData()
        listFeature = []
        for elements, feature in FilteredTrainingSet:
            listFeature.append(feature)

        return list(set(listFeature))

    @staticmethod
    def trainModel():
    
        train_x, train_y = FeatureDetectionEngine.getTrainingSet()
        print train_x
        print train_y
        print "training statement %s" % len(train_x)       
        tf.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        FeatureDetectionEngine.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        # Start training (apply gradient descent algorithm)
        FeatureDetectionEngine.model.fit(train_x, train_y, n_epoch=500, batch_size=16, show_metric=True)

    @staticmethod
    def getInputArray(var):        
        bagOfWords = FeatureDetectionEngine.bagOfWords()
        #filteredData = TockenizeData.getTockenizedDataWithStem(var)
        filteredData = TockenizeData.getTockenizedData(var)

        localTrainingSet = []
        for word in bagOfWords:        
            if word in filteredData:
                localTrainingSet.append(1)
            else:
                localTrainingSet.append(0)

        return localTrainingSet

    @staticmethod
    def getFeature(statement):
        Input = FeatureDetectionEngine.getInputArray(statement)       
        r = FeatureDetectionEngine.model.predict([Input]) 
        var = Dataconverter.convertBinaryListToInt(r)

        if var != -1:
            listFeature = FeatureDetectionEngine.listOfFeature()       
            feature = listFeature[var]
        else:
            return "None"

        print Input
        print statement
        print feature
        print var
        print r
        return feature


    @staticmethod
    def getTrainingSet():
        FilteredTrainingSet = FeatureDetectionEngine.getFilteredTrainingData()
        bagOfWords = FeatureDetectionEngine.bagOfWords()
        listFeature = FeatureDetectionEngine.listOfFeature()

        print listFeature
        
        trainingSet = []

        for wordCollection, intent in FilteredTrainingSet:
            localTrainingSet = []
            for word in bagOfWords:
                if word in wordCollection:
                    localTrainingSet.append(1)
                else:
                    localTrainingSet.append(0)
            
            trainingSet.append([localTrainingSet, Dataconverter.convertIntToBinaryList(listFeature.index(intent), len(listFeature))])    
            
            
        random.shuffle(trainingSet)
        features = np.array(trainingSet)

        # create train and test lists
        train_x = list(features[:,0])
        train_y = list(features[:,1])

        return train_x, train_y

    

class FeatureDetection:
    
    def __init__(self):
        self.feature = ""

    def getFeature(self, statement):
    
        if "NO#Choice" not in statement and FeatureDetectionEngine.getFeature(statement) != "None":
            return FeatureDetectionEngine.getFeature(statement)
        else:
            #if not able to determine the feature from user input, live in the same feature context in which question was asked.
            return self.feature 
        
    
    def setcontext(self, feature):
        self.feature = feature

if __name__ == "__main__":    
    FeatureDetectionEngine.initialize()
    inAnaly = FeatureDetection()
    while(1):
        var = raw_input(">>")
        featureValue = inAnaly.getFeature(var)