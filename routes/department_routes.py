from flask import Blueprint, jsonify, request
from services.db_service import get_ug_programs, get_pg_programs, get_db

department_bp = Blueprint("department_bp", __name__)

# ✅ Get all UG Programs
def fetch_ug_programs():
    try:
        programs = get_ug_programs()

        if not programs:
            return jsonify({"fulfillmentText": "No UG programs found."})

        text = "UG Programs offered at GEC Thrissur:\n"
        for p in programs:
            text += f"- {p}\n"

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch UG programs at the moment."})


# ✅ Get all PG Programs
def fetch_pg_programs():
    try:
        programs = get_pg_programs()

        if not programs:
            return jsonify({"fulfillmentText": "No PG programs found."})

        text = "PG Programs offered at GEC Thrissur:\n"
        for p in programs:
            text += f"- {p}\n"

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch PG programs at the moment."})


# ✅ Get all Departments (with UG + PG Programs)
def fetch_departments():
    try:
        db = get_db()
        departments = list(db.departments.find({}, {"_id": 0}))

        if not departments:
            return jsonify({"fulfillmentText": "No departments found."})

        text = "Departments at GEC Thrissur:\n"
        for d in departments:
            text += f"- {d.get('branch')}\n"

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch departments."})

# Get department info
def get_department(req):
    try:
        db = get_db()
        params = req["queryResult"]["parameters"]
        name = params.get("department")

        if not name:
            return jsonify({"fulfillmentText": "Please specify the department name."})

        department = db.departments.find_one({"branch": name}, {"_id": 0})

        if not department:
            return jsonify({"fulfillmentText": "Department not found."})

        text = (
            f"Department: {department.get('branch')}\n"
            f"HOD: {department.get('hod')}\n"
            f"Programs: {', '.join(department.get('programs', []))}\n"
            f"Contact: {department.get('email')}"
        )

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch department details."})

