from flask import Blueprint, jsonify, request
from services.db_service import get_db

faculty_bp = Blueprint("faculty_bp", __name__)

@faculty_bp.route("/faculties", methods=["GET"])
def get_faculties():
    db = get_db()
    faculties = list(db.faculty.find({}, {"_id": 0}))
    return jsonify(faculties)

# ✅ Get all Faculty Contacts
@faculty_bp.route("/faculties/contacts", methods=["GET"])
def fetch_faculty_contacts():
    try:
        from services.db_service import get_faculty_contacts
        contacts = get_faculty_contacts()
        return jsonify({"faculty_contacts": contacts}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Get faculties by department
@faculty_bp.route("/faculties/department", methods=["GET"])
def get_faculties_by_department():
    db= get_db()
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Department name is required"}), 400
    data = list(db.faculty.find({"Department":  {"$regex": f"^{name}$", "$options": "i"}}, {"_id": 0}))
    if not data:
        return jsonify({"error": "Department not found"}), 404
    print("Querying department:", name)
    print("Matching faculty:")
    for f in db.faculty.find({"Department": {"$regex": f"^{name}$", "$options": "i"}}, {"_id":0}):
       print(f)

    return jsonify(data)