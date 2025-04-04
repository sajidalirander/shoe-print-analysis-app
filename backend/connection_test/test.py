import os
from dotenv import load_dotenv
from pymongo import MongoClient


# Load env variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

user = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASS")
cluster = os.getenv("MONGO_CLUSTER")

MONGO_URI = f"mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority&appName=database"

client = MongoClient(MONGO_URI)
db = client["shoeprint_db"]
collection = db["shoeprints"]

print(collection.count_documents({}))