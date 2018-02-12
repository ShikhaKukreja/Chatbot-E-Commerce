from flask import Flask, render_template, request, redirect, url_for
import sys
import json
from json import dumps
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/' , methods=['POST'])
def Welcome():
    p = json.loads(request.data)
    
    return dumps(
        {
            "Text": "",
            "Button": ["product","FAQ"],
            "template": [],
            "Input_status": "Welcome to %s" % p["Domain"],
            "client_id": 1,
            "Error": ""
        }
        )

    

@app.route('/Input' , methods=['POST'])
def processInput():
    
    return dumps(
        {
            "Text": "Please select colors:",
            "Button": ["Blue","Yellow"],
            "template": [],
            "Input_status": "",
            "client_id": 1,
            "Error": ""
        }
        )   
    
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5001)