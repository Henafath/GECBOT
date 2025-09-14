from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_database()

# ✅ Fetch all UG programs from all departments
def get_ug_programs():
    departments = db.departments.find({}, {"ug programs": 1, "_id": 0})
    ug_programs = []
    for dept in departments:
        if "ug programs" in dept:
            ug_programs.extend(dept["ug programs"])
    return ug_programs

# ✅ Fetch all PG programs from all departments
def get_pg_programs():
    departments = db.departments.find({}, {"pg programs": 1, "_id": 0})
    pg_programs = []
    for dept in departments:
        if "pg programs" in dept:
            pg_programs.extend(dept["pg programs"])
    return pg_programs

# ✅ Placements stored separately (unchanged)
def get_placements(year=None):
    query = {"year": year} if year else {}
    return list(db.placements.find(query, {"_id": 0}))

# ✅ Contact info stored separately (unchanged)
def get_faculty_contacts():
 
    return list(db.faculty.find({}, {"_id": 0, "Name": 1, "Email": 1, "PhoneNumber": 1, "Department": 1}))


# ✅ Generic DB accessor
def get_db():
    return db

