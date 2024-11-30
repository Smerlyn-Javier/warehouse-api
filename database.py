from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["warehouse"]
products_collection = db["products"]

def get_products_collection():
    return products_collection