from flask import Blueprint, jsonify
from services.db_service import get_db

faculty_bp = Blueprint("faculty_bp", __name__)

@faculty_bp.route("/api/faculties", methods=["GET"])
def get_faculties():
    db = get_db()
    faculties = list(db.faculty.find({}, {"_id": 0}))
    return jsonify(faculties)
