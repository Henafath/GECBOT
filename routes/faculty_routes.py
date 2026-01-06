from flask import Blueprint, jsonify, request
from services.db_service import get_db

faculty_bp = Blueprint("faculty_bp", __name__)

@faculty_bp.route("/faculties", methods=["GET"])

def get_faculties():

  db = get_db()
  faculties = list(db.faculty.find({}, {"_id": 0}))
  return jsonify(faculties)

#Get all Faculty Contacts

@faculty_bp.route("/faculties/contacts", methods=["GET"])

def fetch_faculty_contacts():

 try:

  from services.db_service import get_faculty_contacts

  contacts = get_faculty_contacts()

  return jsonify({"faculty_contacts": contacts}), 200

 except Exception as e:

  return jsonify({"error": str(e)}), 500

# Get faculties by department

@faculty_bp.route("faculties/department", methods=["GET"])

def get_faculties_by_department():
   db= get_db()
   name = request.args.get("name")
   if not name:
     return jsonify({"error": "Department name is required"}), 400
   data = list(db.faculty.find({"Department": {"$regex": f"^{name}$", "$options": "i"}}, {"_id": 0})) 
   if not data: 
    return jsonify({"error": "Department not found"}), 404 
   print("Querying department:", name)
   print("Matching faculty:")
   for f in db.faculty.find({"Department": {"$regex": f"^{name}$", "$options": "i"}}, {"_id":0}):
     print(f) 
   return jsonify(data)
# ============================
# DIALOGFLOW HANDLERS
# ============================

def df_get_all_faculties():
    try:
        db = get_db()
        faculties = list(db.faculty.find({}, {"_id": 0}))

        if not faculties:
            return jsonify({"fulfillmentText": "No faculty information available."})

        text = "Faculty members at GEC Thrissur:\n"
        for f in faculties:
            text += f"- {f.get('Name')} ({f.get('Department')})\n"

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch faculty details at the moment."})

# ✅ Get all Faculty Contacts
def df_get_faculty_contacts():
    try:
        from services.db_service import get_faculty_contacts
        contacts = get_faculty_contacts()

        if not contacts:
            return jsonify({"fulfillmentText": "No faculty contacts available."})

        text = "Faculty Contacts:\n"
        for c in contacts:
            text += f"- {c['name']} ({c['department']}) – {c['email']}\n"

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch faculty contacts."})

    
# Get faculties by department
def df_get_faculty_by_department(req):
    try:
        db = get_db()
        params = req["queryResult"]["parameters"]
        name = params.get("department")

        if not name:
            return jsonify({"fulfillmentText": "Please specify a department name."})

        data = list(db.faculty.find(
            {"Department": {"$regex": f"^{name}$", "$options": "i"}},
            {"_id": 0}
        ))

        if not data:
            return jsonify({"fulfillmentText": "No faculty found for that department."})

        text = f"Faculty members in {name} department:\n"
        for f in data:
            text += f"- {f.get('Name')} ({f.get('Designation')})\n"

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch faculty details."})
