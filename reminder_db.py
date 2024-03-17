from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
import time
import os


# loads the environment file
load_dotenv()


# connects to the MongoDB database
uri = f"mongodb+srv://admin:{os.getenv("DB_PASS")}@cluster.fw3h02i.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)


db = client["discord"]
collection = db["reminders"]


# adds a reminder to the database
def add_reminder(timestamp, username, user_id, reason):
    reminder = {
        "reminder_id": str(uuid.uuid4()), # generates a id for the reminder
        "timestamp": timestamp,
        "reason": reason,
        "user": username,
        "user_id": user_id # needed to ping the user later
    }

    collection.insert_one(reminder) # inserts the reminder into the database


# checks for all due reminders
def check_due_reminders():
    query = {
        "timestamp": {"$lt": int(time.time())} # checks if a reminder timestamp is less than the current timestamp
    }
    due_reminders = collection.find(query)
    return due_reminders


# deletes a reminder after it has been delivered
def delete_reminder(reminder_id):
    collection.delete_one({"reminder_id": reminder_id})