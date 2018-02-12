import sys
sys.path.append('../Data')
sys.path.append('../WebDataParser')
sys.path.append('../Utility')

import config
import re

class IntentTrainingDataFileReader:

    def __init__(self):
        
        f = open(config.INTENT_DATA_FILE)
        feature = ""
        intent = ""

        self.intentData = {}
        IntentObject = []   
                

        lines = f.readlines()
        for line in lines:
            line = str.rstrip(str.lstrip(line))
            if "#END" in line:
                if feature != "":
                    self.intentData[feature] = IntentObject                
                return
            else:                
                if re.match(r"^@.*", line):
                    line = re.search(r"^@(.*):", line)
                    if line != feature:
                        if feature != "":
                            self.intentData[feature] = IntentObject
                            IntentObject = []

                        feature = line.group(1)
                        

                elif re.match(r"^~.*:", line):
                    line = re.search(r"^~(.*):", line)
                    if line != intent:
                        #re.match()
                        intent = line.group(1)
                        
                elif len(line):
                    statement = line
                    IntentObject.append((statement,intent))


    def getIntentTrainingData(self, feature):
        return self.intentData[feature]   

