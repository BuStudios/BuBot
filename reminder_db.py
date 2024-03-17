from pymongo import MongoClient
from dotenv import load_dotenv
import time
import os

load_dotenv()

uri = f"mongodb+srv://admin:{os.getenv("DB_PASS")}@cluster.fw3h02i.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client["discord"]
collection = db["reminders"]

def add_reminder(timestamp, username):
    reminder = {
        "timestamp": timestamp,
        "user": username
    }

    collection.insert_one(reminder)

def check_due_reminders():
    query = {
        "timestamp": {"$lt": int(time.time())}
    }
    try:
        due_reminders = collection.find(query)
        return due_reminders
    except Exception:
        return "Error"
    
def delete_reminder(reminder_id):
    pass