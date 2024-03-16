from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = f"mongodb+srv://admin:{os.getenv("DB_PASS")}@cluster.fw3h02i.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client["discord"]
collection = db["reminders"]

def add_reminder(time):
    reminder = {
        "time": time
    }

    collection.insert_one(reminder)