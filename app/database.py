import os

from pymongo import MongoClient


MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Create a MongoClient instance
client = MongoClient(MONGODB_URL)

db = client[DATABASE_NAME]
collection = db["mycollection"]


# Optional: Function to get the database
def get_database():
    return db


# Optional: Function to get a collection
def get_collection(collection_name):
    return db[collection_name]
