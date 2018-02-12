from tockenizeData import *
import random
import numpy as np
from Dataconverter import *
from intentTrainingDataFileReader import *
import tflearn
import tensorflow as tf
from database import Database





class IntentTrainingData:    
     
    featureList = Database.getFeatureList()
    trainingData = {}
    model = {}
    @staticmethod
    def initialize():
               
        for feature in IntentTrainingData.featureList:
            IntentTrainingData.trainingData[feature] = IntentTrainingDataFileReader().getIntentTrainingData(feature)
            IntentTrainingData.trainModel(feature)

    @staticmethod
    def getFilteredTrainingData(feature):
        FilteredTrainingSet = []

        for statement, intent in IntentTrainingData.trainingData[feature]:
            #f = TockenizeData.getTockenizedDataWithStem(statement)
            f = TockenizeData.getTockenizedData(statement)
            FilteredTrainingSet.append((f, intent))

        return FilteredTrainingSet
    
    @staticmethod
    def bagOfWords(feature):
        FilteredTrainingSet = IntentTrainingData.getFilteredTrainingData(feature)
        
        listElements = []
        for elements, intent in FilteredTrainingSet:
            for element in elements:
                listElements.append(element)
        
        return list(set(listElements))

    @staticmethod
    def listOfIntent(feature):
        FilteredTrainingSet = IntentTrainingData.getFilteredTrainingData(feature)
        listIntent = []
        for elements, intent in FilteredTrainingSet:
            listIntent.append(intent)

        return list(set(listIntent))

    @staticmethod
    def trainModel(feature):
    
        train_x, train_y = IntentTrainingData.getTrainingSet(feature)      
        print train_x
        print train_y
        tf.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, 32)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        # Define model and setup tensorboard
        IntentTrainingData.model[feature] = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        # Start training (apply gradient descent algorithm)
        IntentTrainingData.model[feature].fit(train_x, train_y, n_epoch=500, batch_size=16, show_metric=True)

    @staticmethod
    def predictIntent(feature,Input):
        return IntentTrainingData.model[feature].predict([Input])


    @staticmethod
    def getTrainingSet(feature):
        FilteredTrainingSet = IntentTrainingData.getFilteredTrainingData(feature)
        bagOfWords = IntentTrainingData.bagOfWords(feature)
        listIntent = IntentTrainingData.listOfIntent(feature)
        
        trainingSet = []

        for wordCollection, intent in FilteredTrainingSet:
            localTrainingSet = []
            for word in bagOfWords:
                if word in wordCollection:
                    localTrainingSet.append(1)
                else:
                    localTrainingSet.append(0)
            
            trainingSet.append([localTrainingSet, Dataconverter.convertIntToBinaryList(listIntent.index(intent), len(listIntent))])    
            
            
        random.shuffle(trainingSet)
        features = np.array(trainingSet)

        # create train and test lists
        train_x = list(features[:,0])
        train_y = list(features[:,1])

        return train_x, train_y