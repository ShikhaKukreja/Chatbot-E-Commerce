import sys
sys.path.append('../WebDataParser')

from database import Database

class TrainingDataGenerator:
    @staticmethod
    def getFeatureList(condition):
        featureList = Database.getFeatureList(condition)
        return featureList

    @staticmethod
    def getFeatureInfo():
        condition = {}
        TrainingDataGenerator.featureList = TrainingDataGenerator.getFeatureList(condition)
        TrainingDataGenerator.featureInfo = {}
        for f in TrainingDataGenerator.featureList:       
            TrainingDataGenerator.featureInfo[f] = Database.getFeatureInfo(condition,f)

        print TrainingDataGenerator.featureInfo

    @staticmethod
    def generateDataUsingGrammar(grammarLines, feature):
        #print grammarLines
        generatedLines = []
        for line in grammarLines:
            if "<feature>" in line:
                line = line.replace("<feature>",feature)
            if "<featureInfo>" in line:
                for featureInfo in TrainingDataGenerator.featureInfo[feature]:
                    generatedLines.append(line.replace("<featureInfo>",featureInfo))
                continue
            generatedLines.append(line)
        return generatedLines

    @staticmethod
    def createFeatureTrainingData():
        file = open('Feature.txt','w')

        for feature in TrainingDataGenerator.featureList:            
            file.write("@"+feature+":\n")
            file.write("\t"+feature+"\n")
            for featureInfo in TrainingDataGenerator.featureInfo[feature]:
                file.write("\t"+featureInfo+"\n")
            file.write("\n")
        file.write("#END")

    @staticmethod
    def createIntentTrainingData():
        file = open("Intent.txt","w")
        grammar = open("IntentGrammar.txt","r")
        grammarLines = grammar.readlines()
        for feature in TrainingDataGenerator.featureList:
            file.write("@"+feature+":\n")            
            output = TrainingDataGenerator.generateDataUsingGrammar(grammarLines, feature)

            for line in output:
                file.write(line)
            
        file.write("\n")
        file.write("#END")
            



if __name__ == "__main__":
    TrainingDataGenerator.getFeatureInfo()
    TrainingDataGenerator.createFeatureTrainingData()
    TrainingDataGenerator.createIntentTrainingData()

    
    