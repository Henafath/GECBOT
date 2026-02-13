from pymongo import MongoClient
from config import Config
import json
client = MongoClient(Config.MONGO_URI)
db = client.get_database("gect_chatbot")  # your DB name

with open("ml/model.json", "r") as f:
        data = json.load(f)

result = db.unanswered_queries.insert_many(data)


print(f"✅ Modified {result.inserted_ids} documents")



