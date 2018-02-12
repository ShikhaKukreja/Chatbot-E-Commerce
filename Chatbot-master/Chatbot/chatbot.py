
import sys
from json import dumps
import json


from salespersonChatbot import SalespersonChatbot


class Chatbot:
    def __init__(self,domain):        

        self.chatMode = "greeting"
        self.salesPerson = SalespersonChatbot(domain)

        #self.salesPerson.createFeatureInstance("shoes")
        #Need to implement 
        #self.FAQPerson = FAQChatbot(domain)

    

    def greeting(self):        
        return dumps({"Text": "Hello! Welcome.","Button": ["product", "FAQ"]})

    def processInput(self, statement):
        
        print statement
        text, action = self.getText(statement)

        if action == "reset":
            self.chatMode = "greeting"
            self.salesPerson.product = False
            return self.greeting()

        if self.chatMode == "greeting":
            if text == "product":
                self.chatMode = "sales"

                if self.salesPerson.product == False:
                    return self.salesPerson.getProductList()

            elif text == "FAQ":
                self.chatMode = "FAQ"

        if self.chatMode == "greeting":
            return self.greeting()
        elif self.chatMode == "sales":
            if self.salesPerson.product == True:
                self.salesPerson.createFeatureInstance(text)
                return self.salesPerson.output("","")
            
            return self.salesPerson.processInput(text)
        #Need to implement this.
        #elif self.chatMode == "FAQ":
            #self.FAQPerson.input(statement)

    def getText(self, statement):
        print statement
        p = json.loads(dumps(statement))
        return (p["Text"], p["action"])
        
            
        