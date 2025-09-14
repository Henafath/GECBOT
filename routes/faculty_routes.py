from flask import Blueprint, jsonify
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
