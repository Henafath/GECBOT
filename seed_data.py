from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database("gect_chatbot")  # your DB name

# Update all faculties with branch = "Computer Science And Engineering"
result = db.faculty.update_many(
    {"Department": "Computer Science And Engineering"},
    {"$set": {"Department": "Computer Science and Engineering"}}
)

print(f"✅ Modified {result.modified_count} documents")



