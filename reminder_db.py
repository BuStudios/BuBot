from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
import time
import os

load_dotenv()

uri = f"mongodb+srv://admin:{os.getenv("DB_PASS")}@cluster.fw3h02i.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client["discord"]
collection = db["reminders"]

def add_reminder(timestamp, username, user_id):
    reminder = {
        "reminder_id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "user": username,
        "user_id": user_id
    }

    collection.insert_one(reminder)

def check_due_reminders():
    query = {
        "timestamp": {"$lt": int(time.time())}
    }
    due_reminders = collection.find(query)
    return due_reminders
    
def delete_reminder(reminder_id):
    collection.delete_one({"reminder_id": reminder_id})