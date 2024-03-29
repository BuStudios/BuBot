from pymongo import MongoClient
from dotenv import load_dotenv
import uuid
import time
import os


# loads the environment file
load_dotenv(dotenv_path="config/.env")


# connects to the MongoDB database
uri = f"mongodb+srv://admin:{os.getenv("DB_PASS")}@cluster.fw3h02i.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)


db = client["discord"]
collection = db["reminders"]


# adds a reminder to the database
def add_reminder(timestamp, username, user_id, reason):
    reminder = {
        "reminder_id": (str(uuid.uuid4()))[:7], # generates a id for the reminder
        "timestamp": timestamp,
        "reason": reason,
        "user": username,
        "user_id": user_id # needed to ping the user later
    }

    collection.insert_one(reminder) # inserts the reminder into the database


# checks for all due reminders
def check_due_reminders():
    query = {
        "timestamp": {"$lt": int(time.time() * 1000)} # checks if a reminder timestamp is less than the current timestamp
    }
    due_reminders = collection.find(query)
    return due_reminders


# deletes a reminder after it has been delivered
def delete_reminder(reminder_id):
    count = collection.count_documents(filter={"reminder_id": reminder_id})
    if count >= 1:
        collection.delete_one({"reminder_id": reminder_id})
        return "success"
    else:
        return "error"


# find the active reminders of a user
def get_user_reminders(username_id):
    query = {
        "user_id": username_id
    }
    user_reminders = collection.find(query)
    count = collection.count_documents(filter=query)
    user_reminders = list(user_reminders)
    return user_reminders, count