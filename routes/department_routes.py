from flask import Blueprint, jsonify, request
from services.db_service import get_ug_programs, get_pg_programs, get_db

department_bp = Blueprint("department_bp", __name__)

# ✅ Get all UG Programs
@department_bp.route("/programs/ug", methods=["GET"])
def fetch_ug_programs():
    try:
        programs = get_ug_programs()
        return jsonify({"ug_programs": programs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Get all PG Programs
@department_bp.route("/programs/pg", methods=["GET"])
def fetch_pg_programs():
    try:
        programs = get_pg_programs()
        return jsonify({"pg_programs": programs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Get all Departments (with UG + PG Programs)
@department_bp.route("/departments", methods=["GET"])
def fetch_departments():
    try:
        db = get_db()
        departments = list(db.departments.find({}, {"_id": 0}))
        return jsonify({"departments": departments}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Get department info
@department_bp.route("/department", methods=["GET"])
def get_department():
    db= get_db()
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Department name is required"}), 400
    department = db.departments.find_one({"branch": name}, {"_id": 0})
    if not department:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(department)
