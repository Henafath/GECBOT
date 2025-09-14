from flask import Blueprint, jsonify
from services.db_service import get_db

department_bp = Blueprint("department_bp", __name__)

@department_bp.route("/api/departments", methods=["GET"])
def get_departments():
    db = get_db()
    departments = list(db.departments.find({}, {"_id": 0}))  # exclude _id
    return jsonify(departments)
