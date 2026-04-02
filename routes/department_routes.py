from flask import Blueprint, jsonify, request
from services.db_service import get_ug_programs, get_pg_programs, get_db
import random
department_bp = Blueprint("department_bp", __name__)

# ✅ Get all UG Programs
def fetch_ug_programs():
    try:
        programs = get_ug_programs()

        if not programs:
            return jsonify({"fulfillmentText": "No UG programs found."})
        formatted_programs = "<br>".join([f"• {p['course']} (Intake: {p['intake']})" for p in programs])
       
        responses = [
    "Here are the PG programs available:",
    "You can explore the following postgraduate courses:",
    "These are the M.Tech programs offered:"
]
        intro = random.choice(responses)
        result= jsonify({
    "fulfillmentText": f"{intro}<br><br>{formatted_programs}<br><br>Let me know if you need details about any specific course!"
})
        return result

    except Exception:
        return jsonify({
    "fulfillmentText": "Hmm, I’m not completely sure about that yet 🤔. But I’ll learn it soon! Meanwhile, you can try asking about courses, faculty, or placements."
})

# ✅ Get all PG Programs
def fetch_pg_programs():
    try:
        programs = get_pg_programs()

        if not programs:
            return jsonify({"fulfillmentText": "No PG programs found."})
        formatted_programs = "<br>".join([f"• {p['course']} (Intake: {p['intake']})" for p in programs])
        responses = [
    "Here are the PG programs available:",
    "You can explore the following postgraduate courses:",
    "These are the M.Tech programs offered:"
]
        intro = random.choice(responses)
        result= jsonify({
    "fulfillmentText": f"{intro}<br><br>{formatted_programs}<br><br>Let me know if you need details about any specific course!"
})
        return result

    except Exception:
        return jsonify({
    "fulfillmentText": "Hmm, I’m not completely sure about that yet 🤔. But I’ll learn it soon! Meanwhile, you can try asking about courses, faculty, or placements."
})


# ✅ Get all Departments (with UG + PG Programs)
def fetch_departments():
    try:
        db = get_db()
        departments = list(db.departments.find({}, {"_id": 0}))

        if not departments:
            return jsonify({"fulfillmentText": "No departments found."})
        responses = [
    "Here are all the departments available at gec thrissur:",
    "The following departments are available:",
    "These are the departments in gec thrissur:"
]
        intro = random.choice(responses)
        formatted_departments = "<br>".join([f"• {d.get('branch')}" for d in departments])
        result= jsonify({
    "fulfillmentText": f"{intro}<br><br>{formatted_departments}<br><br>Let me know if you need details about any specific department!"
})

        return result

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
        
        print("Department found:", name)
        department = db.departments.find_one(
         {"branch": name},
         {"_id": 0})
        
        print("Department found:", department)
            
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

