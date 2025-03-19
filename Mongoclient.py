from pymongo import MongoClient
from creds import cred  # Assuming this contains your MongoDB URL

client = MongoClient(cred.DB_URL, connect=False)  # Add connect=False here
db = client['your_database_name']  # Replace 'your_database_name' with the actual DB name

client = MongoClient(cred.DB_URL, connect=False)
