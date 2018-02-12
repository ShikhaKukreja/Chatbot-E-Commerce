
from featureIntentEngine import *

class FeatureEngine:   

    def __init__(self, feature, product, domain):
        self.feature = feature
        self.slot = ""
        self.like = []
        self.dislike = []
        self.intentAnalyzer = IntentAnalyzer(feature, product, domain)
        

    def getIntentAndValue(self, statement):    

        if "NO#Choice" in statement:
            self.slot = "NO#Choice"
            return "like","NO#Choice"

        intent, value = self.intentAnalyzer.getIntentAndValue(statement)       
            
        if intent == "dislike":
            if value != "":
                self.dislike.append(value)            
        elif intent == "like":
            if value != "":
                self.like.append(value)
                self.slot = value

        return intent, value    

    def getQuestion(self):
        return self.intentAnalyzer.question()

    def isSlothasValue(self):
        if self.slot != "":
            return True
        else:
            return False
