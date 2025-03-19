from pymongo import MongoClient
import datetime
import pytz
from creds import cred

# MongoDB Connection
client = MongoClient(cred.DB_URL)
db = client[cred.DB_NAME]  # Database reference
users_collection = db["users"]
files_collection = db["files"]
stats_collection = db["stats"]

def get_today_date():
    """Get today's date in YYYYMMDD format (IST timezone)."""
    return int(datetime.datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y%m%d"))

today_date = get_today_date()

def check(chatids):
    user = users_collection.find_one({"_id": chatids})
    return user.get("status", "Unknown") if user else "Unknown"

def count(chatids):
    user = users_collection.find_one({"_id": chatids})
    return user.get("count", 0) if user else 0

def update(id, count, status):
    update_data = {
        "_id": id,
        "status": status,
        "count": count,
        "date": today_date,
    }
    users_collection.update_one({"_id": id}, {"$set": update_data}, upsert=True)

def dt(chatids):
    user = users_collection.find_one({"_id": chatids})
    return user.get("date", "")

def format_time(elapsed):
    """Formats elapsed seconds into a human-readable format."""
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    return f"{hours}h {minutes}m {seconds}s".strip()

def updateFile():
    files_data = files_collection.find_one({"_id": "files"}) or {"files": 0}
    files_collection.update_one({"_id": "files"}, {"$set": {"files": files_data["files"] + 1}}, upsert=True)

def insertlog():
    total_users = users_collection.count_documents({})
    active_today = users_collection.count_documents({"date": today_date})

    files_data = files_collection.find_one({"_id": "files"}) or {"files": 0}
    total_files = files_data["files"]

    data = {
        "active_users": active_today,
        "translated_files": total_files,
        "total_users": total_users,
    }
    stats_collection.update_one({"_id": today_date}, {"$set": data}, upsert=True)

def logreturn():
    total_users = users_collection.count_documents({})
    active_today = users_collection.count_documents({"date": today_date})

    files_data = files_collection.find_one({"_id": "files"}) or {"files": 0}
    total_files = files_data["files"]

    stato = (
        f"`Total subtitles translated` : **{total_files}**\n"
        f"`Total bot users`                          : **{total_users}**\n"
        f"`Active users today`                   : **{active_today}**"
    )
    return stato
