from flask import Flask, render_template, request, redirect, url_for
import sys
import json
from json import dumps
from flask_cors import CORS

sys.path.append('Chatbot')
sys.path.append('SalespersonChatbot')
sys.path.append('featureDetection')
sys.path.append('FeatureIntentAnalysis')
sys.path.append('WebDataParser')
sys.path.append('Utility')
sys.path.append('Data')

from chatbot import Chatbot
from uniqueID import UniqueID
from featureIntentData import IntentTrainingData
from featureDetection import FeatureDetectionEngine

app = Flask(__name__)
CORS(app)
IntentTrainingData.initialize()
FeatureDetectionEngine.initialize()

userDatabase = {}


@app.route('/' , methods=['POST'])
def Welcome():
    p = json.loads(request.data)
    print "%s" % p
    uniqueID = UniqueID.getUniqueID()
    userDatabase[uniqueID] = Chatbot(p["Domain"])
    res = json.loads(userDatabase[uniqueID].greeting())
    res['clientID'] = uniqueID
    res['Template'] = []
    res['Error'] = ""
    res['Input_status'] = "Welcome to %s" % p["Domain"]
    return dumps(res)

    

@app.route('/Input' , methods=['POST'])
def processInput():
    p = json.loads(request.data)
    print "%s" % p
    #try:
    uniqueID = p["userID"]
    res = json.loads(userDatabase[uniqueID].processInput(p))
    res['clientID'] = uniqueID
    return dumps(res)
    """
    except:
        return dumps(
            {
                "Text": "",
                "Button": [],
                "template": [],
                "Input_status": "",
                "client_id": uniqueID,
                "Error": "Cannot Connect. Please close chat window and reopen."
            }
            )   
    """
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5001)