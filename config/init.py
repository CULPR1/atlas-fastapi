import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
import os
from dotenv import load_dotenv

load_dotenv("C:\\Users\\pavit\\Documents\\Projects\\atlas-fastapi\\.env")

#"/home/ubuntu/atlas-fastapi/.env"
#C:\\Users\\pavit\\Documents\\Projects\\atlas-fastapi\\.env

MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASS = os.getenv("MONGODB_PASS")
MONGODB_CLUSTER = os.getenv("MONGODB_CLUSTER")
MONGODB_URI = f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER}/"
#f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_CLUSTER}/"

def get_mongo_client():
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        return client
    except ConnectionFailure as e:
        raise Exception(f"MongoDB connection failed: {str(e)}")

connect_error = ConnectionFailure
operate_error = OperationFailure

client = get_mongo_client()

db = client["SHOP"]
profile = db["Profile"]
inv = db["Inventory"]
trans = db["Transactions"]
cart = db["Cart"]