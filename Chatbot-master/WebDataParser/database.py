import json
from json import dumps

from pymongo import MongoClient


class Database:

    #client = MongoClient("mongodb://127.0.0.1:27017/ProductList")
    client = MongoClient("mongodb://admin:admin@ds227865.mlab.com:27865/productdb")
    db = client.get_default_database()

    @staticmethod
    def getProductInfo(condition):
        try:
            #condition = { "product_list.product": "shoes", "product_list.brand":"adidas" }
            d = Database.db.Product.aggregate([
                { "$match": condition },
                { "$unwind": "$product_list" },
                { "$match": condition },
                { "$group": {
                    "_id": "$_id",
                    "product_list": { "$push": "$product_list" }
                }},
                {
                    "$project":{"product_list" : 1, "_id":0}
                }
            ])            
            return list(d)
            
        except:
            return []

    @staticmethod
    def getFeatureList(condition={}):
        d = Database.getProductInfo(condition)
        f = []
        for domain in d:
            for product in domain["product_list"]:
                p = product.keys()
                f.append(p)    

        f= reduce(lambda x,y: x+y,f)
        f = list(set(f))         
        f.remove("product")
        return f
        
    @staticmethod
    def getProductDetails(condition):
        d = Database.getProductInfo(condition)
        Products = []
        if len(d) != 0:
            Products = d[0]["product_list"]
            
        return Products


    @staticmethod
    def getProductList(condition): 
        d = Database.getProductInfo(condition) 
        listProduct = []
        Products = d[0]["product_list"]
        for product in Products:
            listProduct.append(product["product"])
        return list(set(listProduct))


    @staticmethod
    def getFeatureInfo(condition,feature):
        d = Database.getProductInfo(condition) 
        listFeature = []
        for domain in d:
            for product in domain["product_list"]:    
                p = product.keys()
                if feature not in p:
                    continue;
                ft = product[feature]
                if isinstance(ft, list):
                    for f in product[feature]:
                        listFeature.append(f)
                else:
                    listFeature.append(product[feature])
        return list(set(listFeature))


    @staticmethod
    def storeProductInfo():
        """
        This function is used only to push dummy data into database for prototyping. Actual data into database will come from
        scrapy application
        """
        bulk = Database.db.Product.update(
            {"Key":"amazon.com"},
            {"$set":
            { "product_list": 
                [
                    {
                        "product": "shoes",
                        "brand": "adidas",
                        "price": "50",
                        "size": ["4","6","7","8","9","10","11","12"],
                        "color": ["red","blue","green","white","black"]
                    },
                    {
                        "product": "shoes",
                        "brand": "nike",
                        "price": "100",
                        "size": ["4","6","7","8","9","10","11","12"],
                        "color": ["red","blue","green","white","black"]
                    },
                    {
                        "product": "shoes",
                        "brand": "nike",
                        "price": "70",
                        "size": ["4","6","7","10","11","12"],
                        "color": ["white","black"]
                    },
                    {
                        "product": "jeans",
                        "style": "tight_fit",
                        "brand": "levis",
                        "price": "38",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","white","black"]
                    },
                    {
                        "product": "jeans",
                        "style": "regular_fit",
                        "brand": "levis",
                        "price": "28",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","white","black"]
                    },
                    {
                        "product": "jeans",
                        "style": "regular_fit",
                        "brand": "old_navi",
                        "price": "28",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","black"]
                    },

                ]
            }
        },
        upsert = True
        )

        bulk = Database.db.Product.update(
            {"Key":"Kohls.com"},
            {"$set":
            { "product_list": 
                [
                    {
                        "product": "sandal",
                        "brand": "adidas",
                        "price": "50",
                        "size": ["4","6","7","8","9","10","11","12"],
                        "color": ["red","blue","green","white","black"]
                    },
                    {
                        "product": "sandal",
                        "brand": "nike",
                        "price": "100",
                        "size": ["4","6","7","8","9","10","11","12"],
                        "color": ["red","blue","green","white","black"]
                    },
                    {
                        "product": "sandal",
                        "brand": "nike",
                        "price": "70",
                        "size": ["4","6","7","10","11","12"],
                        "color": ["white","black"]
                    },
                    {
                        "product": "pants",
                        "style": "tight_fit",
                        "brand": "levis",
                        "price": "38",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","white","black"]
                    },
                    {
                        "product": "pants",
                        "style": "regular_fit",
                        "brand": "levis",
                        "price": "28",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","white","black"]
                    },
                    {
                        "product": "pants",
                        "style": "regular_fit",
                        "brand": "old_navi",
                        "price": "28",
                        "size": ["28","30","32","34","38"],
                        "color": ["blue","green","black"]
                    },

                ]
            }
        },
        upsert = True
        )

if __name__ == "__main__":
    Database.storeProductInfo()
    # condition = {}
    # featureList = Database.getFeatureList(condition)
    # for f in featureList:
    #     print Database.getFeatureInfo(condition,f)