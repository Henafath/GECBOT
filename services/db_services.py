from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database()

def get_ug_programs():
    return list(db.programs.find({"type": "UG"}, {"_id": 0}))

def get_pg_programs():
    return list(db.programs.find({"type": "PG"}, {"_id": 0}))

def get_placements(year=None):
    query = {"year": year} if year else {}
    return list(db.placements.find(query, {"_id": 0}))

def get_contact():
    return db.contacts.find_one({}, {"_id": 0})
