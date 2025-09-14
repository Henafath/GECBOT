import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://tcr22cs036:rLESg7RdnrH4Sedd@henascluster.ifrft.mongodb.net/gect_chatbot?retryWrites=true&w=majority")
db = client["gect_chatbot"]  # Database name

# Load and insert departments
with open("departments.json", "r") as f:
    departments = json.load(f)
    db.departments.delete_many({})   # clear old data
    db.departments.insert_many(departments)
    print(f"Inserted {len(departments)} departments")

# Load and insert faculty
with open("faculty.json", "r") as f:
    faculty = json.load(f)
    db.faculty.delete_many({})   # clear old data
    db.faculty.insert_many(faculty)
    print(f"Inserted {len(faculty)} faculty members")
