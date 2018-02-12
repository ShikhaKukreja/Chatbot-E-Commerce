import sys
sys.path.append('../Data')
sys.path.append('../WebDataParser')
sys.path.append('../Utility')

import config
import re

class FeatureTrainingDataFileReader:

    def __init__(self):
        
        f = open(config.FEATURE_DATA_FILE)
        feature = ""
        self.FeatureObject = []        

        lines = f.readlines()
        for line in lines:
            line = str.rstrip(str.lstrip(line))
            if "#END" in line:                                
                return
            else:                
                if re.match(r"^@.*", line):
                    line = re.search(r"^@(.*):", line)
                    if line != feature:
                        feature = line.group(1)
                elif len(line):
                    statement = line
                    self.FeatureObject.append((statement,feature))    

    def getFeatureTrainingData(self):
        return self.FeatureObject;

