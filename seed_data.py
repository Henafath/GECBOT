import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://tcr22cs036:rLESg7RdnrH4Sedd@henascluster.ifrft.mongodb.net/gect_chatbot?retryWrites=true&w=majority")
db = client["gect_chatbot"]  # Database name

with open("" \
"data/placement.json") as f:
    placement = json.load(f)


history = placement.get("Placement_History", [])

if history:
    # add officer/phone/email info to each year’s record
    
# 🔥 Delete old data
    db.placement.delete_many({})
    for record in history:
        record["Training_and_Placement_Officer"] = placement["Training_and_Placement_Officer"]
        record["Phone_Number"] = placement["Phone_Number"]
        record["Email"] = placement["Email"]

    db.placement.insert_many(history)
else:
    print("⚠️ No placement history found")


